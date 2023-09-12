import traceback

import feedparser

from app import config
from app.models.mikan_rss_info import RssItemInfo
from app.models.sql import BangumiTable, RssItemTable
from app.utils.log_utils import set_up_logger
from app.utils.net_utils import download_file, fetch
from app.utils.parser.bangumi_parser import get_subject_info
from app.utils.parser.mikan_parser import get_anime_home_url_from_mikan, get_bangumi_url_from_mikan
from app.utils.parser.title_parser import get_episode, get_subtitle_language, get_title, \
    universal_replace_name
from app.utils.qbittorrent_utils import download_one_file
from app.utils.time_utils import datetime_to_str, str_to_datetime

logger = set_up_logger(__name__)


async def fresh_rss():
    try:
        rss_url = config.get_config("mikan_rss_url")
        if rss_url == "":
            raise Exception('rss link is empty')

        # 访问rss链接，并解析
        rss_page = await fetch(rss_url)
        feed = feedparser.parse(rss_page[1])

        # 查询每一个item
        for item in reversed(feed.entries):
            await item_analysis(item)
    except Exception as e:
        error_str = str(e)
        tb = traceback.extract_tb(e.__traceback__)
        filename = tb[-1].filename
        lineno = tb[-1].lineno
        logger.error(f"Try to fresh rss failed: {error_str}; file name: {filename}, line: {lineno}")
        return False, error_str


async def item_analysis(item):
    item_title = item.title
    now_language = get_subtitle_language(item_title)
    target_language = config.get_config("subtitle_language")

    # 目标语言和这个种子语言不一致
    if now_language != target_language:
        return

    origin_title = get_title(item_title)
    if origin_title == "":
        return
    mikan_url = item["link"].split('https://mikanani.me/Home/Episode/')[-1]

    # 数据库中已经有该种子信息
    if RssItemTable.check_item_exist(mikan_url):
        return
    logger.info(f"add new torrent:{item_title}")
    bangumi_id = RssItemTable.get_bangumi_id_by_anime_name(origin_title)
    if bangumi_id == -1:
        await add_item_when_bangumi_dont_have(item)
    else:
        await add_item_when_bangumi_have(item, bangumi_id)


async def add_item_when_bangumi_dont_have(item):
    item_title = item.title
    origin_title = get_title(item_title)
    episode = get_episode(item_title)

    # 只保留最后面一部分，节省空间
    mikan_url = item["link"].split('https://mikanani.me/Home/Episode/')[-1]

    mikan_home_url = await get_anime_home_url_from_mikan(mikan_url)
    if not mikan_home_url[0]:
        return
    bangumi_url = await get_bangumi_url_from_mikan(mikan_home_url[1])
    if not bangumi_url[0]:
        return
    bangumi_id = int(bangumi_url[1].split('https://bgm.tv/subject/')[-1])
    anime_info = await get_subject_info(bangumi_id)
    if anime_info is None:
        return
    item_name = universal_replace_name("file_name", anime_info, episode)
    pub_date = datetime_to_str(str_to_datetime(item['published']))
    item_info = RssItemInfo(item_name, origin_title, item_title, mikan_url, bangumi_id, episode, pub_date, 0)
    await qbittorrent_controller(item, anime_info, item_info)
    if BangumiTable.check_anime_exists(bangumi_id):
        return
    BangumiTable.insert_bangumi_data(anime_info.id,
                                     anime_info.platform,
                                     anime_info.image_url,
                                     anime_info.origin_name,
                                     anime_info.cn_name,
                                     anime_info.now_type.value,
                                     anime_info.pub_date)


async def add_item_when_bangumi_have(item, bangumi_id):
    item_title = item.title
    origin_title = get_title(item_title)
    episode = get_episode(item_title)
    mikan_url = item["link"].split('https://mikanani.me/Home/Episode/')[-1]
    anime_info = BangumiTable.get_anime_info_by_id(bangumi_id)
    if not anime_info[0]:
        return
    item_name = universal_replace_name("file_name", anime_info[1], episode)
    pub_date = datetime_to_str(str_to_datetime(item['published']))
    item_info = RssItemInfo(item_name, origin_title, item_title, mikan_url, bangumi_id, episode, pub_date, 0)
    await qbittorrent_controller(item, anime_info[1], item_info)


async def download_torrent(item):
    """
    :param item:
    :return tuple[bool,str]:
    """
    for enclosure in item.enclosures:
        # 检查是否为 .torrent 链接
        if enclosure.type != "application/x-bittorrent":
            continue
        torrent_url = enclosure['href']
        response = await download_file(torrent_url, 'download')
        if not response[0]:
            logger.error(f'下载torrent文件失败: {response[1]}')
            return False, response[1]
        torrent_path = response[1]
        logger.info(f'下载torrent文件, 路径:{torrent_path}')
        return True, torrent_path
    return False, '没有torrent链接'


async def qbittorrent_controller(item, anime_info, item_info):
    """
    :param item:
    :param BangumiSubjectInfo anime_info:
    :param RssItemInfo item_info:
    :return:
    """
    torrent_path = await download_torrent(item)
    if not torrent_path[0]:
        return torrent_path
    if anime_info.now_type.value == 2:
        save_path = f"{config.get_config('download_path')}/{config.get_config('anime_path')}"
    else:
        save_path = f"{config.get_config('download_path')}/{config.get_config('tokusatsu_path')}"
    dir_name = universal_replace_name("dir_name", anime_info)
    file_name = universal_replace_name("file_name", anime_info, item_info.episode)
    new_torrent_name = universal_replace_name("qbittorrent_name", anime_info, item_info.episode)
    await download_one_file(torrent_path[1], new_torrent_name, save_path, dir_name, file_name, 'mikan',
                            item_info)

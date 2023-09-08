import feedparser

from app import config
from app.models.sql import BangumiTable, RssItemTable
from app.utils.log_utils import set_up_logger
from app.utils.net_utils import fetch
from app.utils.parser.bangumi_parser import get_subject_info, get_subject_name
from app.utils.parser.mikan_parser import get_anime_home_url_from_mikan, get_bangumi_url_from_mikan
from app.utils.parser.title_parser import get_episode, get_subtitle_language, get_title
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
        target_language = config.get_config("subtitle_language")

        # 查询每一个item
        for item in reversed(feed.entries):
            item_title = item.title
            now_language = get_subtitle_language(item_title)

            # 目标语言和这个种子语言不一致
            if now_language != target_language:
                continue

            origin_title = get_title(item_title)
            episode = get_episode(item_title)

            # 数据库中已经有该种子信息
            if RssItemTable.check_item_exist(item):
                continue

            bangumi_id = RssItemTable.get_bangumi_id_by_anime_name(origin_title)
            if bangumi_id == -1:
                await add_item_when_bangumi_dont_have(item)
            else:
                BangumiTable.get_anime_info_by_id(bangumi_id)
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to fresh rss failed: {error_str}")
        return False, error_str


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
    item_name = get_file_name(anime_info, episode)
    pub_date = datetime_to_str(str_to_datetime(item['published']))
    RssItemTable.insert_rss_data(item_name, origin_title, item_title, mikan_url, bangumi_id, episode, pub_date)
    if BangumiTable.check_anime_exists(bangumi_id):
        return
    BangumiTable.insert_bangumi_data(anime_info.id,
                                     anime_info.platform,
                                     anime_info.image_url,
                                     anime_info.origin_name,
                                     anime_info.cn_name,
                                     anime_info.pub_date,
                                     anime_info.now_type.value)


async def add_item_when_bangumi_have(item, bangumi_id):
    item_title = item.title
    origin_title = get_title(item_title)
    episode = get_episode(item_title)
    mikan_url = item["link"].split('https://mikanani.me/Home/Episode/')[-1]
    anime_info = BangumiTable.get_anime_info_by_id(bangumi_id)
    item_name = get_file_name(anime_info, episode)
    pub_date = datetime_to_str(str_to_datetime(item['published']))
    RssItemTable.insert_rss_data(item_name, origin_title, item_title, mikan_url, bangumi_id, episode, pub_date)


def get_file_name(anime_info, episode):
    """
    :param  BangumiSubjectInfo anime_info:
    :param int episode:
    :return:
    """
    # 提取年、月、日
    year = anime_info.pub_date.year
    month = anime_info.pub_date.month
    day = anime_info.pub_date.day

    # 格式化月和日，位数不足用0填充
    year_str = str(year)
    month_str = f"{month:02d}"
    day_str = f"{day:02d}"

    name = config.get_config('file_name')
    name = name.replace('/cn_name/', anime_info.cn_name)
    name = name.replace('/origin_name/', anime_info.origin_name)
    name = name.replace('/id/', anime_info.id)
    name = name.replace('/type/', anime_info.now_type.name)
    name = name.replace('/year/', year_str)
    name = name.replace('/month/', month_str)
    name = name.replace('/day/', day_str)
    name = name.replace('/episode/', str(episode))
    name = name.replace('/platform/', str(anime_info.platform))
    return name


def get_dir_name(anime_info):
    """
    :param  BangumiSubjectInfo anime_info:
    :return:
    """
    # 提取年、月、日
    year = anime_info.pub_date.year
    month = anime_info.pub_date.month
    day = anime_info.pub_date.day

    # 格式化月和日，位数不足用0填充
    year_str = str(year)
    month_str = f"{month:02d}"
    day_str = f"{day:02d}"

    name = config.get_config('dir_name')
    name = name.replace('/cn_name/', anime_info.cn_name)
    name = name.replace('/origin_name/', anime_info.origin_name)
    name = name.replace('/id/', anime_info.id)
    name = name.replace('/type/', anime_info.now_type.name)
    name = name.replace('/year/', year_str)
    name = name.replace('/month/', month_str)
    name = name.replace('/day/', day_str)
    name = name.replace('/platform/', str(anime_info.platform))
    return name

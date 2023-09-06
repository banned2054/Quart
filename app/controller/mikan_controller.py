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

            # 只保留最后面一部分，节省空间
            mikan_url = item["link"].split('https://mikanani.me/Home/Episode/')[-1]

            # 数据库中已经有该种子信息
            if RssItemTable.check_item_exist(mikan_url):
                continue

            bangumi_id = RssItemTable.get_bangumi_id_by_origin_name(origin_title)
            if bangumi_id == -1:
                mikan_home_url = await get_anime_home_url_from_mikan(mikan_url)
                if not mikan_home_url[0]:
                    continue
                bangumi_url = await get_bangumi_url_from_mikan(mikan_home_url[1])
                if not bangumi_url[0]:
                    continue
                bangumi_id = int(bangumi_url[1].split('https://bgm.tv/subject/')[-1])
                anime_info = await get_subject_info(bangumi_id)
                if anime_info is None:
                    continue
                anime_name = anime_info.cn_name
                pub_date = datetime_to_str(str_to_datetime(item['published']))
                RssItemTable.insert_rss_data(anime_name, mikan_url, bangumi_id, episode, pub_date)
                if BangumiTable.check_anime_exists(bangumi_id):
                    continue
                BangumiTable.insert_bangumi_data(anime_info.id, anime_info.platform, anime_info.image_url,
                                                 anime_info.origin_name, anime_info.cn_name, anime_info.pub_date,
                                                 anime_info.now_type.value)
            else:
                BangumiTable.get_anime_info_by_id(bangumi_id)
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to fresh rss failed: {error_str}")
        return False, error_str

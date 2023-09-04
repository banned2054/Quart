import feedparser
from lxml import html

from app.models.mikan_rss_info import RssItemInfo
from app.models.sql import RssItemTable
from app.utils.log_utils import set_up_logger
from app.utils.net_utils import fetch
from app.utils.parser.title_parser import get_episode, get_title
from app.utils.time_utils import str_to_datetime

logger = set_up_logger(__name__)


def get_bangumi_url_from_mikan(html_str):
    """
    解析html信息，从单部动画在mikan上的页面解析到对应的该动画在bangumi地址
    :param str html_str: mikan上单部动画的页面
    :return tuple[bool, str]: 该动画对应的bangumi地址
    """
    try:
        tree = html.fromstring(html_str)
        a_tag = tree.xpath('//p[@class="bangumi-info"]/a[contains(@href, "bgm.tv")]')[0]
        href = a_tag.get_config('href')
        logger.info(f"Get bangumi url from mikan page.{href}")
        return True, href
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get bangumi url from mikan page failed.")
        return False, error_str


def get_anime_home_url_from_mikan(html_str):
    """
    解析html信息，从单集动画在mikan上的页面解析到对应的该动画在mikan上的home地址
    :param str html_str: mikan上单集动画的页面
    :return tuple[bool, str]: 该动画对应的home地址
    """
    try:
        tree = html.fromstring(html_str)
        a_tag = tree.xpath('//p[@class="bangumi-title"]/a')[0]
        href = a_tag.get_config('href')
        logger.info(f"Get anime home url from mikan page.https://mikanani.me{href}")
        return True, f"https://mikanani.me{href}"
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get anime home url from mikan page failed.")
        return False, error_str


async def get_rss_item_list(html_str):
    """
    解析html信息，从rss页面解析到所有动画单集的种子
    :param str html_str: rss链接获取的页面
    :return: 动画单集的种子信息组成rss
    """
    feed = await feedparser.parse(html_str)
    last_pub_time = RssItemTable.get_latest_pub_time()
    for item in reversed(feed.entries):
        origin_url = item["link"]
        if not origin_url.startswith("https://mikanani.me/Home/Episode/"):
            # 链接不正确
            continue
        mikan_url = origin_url.split("Episode/")[-1]
        if RssItemTable.check_item_exist(mikan_url):
            # 数据库里已经包含，就不再存入
            continue
        now_pub_time = str_to_datetime(item["default_pubdate"])
        origin_name = item["name"]
        episode = get_episode(origin_name)
        origin_name = get_title(origin_name)
        bangumi_id = RssItemTable.get_bangumi_id_by_origin_name(origin_name)

        RssItemInfo(, mikan_url, bangumi_id, episode)

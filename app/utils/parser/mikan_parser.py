import feedparser
from lxml import html

from app.models.sql import RssItemTable
from app.utils.log_utils import SetUpLogger
from app.utils.time_utils import str_to_datetime

logger = SetUpLogger(__name__)


def GetBangumiUrlFromMikan(html_str):
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


def GetAnimeHomeUrlFromMikan(html_str):
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


async def GetRssItemList(html_str):
    """
    解析html信息，从rss页面解析到所有动画单集的种子
    :param str html_str: rss链接获取的页面
    :return: 动画单集的种子信息组成rss
    """
    feed = await feedparser.parse(html_str)
    last_pub_time = RssItemTable.get_latest_pub_time()
    for item in reversed(feed.entries):
        now_pub_time = str_to_datetime(item["default_pubdate"])
        mikan_url = item["link"]
        if not mikan_url.startswith("https://mikanani.me/Home/Episode/"):
            continue
        mikan_url = mikan_url.split("Episode/")[-1]

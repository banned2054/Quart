import asyncio

import feedparser
from lxml import html

from app.utils.log_utils import SetUpLogger

logger = SetUpLogger(__name__)


def GetBangumiUrlFromMikan(html_str: str):
    """
    解析html信息，从单部动画在mikan上的页面解析到对应的该动画在bangumi地址
    :param html_str: mikan上单部动画的页面
    :return: 该动画对应的bangumi地址
    """
    try:
        tree = html.fromstring(html_str)
        a_tag = tree.xpath('//p[@class="bangumi-info"]/a[contains(@href, "bgm.tv")]')[0]
        href = a_tag.get_config('href')
        logger.info(f"Get bangumi url from mikan page.{href}")
        return f"Success:{href}"
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get bangumi url from mikan page failed.")
        return f"Error:{error_str}"


def GetAnimeHomeUrlFromMikan(html_str: str):
    """
    解析html信息，从单集动画在mikan上的页面解析到对应的该动画在mikan上的home地址
    :param html_str: mikan上单集动画的页面
    :return: 该动画对应的home地址
    """
    try:
        tree = html.fromstring(html_str)
        a_tag = tree.xpath('//p[@class="bangumi-title"]/a')[0]
        href = a_tag.get_config('href')
        logger.info(f"Get anime home url from mikan page.https://mikanani.me{href}")
        return f"https://mikanani.me{href}"
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get anime home url from mikan page failed.")
        return f"Error:{error_str}"


async def GetRssItem(html_str: str):
    loop = asyncio.get_event_loop()
    feed = await loop.run_in_executor(None, feedparser.parse, html_str)

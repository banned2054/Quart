from lxml import html

from app import config
from app.utils.log_utils import setup_logger

logger = setup_logger(__name__, 'log', config.get('TZ'))


def GetBangumiUrlFromMikan(html_str: str):
    try:
        tree = html.fromstring(html_str)
        a_tag = tree.xpath('//p[@class="bangumi-info"]/a[contains(@href, "bgm.tv")]')[0]
        href = a_tag.get('href')
        logger.info(f"Get bangumi url from mikan page.{href}")
        return f"Success:{href}"
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get bangumi url from mikan page failed.")
        return f"Error:{error_str}"


def GetAnimeHomeUrlFromMikan(html_str: str):
    try:
        tree = html.fromstring(html_str)
        a_tag = tree.xpath('//p[@class="bangumi-info"]/a')[0]
        href = a_tag.get('href')
        logger.info(f"Get anime home url from mikan page.{href}")
        return href
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get anime home url from mikan page failed.")
        return f"Error:{error_str}"

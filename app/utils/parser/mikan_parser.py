from lxml import html

from app.utils.log_utils import SetUpLogger

logger = SetUpLogger(__name__)


def GetBangumiUrlFromMikan(html_str: str):
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

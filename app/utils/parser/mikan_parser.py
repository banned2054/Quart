from lxml import html

from app.utils.log_utils import set_up_logger
from app.utils.net_utils import fetch

logger = set_up_logger(__name__)


async def get_bangumi_url_from_mikan(mikan_url):
    """
    解析html信息，从单部动画在mikan上的页面解析到对应的该动画在bangumi地址
    :param str mikan_url: mikan上单部动画的页面的地址在Bangumi/后面的部分
    :return tuple[bool, str]: 该动画对应的bangumi地址
    """
    try:
        reponse = await fetch(f"https://mikanani.me/Home/Bangumi/{mikan_url}")
        if reponse[0]:
            tree = html.fromstring(reponse[1])
            a_tag = tree.xpath('//p[@class="bangumi-info"]/a[contains(@href, "bgm.tv")]')[0]
            href = a_tag.attrib['href']
            logger.info(f"Get bangumi url from mikan page: {href}")
            return True, href
        else:
            raise Exception
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get bangumi url from mikan page failed.")
        return False, error_str


async def get_anime_home_url_from_mikan(mikan_url):
    """
    解析html信息，从单集动画在mikan上的页面解析到对应的该动画在mikan上的home地址
    :param str mikan_url: mikan上单集动画的页面的地址在Episode/后面的部分
    :return tuple[bool, str]: 该动画对应的home地址
    """
    try:
        response = await fetch(f"https://mikanani.me/Home/Episode/{mikan_url}")
        if response[0]:
            tree = html.fromstring(response[1])
            a_tag = tree.xpath('//p[@class="bangumi-title"]/a')[0]
            href = a_tag.attrib['href']
            logger.info(f"Get anime home url from mikan page: https://mikanani.me{href}")
            return True, href.split("/Home/Bangumi/")[-1]
        else:
            raise Exception
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to get anime home url from mikan page failed.")
        return False, error_str

from app import config
from app.utils.log_utils import SetUpLogger
from app.utils.net_utils import fetch
from app.utils.parser.mikan_parser import GetRssItem

logger = SetUpLogger(__name__)


async def fresh_rss():
    try:
        rss_url = (config.get_config("mikan_rss_url"))
        response = await fetch(rss_url)
        if response[0]:
            return GetRssItem(response[1])
        else:
            raise Exception(f"Cannot download file, status code: {response[1]}")
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to fetch Rss, error:{error_str}")

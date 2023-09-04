from app import config
from app.utils.log_utils import set_up_logger
from app.utils.net_utils import fetch
from app.utils.parser.mikan_parser import get_rss_item_list

logger = set_up_logger(__name__)


async def fresh_rss():
    try:
        rss_url = (config.get_config("mikan_rss_url"))
        response = await fetch(rss_url)
        if response[0]:
            return get_rss_item_list(response[1])
        else:
            raise Exception(f"Cannot download file, status code: {response[1]}")
    except Exception as e:
        error_str = str(e)
        logger.error(f"Try to fetch Rss, error:{error_str}")

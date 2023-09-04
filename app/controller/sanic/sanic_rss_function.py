import sanic
from sanic import json

from app import config
from app.utils.log_utils import set_up_logger

logger = set_up_logger(__name__)


async def change_rss_url(request: sanic.request.Request):
    """
    修改rss订阅链接
    :param request: body里有一个包含"new_rss_url"的json的request
    :return: 包含正确的地址的话返回success，否则返回fail
    """
    data = request.json
    new_rss_url = data.get("new_rss_url", None)
    request_ip = request.remote_addr

    if not new_rss_url:
        logger.error(f"ip:{request_ip} request to change rss, but miss 'new_rss_url' parameter")
        return json({"error": "Missing 'new_rss_url' parameter"}, status = 400)
    if new_rss_url.startswith('http://') or new_rss_url.startswith('https://') or new_rss_url.startswith("localhost"):
        logger.info(f"ip:{request_ip} request to change rss, success")
        config.set_config("mikan_rss_url", new_rss_url)
        return json("success")
    logger.error(f"ip:{request_ip} request to change rss, but 'new_rss_url' is not url")
    return json("fail")

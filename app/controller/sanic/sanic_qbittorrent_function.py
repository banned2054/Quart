import sanic
from sanic import json

from app import config
from app.utils.log_utils import SetUpLogger

logger = SetUpLogger(__name__)


async def qbittorrent_finish_download(request: sanic.request.Request):
    request_ip = request.remote_addr
    data = request.json
    hash_code = data.get("hash_code", None)
    torrent_name = data.get("torrent_name", None)

    if not hash_code:
        logger.error(f"ip:{request_ip} request to finish download torrent, but miss 'hash_code' parameter")
        return json({"error": "Missing 'hash_code' parameter"}, status = 400)

    if not torrent_name:
        logger.error(f"ip:{request_ip} request to finish download torrent, but miss 'torrent_name' parameter")
        return json({"error": "Missing 'torrent_name' parameter"}, status = 400)
    config.set_config("mikan_rss_url", hash_code)
    return json("success")

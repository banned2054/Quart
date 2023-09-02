import sanic
from sanic import json

from app import config
from app.utils.log_utils import SetUpLogger
from app.utils.qbittorrent_utils import is_torrent_complete_and_matching

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

    check_result = is_torrent_complete_and_matching(hash_code, torrent_name)
    if check_result[0]:
        logger.info(f"ip:{request_ip} request to finish download torrent")
        return json("success")
    else:
        logger.error(f"ip:{request_ip} request to finish download torrent,{check_result[1]}")
        return json({"error": check_result[1]}, status = 400)

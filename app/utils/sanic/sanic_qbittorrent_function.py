import sanic
from sanic import json

from app import config


async def change_rss_url(request: sanic.request.Request):
    data = request.json
    new_rss_url = data.get("new_rss_url", None)

    if not new_rss_url:
        return json({"error": "Missing 'new_rss_url' parameter"}, status = 400)
    config.set_config("mikan_rss_url", new_rss_url)
    return json("success")

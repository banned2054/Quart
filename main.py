import asyncio
import threading

import feedparser
import qbittorrentapi

from app import config
from app.controller.mikan_controller import fresh_rss
from app.models.sql import RssItemTable
from app.utils.net_utils import fetch
from app.utils.parser.bangumi_parser import get_subject_name
from app.utils.parser.mikan_parser import get_anime_home_url_from_mikan, get_bangumi_url_from_mikan
from app.utils.parser.title_parser import get_episode, get_subtitle_language, get_title
from app.utils.time_utils import datetime_to_str, str_to_datetime


def thread_function():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(infinite_loop_coroutine())


async def infinite_loop_coroutine():
    sleep_time = int(config.get_config('IntervalTimeToRss'))
    if sleep_time <= 0:
        sleep_time = 1
    while True:
        await fresh_rss()
        await asyncio.sleep(sleep_time)


if __name__ == '__main__':
    # 创建并启动一个新线程来运行 thread_function
    thread = threading.Thread(target = thread_function)
    thread.start()
    # # 在主线程中运行 Sanic 服务器
    # sanic_server.run(host = "0.0.0.0", port = 18341)
    # RssItemTable.insert_rss_data("adsa", "sda", 111, 1, "2019.09.07")
    # test = RssItemTable.check_item_exist("sda")
    # print(test)
    # test = RssItemTable.get_latest_pub_time()
    # print(test)

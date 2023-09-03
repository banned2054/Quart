import asyncio
import threading

import feedparser
import qbittorrentapi

from app.utils.net_utils import fetch
from app.utils.parser.title_parser import get_episode, get_title
from app.utils.qbittorrent_utils import is_torrent_complete_and_matching, qbt_client
from app.controller.sanic import sanic_server
from app import config


def thread_function():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(infinite_loop_coroutine())


async def infinite_loop_coroutine():
    # sleep_time = int(config.get_config('IntervalTimeToRss'))
    # if sleep_time <= 0:
    #     sleep_time = 1
    # while True:
    #     print("内容已追加到文件中。")
    #     await asyncio.sleep(sleep_time)
    html_text = await fetch("https://mikanani.me/RSS/MyBangumi?token=ZoVG3vGFwo5h1JXB8A0FiA%3d%3d")
    feed = feedparser.parse(html_text[1])
    for item in reversed(feed.entries):
        a = get_title(item.title)
        print(a, item.title)


if __name__ == '__main__':
    # 创建并启动一个新线程来运行 thread_function
    thread = threading.Thread(target = thread_function)
    thread.start()
    # # 在主线程中运行 Sanic 服务器
    # sanic_server.run(host = "0.0.0.0", port = 18341)

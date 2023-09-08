import asyncio
import threading

from app import config
from app.controller.mikan_controller import fresh_rss
from app.models.sql import BangumiTable
from app.utils.parser.bangumi_parser import get_subject_info


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
    # result = BangumiTable.get_anime_info_by_id(176974)
    # result = await get_subject_info(176974)
    # print(result)


if __name__ == '__main__':
    # 创建并启动一个新线程来运行 thread_function
    thread = threading.Thread(target = thread_function)
    thread.start()
    # # 在主线程中运行 Sanic 服务器
    # sanic_server.run(host = "0.0.0.0", port = 18341)

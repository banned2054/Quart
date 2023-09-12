import asyncio
import multiprocessing

from app import config
from app.controller.mikan_controller import fresh_rss
from app.controller.sanic import sanic_server


def process_async_loop_function():
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


def process_start_sanic_function():
    sanic_server.run(host = "0.0.0.0", port = 18341)


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force = True)
    p1 = multiprocessing.Process(target = process_async_loop_function)
    p2 = multiprocessing.Process(target = process_start_sanic_function)
    p1.start()
    p2.start()

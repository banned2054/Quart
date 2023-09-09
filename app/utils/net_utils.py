import os
from urllib.parse import urlparse

import aiohttp

from app import config
from app.utils.log_utils import set_up_logger

logger = set_up_logger(__name__)


async def download_file(url, dir_path, retries = 3, timeout = 10):
    """
    下载文件，返回下载文件的路径
    :param str url: 文件下载地址.
    :param str dir_path: 下载文件放置的目录.
    :param int retries: 失败重试次数.
    :param int timeout: 超时的秒数.
    :return: `Success: [下载文件本地路径]` 或者 `Error: [错误信息]`
    """
    proxy = config.get_config('proxy_url')
    clientTimeout = aiohttp.ClientTimeout(total = timeout)
    async with aiohttp.ClientSession(timeout = clientTimeout) as session:
        filename = os.path.basename(urlparse(url).path)
        file_path = f'{dir_path}/{filename}'
        try:
            async with session.get(url, proxy = proxy, ssl = False) as resp:
                if resp.status == 200:
                    with open(file_path, 'wb') as f:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    logger.info(f"Download {url} success, file path: {file_path}.")
                    return True, f"{file_path}"
                else:
                    raise Exception(f"Cannot download file, status code: {resp.status}")
        except Exception as e:
            if retries > 0:
                logger.error(f"Failed to download {url}, try again.")
                return await download_file(url, dir_path, retries - 1, timeout)
            else:
                error_str = str(e)
                logger.error(f"Failed to download {url}, error: {error_str}")
                return False, f"Download file failed, error: {error_str}"


async def fetch(url, headers = None, retries = 3, timeout = 10):
    """
    访问网页返回html，通过str返回
    :param str url: 文件下载地址.
    :param dict headers: header参数.
    :param int retries: 失败重试次数.
    :param int timeout: 超时的秒数.
    :return: `Success: [html文本]` 或者 `Error: [错误信息]`
    """
    proxy = config.get_config('proxy_url')
    clientTimeout = aiohttp.ClientTimeout(total = timeout)
    async with aiohttp.ClientSession(timeout = clientTimeout) as session:
        try:
            async with session.get(url, headers = headers, proxy = proxy, ssl = False) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    logger.info(f"Fetch {url} success.")
                    return True, f"{text}"
                else:
                    raise Exception(f"Cannot fetch data, status code: {resp.status}")
        except Exception as e:
            if retries > 0:
                logger.error(f"Failed to fetch {url}, try again.")
                return await fetch(url, headers, retries - 1, timeout)
            else:
                error_str = str(e)
                logger.error(f"Failed to fetch {url}, error: {error_str}")
                return False, f"Fetch data failed, error: {error_str}"

import os
from urllib.parse import urlparse

import aiohttp

from app import config
from app.utils.log_utils import setup_logger

logger = setup_logger(__name__, config.get('TZ'), config.get('TZ'))


async def download_file(url, dir_path, proxy = None, retries = 3, timeout = 10):
    clientTimeout = aiohttp.ClientTimeout(total = timeout)
    async with aiohttp.ClientSession(timeout = clientTimeout) as session:
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(dir_path, filename)
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
                    return f"Success: {file_path}"
                else:
                    raise Exception(f"Cannot download file, status code: {resp.status}")
        except Exception as e:
            if retries > 0:
                logger.error(f"Failed to download {url}, try again.")
                return await download_file(url, dir_path, proxy, retries - 1, timeout)
            else:
                error_str = str(e)
                logger.error(f"Failed to download {url}, error: {error_str}")
                return f"Error: Download file failed, error: {error_str}"


async def fetch(url, dir_path, proxy = None, retries = 3, timeout = 10):
    clientTimeout = aiohttp.ClientTimeout(total = timeout)
    async with aiohttp.ClientSession(timeout = clientTimeout) as session:
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(dir_path, filename)
        try:
            async with session.get(url, proxy = proxy, ssl = False) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    with open(file_path, 'wb') as f:
                        f.write(text.encode())
                    logger.info(f"Fetch {url} success, file path: {file_path}.")
                    return f"Success: {text}"
                else:
                    raise Exception(f"Cannot fetch data, status code: {resp.status}")
        except Exception as e:
            if retries > 0:
                logger.error(f"Failed to fetch {url}, try again.")
                return await fetch(url, dir_path, proxy, retries - 1, timeout)
            else:
                error_str = str(e)
                logger.error(f"Failed to fetch {url}, error: {error_str}")
                return f"Error: Fetch data failed, error: {error_str}"

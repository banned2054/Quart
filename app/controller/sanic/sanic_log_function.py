import os

import sanic
from sanic import json

from app.utils.log_utils import set_up_logger

logger = set_up_logger(__name__)


async def get_log_file_list(request: sanic.request.Request):
    """
    读取log文件目录下所有的log文件，然后返回对应的文件名
    :param request:
    :return: json格式的log文件名组成的数组
    """
    log_directory = 'log'
    all_logs = os.listdir(log_directory)
    request_ip = request.remote_addr
    logger.info(f'ip:{request_ip} request to get log file list')

    files = [item[:-4] for item in all_logs if os.path.isfile(os.path.join(log_directory, item))]
    return json(files)


async def get_log_file(request: sanic.request.Request):
    """
    读取特定log文件的内容，返回里面的内容
    :param request: body里有一个包含"log_date"的json的request
    :return:读取对应文件，一行作为一个数据，组成一个json的数组
    """
    data = request.json
    log_date = data.get('log_date', None)
    request_ip = request.remote_addr
    if not log_date:
        logger.error(f"ip:{request_ip} request to read log file, but miss 'log_date' parameter")
        return json({"error": "Missing 'log_date' parameter"}, status = 400)

    log_file_path = os.path.join('log', f"{log_date}.log")
    if not os.path.exists(log_file_path):
        logger.error(f"ip:{request_ip} request to read {log_date}.log, but this log file doesn't exist")
        return json({"error": f"No log file found for date: {log_date}"}, status = 404)
    with open(log_file_path, 'r', encoding = 'utf-8') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    logger.error(f"ip:{request_ip} request to read {log_date}.log")
    return json({"logs": lines})

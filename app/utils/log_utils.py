import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import pytz

from app import config


class TimeZoneFormatter(logging.Formatter):
    def __init__(self, tz, fmt = None, datefmt = None):
        super().__init__(fmt, datefmt)
        self.tz = pytz.timezone(tz)

    def formatTime(self, record, datefmt = None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")


def set_up_logger(logger_name, loglevel = logging.INFO):
    """
    生成特定的logger
    :return:
    """
    current_time = datetime.now()
    # 创建包含年月的子目录
    log_dir = os.path.join("log", current_time.strftime("%Y-%m"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # 如果不存在，创建该目录
    logfile = os.path.join(log_dir, f"{current_time.strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger(logger_name)  # 获取或创建logger
    logger.setLevel(loglevel)

    c_handler = logging.StreamHandler()
    f_handler = TimedRotatingFileHandler(logfile, when = "midnight", encoding = "utf-8")
    c_handler.setLevel(loglevel)
    f_handler.setLevel(loglevel)

    # 创建格式器并将其添加到处理程序
    formatter = TimeZoneFormatter(
            config.get_config("TZ"),
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "%Y-%m-%d %H:%M:%S",
    )
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # 将处理程序添加到logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

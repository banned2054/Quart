import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import pytz

from app import config


class TimeZoneFilter(logging.Filter):
    def __init__(self, tz):
        super().__init__()
        self.tz = pytz.timezone(tz)  # Convert string to timezone object

    def filter(self, record):
        print("TimeZoneFilter is being called!")  # Add this line for debugging
        # Convert the record's timestamp to the desired timezone
        dt = datetime.fromtimestamp(record.created, tz = pytz.utc).astimezone(self.tz)
        record.asctime = dt.strftime('%Y-%m-%d %H:%M:%S')
        return True


# Set up the logger
def set_up_logger(logger_name, loglevel = logging.INFO):
    """
    生成特定的logger
    :return:
    """
    current_time = datetime.now()
    logfile = os.path.join('log', f"{current_time.strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger(logger_name)  # Change here
    logger.setLevel(loglevel)

    c_handler = logging.StreamHandler()
    f_handler = TimedRotatingFileHandler(logfile, when = 'midnight', encoding = 'utf-8')  # Added encoding='utf-8'
    c_handler.setLevel(loglevel)
    f_handler.setLevel(loglevel)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    tz_filter = TimeZoneFilter(config.get_config("TZ"))
    c_handler.addFilter(tz_filter)
    f_handler.addFilter(tz_filter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

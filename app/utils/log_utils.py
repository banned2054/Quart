import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class TimeZoneFilter(logging.Filter):
    def __init__(self, tz):
        super().__init__()
        self.tz = tz

    def filter(self, record):
        record.tzname = self.tz
        return True


# Set up the logger
def setup_logger(logger_name, log_dir, tz, loglevel = logging.INFO):
    current_time = datetime.now()
    logfile = os.path.join(log_dir, f"{current_time.strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger(logger_name)  # Change here
    logger.setLevel(loglevel)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = TimedRotatingFileHandler(logfile, when = 'midnight')
    c_handler.setLevel(loglevel)
    f_handler.setLevel(loglevel)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    tz_filter = TimeZoneFilter(tz)
    logger.addFilter(tz_filter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

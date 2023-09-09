from datetime import datetime


def str_to_datetime(time_str):
    """
    从str格式的时间转换成datetime
    :param str time_str: str格式的时间
    :return datetime: datetime格式的时间
    """
    try:
        # 尝试解析包含小数秒的格式
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        # 如果失败，尝试解析不包含小数秒的格式
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")


def datetime_to_str(time_datetime):
    """
    从datetime格式的时间转换成str
    :param datetime time_datetime:datetime格式的时间
    :return str: str格式的时间
    """
    return time_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")


def str_to_date(date_str):
    """
    从str格式的时间转换成date
    :param str date_str: str格式的时间
    :return date: date格式的时间
    """
    return datetime.strptime(date_str, '%Y-%m-%d').date()

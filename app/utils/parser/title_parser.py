import re

from app.utils.log_utils import set_up_logger

logger = set_up_logger(__name__)

RULES = [
    r"(.*) - (\d{1,4}(?!\d|p)|\d{1,4}\.\d{1,2}(?!\d|p))(?:v\d{1,2})?(?: )?(?:END)?(.*)",
    r"(.*)[\[\ E](\d{1,4}|\d{1,4}\.\d{1,2})(?:v\d{1,2})?(?: )?(?:END)?[\]\ ](.*)",
    r"(.*)\[(?:第)?(\d*\.*\d*)[话集話](?:END)?\](.*)",
    r"(.*)第?(\d*\.*\d*)[话話集](?:END)?(.*)",
    r"(.*)(?:S\d{2})?EP?(\d+)(.*)",
]

SUBTITLE_LANG = {
    "zh-tc"       : ["tc", "cht", "繁体", "繁日", "繁中", "zh-tw", "big5"],
    "zh-sc"       : ["sc", "chs", "简体", "简日", "简中", "zh"],
    "zh-sc-and-tc": ["繁简", "简繁"]
}


def get_subtitle_language(subtitle_name: str) -> str:
    for key, value in SUBTITLE_LANG.items():
        for v in value:
            if v in subtitle_name.lower():
                return key


def clear_title(origin_title):
    """
    清理例如'★07月新番★'的多余的文字，减少匹配难度
    :param str origin_title: 原始语句
    :return str: 清洁后的语句
    """
    result = re.sub(r' ★\d{2}月新番★ ', '', origin_title)
    result = re.sub(r' ★\d{2}月新番★', '', result)
    result = re.sub(r'★\d{2}月新番★', '', result)
    result = result.replace('[招募翻译]', '')
    result = result.replace('（急招校对、后期）', '')
    result = result.replace('[MP4]', '')

    return result


def get_title_first_step(origin_title):
    cleared_title = clear_title(origin_title)
    n = re.split(r"[\[\]()【】（）]", cleared_title)
    while "" in n:
        n.remove("")
    if len(n) > 1:
        if re.match(r"\d+", n[1]):
            return cleared_title
        return n[1]
    else:
        return n[0]


def get_title(origin_title):
    """
    从rss里item的name解析到动画的文件名
    :param str origin_title: item的name
    :return str: 动画的文件名
    """
    cleared_title = clear_title(origin_title)
    for rule in RULES:
        if not cleared_title:
            continue
        match_obj = re.match(rule, cleared_title, re.I)
        if not match_obj:
            continue
        origin_title = get_title_first_step(match_obj.group(1)).strip()
        title = origin_title.split('/')[0]
        title = title.strip()
        return title
    return ""


def get_episode(origin_title):
    """
    从rss里item的name解析到动画的集数
    :param str origin_title: item的name
    :return int: 动画的集数
    """
    cleared_title = clear_title(origin_title)
    for rule in RULES:
        if not cleared_title:
            continue
        match_obj = re.match(rule, cleared_title, re.I)
        if not match_obj:
            continue
        episode = int(match_obj.group(2))
        return episode
    return -1

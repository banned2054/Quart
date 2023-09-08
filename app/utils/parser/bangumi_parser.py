import json
from datetime import datetime

from app import config
from app.models.bangumi_subject_info import BangumiSubjectInfo, BangumiType
from app.utils.log_utils import set_up_logger
from app.utils.net_utils import fetch

logger = set_up_logger(__name__)


def get_image_url(data_dict):
    """
    获取bangumi对应的封面地址，优先度分别为common>medium>large>small>grid
    :param dict data_dict: 转换成dict格式的bangumi api返回的json
    :return str: 返回封面的地址
    """
    keys_order = ["common", "medium", "large", "small", "grid"]
    for key in keys_order:
        if key in data_dict and data_dict[key]:
            return data_dict[key]
    return ""


async def fetch_bangumi(url):
    headers = {
        'User-Agent'   : config.get_setting('User-Agent'),
        'Authorization': config.get_setting('Authorization'),
        'Cookie'       : config.get_setting('Cookie')
    }
    response = await fetch(url, headers)
    return response


async def get_episode_list(subject_id):
    """
    返回对应动画的所有集数
    :param int subject_id:动画的id
    :return tuple[bool, str]: 返回string，用','分隔
    """
    url = f"https://api.bgm.tv/v0/episodes?subject_id={subject_id}"
    response = await fetch_bangumi(url)
    if response[0]:
        subject_dict = json.loads(response[1])
        data_list = subject_dict['data']
        episode_list = ''
        for da in data_list:
            if episode_list != '':
                episode_list = episode_list + ','
            episode_list += str(da['sort'])
        logger.info(f'Get anime episodes:[{episode_list}]')
        return True, f'{episode_list}'
    else:
        return response


async def get_subject_info(subject_id):
    """
    返回对应的bangumi的信息
    :param int subject_id:对应动画/电视剧的subject id
    :return BangumiSubjectInfo:返回BangumiSubjectInfo格式的结果
    """
    url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
    response = await fetch_bangumi(url)
    if response[0]:
        subject_dict = json.loads(response[1])
        image_url = get_image_url(subject_dict['images'])
        platform = subject_dict['platform']
        origin_name = subject_dict['name']
        cn_name = subject_dict['name_cn']
        pub_date = datetime.strptime(subject_dict['date'], "%Y-%m-%d").date()
        anime_type = BangumiType(subject_dict['type'])
        subject_info = BangumiSubjectInfo(subject_id, platform, image_url, origin_name, cn_name, pub_date, anime_type)
        logger.info(f'Get anime info, subject id:{subject_id}, cn_name:{cn_name}, pub_date:{pub_date}')
        return subject_info
    else:
        return None


async def get_subject_name(subject_id):
    headers = {
        'User-Agent'   : config.get_setting('User-Agent'),
        'Authorization': config.get_setting('Authorization'),
        'Cookie'       : config.get_setting('Cookie')
    }
    url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
    response = await fetch(url, headers)
    if response[0]:
        subject_dict = json.loads(response[1])
        cn_name = subject_dict['name_cn']
        return True, cn_name
    else:
        return False, ""

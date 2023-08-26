import json
from datetime import datetime

from app import config
from app.models.bangumi.bangumi_subject_info import BangumiSubjectInfo
from app.utils.log_utils import SetUpLogger
from app.utils.net_utils import fetch

logger = SetUpLogger(__name__)


def get_image_url(data_dict):
    keys_order = ["common", "medium", "large", "small", "grid"]

    for key in keys_order:
        if key in data_dict and data_dict[key]:
            return data_dict[key]
    return None


async def get_subject_info(subject_id: int):
    headers = {
        'User-Agent'   : config.get_setting('User-Agent'),
        'Authorization': config.get_setting('Authorization'),
        'Cookie'       : config.get_setting('Cookie')
    }
    url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
    text = await fetch(url, headers)

    subject_dict = json.loads(text[9:])

    image_url = get_image_url(subject_dict['images'])
    cn_name = subject_dict['name_cn']
    pub_date = datetime.strptime(subject_dict['infobox'][3]['value'], "%Y年%m月%d日").date()

    subject_info = BangumiSubjectInfo(subject_id, image_url, cn_name, pub_date)
    logger.info(f'Get anime info, subject id:{subject_id}, cn_name:{cn_name}, pub_date:{pub_date}')
    return subject_info

from dataclasses import dataclass
from datetime import date
from enum import Enum


class BangumiType(Enum):
    Anime = 2
    TokuSaTsu = 6


@dataclass
class BangumiSubjectInfo:
    id: int
    platform: str
    image_url: str
    origin_name: str
    cn_name: str
    pub_date: date
    now_type: BangumiType

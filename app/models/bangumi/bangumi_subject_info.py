from dataclasses import dataclass
from datetime import date


@dataclass
class BangumiSubjectInfo:
    id: int
    image: str
    cn_name: str
    pub_date: date

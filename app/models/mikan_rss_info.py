from dataclasses import dataclass
from datetime import datetime


@dataclass
class RssItemInfo:
    item_name: str
    mikan_url: str
    bangumi_id: int
    episode: int
    pub_date: datetime
    origin_name: str

from app.models.sql.mikan_table import MikanTable
from app.models.sql.bangumi_table import BangumiTable
from app.models.sql.rss_item_table import RssItemTable

MikanTable.create_mikan_table_if_not_exists()
BangumiTable.create_bangumi_table_if_not_exists()
RssItemTable.create_rss_table_if_not_exists()
import sqlite3

from app.models.sql.mikan_table import MikanTable
from app.models.sql.bangumi_table import BangumiTable
from app.models.sql.rss_item_table import RssItemTable


def create_table_if_not_exists(table_schema):
    """
    假设没有数据库文件、或者没有对应的数据库的表，会执行table_schema创建对应的表格
    :param table_schema: 创建对应表格的参数
    """
    conn = sqlite3.connect('data/anime.sqlite')
    cursor = conn.cursor()
    cursor.execute(table_schema)
    conn.commit()
    conn.close()


MikanTable.create_mikan_table_if_not_exists()
BangumiTable.create_bangumi_table_if_not_exists()
RssItemTable.create_rss_table_if_not_exists()

mikan_sql = MikanTable
bangumi_sql = BangumiTable
rss_item_sql = RssItemTable

import sqlite3

from app.models.sql import create_table_if_not_exists


class RssItemTable:
    """
    用来处理和rss相关的数据库的类
    """

    @staticmethod
    def create_rss_table_if_not_exists():
        table_schema = '''
            create table if not exists rss_item
            (
                item_name varchar
                    constraint mikan_url
                        primary key,
                bangumi_id integer,
                episode integer,
                pub_date varchar
            )
        '''
        create_table_if_not_exists(table_schema)

    @staticmethod
    def insert_mikan_data(mikan_url, bangumi_id):
        database_path = 'data/anime.sql'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            insert into rss_item (mikan_url, bangumi_id)
            values (?, ?)
        ''', (mikan_url, bangumi_id))
        conn.commit()
        conn.close()

    @staticmethod
    def find_id_from_mikan_data(mikan_url: str):
        database_path = 'data/anime.sql'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from mikan_info where mikan_url=?
            ''', (mikan_url,))
        conn.close()

    @staticmethod
    def find_url_from_mikan_data(bangumi_id: int):
        database_path = 'data/anime.sql'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from mikan_info where bangumi_id=?
            ''', (bangumi_id,))
        conn.close()

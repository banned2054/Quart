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
                                pub_date varchar,
                                download_finish integer
                            )
                        '''
        create_table_if_not_exists(table_schema)

    @staticmethod
    def insert_rss_data(item_name, bangumi_id, episode, pub_date):
        database_path = 'data/anime.sql'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                                insert into rss_item (item_name, bangumi_id, episode, pub_date, download_finish)
                                values (?, ?, ?, ?, ?)
                            ''',
                       (item_name, bangumi_id, episode, pub_date, 0))
        conn.commit()
        conn.close()

    @staticmethod
    def get_rss_order_by_time():
        database_path = 'data/anime.sql'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                            select * from rss_item ORDER BY pub_date DESC
                        ''',
                       )
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

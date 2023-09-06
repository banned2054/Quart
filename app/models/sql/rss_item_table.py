import datetime
import sqlite3

from app.models.sql.universal_sql_function import create_table_if_not_exists
from app.utils.time_utils import str_to_datetime


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
                                mikan_url varchar,
                                torrent_hash varchar,
                                bangumi_id integer,
                                episode integer,
                                pub_date varchar,
                                download_finish integer
                            )
                        '''
        create_table_if_not_exists(table_schema)

    @staticmethod
    def insert_rss_data(item_name, mikan_url, bangumi_id, episode, pub_date):
        database_path = 'data/anime.db'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                                insert into rss_item (
                                                        item_name, 
                                                        mikan_url, 
                                                        torrent_hash, 
                                                        bangumi_id, 
                                                        episode, 
                                                        pub_date, 
                                                        download_finish
                                                    )
                                values (?, ?, ?, ?, ?, ?, ?)
                            ''',
                       (item_name, mikan_url, "", bangumi_id, episode, pub_date, 0))
        conn.commit()
        conn.close()

    @staticmethod
    def get_rss_order_by_time():
        database_path = 'data/anime.db'
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

    @staticmethod
    def get_latest_pub_time():
        """
        查询rss的item里最晚的pub_date
        :return datetime: datetime格式的pub_date
        """
        database_path = 'data/anime.db'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                            select pub_date from rss_item ORDER BY pub_date DESC
                        ''',
                       )
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(results) > 0:
            time_datetime = str_to_datetime(results[0])
        else:
            time_datetime = datetime.datetime.min
        return time_datetime

    @staticmethod
    def change_rss_item_hash(mikan_url, hash_code):
        """
        给torrent添加hash值
        :param str mikan_url: 该item的mikan链接
        :param str hash_code: 该item的hash值
        """
        database_path = 'data/anime.db'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                            select pub_date from rss_item ORDER BY pub_date DESC
                        ''',
                       )
        conn.commit()
        conn.close()

    @staticmethod
    def check_item_exist(mikan_url):
        """
        判断该种子是否已经添加到qbittorrent
        :param str mikan_url:https://mikanani.me/Home/Episode/后面的内容
        :return bool:  当存在该种子，返回True;否则返回False
        """
        database_path = 'data/anime.db'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                            select * from rss_item where mikan_url = (?)
                        ''',
                       (mikan_url,)
                       )
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return len(results) > 0

    @staticmethod
    def get_bangumi_id_by_origin_name(origin_name):
        """
        通过origin_name找到对应的bangumi_id
        :param str origin_name: 用title_parser解析的title
        :return int: bangumi_id
        """
        database_path = 'data/anime.db'
        RssItemTable.create_rss_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                            select distinct bangumi_id from rss_item where item_name = (?)
                        ''',
                       (origin_name,)
                       )
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(results) > 0:
            return results[0][0]
        return -1

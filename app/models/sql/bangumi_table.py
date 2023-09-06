import sqlite3

from app.models.bangumi_subject_info import BangumiSubjectInfo, BangumiType
from app.models.sql.universal_sql_function import create_table_if_not_exists


class BangumiTable:
    """
    用来处理和bangumi相关的数据库的类
    """

    @staticmethod
    def create_bangumi_table_if_not_exists():
        table_schema = '''
            create table if not exists bangumi_info
            (
                bangumi_id integer not null
                    constraint bangumi_id
                        primary key,
                platform varchar,
                image_url varchar,
                origin_name varchar,
                cn_name varchar,
                now_type integer,
                pubdate date
            );
        '''
        create_table_if_not_exists(table_schema)

    @staticmethod
    def insert_bangumi_data(bangumi_id, platform, image_url, origin_name, cn_name, now_type, pub_date):
        """
        插入一行数据
        :param int bangumi_id: bangumi上subject_id
        :param str platform: bangumi获取的api数据之一，包含TV、OVA、剧场版等
        :param str image_url: 封面图片地址
        :param str origin_name: 翻译之前的名字，日文或英文
        :param str cn_name: 翻译之后的名字
        :param int now_type: 类型
        :param datetime pub_date: 发表日期
        """
        database_path = 'data/anime.db'
        BangumiTable.create_bangumi_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bangumi_info (bangumi_id, platform, image_url, origin_name, cn_name, now_type, pubdate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (bangumi_id, platform, image_url, origin_name, cn_name, now_type, pub_date))
        conn.commit()
        conn.close()

    @staticmethod
    def get_anime_info_by_id(bangumi_id: int):
        database_path = 'data/anime.db'
        BangumiTable.create_bangumi_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from bangumi_info where bangumi_id=?
            ''', (bangumi_id,))
        results = cursor.fetchall()
        conn.close()
        if len(results) > 0:
            result = BangumiSubjectInfo(results[0][0],
                                        results[0][1],
                                        results[0][2],
                                        results[0][3],
                                        results[0][4],
                                        results[0][5],
                                        BangumiType(results[0][6]))
            return True, result
        else:
            return False, None

    @staticmethod
    def check_anime_exists(bangumi_id: int):
        database_path = 'data/anime.db'
        BangumiTable.create_bangumi_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from bangumi_info where bangumi_id=?
            ''', (bangumi_id,))
        results = cursor.fetchall()
        conn.close()
        if len(results) > 0:
            return True
        else:
            return False

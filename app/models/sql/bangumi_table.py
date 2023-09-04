import sqlite3

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
                cn_name    varchar,
                pubdate    date,
                bangumi_id integer not null
                    constraint bangumi_id
                        primary key,
                image_url  varchar
            );
        '''
        create_table_if_not_exists(table_schema)

    @staticmethod
    def insert_bangumi_data(cn_name, pub_date, bangumi_id, image_url):
        database_path = 'data/anime.db'
        BangumiTable.create_bangumi_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bangumi_info (cn_name, pubdate, bangumi_id, image_url)
            VALUES (?, ?, ?, ?)
        ''', (cn_name, pub_date, bangumi_id, image_url))
        conn.commit()
        conn.close()

    @staticmethod
    def get_anime_name_by_id(bangumi_id: str):
        database_path = 'data/anime.db'
        BangumiTable.create_bangumi_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select cn_name from bangumi_info where bangumi_id=?
            ''', (bangumi_id,))
        results = cursor.fetchall()
        conn.close()

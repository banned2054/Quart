import sqlite3


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


class MikanTable:
    """
    用来处理和mikan相关的数据库的类
    """

    @staticmethod
    def create_mikan_table_if_not_exists():
        table_schema = '''
            create table if not exists mikan_info
            (
                mikan_url  varchar
                    constraint mikan_url
                        primary key,
                bangumi_id integer
            )
        '''
        create_table_if_not_exists(table_schema)

    @staticmethod
    def insert_mikan_data(mikan_url, bangumi_id):
        database_path = 'data/anime.sql'
        MikanTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            insert into mikan_info (mikan_url, bangumi_id)
            values (?, ?)
        ''', (mikan_url, bangumi_id))
        conn.commit()
        conn.close()

    @staticmethod
    def find_id_from_mikan_data(mikan_url: str):
        database_path = 'data/anime.sql'
        MikanTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from mikan_info where mikan_url=?
            ''', (mikan_url,))
        conn.close()

    @staticmethod
    def find_url_from_mikan_data(bangumi_id: int):
        database_path = 'data/anime.sql'
        MikanTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from mikan_info where bangumi_id=?
            ''', (bangumi_id,))
        conn.close()


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
        database_path = 'data/anime.sql'
        MikanTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bangumi_info (cn_name, pubdate, bangumi_id, image_url)
            VALUES (?, ?, ?, ?)
        ''', (cn_name, pub_date, bangumi_id, image_url))
        conn.commit()
        conn.close()

    @staticmethod
    def find_id_from_mikan_data(bangumi_id: str):
        database_path = 'data/anime.sql'
        MikanTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from bangumi_info where bangumi_id=?
            ''', (bangumi_id,))
        conn.close()

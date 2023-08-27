import os
import sqlite3


class AnimeTable:
    @staticmethod
    def create_mikan_table_if_not_exists():
        conn = sqlite3.connect('data/anime.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            create table if not exists mikan_info (
                mikan_url  varchar
                    constraint mikan_url
                        primary key,
                bangumi_id integer
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def insert_mikan_data(mikan_url, bangumi_id):
        database_path = 'data/anime.sql'
        if not os.path.isfile(database_path):
            AnimeTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mikan_info (mikan_url, bangumi_id)
            VALUES (?, ?)
        ''', (mikan_url, bangumi_id))
        conn.commit()
        conn.close()

    @staticmethod
    def find_id_from_mikan_data(mikan_url: str):
        database_path = 'data/anime.sql'
        if not os.path.isfile(database_path):
            AnimeTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from mikan_info where mikan_url=?
            ''', (mikan_url,))
        conn.close()

    @staticmethod
    def find_url_from_mikan_data(bangumi_id: int):
        database_path = 'data/anime.sql'
        if not os.path.isfile(database_path):
            AnimeTable.create_mikan_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
                select * from mikan_info where bangumi_id=?
            ''', (bangumi_id,))
        conn.close()

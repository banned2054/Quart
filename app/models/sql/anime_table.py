import os
import sqlite3


class AnimeTable:
    @staticmethod
    def create_mikan_table_if_not_exists():
        print('create')
        conn = sqlite3.connect('data/anime.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mikan_info (
                mikan_url varchar PRIMARY KEY,
                bangumi_id INTEGER
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

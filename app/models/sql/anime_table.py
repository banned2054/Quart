import os
import sqlite3


class AnimeTable:
    @staticmethod
    def create_table_if_not_exists():
        print('create')
        conn = sqlite3.connect('data/anime.sql')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AnimeInfo (
                id INTEGER PRIMARY KEY,
                mikan_url TEXT,
                bangumi_id INTEGER,
                cn_name TEXT,
                file_name TEXT,
                episode_list TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def insert_data(mikan_url, bangumi_id, cn_name, file_name, episode_list):
        database_path = 'data/anime.sql'
        if not os.path.isfile(database_path):
            AnimeTable.create_table_if_not_exists()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO AnimeInfo (mikan_url, bangumi_id, cn_name, file_name, episode_list)
            VALUES (?, ?, ?, ?, ?)
        ''', (mikan_url, bangumi_id, cn_name, file_name, episode_list))
        conn.commit()
        conn.close()

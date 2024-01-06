#!/bin/bash

if [[ -z "${mikan_rss_url}" ]]; then
    echo "Environment variable mikan_rss_url is not set. Exiting."
    exit 1
fi

echo "{
    \"download_path\": \"${DOWNLOAD_PATH:-/downloads}\",
    \"mikan_rss_url\": \"${mikan_rss_url}\",
    \"proxy_url\": \"${proxy_url:-}\",
    \"TZ\": \"${TZ:-Asia/ShangHai}\",
    \"IntervalTimeToRss\":\"${IntervalTimeToRss:-300}\",
    \"qbittorrent_url\":\"${qbittorrent_url:-http://localhost:8080}\",
    \"qbittorrent_username\":\"${qbittorrent_username:-admin}\",
    \"qbittorrent_password\":\"${qbittorrent_password:-adminadmin}\",
    \"subtitle_language\":\"${subtitle_language:-zh-sc}\",
    \"file_name\": \"${file_name:-/cn_name/ E/episode/}\",
    \"dir_name\":\"${dir_name:-[/year/./month/]/cn_name/}\",
    \"anime_path\": \"${anime_path:-Anime}\",
    \"tokusatsu_path\": \"${tokusatsu_path:-Tokusatsu}\",
    \"qbittorrent_name\": \"${qbittorrent_name:-[/type/]/cn_name/ E/episode/}\",
    \"contain_filter\": \"${contain_filter:-1080p}\",
    \"my_url\": \"${my_url:-http://quart}\",
    \"web_port\": \"${web_port:-18341}\"
}" >data/config.json

echo "{
    \"User-Agent\": \"banned/Anime-Qbittorrent/1.0 (https://github.com/banned2054/Anime-Qbittorrent)\",
    \"Authorization\": \"Bearer L3vSstjEQ4xeUXSPRLSFK7vQ3EzFkhkslLquYfev\",
    \"Cookie\": \"chii_sec_id=LjHxKm1moAnfYrO5oxPYAf0sqkm5aBAa1FeJaqk\"

}" >data/setting.json

python3 main.py

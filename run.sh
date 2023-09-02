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
    \"qbittorrent_url\":${qbittorrent_url:-http://localhost:8080}\",
    \"qbittorrent_name\":${qbittorrent_name:-admin}\",
    \"qbittorrent_password\":${qbittorrent_password:-adminadmin}\"
}" >data/config.json

python3 main.py

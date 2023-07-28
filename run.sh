#!/bin/bash

if [[ -z "${mikan_rss_url}" ]]; then
    echo "Environment variable mikan_rss_url is not set. Exiting."
    exit 1
fi

echo "{
    \"download_path\": \"${DOWNLOAD_PATH:-/downloads}\",
    \"mikan_rss_url\": \"${mikan_rss_url}\",
    \"proxy_url\": \"${proxy_url:-}\",
    \"TZ\": \"${TZ:-Asia/ShangHai}\"
}" >data/config.json

python3 main.py

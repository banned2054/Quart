#!/bin/bash

if [[ -z "${mikan_rss_url}" ]]; then
    echo "Environment variable mikan_rss_url is not set. Exiting."
    exit 1
fi

echo "{
    \"download_path\": \"${DOWNLOAD_PATH:-/downloads}\",
    \"mikan_rss_url\": \"${mikan_rss_url}\",
    \"proxy_url\": \"${proxy_url:-}\"
}" >data/config.json

# Check if python3 or python command is available
if command -v python3 &>/dev/null; then
    python3 main.py
elif command -v python &>/dev/null; then
    python main.py
else
    echo "Python is not installed. Exiting."
    exit 1
fi

import asyncio
import os

import qbittorrentapi

from app import config
from app.utils.log_utils import set_up_logger

qbt_client = qbittorrentapi.Client(host = config.get_config("qbittorrent_url"),
                                   username = config.get_config("qbittorrent_name"),
                                   password = config.get_config("qbittorrent_password"))
logger = set_up_logger(__name__)


def is_torrent_complete_and_matching(torrent_hash, expected_name):
    """
    判断hash值和name是否相匹配，并且该torrent是否下载完成

    :param str torrent_hash: The hash of the torrent to check
    :param str expected_name: The expected name of the torrent
    :return tuple[bool, str]: 当hash值和name相匹配，而且该torrent下载完成，返回ture，否则返回false
    """
    try:
        torrent_info = qbt_client.torrents_info(torrent_hashes = torrent_hash)[0]
        if torrent_info.name != expected_name:
            logger.error(f"hash:{torrent_hash}, this torrent's name is not {expected_name}")
            return False, "Don't match"
        if torrent_info.progress < 1:
            logger.error(f"hash:{torrent_hash}, this torrent is not download complete")
            return False, "Download not complete"

        logger.info(f"hash:{torrent_hash}, name: {expected_name}, this torrent download complete")
        return True, "Download complete"
    except IndexError:
        logger.error(f"hash:{torrent_hash}, this torrent has some error unusual")
        return False, "Other error"


async def download_one_file(torrent_path, save_path, dir_name, file_name, tag):
    """
    添加种子到qbittorrent
    :param str torrent_path: torrent文件的路径
    :param str save_path: 下载的路径，例如`/downloads/Anime`
    :param str dir_name: 下载的动画的文件夹，例如`[2023.01]白圣女与黑牧师`
    :param str file_name: 下载的单集动画名，例如`白圣女与黑牧师 E01.mp4`
    :param str tag:
    :return:
    """
    startTorrentList = {torrent.hash: torrent for torrent in qbt_client.torrents_info()}
    with open(torrent_path, 'rb') as f:
        torrent_content = f.read()
    qbt_client.torrents_add(torrent_files = torrent_content,
                            savepath = save_path,
                            is_paused = True)
    await asyncio.sleep(2)
    endTorrentList = {torrent.hash: torrent for torrent in qbt_client.torrents_info()}
    newTorrents = set(endTorrentList) - set(startTorrentList)
    newTorrentHash = newTorrents.pop()
    qbt_client.torrents_rename(torrent_hash = newTorrentHash, new_torrent_name = dir_name)
    qbt_client.torrents_rename_file(torrent_hash = newTorrentHash, file_id = 0,
                                    new_file_name = os.path.join(dir_name, file_name))
    qbt_client.torrents_add_tags(torrent_hashes = newTorrentHash, tags = tag)
    qbt_client.torrents_recheck(newTorrentHash)
    await asyncio.sleep(10)
    qbt_client.torrents_resume(newTorrentHash)
    qbt_client.torrents_reannounce(torrent_hashes = newTorrentHash)

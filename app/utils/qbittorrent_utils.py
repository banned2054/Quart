import asyncio
import traceback

import qbittorrentapi

from app import config
from app.models.sql import RssItemTable
from app.utils.file_utils import remove_file
from app.utils.log_utils import set_up_logger

qbt_client = qbittorrentapi.Client(host = config.get_config("qbittorrent_url"),
                                   username = config.get_config("qbittorrent_username"),
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


async def download_one_file(torrent_path, new_torrent_name, save_path, dir_name, file_name, tag, item_info):
    """
    添加种子到qbittorrent
    :param str torrent_path: torrent文件的路径
    :param str save_path: 下载的路径，例如`/downloads/Anime`
    :param str dir_name: 下载的动画的文件夹，例如`[2023.01]白圣女与黑牧师`
    :param str file_name: 下载的单集动画名，例如`白圣女与黑牧师 E01.mp4`
    :param str tag:
    :return:
    """
    try:
        start_torrent_list = {torrent.hash: torrent for torrent in qbt_client.torrents_info()}
        with open(torrent_path, 'rb') as f:
            torrent_content = f.read()
        # 一开始就暂停下载，方便改名字
        qbt_client.torrents_add(torrent_files = torrent_content,
                                savepath = save_path,
                                is_paused = True)
        await asyncio.sleep(2)
        end_torrent_list = {torrent.hash: torrent for torrent in qbt_client.torrents_info()}
        # 获取最新添加的torrent
        new_torrents = set(end_torrent_list) - set(start_torrent_list)
        # 检查new_torrents是否为空
        if not new_torrents:
            await torrent_already_add(torrent_path, new_torrent_name, dir_name, file_name, tag, item_info)
            return
        torrent_hash = new_torrents.pop()
        await after_add_torrent(torrent_path, torrent_hash, new_torrent_name, dir_name, file_name, tag, item_info)
    except Exception as e:
        error_str = str(e)
        tb = traceback.extract_tb(e.__traceback__)
        filename = tb[-1].filename
        lineno = tb[-1].lineno
        logger.error(f"Try to add qbittorrent torrent failed: {error_str}; file name: {filename}, line: {lineno}")


def get_torrent_info(specific_name):
    # 获取所有torrents的信息
    all_torrents = qbt_client.torrents_info()
    # 遍历所有torrents，查找与指定名称匹配的torrent
    target_torrent = None
    for torrent in all_torrents:
        if torrent.name == specific_name:
            target_torrent = torrent
            break
    if target_torrent:
        return True, target_torrent.info
    else:
        return False, None


async def torrent_already_add(torrent_path, new_torrent_name, dir_name, file_name, tag, item_info):
    specific_info = get_torrent_info(new_torrent_name)
    if not specific_info[0]:
        return
    torrent_hash = specific_info.__hash__()
    await after_add_torrent(torrent_path, torrent_hash, new_torrent_name, dir_name, file_name, tag, item_info)


async def after_add_torrent(torrent_path, torrent_hash, new_torrent_name, dir_name, file_name, tag, item_info):
    # 重命名qbittorrent里的种子名
    qbt_client.torrents_rename(torrent_hash = torrent_hash, new_torrent_name = new_torrent_name)
    # 更改文件名
    files = qbt_client.torrents_files(torrent_hash = torrent_hash)
    if dir_name[-1] == '/':
        dir_name = dir_name[:-1]
    new_file_name = f'{dir_name}/{file_name}.{files[0].name.split(".")[-1]}'
    qbt_client.torrents_rename_file(torrent_hash = torrent_hash, file_id = 0,
                                    new_file_name = new_file_name)
    qbt_client.torrents_add_tags(torrent_hashes = torrent_hash, tags = tag)
    # 重新检查文件是否下载完成
    qbt_client.torrents_recheck(torrent_hash)
    await asyncio.sleep(10)
    # 继续下载
    qbt_client.torrents_resume(torrent_hash)
    qbt_client.torrents_reannounce(torrent_hashes = torrent_hash)
    RssItemTable.insert_rss_data(item_info, torrent_hash)
    remove_file(torrent_path)

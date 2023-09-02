import qbittorrentapi
from app import config
from app.utils.log_utils import SetUpLogger

qbt_client = qbittorrentapi.Client(host = config.get_config("qbittorrent_url"),
                                   username = config.get_config("qbittorrent_name"),
                                   password = config.get_config("qbittorrent_password"))

logger = SetUpLogger(__name__)


def is_torrent_complete_and_matching(torrent_hash, expected_name):
    """
    判断hash值和name是否相匹配，并且该torrent是否下载完成

    :param torrent_hash: The hash of the torrent to check
    :param expected_name: The expected name of the torrent
    :return: 当hash值和name相匹配，而且该torrent下载完成，返回ture，否则返回false
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

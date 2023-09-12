from sanic import text

from app.controller.sanic.my_sanic import MySanic
from app.controller.sanic.sanic_log_function import get_log_file, get_log_file_list
from app.controller.sanic.sanic_qbittorrent_function import qbittorrent_finish_download
from app.controller.sanic.sanic_rss_function import change_rss_url

sanic_server = MySanic("FileListApp")

# 注册新的路径函数
sanic_server.add_route(get_log_file_list, "getLogList", methods = ["POST"])
sanic_server.add_route(get_log_file, 'getLog', methods = ['POST'])
sanic_server.add_route(change_rss_url, 'changeRss', methods = ['POST'])
sanic_server.add_route(qbittorrent_finish_download, 'finishDownload')


@sanic_server.route("/")
async def default_route(request):
    return text("Hello, this is the default route!")

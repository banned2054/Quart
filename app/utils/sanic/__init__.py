from sanic import Sanic
from app.utils.sanic.sanic_log_function import get_log_file_list, get_log_file
from app.utils.sanic.sanic_rss_function import change_rss_url

sanic_server = Sanic("FileListApp")

# 注册新的路径函数
sanic_server.add_route(get_log_file_list, "getLogList", methods = ["POST"])
sanic_server.add_route(get_log_file, 'getLog', methods = ['POST'])
sanic_server.add_route(change_rss_url, 'changeRss', methods = ['POST'])

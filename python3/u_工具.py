import io
import requests
from flask import request, jsonify, send_file, Blueprint, redirect
from rediscluster import RedisCluster

from bll.nas_manager import get_token_from_cache
from comm.flask_api_register_helper import register_flask_api
from comm.u_util import *
from conf.nas_conf import 群晖地址


# 生成蓝图(部分api)
nas = Blueprint('nas', __name__)

# 注册蓝图，并指定其对应的前缀（url_prefix 可以为控制器设置统一前缀）
@register_flask_api(nas, url_prefix = "/nas")
def register_flask_api():
    pass



文件查看url_部分 = f"{群晖地址}/webapi/entry.cgi?api=SYNO.FileStation.Download&version=1&method=download&mode=open"
文件上传url_部分 = f"{群晖地址}/webapi/entry.cgi?api=SYNO.FileStation.Upload&method=upload&version=2"
文件共享url_部分 = f"{群晖地址}/webapi/entry.cgi?api=SYNO.FileStation.Sharing&version=1&method=create"


@nas.route('/file/upload', methods=['POST'])
def file_upload():
    rst = {
        "code": 200,
        "msg": "ok",
    }

    sid = flask_get输入参数(request, "sid", get_token_from_cache())
    path = flask_get输入参数(request, "path")
    if not path:
        rst["code"] = 211
        rst["msg"] = "path不能为空"
        return jsonify(rst)
    create_parents = flask_get输入参数(request, "create_parents", True)
    overwrite = flask_get输入参数(request, "overwrite", True)
    fileName = flask_get输入参数(request, "fileName", "a1.txt")
    file = request.files.get("file") # type:FileStorage
    if not file:
        rst["code"] = 212
        rst["msg"] = "file不能为空"
        return jsonify(rst)

    file = file.read()
    部分url = f"{文件上传url_部分}&_sid={sid}"

    # 上传群晖
    files = {fileName: file}
    postData = {
        "path": path,
        "create_parents": create_parents,
        "overwrite": overwrite,
    }
    resp = requests.post(url=部分url, data=postData, files=files)

    if resp.status_code != 200:
        rst["code"] = 221
    else:
        obj = to_json_obj(resp.text)
        if not obj["success"]:
            rst["code"] = 222

    return jsonify(rst)


@nas.route('/open', methods=['GET'])
def open_file():
    sid = request.values.get("sid")
    if not sid:
        sid = get_token_from_cache()
    path = request.values.get("path")

    部分url = f"{文件查看url_部分}&_sid={sid}&path="

    url = 部分url + path
    resp = requests.get(url)

    if resp.status_code != 200:
        path = "/home/500.jpg"
        if resp.status_code == 404:
            path = "/home/404.jpg"
        url = 部分url + path
        resp = requests.get(url)

    return send_file(
        io.BytesIO(resp.content),
        # mimetype='image/png',
        as_attachment=False,
        attachment_filename=get文件名(path)
    )


@nas.route('/share', methods=['GET'])
def share_file():
    # 获取参数
    sid = request.values.get("sid")
    if not sid:
        sid = get_token_from_cache()
    path = request.values.get("path")

    部分url = f"{文件共享url_部分}&_sid={sid}&path="
    群晖url = 部分url + path

    # 先找缓存
    r = RedisCluster(startup_nodes=[{"host": "192.168.1.40", "port": 7001}])
    url = r.hget("nas:share",path)
    if url:
        print()
        print(to_now_时间字符串())
        print("使用缓存：")
        print(url)
        return redirect(url, code=302)

    resp = requests.get(群晖url)

    if resp.status_code != 200:
        path = "/home/500.jpg"
        if resp.status_code == 404:
            path = "/home/404.jpg"
        url = 部分url + path
        resp = requests.get(url)

        return send_file(
            io.BytesIO(resp.content),
            # mimetype='image/png',
            as_attachment=False,
            attachment_filename=get文件名(path)
        )

    obj = to_json_obj(resp.text)
    url = getDictValue(obj,"data.links.0.url")
    print()
    print(to_now_时间字符串())
    print("new：")
    print(url)
    r.hset("nas:share",path,url)
    return redirect(url, code=302)


@nas.route('/a11', methods=['GET'])
def test():
    rst = {
        "code":200,
        "msg":"ok",
        "data":"中文数据123",
    }
    return jsonify(rst)

# coding:utf-8

import os
import shutil
from u_util.core import stream

def exist(文件全路径):
    return os.path.exists(文件全路径)

def isdir(文件全路径):
    if exist(文件全路径):
        return os.path.isdir(文件全路径)
    else:
        文件后缀 = get文件后缀(文件全路径)
        if not 文件后缀:
            return True
        else:
            return False

def ls(文件全路径, 选项="", 要包含前缀=False):
    选项 = 选项.lower()
    if exist(文件全路径):
        if isdir(文件全路径):
            if ("p" in 选项) or ("r" in 选项):
                return _getAllFilePaths(文件全路径)
            else:
                if 要包含前缀:
                    return stream(os.listdir(文件全路径))\
                            .map(lambda i: os.path.join(文件全路径,i)).collect()
                else:
                    return os.listdir(文件全路径)
        else:
            return [文件全路径];
    else:
        return []

def mkdir(文件全路径, 选项="-p"):
    选项 = 选项.lower()
    if not exist(文件全路径):
        if ("p" in 选项) or ("r" in 选项):
            os.makedirs(文件全路径)
        else:
            os.mkdir(文件全路径)

def mk(文件全路径, 选项="-p", 要删除旧文件=False):
    选项 = 选项.lower()
    if exist(文件全路径):
        if 要删除旧文件:
            rm(文件全路径)
        else:
            return

    if isdir(文件全路径):
        mkdir(文件全路径, 选项)
    else:
        所在目录 = get文件所在目录(文件全路径)
        if 所在目录 and (not exist(所在目录)):
            mk(所在目录, 选项)
        with open(文件全路径,"a"):
            pass

def rm(文件全路径, 选项="-rf"):
    if exist(文件全路径):
        if isdir(文件全路径):
            if ("p" in 选项) or ("r" in 选项):
                shutil.rmtree(文件全路径)
            else:
                try:
                    os.rmdir(文件全路径)
                except:
                    stream(ls(文件全路径)).filter(lambda i: not isdir(i)) \
                        .forEach(lambda i: rm(i))
        else:
            os.remove(文件全路径)

def get文件后缀(文件全路径):
    return os.path.splitext(文件全路径)[1]

def get文件名(文件全路径):
    return os.path.basename(文件全路径)

def get文件所在目录(文件全路径):
    return os.path.dirname(文件全路径)

def cp(旧文件, 新文件, 要删除旧文件=False):
    旧文件类型 = "dir" if isdir(旧文件) else "file"
    新文件类型 = "dir" if isdir(新文件) else "file"

    def file_file():
        # shutil.copyfile(旧文件,新文件)  # 只复制内容
        # 复制内容和权限 新文件不存在：新建，存在：覆盖
        shutil.copy(旧文件, 新文件)

    def file_dir():
        if not exist(新文件):
            mk(新文件)
        shutil.copy(旧文件,新文件)

    def dir_file():
        if not exist(新文件):
            mk(新文件)
        with open(新文件, "ab") as ff:
            for i in ls(旧文件, 要包含前缀=True):
                with open(i, "rb") as f:
                    ff.write(f.read())

    def dir_dir():
        shutil.copytree(旧文件, 新文件)

    def default():
        raise Exception("复制失败,参数类型未支持")

    switch = {
        "file-file": file_file,
        "file-dir": file_dir,
        "dir-file": dir_file,
        "dir-dir": dir_dir
    }
    switch.get(f"{旧文件类型}-{新文件类型}", default)()

    if 要删除旧文件:
        rm(旧文件)


# 递归获取 指定目录下，拥有指定后缀，的文件路径
def getDeepFilePaths(baseFilePath, ext="txt", is_deep = True, rst_filePaths=[]):
    if not baseFilePath:
        baseFilePath = "."
    # 处理ext后缀
    is_all_ext = False
    selectExt_list = []
    if not ext:
        selectExt_list.append("")
    else:
        if ext == "*":
            is_all_ext = True
        elif isinstance(ext, str):
            selectExt_list.append(f".{ext}")
        elif isinstance(ext, list):
            selectExt_list = stream(ext).filter(lambda i: i).map(lambda i: f".{i}").collect()
            if "" in ext:
                selectExt_list.append("")
        else:
            raise Exception("ext的类型不支持")

    # 获取当前目录下的所有文件名
    f_list = stream(os.listdir(baseFilePath)) \
                .map(lambda fileName: f"{baseFilePath}/{fileName}") \
                .collect()

    if is_all_ext:
        rst_filePaths += stream(f_list) \
                            .filter(lambda f: not os.path.isdir(f)) \
                            .collect()
    else:
        # 将当前目录下后缀名为指定后缀的文件，放入rst_filePaths列表
        stream(f_list) \
            .filter(lambda f: not os.path.isdir(f)) \
            .filter(lambda f: os.path.splitext(f)[1] in selectExt_list) \
            .forEach(lambda f: rst_filePaths.append(f))

    # 递归当前目录下的目录
    if is_deep:
        stream(f_list) \
            .filter(lambda f: os.path.isdir(f)) \
            .forEach(lambda dir: getDeepFilePaths(dir, ext, True, rst_filePaths))

    return rst_filePaths

def _getAllFilePaths(baseFilePath, is_deep=True, rst_filePaths=[]):
    if not baseFilePath:
        baseFilePath = "."
    # 获取当前目录下的所有文件名
    f_list = stream(ls(baseFilePath, 选项="", 要包含前缀=True)) \
                .collect()
    rst_filePaths += f_list
    # 递归当前目录下的目录
    if is_deep:
        stream(f_list) \
            .filter(lambda f: isdir(f)) \
            .forEach(lambda dir: _getAllFilePaths(dir, True, rst_filePaths))

    return rst_filePaths

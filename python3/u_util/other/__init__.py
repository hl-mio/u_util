# coding:utf-8
import ctypes
import datetime
import hashlib
import json
import os
import re
import time
import traceback

from u_util import *

# region 未分类

def 每x行取第y行_生成器(x,y):
    行数 = -1 - (y - 1)
    while True:
        行数 += 1
        if 行数 % x == 0:
            yield True
        else:
            yield False

def 每x行取任意行_生成器(x, *args):
    行数 = -1
    while True:
        行数 += 1
        余数 = 行数 % x
        if (余数+1) in args:
            yield True
        else:
            yield False

def x分钟后的unix(minutes=30):

    return time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=minutes)).timetuple())

def x分钟前的unix(minutes=30):
    return time.mktime((datetime.datetime.now() - datetime.timedelta(minutes=minutes)).timetuple())



def change_locals(frame, 修改表={}):
    frame.f_locals.update(修改表)
    ctypes.pythonapi.PyFrame_LocalsToFast(
        ctypes.py_object(frame),
        ctypes.c_int(0)
    )


# 文件名添加数字后缀以避免重名
def 文件名防重_追加数字(filename, base_dir = "", is_中间加斜杠 = False, is_数字前加下划线 = True, 后缀数字 = 2, 步长=1):
    if is_中间加斜杠:
        base_dir = base_dir + "/"
    输出文件 = base_dir + filename

    # 确定输出的文件名
    前缀字符 = os.path.splitext(输出文件)[0]
    后缀类型 = os.path.splitext(输出文件)[1]
    while os.path.exists(输出文件):
        if is_数字前加下划线:
            输出文件 = f"{前缀字符}_{后缀数字}{后缀类型}"
        else:
            输出文件 = f"{前缀字符}{后缀数字}{后缀类型}"
        后缀数字 += 步长

    match结果 = re.match(f"({base_dir})([\s\S]*)", 输出文件)
    if match结果:
        return match结果.group(2)
    else:
        return 输出文件




# 获取当前时间的字符串
def getCurrentDatetime_str(format_str="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format_str)



# endregion 未分类

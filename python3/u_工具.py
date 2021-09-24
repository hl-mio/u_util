# -*- coding: utf-8 -*-
# @Time    : 2021-08-16
# @Author  : hlmio
import hashlib
import json
import os
import shutil
import time
import datetime
import random
import threading
import uuid
import re
import traceback
import ctypes
import functools
import pathlib
import concurrent.futures
from functools import wraps



# region 未分类


# region flask_api

def flask_get输入参数(request, 参数名, 默认值=None, 参数在json的路径=None):
    try:
        rst = request.values.get(参数名)
        if not rst:
            if not 参数在json的路径:
                rst = getDictValue(request.json, 参数名)
            else:
                rst = getDictValue(request.json, 参数在json的路径)

        if not rst:
            raise Exception(f"未找到{参数名}参数")
        return rst
    except:
        return 默认值

# endregion


__lock_print = threading.Lock()
def print_加锁(*args, **kwargs):
    with __lock_print:
        print(*args, **kwargs)

def change_locals(frame, 修改表={}):
    frame.f_locals.update(修改表)
    ctypes.pythonapi.PyFrame_LocalsToFast(
        ctypes.py_object(frame),
        ctypes.c_int(0)
    )

# endregion 未分类


# region excel
import xlrd
import openpyxl

excel类型 = {
    "xlrd":{
        "workbook": "<class 'xlrd.book.Book'>",
        "sheet": "<class 'xlrd.sheet.Sheet'>",
    },
    "openpyxl": {
        "workbook": "<class 'openpyxl.workbook.workbook.Workbook'>",
        "sheet": "<class 'openpyxl.worksheet.worksheet.Worksheet'>",
    }
}


def get_excel_workbook(文件路径, 底层实现="xlrd"):
    底层实现 = 底层实现.lower()
    if 底层实现.lower() == "xlrd":
        return get_excel_workbook__xlrd(文件路径)
    if 底层实现.lower() == "openpyxl":
        return get_excel_workbook__openpyxl(文件路径)
    return Exception("底层实现未支持")
def get_excel_workbook__xlrd(文件路径):
    return xlrd.open_workbook(文件路径)
def get_excel_workbook__openpyxl(文件路径):
    return openpyxl.load_workbook(文件路径)

def get_excel_sheet(文件路径, sheet下标=0, sheet名=None, 底层实现="xlrd"):
    底层实现 = 底层实现.lower()
    if 底层实现 == "xlrd":
        return get_excel_sheet__xlrd(文件路径,sheet下标,sheet名)
    if 底层实现 == "openpyxl":
        return get_excel_sheet__openpyxl(文件路径,sheet下标,sheet名)
    return Exception("底层实现未支持")
def get_excel_sheet__xlrd(文件路径, sheet下标=0, sheet名=None):
    workbook = get_excel_workbook__xlrd(文件路径)
    if sheet名:
        return workbook.sheet_by_name(sheet名)
    else:
        return workbook.sheet_by_index(int(sheet下标))
def get_excel_sheet__openpyxl(文件路径, sheet下标=0, sheet名=None):
    workbook = get_excel_workbook__openpyxl(文件路径)
    if sheet名:
        return workbook.get_sheet_by_name(sheet名)
    else:
        return workbook.worksheets[sheet下标]




def get_excel_行数(sheet):
    def xlrd_sheet():
        return sheet.nrows

    def openpyxl_sheet():
        return sheet.max_row

    def default():
        raise Exception("参数类型未支持")

    switch = {
        excel类型["xlrd"]["sheet"] : xlrd_sheet,
        excel类型["openpyxl"]["sheet"]: openpyxl_sheet,
    }
    return switch.get(repr(type(sheet)), default)()
def get_excel_列数(sheet):
    def xlrd_sheet():
        return sheet.ncols

    def openpyxl_sheet():
        return sheet.max_column

    def default():
        raise Exception("参数类型未支持")

    switch = {
        excel类型["xlrd"]["sheet"] : xlrd_sheet,
        excel类型["openpyxl"]["sheet"]: openpyxl_sheet,
    }
    return switch.get(repr(type(sheet)), default)()


def get_excel_值(sheet, 行下标, 列下标):
    def xlrd_sheet():
        return _get_excel_合并单元格__xlrd(sheet, 行下标, 列下标)

    # 待处理合并单元格
    def openpyxl_sheet():
        return sheet.cell(row=行下标+1, column=列下标+1).value

    def default():
        raise Exception("参数类型未支持")

    switch = {
        excel类型["xlrd"]["sheet"] : xlrd_sheet,
        excel类型["openpyxl"]["sheet"]: openpyxl_sheet,
    }
    return switch.get(repr(type(sheet)), default)()
def get_excel_值_by序号(sheet, 行序号, 列序号):
    行下标 = to_excel序号_数字(行序号) - 1
    列下标 = to_excel序号_数字(列序号) - 1
    return get_excel_值(sheet, 行下标, 列下标)
def get_excel_值_by单词(sheet, 单词="A1"):
    单词match = re.match("([a-z A-Z]*)([0-9]*)([a-z A-Z]*)", 单词)
    列序号 = 单词match.group(1)
    if not 列序号: 列序号 = 单词match.group(3)
    行下标 = int(单词match.group(2)) - 1
    列下标 = to_excel序号_数字(列序号) - 1
    return get_excel_值(sheet, 行下标, 列下标)


def get_excel_行(sheet, 行下标):
    def xlrd_sheet():
        值list = []
        for j in range(get_excel_列数(sheet)):
            值list.append(get_excel_值(sheet,行下标,j))
        return 值list

    def default():
        raise Exception("参数类型未支持")

    switch = {
        excel类型["xlrd"]["sheet"] : xlrd_sheet,
    }
    return switch.get(repr(type(sheet)), default)()
def get_excel_列(sheet, 列下标):
    def xlrd_sheet():
        值list = []
        for i in range(get_excel_行数(sheet)):
            值list.append(get_excel_值(sheet, i, 列下标))
        return 值list
        return sheet.ncols

    def default():
        raise Exception("参数类型未支持")

    switch = {
        excel类型["xlrd"]["sheet"] : xlrd_sheet,
    }
    return switch.get(repr(type(sheet)), default)()


def get_excel_表头(sheet, 表头行下标__int或list):
    def xlrd_sheet():
        表头行下标 = 表头行下标__int或list
        if isinstance(表头行下标, int):
            表头list = get_excel_行(sheet, 表头行下标)
            return stream(表头list).map(lambda i: str(i).strip()).collect()
        assert not isinstance(表头行下标, (int, str))
        sheet_columns = sheet.ncols
        表头list = ["" for i in range(sheet_columns)]
        表头行下标.sort()
        for i in 表头行下标:
            for j in range(sheet_columns):
                if _is_excel_合并单元格__xlrd(sheet, i, j):
                    if _is_excel_第一行的合并单元格__xlrd(sheet, i, j):
                        cell_value = get_excel_值(sheet, i, j)
                        表头list[j] = f"{表头list[j]}-{cell_value}"
                else:
                    cell_value = sheet.cell_value(i, j)
                    表头list[j] = f"{表头list[j]}-{cell_value}"
        表头list = stream(表头list).map(lambda i: i[1:]).collect()
        return 表头list

    def default():
        raise Exception("参数类型未支持")

    switch = {
        excel类型["xlrd"]["sheet"] : xlrd_sheet,
    }
    return switch.get(repr(type(sheet)), default)()




from openpyxl.utils import get_column_letter, column_index_from_string
def to_excel序号_字母(数字):
    if isinstance(数字, str):
        try:
            数字 = int(数字)
        except Exception as e: return 数字
    return get_column_letter(数字)
def to_excel序号_数字(字母):
    if isinstance(字母, int): return 字母
    return column_index_from_string(字母)
def get_excel序号_列表(开头序号_字母或数字__包括开头, 结尾序号_字母或数字__包括结尾, 生成字母列表=True):
    开头序号 = to_excel序号_数字(开头序号_字母或数字__包括开头)
    结尾序号 = to_excel序号_数字(结尾序号_字母或数字__包括结尾)
    返回列表 = []
    for i in range(开头序号, 结尾序号 + 1):
        返回列表.append(i)
    if 生成字母列表:
        返回列表 = stream(返回列表).map(lambda i: to_excel序号_字母(i)).collect()
    return 返回列表




def _get_excel_合并单元格__xlrd(sheet, 行下标, 列下标):
    单元格值 = sheet.cell_value(行下标, 列下标)
    if not 单元格值:
        merged = sheet.merged_cells
        for (row_index_min, row_index_max, col_index_min, col_index_max) in merged:
            if row_index_min <= 行下标 and 行下标 < row_index_max:
                if col_index_min <= 列下标 and 列下标 < col_index_max:
                    单元格值 = sheet.cell_value(row_index_min, col_index_min)
                    break
    return 单元格值
def _is_excel_合并单元格__xlrd(sheet, 行下标, 列下标):
    merged = sheet.merged_cells
    for (row_index_min, row_index_max, col_index_min, col_index_max) in merged:
        if row_index_min <= 行下标 and 行下标 < row_index_max:
            if col_index_min <= 列下标 and 列下标 < col_index_max:
                return True
    return False
def _is_excel_第一行的合并单元格__xlrd(sheet, 行下标, 列下标):
    merged = sheet.merged_cells
    for (row_index_min, row_index_max, col_index_min, col_index_max) in merged:
        if row_index_min == 行下标:
            if col_index_min <= 列下标 and 列下标 < col_index_max:
                return True
    return False
# endregion


# region shell
import subprocess
import platform


def is_linux_system():
    return 'linux' in platform.system().lower()

def is_windows_system():
    return 'windows' in platform.system().lower()

def shell(cmd, stdout=subprocess.PIPE, encoding="utf8", shell=True, check=True, **kwargs):
    return subprocess.run(cmd, stdout=stdout, encoding=encoding, shell=shell, check=check, **kwargs)\
                    .stdout
# endregion


# region 生成器
def 每x行取第y行_生成器类(x, y):
    行数 = -1 - (y - 1)
    while True:
        行数 += 1
        if 行数 % x == 0:
            yield True
        else:
            yield False


def 每x行取任意行_生成器类(x, 行编号=[]):
    if isinstance(行编号, int):
        行编号 = [行编号]
    行数 = -1
    while True:
        行数 += 1
        余数 = 行数 % x
        if (余数 + 1) in 行编号:
            yield True
        else:
            yield False


def 计时点_生成器类(几个点一组=3, 几个组换行=5, 输出的点="."):
    每x行取第x行 = 每x行取第y行_生成器类(几个点一组, 几个点一组)
    每y行取第y行 = 每x行取第y行_生成器类(几个点一组 * 几个组换行, 几个点一组 * 几个组换行)
    while True:
        最终输出 = 输出的点
        if next(每x行取第x行):
            最终输出 += " "
        if next(每y行取第y行):
            最终输出 += "\n"
        yield 最终输出
# endregion


# region 装饰器

# region 计时
def 打点计时(func):
    @wraps(func)  # 复制原始函数信息，并保留下来
    def inner(*args, **kwargs):  # args和kwargs，是原始函数的参数；args是元祖，kwargs是字典

        # region 执行原始函数前
        计时器 = 打点计时类.实例化()
        计时器.打点()
        # endregion

        rst = func(*args, **kwargs)  # 执行原始函数

        # region 执行原始函数后
        计时器.打点()
        print_加锁(f'''{func.__name__}: {计时器.计时()}''')
        # endregion

        return rst

    return inner
# endregion

# region 线程
# -- 关于初始化区，扫描到几个@就执行几次

__线程池_装饰专用 = concurrent.futures.ThreadPoolExecutor(12)


def 线程模式_改(is_VIP = False, VIP_name = None):  # 这里的参数，是给装饰器的参数
    # region 装饰器的初始化区1
    # endregion
    def wrap(func):
        # region 装饰器的初始化区3
        # endregion
        @wraps(func)  # 复制原始函数信息，并保留下来
        def inner(*args, **kwargs):  # args和kwargs，是原始函数的参数；args是元祖，kwargs是字典

            # region 执行原始函数前
            # endregion

            if is_VIP:
                rst = threading.Thread(target=func, name=VIP_name, args=args, kwargs=kwargs)
                rst.start()
            else:
                rst = __线程池_装饰专用.submit(func, *args, **kwargs)  # 执行原始函数

            # region 执行原始函数后
            # endregion

            return rst
        # region 装饰器的初始化区4
        # endregion
        return inner
    # region 装饰器的初始化区2
    # endregion
    return wrap


def 线程模式(func):
    # region 装饰器的初始化区3
    # endregion
    @wraps(func)  # 复制原始函数信息，并保留下来
    def inner(*args, **kwargs):  # args和kwargs，是原始函数的参数；args是元祖，kwargs是字典

        # region 执行原始函数前
        # endregion

        rst = __线程池_装饰专用.submit(func, *args, **kwargs)  # 执行原始函数

        # region 执行原始函数后
        # endregion

        return rst
    # region 装饰器的初始化区4
    # endregion
    return inner

# endregion

# region 定时任务
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

_scheduler = None
_定时任务列表 = []


def 定时任务_注册(触发器类型='interval', id=None, 首次是否执行=True, *任务args, **任务kwargs):  # 这里的参数，是给装饰器的参数
    # region 装饰器的初始化区：（1）装饰了别人才会执行 （2）有几个@，就执行几次
    # endregion

    def wrap(func):
        @wraps(func)  # 复制原始函数信息，并保留下来
        def inner(*args, **kwargs):  # args和kwargs，是原始函数的参数；args是元祖，kwargs是字典

            # region 执行原始函数前
            注册定时任务(func, 触发器类型, args, kwargs, id, *任务args, **任务kwargs)
            # endregion

            if 首次是否执行:
                func(*args, **kwargs)

            # region 执行原始函数后
            # endregion

        return inner

    return wrap


def 定时任务_启动():  # 这里的参数，是给装饰器的参数
    # region 装饰器的初始化区：（1）装饰了别人才会执行 （2）有几个@，就执行几次
    # endregion

    def wrap(func):
        @wraps(func)  # 复制原始函数信息，并保留下来
        def inner(*args, **kwargs):  # args和kwargs，是原始函数的参数；args是元祖，kwargs是字典

            # region 执行原始函数前
            启动定时任务()
            # endregion

            func(*args, **kwargs)  # 执行原始函数

            # region 执行原始函数后
            # endregion

        return inner

    return wrap


def 注册定时任务(func, 触发器类型, args, kwargs, id, *任务args, **任务kwargs):
    新任务 = {}
    新任务["任务"] = func
    新任务["触发器类型"] = 触发器类型
    新任务["原始函数args"] = args
    新任务["原始函数kwargs"] = kwargs
    新任务["id"] = id
    新任务["任务args"] = 任务args
    新任务["任务kwargs"] = 任务kwargs
    global _定时任务列表
    _定时任务列表.append(新任务)


def 启动定时任务():
    __executors = {
        'default': ThreadPoolExecutor(20),  # 线程池
        'processpool': ProcessPoolExecutor(5)  # 进程池
    }
    __job_defaults = {
        'coalesce': True,  # 当有任务中途中断，后面恢复后，有N个任务没有执行 coalesce：true ，恢复的任务会执行一次  coalesce：false，恢复后的任务会执行N次配合misfire_grace_time使用
        'max_instances': 1,  # 同一任务的运行实例个数
        'misfire_grace_time': 60  # 超时间隔，超过了就弃掉任务
    }
    global _scheduler
    _scheduler = BackgroundScheduler(executors=__executors, job_defaults=__job_defaults,
                                     timezone='Asia/Shanghai')
    for i in _定时任务列表:
        _scheduler.add_job(i["任务"], i["触发器类型"], i["原始函数args"], i["原始函数kwargs"], i["id"], *i["任务args"], **i["任务kwargs"])
    _scheduler.start()


@定时任务_启动()
def 启动定时任务_阻塞主线程():
    while True:
        time.sleep(60*60*1)

# endregion

# endregion


# region to_xxx

def from_hex_to_byte(str):
    return bytes.fromhex(str)
def from_byte_to_hex(字节):
    return 字节.hex()


# region time  -- datetime.datetime是原点，是核心中间类

时间字符串_模板 = "%Y-%m-%d %H:%M:%S"

def to_time_datetime(字符串or时间戳or时间元组=0, 格式字符串=时间字符串_模板, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    obj = 字符串or时间戳or时间元组

    def from_str_to_datetime():
        字符串 = obj  # type:str
        字符串 = 字符串.strip()
        if 字符串 == "" or 字符串 == "0":
            return get_now_datetime()
        return datetime.datetime.strptime(字符串, 格式字符串)

    def from_时间元组_to_datetime():
        return datetime.datetime.fromtimestamp(obj)

    def from_普通元组_to_datetime():
        nonlocal obj
        普通元组 = obj  # type:tuple
        if 普通元组.count() < 9:
            补充个数 = 9 - 普通元组.count()
            for i in range(补充个数):
                普通元组 += (-1)
        obj = time.mktime(普通元组)
        return from_时间戳_to_datetime()

    def from_时间戳_to_datetime():
        时间戳 = obj  # type:float
        if 时间戳 == 0:
            return get_now_datetime()
        return datetime.datetime.fromtimestamp(时间戳)

    def from_datetime_to_datetime():
        return obj

    def default():
        raise Exception(f"参数类型未支持：{repr(type(obj))}")

    def get_now_datetime():
        return datetime.datetime.now()

    switch = {
        "<class 'str'>": from_str_to_datetime,
        "<class 'int'>": from_时间戳_to_datetime,
        "<class 'float'>": from_时间戳_to_datetime,
        "<class 'tuple'>": from_普通元组_to_datetime,
        "<class 'time.struct_time'>": from_时间元组_to_datetime,
        "<class 'datetime.datetime'>": from_datetime_to_datetime,
    }
    原点时间 = switch.get(repr(type(obj)), default)()

    # 接下来处理时间的增减
    增加的时间 = datetime.timedelta(seconds=增加几秒, minutes=增加几分钟, hours=增加几小时, days=增加几天)
    return 原点时间 + 增加的时间

def to_time_str(datetime_or_字符串or时间戳or时间元组=0, 格式字符串=时间字符串_模板, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间元组, 格式字符串, 增加几秒, 增加几分钟, 增加几小时, 增加几天)
    return 时间对象.strftime(格式字符串)

def to_time_unix(datetime_or_字符串or时间戳or时间元组=0, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间元组, 时间字符串_模板, 增加几秒, 增加几分钟, 增加几小时, 增加几天)
    return time.mktime(时间对象.timetuple())

def to_time_tuple(datetime_or_字符串or时间戳or时间元组=0, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    时间对象 = to_time_datetime(datetime_or_字符串or时间戳or时间元组, 时间字符串_模板, 增加几秒, 增加几分钟, 增加几小时, 增加几天)
    return 时间对象.timetuple()


def to_now_datetime():
    return to_time_datetime(0)

def to_now_str(格式字符串=时间字符串_模板):
    return to_time_str(0, 格式字符串)

def to_now_unix():
    return to_time_unix(0)

def to_now_tuple():
    return to_time_tuple(0)


to_datetime = functools.partial(to_time_datetime)
to_时间字符串 = functools.partial(to_time_str)
to_时间戳 = functools.partial(to_time_unix)
to_时间元组 = functools.partial(to_time_tuple)
to_unix = functools.partial(to_time_unix)
to_now_时间戳 = functools.partial(to_now_unix)
to_now_时间元组 = functools.partial(to_now_tuple)
to_now_时间字符串 = functools.partial(to_now_str)


def x分钟前的unix(分钟数=0):
    return to_time_unix(0, 增加几分钟=-分钟数)

def 整分钟数的当前时间(整多少分钟=30):
    return 整分钟数的指定时间(整多少分钟=整多少分钟)

def 整分钟数的指定时间(指定的时间=None, 整多少分钟=30):
    分钟间隔 = 整多少分钟
    if not 指定的时间:
        指定的时间 = to_now_datetime()
    else:
        指定的时间 = to_time_datetime(指定的时间)
    当前整点时间 = 指定的时间.replace(minute=0, second=0, microsecond=0)
    当前整点时间_加一小时 = to_time_datetime(当前整点时间, 增加几小时=1)
    拿来比较的时间 = 当前整点时间_加一小时
    while 拿来比较的时间 >= 当前整点时间:
        拿来比较的时间 = to_time_datetime(拿来比较的时间, 增加几分钟=-分钟间隔)
        if 指定的时间 >= 拿来比较的时间:
            return 拿来比较的时间

# 获取当前时间的字符串
def getCurrentDatetime_str(format_str="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format_str)

# endregion

def to_self(obj):
    return to_json_obj(to_json_str(obj))

# region json

class _MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return to_time_str(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf8")
        raise Exception(f"{obj}  {repr(type(obj))}  不能被处理")

def _get_dict(obj):
    try:
        rst = dict(obj)
    except:
        rst = obj.__dict__
    return rst

def from_class_to_dict(obj):
    obj = _get_dict(obj)
    for i in obj:
        try:
            obj[i] = _get_dict(obj[i])
        except:
            pass
    return obj

def to_json_str(obj,ensure_ascii=False,check_class=True):
    if check_class:
        try:
            obj_dict = obj.__dict__
            obj = from_class_to_dict(obj)
        except:
            pass
    return json.dumps(obj,ensure_ascii=ensure_ascii, cls=_MyEncoder)

def to_json_file(obj, 文件对象, ensure_ascii=False, indent=2):
    return json.dump(obj, 文件对象, ensure_ascii=ensure_ascii, indent=indent)

def to_json_obj(字符串or文件对象):
    def from_str_to_dict():
        return json.loads(字符串or文件对象)

    def from_file_to_dict():
        return json.load(字符串or文件对象)

    def default():
        raise Exception("参数类型未支持")

    switch = {
        "<class 'str'>": from_str_to_dict,
        "<class '_io.TextIOWrapper'>": from_file_to_dict,
    }
    return switch.get(repr(type(字符串or文件对象)), default)()

# endregion

def to_md5(data):
    type_str = repr(type(data))
    if type_str != "<class 'bytes'>" and type_str != "<class 'str'>":
        data = json.dumps(data)
    if repr(type(data)) == "<class 'str'>":
        data = data.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def to_uuid(去除中横线=True, 使用随机数=True):
    if 使用随机数:
        id = uuid.uuid4()
    else:
        id = uuid.uuid1()
    id = str(id)
    if 去除中横线:
        id = id.replace("-", "")
    return id

__to_变量名__pattren = re.compile(r'[\W+\w+]*?to_变量名\((\w+)\)')
__to_变量名__变量名集 = []

def to_变量名(变量):
    global __to_变量名__变量名集
    if not __to_变量名__变量名集:
        __to_变量名__变量名集 = __to_变量名__pattren.findall(traceback.extract_stack(limit=2)[0][3])
    return __to_变量名__变量名集.pop(0)

# endregion


# region fileSystem

def exist(文件全路径):
    return os.path.exists(文件全路径)

def isdir(文件全路径):
    if exist(文件全路径):
        return os.path.isdir(文件全路径)
    else:
        if get文件后缀(文件全路径):
            return False
        else:
            return True

def pwd(文件全路径):
    return os.path.abspath(文件全路径)

def ls(文件全路径, 包含前缀=True, 选项=""):
    选项 = 选项.lower()
    if not exist(文件全路径):
        return []
    if not isdir(文件全路径):
        return [文件全路径]

    if ("p" in 选项) or ("r" in 选项):
        filePaths = getAllFilePaths(文件全路径, is_deep=True)
        if not 包含前缀:
            filePaths = stream(filePaths).map(lambda i: get文件名(i)).collect()
        return filePaths
    else:
        if 包含前缀:
            return stream(os.listdir(文件全路径)) \
                    .map(lambda i: os.path.join(文件全路径, i)).collect()
        else:
            return os.listdir(文件全路径)

def mkdir(文件全路径, 选项="-p"):
    选项 = 选项.lower()
    if not exist(文件全路径):
        if ("p" in 选项) or ("r" in 选项):
            os.makedirs(文件全路径)
        else:
            os.mkdir(文件全路径)

def mk(文件全路径, 已有跳过_不删除=True, 选项="-p"):
    选项 = 选项.lower()
    if exist(文件全路径):
        if 已有跳过_不删除:
            return
        else:
            rm(文件全路径, "-rf")

    if isdir(文件全路径):
        mkdir(文件全路径, 选项)
    else:
        所在目录 = get文件所在目录(文件全路径)
        if 所在目录 and (not exist(所在目录)):
            mkdir(所在目录, 选项)
        with open(文件全路径, "a"):
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

def clear(文件全路径, 选项="-rf"):
    if not isdir(文件全路径): rm(文件全路径, 选项); return;
    if not exist(文件全路径): mk(文件全路径, 选项="-p"); return;
    stream(ls(文件全路径)).forEach(lambda f: rm(f, 选项))

def cp(旧文件, 新文件, 不删旧文件=True):
    旧文件类型 = "dir" if isdir(旧文件) else "file"
    新文件类型 = "dir" if isdir(新文件) else "file"

    # 确保文件夹存在
    if 新文件类型 == "dir":
        mk(新文件)
    if not exist(get文件所在目录(新文件)):
        mk(get文件所在目录(新文件))

    def file_file():
        # shutil.copyfile(旧文件,新文件)  # 只复制内容
        # 复制内容和权限 新文件不存在：新建，存在：覆盖
        shutil.copy(旧文件, 新文件)

    def file_dir():
        if not exist(新文件):
            mk(新文件)
        shutil.copy(旧文件, 新文件)

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

    if not 不删旧文件:
        rm(旧文件, "-rf")


def get文件名(文件全路径):
    return os.path.basename(文件全路径)
def get文件后缀(文件全路径):
    return os.path.splitext(文件全路径)[1]
def get文件所在目录(文件全路径):
    return os.path.dirname(文件全路径)


def getAllFilePaths(baseFilePath, is_deep=True):
    return getDeepFilePaths(baseFilePath, "*", is_deep)
# 递归获取 指定目录下，拥有指定后缀，的文件路径
def getDeepFilePaths(baseFilePath, ext_list="txt", is_deep=True):
    rst_filePaths = []
    _getDeepFilePaths(rst_filePaths, baseFilePath, ext_list, is_deep)
    return rst_filePaths
def _getDeepFilePaths(rst_filePaths, baseFilePath, ext_list="txt", is_deep=True):
    rst_filePaths += _getCurrentFilePaths(baseFilePath, ext_list)
    # 递归当前目录下的目录
    if is_deep:
        f_list = stream(os.listdir(baseFilePath)) \
                    .map(lambda fileName: os.path.join(baseFilePath, fileName)) \
                    .collect()
        stream(f_list) \
            .filter(lambda f: os.path.isdir(f)) \
            .forEach(lambda dir: _getDeepFilePaths(rst_filePaths, dir, ext_list, True))
def _getCurrentFilePaths(baseFilePath, ext_list="txt"):
    rst_filePaths = []
    if not baseFilePath:
        baseFilePath = "."
    # 处理ext后缀
    is_all_ext = False
    if not isinstance(ext_list, (list,tuple)):
        ext_list = [ext_list]
    selectExt_list = stream(ext_list).map(lambda i: i if (i and i[0]==".") else f".{i}").collect()
    if ("." in selectExt_list) or (".None" in selectExt_list):
        selectExt_list.append("")
    if (".*" in selectExt_list):
        is_all_ext = True
    selectExt_list = stream(selectExt_list).filter(lambda i: i!="." and i!=".None" and i!=".*").collect()

    # 获取当前目录下的所有文件名
    f_list = stream(os.listdir(baseFilePath)) \
                .map(lambda fileName: os.path.join(baseFilePath,fileName)) \
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
    return rst_filePaths

# endregion fileSystem


# region dao

def __get_conf_vlaue(conf, key_list, default=""):
    value = default
    for key in key_list:
        try:
            value = conf[key]
            return value
        except:
            continue
    return value

# region redis
import redis as redis_py

_redis_conf = {
    "host": "127.0.0.1",
    "port": 6375,
    "username": "",
    "password": "redis",
    "db": 0,

    "decode_responses": True,
    "charset": "utf-8"
}

def _get_redis_conf(new_conf={}):
    conf = {}
    conf["host"] = new_conf.get("host", _redis_conf["host"])
    conf["port"] = new_conf.get("port", _redis_conf["port"])
    conf["username"] = __get_conf_vlaue(new_conf, ["username", "user", "name", "userName"], _redis_conf["username"])
    conf["password"] = __get_conf_vlaue(new_conf, ["password", "pass", "pw"], _redis_conf["password"])
    conf["db"] = __get_conf_vlaue(new_conf, ["db", "database"], _redis_conf["db"])

    conf["decode_responses"] = __get_conf_vlaue(new_conf, ["decode_responses"], _redis_conf["decode_responses"])
    conf["charset"] = __get_conf_vlaue(new_conf, ["charset"], _redis_conf["charset"])
    return conf


class Redis:
    def __init__(self, conf=_get_redis_conf()):
        self.conn = redis_py.StrictRedis(host=conf["host"], port=conf["port"], password=conf["password"], db=conf["db"], decode_responses=conf["decode_responses"], charset=conf["charset"])

    def __del__(self):
        if self.conn:
            try:
                self.conn.close()
            except: pass

    @staticmethod
    def 实例化(new_conf={}):
        conf = _get_redis_conf(new_conf)
        return Redis(conf)


    def 分布式锁_加锁(self, 锁名, 加锁人, 超时时间_秒=30):
        rst = self.conn.set(name=锁名, value=加锁人, nx=True, ex=超时时间_秒)
        return rst

    def 分布式锁_解锁(self, 锁名, 加锁人):
        lua = f"""
            if redis.call('get', KEYS[1]) == ARGV[1] then 
                return redis.call('del', KEYS[1])
            else 
                return 0 
            end
        """
        cmd = self.conn.register_script(lua)
        rst = cmd(keys=[锁名], args=[加锁人])
        return rst


def redis(new_conf={}):
    return Redis.实例化(new_conf)


# endregion oracle

# region oracle
import cx_Oracle

# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# select userenv('language') from dual;
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

_oracle_conf = {
    "host": "192.168.15.132",
    "port": 1521,
    "username": "c##dba",
    "password": "oracle",
    "db": "orcl"
}



def _get_oracle_conf(new_conf={}):
    conf = {}
    conf["host"] = new_conf.get("host", _oracle_conf["host"])
    conf["port"] = new_conf.get("port", _oracle_conf["port"])
    conf["username"] = __get_conf_vlaue(new_conf, ["username", "user", "name", "userName"], _oracle_conf["username"])
    conf["password"] = new_conf.get("password", _oracle_conf["password"])
    conf["db"] = new_conf.get("db", _oracle_conf["db"])
    return conf


class Oracle:
    def __init__(self, conf=_get_oracle_conf()):
        self.conn = cx_Oracle.connect(f'{conf["username"]}/{conf["password"]}@{conf["host"]}:{conf["port"]}/{conf["db"]}')
        self.cursor = self.conn.cursor()

        self.count = 0
        self.rows = []
        self.lines = []

    def __del__(self):
        if self.cursor:
            try:
                self.cursor.close()
            except: pass
        if self.conn:
            try:
                self.conn.close()
            except: pass

    @staticmethod
    def 实例化(new_conf={}):
        conf = _get_oracle_conf(new_conf)
        return Oracle(conf)

    def exec(self, sql: str, params=None):
        if params:
            cursor = self.cursor.execute(sql, params)
        else:
            cursor = self.cursor.execute(sql)

        if cursor:
            cursor = self.cursor
            self.rows = cursor.fetchall()
            self.lines = self._rows_to_lines(self.rows, cursor)
            self.count = cursor.rowcount
        else:
            self.rows = ()
            self.lines = {}
            self.count = 0
        return self

    def call(self, proc_name: str, params=[]):
        in_out = self.cursor.callproc(proc_name, params)
        cur_index = -1;
        for i in range(len(params)):
            params[i] = in_out[i]
            if repr(type(in_out[i])) == "<class 'cx_Oracle.Cursor'>":
                cur_index = i

        if cur_index != -1 and in_out[i]:
            cursor = in_out[i]
            self.rows = cursor.fetchall()
            self.lines = self._rows_to_lines(self.rows, cursor)
            self.count = cursor.rowcount
        else:
            self.rows = ()
            self.lines = {}
            self.count = 0

        return self

    def begin(self):
        self.conn.begin()
        return self

    def commit(self):
        self.conn.commit()
        return self

    def rollback(self):
        self.conn.rollback()
        return self

    def _rows_to_lines(self, rows, cursor):
        try:
            col_names = [c[0] for c in cursor.description]
        except:
            pass
        lines = []
        for row in rows:
            r_dict = {}
            for i, col in enumerate(row):
                r_dict[col_names[i]] = col
            lines.append(r_dict)
        return lines


def oracle(new_conf={}):
    return Oracle.实例化(new_conf)


# endregion oracle

# region mysql
import pymysql

_mysql_conf = {
    "host": "106.13.231.168",
    "port": 3306,
    "user": "root",
    "password": "ans573KUR",
    "db": "test",
    "charset": "utf8"
}


def _get_mysql_conf(new_conf={}):
    # if not new_conf:
    #     return copy.deepcopy(_mysql_conf)
    conf = {}
    conf["host"] = new_conf.get("host", _mysql_conf["host"])
    conf["port"] = new_conf.get("port", _mysql_conf["port"])
    conf["user"] = new_conf.get("user", _mysql_conf["user"])
    conf["password"] = new_conf.get("password", _mysql_conf["password"])
    conf["db"] = new_conf.get("db", _mysql_conf["db"])
    conf["charset"] = new_conf.get("charset", _mysql_conf["charset"])
    return conf


class Mysql:
    def __init__(self, conf=_mysql_conf):
        self.conn = pymysql.connect(host=conf["host"], port=conf["port"], user=conf["user"], password=conf["password"],
                                    db=conf["db"], charset=conf["charset"])
        self.cursor = self.conn.cursor()

        self.count = 0
        self.rows = []
        self.lines = []

        self.conn.autocommit(True)

    def __del__(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass

    @staticmethod
    def 实例化(new_conf={}):
        conf = _get_mysql_conf(new_conf)
        return Mysql(conf)

    def exec(self, sql: str, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.rows = self.cursor.fetchall()
        self.lines = self._rows_to_lines(self.rows, self.cursor)
        self.count = self.cursor.rowcount
        return self

    def call(self, proc_name: str, params=[]):
        self.cursor.callproc(proc_name, params)
        self.rows = self.cursor.fetchall()
        self.lines = self._rows_to_lines(self.rows, self.cursor)
        self.count = self.cursor.rowcount
        if params:
            select_params = ",".join([f'@_{proc_name}_{i}' for i in range(len(params))])
            self.cursor.execute(f"select {select_params}")
            in_out = self.cursor.fetchone()
            for i in range(len(params)):
                params[i] = in_out[i]
        return self

    def begin(self):
        self.conn.begin()
        return self

    def commit(self):
        self.conn.commit()
        return self

    def rollback(self):
        self.conn.rollback()
        return self

    def _rows_to_lines(self, rows, cursor):
        try:
            # col_names = stream(self.cursor.description).map(lambda c: c[0]).collect()
            col_names = [c[0] for c in cursor.description]
        except:
            pass
        lines = []
        for row in rows:
            r_dict = {}
            for i, col in enumerate(row):
                r_dict[col_names[i]] = col
            lines.append(r_dict)
        return lines


def mysql(new_conf={}):
    return Mysql.实例化(new_conf)


# endregion mysql


# endregion dao


# region 配置相关
import configparser


def _configparser_to_dict(config):
    my_dict = dict(config._sections)
    for key in my_dict:
        my_dict[key] = dict(my_dict[key])
    return my_dict


class 配置类:

    @staticmethod
    def 实例化():
        return 配置类()

    def __init__(self):
        self.数据源 = {}
        self.配置 = {}
        self.变量集 = {}
        self.关联表 = {}

    def _数据源转dict(self):
        路径 = self.数据源["路径"]
        类型 = self.数据源["类型"]
        来源 = self.数据源["来源"]

        if (not 类型) or 类型 == "auto":
            类型 = os.path.splitext(路径)[-1][1:].lower()

        try:
            if 类型 == "json":
                if 来源 == "filesystem" or 来源 == "file_system" or 来源 == "file" or 来源 == "fs":
                    dict配置 = json.loads(pathlib.Path(路径).read_text(encoding='UTF-8'))
                else:
                    raise Exception("配置加载失败，来源不支持")
            else:
                config = configparser.ConfigParser()
                config.read(路径, encoding='UTF-8')
                dict配置 = _configparser_to_dict(config)
        except:
            dict配置 = {}

        return dict配置

    def _设置数据源(self, 路径, 类型, 来源):
        self.数据源["路径"] = 路径
        self.数据源["类型"] = 类型.lower()
        self.数据源["来源"] = 来源.lower()
        return self

    def _get_dict_keyLocation_list(self, mydict={}, 分隔符=".", 前缀="", rstList=[]):
        for i in mydict.keys():
            if not 前缀:
                临时前缀 = f"{i}"
            else:
                临时前缀 = f"{前缀}{分隔符}{i}"

            if isinstance(mydict[i], dict):
                self._get_dict_keyLocation_list(mydict[i], 分隔符, 临时前缀, rstList)
            else:
                rstList.append(临时前缀)

        return rstList

    def 加载(self, 路径="./配置文件.json", 类型="auto", 来源="filesystem"):
        self.配置 = self._设置数据源(路径, 类型, 来源)._数据源转dict()
        return self

    def 取值(self, key="", 分隔符="."):
        return getDictValue(self.配置, key, 分隔符)

    def 关联(self, 变量集, 关联表={}, 分隔符="."):
        if not 关联表:
            关联表 = {}
            keyLocation = self._get_dict_keyLocation_list(变量集, 分隔符=分隔符)
            for i in keyLocation:
                关联表[i] = i
        self.变量集 = 变量集
        self.关联表 = 关联表
        return self

    def 重载(self, 分隔符=".", is_override_vars=True):
        # 加载配置
        self.配置 = self._数据源转dict()

        if is_override_vars:
            # 覆写变量
            for key in self.关联表.keys():
                old_value = getDictValue(self.变量集, key, 分隔符=分隔符)
                now_value = getDictValue(self.配置, self.关联表.get(key), old_value, 分隔符)
                setDictValue(self.变量集, key, now_value)

        return self

    def set(self, 路径="./配置文件.json", 类型="auto", 来源="filesystem"):
        return self.加载(路径, 类型, 来源)

    def get(self, key="", 分隔符="."):
        return self.取值(key, 分隔符)

    def link(self, 变量集, 关联表={}, 分隔符="."):
        return self.关联(变量集, 关联表, 分隔符=分隔符)

    def reload(self, 分隔符=".", is_override_vars=True):
        return self.重载(分隔符, is_override_vars)

    def export(self, is_del_before=False, vars={}):
        config_filePath = self.数据源["路径"]
        is_file_exist = os.path.exists(config_filePath)

        if is_file_exist:
            if is_del_before:
                os.remove(config_filePath)
            else:
                return self

        所在目录 = os.path.dirname(config_filePath)
        if 所在目录:
            if not os.path.exists(所在目录):
                os.makedirs(所在目录)

        if not vars:
            vars = self.变量集
        with open(config_filePath, 'w', encoding='utf-8') as f:
            json.dump(vars, f, ensure_ascii=False, indent=2)

        return self

    def all(self, 配置文件路径, 变量集, 类型="auto", 来源="filesystem", 关联表={}, 分隔符=".", is_del_before=False, export_vars={},
            is_override_vars=True):
        return self.set(配置文件路径, 类型, 来源).link(变量集, 关联表, 分隔符=分隔符).export(is_del_before, export_vars).reload(分隔符,
                                                                                                          is_override_vars)


配置 = 配置类.实例化()


# endregion 配置相关


# region 线程序号

class 线程序号类:
    def __init__(self, 线程间独立=True):
        self.线程间独立 = 线程间独立
        self._序号集 = {}

    @staticmethod
    def 实例化(线程间独立=True):
        return 线程序号类(线程间独立)

    def 序号_重置(self, 下一个序号数字=1):
        序号值 = 下一个序号数字 - 1
        if self.线程间独立:
            线程标识符 = threading.currentThread().ident
        else:
            线程标识符 = "全局"
        self._序号集[线程标识符] = 序号值

    def 序号(self, 字符串模板="(1)"):
        # region 获取序号值
        if self.线程间独立:
            线程标识符 = threading.currentThread().ident
        else:
            线程标识符 = "全局"

        try:
            序号值 = self._序号集[线程标识符]
        except:
            序号值 = 0

        try:
            序号值 += 1
        except:
            序号值 = 1
        self._序号集[线程标识符] = 序号值
        # endregion

        # region 输出序号值
        if repr(type(字符串模板)) == "<class 'int'>": return 序号值
        字符串模板 = str(字符串模板)
        数字match = re.match("([^0-9]*)([0-9]*)([\s\S]*)", 字符串模板)
        模板序号值 = f"{数字match.group(1)}{序号值}{数字match.group(3)}"
        return 模板序号值
        # endregion


_静态序号生成器 = 线程序号类.实例化()
_静态全局序号生成器 = 线程序号类.实例化(线程间独立=False)


def 序号_重置(下一个序号数字=1):
    _静态序号生成器.序号_重置(下一个序号数字)
def 序号(字符串模板="(1)"):
    return _静态序号生成器.序号(字符串模板)

def 全局序号_重置(下一个序号数字=1):
    _静态全局序号生成器.序号_重置(下一个序号数字)
def 全局序号(字符串模板="(1)"):
    return _静态全局序号生成器.序号(字符串模板)

# endregion 线程序号


# region 打点计时

# region 转换秒数相关
_毫秒_秒数 = 0.001
_秒_秒数 = _毫秒_秒数 * 1000
_分钟_秒数 = _秒_秒数 * 60
_小时_秒数 = _分钟_秒数 * 60
_天_秒数 = _小时_秒数 * 24


def 拆解秒数(秒数, 各时间单位值字典={}):
    if 秒数 > _天_秒数 + _小时_秒数:
        除余结果 = divmod(秒数, _天_秒数)
        各时间单位值字典["天"] = int(除余结果[0])
        return "%d 天, %s" % (int(除余结果[0]), 拆解秒数(除余结果[1], 各时间单位值字典))

    elif 秒数 > _小时_秒数 + _分钟_秒数:
        除余结果 = divmod(秒数, _小时_秒数)
        各时间单位值字典["小时"] = int(除余结果[0])
        return '%d 小时, %s' % (int(除余结果[0]), 拆解秒数(除余结果[1], 各时间单位值字典))

    elif 秒数 > _分钟_秒数 + _秒_秒数:
        除余结果 = divmod(秒数, _分钟_秒数)
        各时间单位值字典["分钟"] = int(除余结果[0])
        return '%d 分钟, %s' % (int(除余结果[0]), 拆解秒数(除余结果[1], 各时间单位值字典))

    elif 秒数 > _秒_秒数 + _毫秒_秒数:
        除余结果 = divmod(秒数, _秒_秒数)
        各时间单位值字典["秒"] = int(除余结果[0])
        return '%d 秒, %s' % (int(除余结果[0]), 拆解秒数(除余结果[1], 各时间单位值字典))

    else:
        除余结果 = divmod(秒数, _毫秒_秒数)
        各时间单位值字典["毫秒"] = int(除余结果[0])
        return "%d 毫秒" % int(除余结果[0])


# endregion

class 打点计时类:
    class 时间值存储类:
        def __init__(self, 时间值=0):
            self.时间值 = 时间值
            self.各时间单位值字典 = {}

        @staticmethod
        def 实例化():
            return 打点计时类.时间值存储类()

        def 可视化时间(self):
            # 清空字典
            self.各时间单位值字典["天"] = 0
            self.各时间单位值字典["小时"] = 0
            self.各时间单位值字典["分钟"] = 0
            self.各时间单位值字典["秒"] = 0
            self.各时间单位值字典["毫秒"] = 0
            return 拆解秒数(self.时间值, self.各时间单位值字典)

        def 秒数(self):
            return self.时间值

        def 最近计算的可视化时间字典(self):
            return self.各时间单位值字典

        def __str__(self):
            return self.可视化时间()

    def __init__(self, 数组型打点上限=150, 删除区间=[5, -5]):
        self.默认打点数组 = []
        self.个性打点字典 = {}
        self.时间值存储实例 = 打点计时类.时间值存储类.实例化()
        self.数组型打点上限 = 数组型打点上限
        self.删除区间 = 删除区间

    @staticmethod
    def 实例化(数组型打点上限=150, 删除区间=[5, -5]):
        return 打点计时类(数组型打点上限, 删除区间)

    def 打点(self, 计时点名称=None):
        计时点 = time.time()
        if len(self.默认打点数组) > self.数组型打点上限:
            self.默认打点数组 = self.默认打点数组[0:self.删除区间[0]] + self.默认打点数组[self.删除区间[1]:]
        self.默认打点数组.append(计时点)
        if 计时点名称:
            计时点名称 = str(计时点名称)
            self.个性打点字典[计时点名称] = 计时点

    def 计时(self, 起始点=None, 结束点=None):
        def 无参_无参_处理():
            所需计时点_数组 = self.默认打点数组[-2:]
            时间差值 = 所需计时点_数组[0] - 所需计时点_数组[-1]
            if 时间差值 < 0:
                时间差值 = -时间差值
            self.时间值存储实例.时间值 = 时间差值
            return self.时间值存储实例

        def 下标_下标_处理():
            所需计时点_数组 = self.默认打点数组[起始点:结束点]
            时间差值 = 所需计时点_数组[0] - 所需计时点_数组[-1]
            if 时间差值 < 0:
                时间差值 = -时间差值
            self.时间值存储实例.时间值 = 时间差值
            return self.时间值存储实例

        def 下标_无参_处理():
            所需计时点_数组 = self.默认打点数组[起始点:]
            时间差值 = 所需计时点_数组[0] - 所需计时点_数组[-1]
            if 时间差值 < 0:
                时间差值 = -时间差值
            self.时间值存储实例.时间值 = 时间差值
            return self.时间值存储实例

        def 名称_名称_处理():
            时间差值 = self.个性打点字典[起始点] - self.个性打点字典[结束点]
            if 时间差值 < 0:
                时间差值 = -时间差值
            self.时间值存储实例.时间值 = 时间差值
            return self.时间值存储实例

        def default():
            raise Exception("计时失败,参数类型未支持")

        switch = {
            "<class 'NoneType'><class 'NoneType'>": 无参_无参_处理,
            "<class 'int'><class 'int'>": 下标_下标_处理,
            "<class 'int'><class 'NoneType'>": 下标_无参_处理,
            "<class 'str'><class 'str'>": 名称_名称_处理
        }

        try:
            return switch.get(repr(type(起始点)) + repr(type(结束点)), default)()
        except Exception as e:
            print("计时出错")
            print(e)


_静态计时器 = 打点计时类.实例化()


def 打点(计时点名称=None):
    _静态计时器.打点(计时点名称)


def 计时(起始点=None, 结束点=None):
    return _静态计时器.计时(起始点, 结束点)


# endregion 打点计时


# region 随机延时

# 固定延时x秒
def delay_x_0_s(fixed_delay_num):
    x = float(fixed_delay_num)
    time.sleep(x)


# 随机延时 0~y 秒
def delay_0_y_s(random_delay_num):
    y = float(random_delay_num)
    time.sleep(random.random() * y)


# 先固定延时x秒，再随机延时 0~y 秒
# 延时区间，包前不包后
def delay_x_y_s(fixed_delay_num, random_delay_num):
    delay_x_0_s(fixed_delay_num)
    delay_0_y_s(random_delay_num)


# 随机延时 x~y 秒
# 延时区间，包前不包后
def delay_between_x_y_s(start_delay_num, end_delay_num):
    x = float(start_delay_num)
    y = float(end_delay_num)
    delay_x_0_s(x)
    delay_0_y_s(y - x)


def delay_x_s(固定延时几秒):
    delay_x_0_s(固定延时几秒)


def delay_y_s(随机延时0到几秒):
    delay_0_y_s(随机延时0到几秒)


# endregion 随机延时


# region 数据集合

def list去掉指定项(数据源list, 序号列表=None, 序号从0开始=True, 元素值列表=None, 不改变原数组=True):
    if 不改变原数组:
        数据源list = to_self(数据源list)

    if 序号列表:
        if isinstance(序号列表, str):
            序号列表 = int(序号列表)
        if isinstance(序号列表, int):
            序号列表 = [序号列表]
        if not 序号从0开始:
            序号列表 = stream(序号列表).map(lambda i: int(i) - 1).collect()
        序号列表.sort(key=None, reverse=True)
        for i in 序号列表:
            数据源list.pop(i)

    if 元素值列表:
        if not isinstance(元素值列表, (list,tuple)):
            元素值列表 = [元素值列表]
        for i in 元素值列表:
            if i in 数据源list:
                数据源list.remove(i)

    return 数据源list

def list去掉指定项_多层list(数据源list, 多层序号字符串_list=None, 序号从0开始=True, 元素值列表=None, 不改变原数组=True, 序号分隔符="."):
    if 不改变原数组:
        数据源list = to_self(数据源list)

    if 多层序号字符串_list:
        if isinstance(多层序号字符串_list, str):
            多层序号字符串_list = [多层序号字符串_list]
        for 多层序号字符串 in 多层序号字符串_list:
            序号list = 多层序号字符串.split(序号分隔符)
            临时list = 数据源list
            for i in 序号list[:-1]:
                if 序号从0开始:
                    临时list = 临时list[int(i)]
                else:
                    临时list = 临时list[int(i)-1]
            list去掉指定项(临时list,序号list[-1],序号从0开始,元素值列表=None,不改变原数组=False)

    if 元素值列表:
        if not isinstance(元素值列表, (list, tuple)):
            元素值列表 = [元素值列表]
        for 元素值 in 元素值列表:
            临时list = 数据源list
            def 递归删除list中的指定元素(数据源list, 元素值):
                list去掉指定项(数据源list, None, 序号从0开始, 元素值列表=[元素值], 不改变原数组=False)
                for i in 数据源list:
                    if isinstance(i, (list, tuple)):
                        递归删除list中的指定元素(i, 元素值)
            递归删除list中的指定元素(临时list,元素值)

    return 数据源list


# 获取多层dict的值
def getDictValue(my_dict, key="", default=None, 分隔符="."):
    if not key:
        return default

    try:
        start_index = 0
        end_index = len(key) - 1
        if key[0] == 分隔符: start_index += 1
        if key[end_index] == 分隔符: end_index -= 1
        key = key[start_index:end_index + 1]
        keys = key.split(分隔符)
        for key in keys:
            if isinstance(my_dict, (list, tuple)):
                my_dict = my_dict[int(key)]
            else:
                my_dict = my_dict[key]
        return my_dict
    except:
        return default
# 设置多层dict的值
def setDictValue(mydict, key, value, 分隔符='.'):
    keys = key.split(分隔符)
    length = len(keys)
    for index, i in enumerate(key.split(分隔符)):
        if int(index) + 1 == length:
            if isinstance(mydict, (list, tuple)):
                mydict[int(i)] = value
            else:
                mydict[i] = value
        else:
            if isinstance(mydict, (list, tuple)):
                mydict = mydict[int(i)]
            else:
                mydict = mydict[i]
# endregion


# region 流式计算

class ListStream:
    def __init__(self, my_list=[]):
        self.list = list(my_list)

    def filter(self, func):
        self.list = list(filter(func, self.list))
        return self

    def map(self, func):
        self.list = list(map(func, self.list))
        return self

    def forEach(self, func):
        list(map(func, self.list))
        return self

    def print(self):
        self.forEach(lambda item: print(item))
        return self

    def collect(self):
        return self.list

class DictStream(ListStream):
    def __init__(self, my_dict={}):
        self.list = self.dict_to_list(my_dict)

    def collect(self, is_to_dict=True):
        if is_to_dict:
            return self.list_to_dict(self.list)
        else:
            return self.list

    def dict_to_list(self, old_dict):
        new_list = []
        for i in old_dict.keys():
            temp_dict = {}
            temp_dict["key"] = i
            temp_dict["value"] = old_dict[i]
            new_list.append(temp_dict)
        return new_list

    def list_to_dict(self, old_list):
        new_dict = {}
        for i in old_list:
            new_dict[i["key"]] = i["value"]
        return new_dict

def stream(iteration):
    def list_处理():
        return ListStream(iteration)

    def dict_处理():
        return DictStream(iteration)

    def default():
        raise Exception("stream化失败,参数类型未支持")

    switch = {
        "<class 'list'>": list_处理,
        "<class 'tuple'>": list_处理,
        "<class 'str'>": list_处理,
        "<class 'dict'>": dict_处理
    }
    return switch.get(repr(type(iteration)), default)()

# endregion 流式计算

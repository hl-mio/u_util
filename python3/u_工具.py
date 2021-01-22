# coding:utf-8
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
from pathlib import Path
from concurrent import futures
from functools import wraps

# region 未分类

__lock_print = threading.Lock()

def print_加锁(*args, **kwargs):
    with __lock_print:
        print(*args, **kwargs)


def 每x行取第y行_生成器(x, y):
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
        if (余数 + 1) in args:
            yield True
        else:
            yield False

def change_locals(frame, 修改表={}):
    frame.f_locals.update(修改表)
    ctypes.pythonapi.PyFrame_LocalsToFast(
        ctypes.py_object(frame),
        ctypes.c_int(0)
    )

# 文件名添加数字后缀以避免重名
def 文件名防重_追加数字(filename, base_dir="", is_中间加斜杠=False, is_数字前加下划线=True, 后缀数字=2, 步长=1):
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

# endregion 未分类


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

__线程池_装饰专用 = futures.ThreadPoolExecutor(12)


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
                                     timezone=pytz.timezone('Asia/Shanghai'))
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

# region time  -- datetime.datetime是原点，是核心中间类

时间字符串_模板 = "%Y-%m-%d %H:%M:%S"

def to_datetime(字符串or时间戳or时间元组=0, 格式字符串=时间字符串_模板, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
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

def to_时间字符串(datetime_or_字符串or时间戳or时间元组=0, 格式字符串=时间字符串_模板, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    时间对象 = to_datetime(datetime_or_字符串or时间戳or时间元组, 格式字符串, 增加几秒, 增加几分钟, 增加几小时, 增加几天)
    return 时间对象.strftime(格式字符串)

def to_时间戳(datetime_or_字符串or时间戳or时间元组=0, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    时间对象 = to_datetime(datetime_or_字符串or时间戳or时间元组, 时间字符串_模板, 增加几秒, 增加几分钟, 增加几小时, 增加几天)
    return time.mktime(时间对象.timetuple())

def to_时间元组(datetime_or_字符串or时间戳or时间元组=0, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    时间对象 = to_datetime(datetime_or_字符串or时间戳or时间元组, 时间字符串_模板, 增加几秒, 增加几分钟, 增加几小时, 增加几天)
    return 时间对象.timetuple()

def to_unix(datetime_or_字符串or时间戳or时间元组=0, 增加几秒=0, 增加几分钟=0, 增加几小时=0, 增加几天=0):
    return to_时间戳(datetime_or_字符串or时间戳or时间元组, 增加几秒, 增加几分钟, 增加几小时, 增加几天)


def to_now_datetime():
    return to_datetime(0)

def to_now_时间字符串():
    return to_时间字符串(0)

def to_now_时间戳():
    return to_时间戳(0)

def to_now_时间元组():
    return to_时间元组(0)


def x分钟前的unix(分钟数=0):
    return to_unix(0, 增加几分钟=-分钟数)

def 整分钟数的当前时间(整多少分钟=30):
    return 整分钟数的指定时间(整多少分钟=整多少分钟)

def 整分钟数的指定时间(指定的时间=None, 整多少分钟=30):
    分钟间隔 = 整多少分钟
    if not 指定的时间:
        指定的时间 = to_now_datetime()
    else:
        指定的时间 = to_datetime(指定的时间)
    当前整点时间 = 指定的时间.replace(minute=0, second=0, microsecond=0)
    当前整点时间_加一小时 = to_datetime(当前整点时间, 增加几小时=1)
    拿来比较的时间 = 当前整点时间_加一小时
    while 拿来比较的时间 >= 当前整点时间:
        拿来比较的时间 = to_datetime(拿来比较的时间, 增加几分钟=-分钟间隔)
        if 指定的时间 >= 拿来比较的时间:
            return 拿来比较的时间

# 获取当前时间的字符串
def getCurrentDatetime_str(format_str="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format_str)

# endregion

# region json

def to_json_str(obj):
    return json.dumps(obj)

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
                return getAllFilePaths(文件全路径)
            else:
                if 要包含前缀:
                    return stream(os.listdir(文件全路径)) \
                        .map(lambda i: os.path.join(文件全路径, i)).collect()
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


def get文件后缀(文件全路径):
    return os.path.splitext(文件全路径)[1]


def get文件名(文件全路径):
    return os.path.basename(文件全路径)


def get文件所在目录(文件全路径):
    return os.path.dirname(文件全路径)


def basename(文件全路径):
    return get文件名(文件全路径)


def dirname(文件全路径):
    return get文件所在目录(文件全路径)


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

    if 要删除旧文件:
        rm(旧文件)


def getAllFilePaths(baseFilePath, is_deep=True, rst_filePaths=[]):
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
            .forEach(lambda dir: getAllFilePaths(dir, True, rst_filePaths))

    return rst_filePaths

# endregion fileSystem


# region dao

# region oracle
import cx_Oracle

# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# select userenv('language') from dual;
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

_oracle_conf = {
    "host": "192.168.15.132",
    "port": 1521,
    "user": "c##dba",
    "password": "oracle",
    "db": "orcl"
}


def _get_oracle_conf(new_conf={}):
    conf = {}
    conf["host"] = new_conf.get("host", _oracle_conf["host"])
    conf["port"] = new_conf.get("port", _oracle_conf["port"])
    conf["user"] = new_conf.get("user", _oracle_conf["user"])
    conf["password"] = new_conf.get("password", _oracle_conf["password"])
    conf["db"] = new_conf.get("db", _oracle_conf["db"])
    return f'{conf["user"]}/{conf["password"]}@{conf["host"]}:{conf["port"]}/{conf["db"]}'


class Oracle:
    def __init__(self, conf=_get_oracle_conf()):
        self.conn = cx_Oracle.connect(conf)
        self.cursor = self.conn.cursor()

        self.count = 0
        self.rows = []
        self.lines = []

    def __del__(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass

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
                    dict配置 = json.loads(Path(路径).read_text(encoding='UTF-8'))
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
    def __init__(self):
        self._序号集 = {}

    @staticmethod
    def 实例化():
        return 线程序号类()

    def 序号_重置(self, 下一个序号数字=1):
        序号值 = 下一个序号数字 - 1
        线程标识符 = threading.currentThread().ident
        self._序号集[线程标识符] = 序号值

    def 序号(self, 字符串模板="(1)"):
        # region 获取序号值
        线程标识符 = threading.currentThread().ident
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


def 序号_重置(下一个序号数字=1):
    _静态序号生成器.序号_重置(下一个序号数字)


def 序号(字符串模板="(1)"):
    return _静态序号生成器.序号(字符串模板)


# endregion 线程序号


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


# region 数据集合

# 获取多层dict的值
def getDictValue(my_dict, key="", default=None, 分隔符="."):
    if not key:
        if default:
            return default
        else:
            return my_dict

    try:
        start_index = 0
        end_index = len(key) - 1
        if key[0] == 分隔符: start_index += 1
        if key[end_index] == 分隔符: end_index -= 1
        key = key[start_index:end_index + 1]
        keys = key.split(分隔符)
        for key in keys:
            if isinstance(my_dict, list):
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
            if isinstance(mydict, list):
                mydict[int(i)] = value
            else:
                mydict[i] = value
        else:
            if isinstance(mydict, list):
                mydict = mydict[int(i)]
            else:
                mydict = mydict[i]


# 递归获取 指定目录下，拥有指定后缀，的文件路径
def getDeepFilePaths(baseFilePath, ext="txt", is_deep=True, rst_filePaths=[]):
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

# endregion

# coding:utf-8
import time
import datetime


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

# endregion
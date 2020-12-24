# coding:utf-8
import hashlib
import json
import re
import traceback
import uuid


def to_md5(data):
    type_str = repr(type(data))
    if type_str != "<class 'bytes'>" and type_str != "<class 'str'>":
        data = json.dumps(data)
    if repr(type(data)) == "<class 'str'>":
        data = data.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def to_uuid(去除中横线=True,使用随机数=True):
    if 使用随机数:
        id = uuid.uuid4()
    else:
        id = uuid.uuid1()
    id = str(id)
    if 去除中横线:
        id = id.replace("-","")
    return id

__to_变量名__pattren = re.compile(r'[\W+\w+]*?to_变量名\((\w+)\)')
__to_变量名__变量名集 = []
def to_变量名(变量):
    global __to_变量名__变量名集
    if not __to_变量名__变量名集:
        __to_变量名__变量名集 = __to_变量名__pattren.findall(traceback.extract_stack(limit=2)[0][3])
    return __to_变量名__变量名集.pop(0)

def to_str(obj):
    return json.dumps(obj)

def to_file(obj, 文件对象, ensure_ascii=False, indent=2):
    return json.dump(obj, 文件对象, ensure_ascii=ensure_ascii, indent=indent)

def to_dict(字符串or文件对象):
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

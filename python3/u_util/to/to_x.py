# coding:utf-8
import hashlib
import json
import re
import traceback

__to_变量名__pattren = re.compile(r'[\W+\w+]*?to_变量名\((\w+)\)')
__to_变量名__变量名集 = []
def to_变量名(变量):
    global __to_变量名__变量名集
    if not __to_变量名__变量名集:
        __to_变量名__变量名集 = __to_变量名__pattren.findall(traceback.extract_stack(limit=2)[0][3])
    return __to_变量名__变量名集.pop(0)

def to_md5(data):
    type_str = repr(type(data))
    if type_str != "<class 'bytes'>" and type_str != "<class 'str'>":
        data = json.dumps(data)
    if repr(type(data)) == "<class 'str'>":
        data = data.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

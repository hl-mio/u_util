# coding:utf-8

# region dict

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
        key = key[start_index:end_index+1]
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
def setDictValue(mydict,key,value,分隔符='.'):
    keys = key.split(分隔符)
    length = len(keys)
    for index,i in enumerate(key.split(分隔符)):
        if int(index)+1 == length:
            if isinstance(mydict, list):
                mydict[int(i)] = value
            else:
                mydict[i] = value
        else:
            if isinstance(mydict, list):
                mydict = mydict[int(i)]
            else:
                mydict = mydict[i]

# endregion
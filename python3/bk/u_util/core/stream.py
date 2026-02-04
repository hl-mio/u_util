# coding:utf-8
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
# coding:utf-8
# region 配置相关
import configparser
import json
import os
from pathlib import Path
from u_util.core import getDictValue,setDictValue


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

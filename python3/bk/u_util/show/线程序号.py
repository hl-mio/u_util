# coding:utf-8

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

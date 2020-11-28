# coding:utf-8
import time

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

    def __init__(self, 数组型打点上限=500, 删除区间=[5,-5]):
        self.默认打点数组 = []
        self.个性打点字典 = {}
        self.时间值存储实例 = 打点计时类.时间值存储类.实例化()
        self.数组型打点上限 = 数组型打点上限
        self.删除区间 = 删除区间

    @staticmethod
    def 实例化(数组型打点上限=500, 删除区间=[5,-5]):
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





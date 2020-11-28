# coding:utf-8
# region 随机延时
import random
import time

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

# endregion 随机延时


class delay:
    @staticmethod
    def x_y_s(fixed_delay_num, random_delay_num):
        delay_x_y_s(fixed_delay_num, random_delay_num)

    @staticmethod
    def 先固定x秒_再随机y秒(fixed_delay_num, random_delay_num):
        delay_x_y_s(fixed_delay_num, random_delay_num)

    @staticmethod
    def between_x_y_s(start_delay_num, end_delay_num):
        delay_between_x_y_s(start_delay_num, end_delay_num)

    @staticmethod
    def 随机x至y秒(start_delay_num, end_delay_num):
        delay_between_x_y_s(start_delay_num, end_delay_num)

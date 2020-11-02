# -*- encoding: utf-8 -*-

import numpy as np
import random
import math


class Robot(object):
    def __init__(self, x0=0, noise=0.0, length=10):
        self.x      = x0
        self.noise  = math.sqrt(noise)
        self.length = length

    def right_sense(self):
        """
        :return: 获得距离右边距离
        """
        right_length = random.random() * self.noise + self.length - (self.x + 1)
        # 转化为位置
        return self.length - right_length

    def left_sense(self):
        """
        :return: 获得距离左边距离
        """
        return random.random() * self.noise + self.x


def get_proba(x, length):
    #todo 根据测量值返回先验概率矩阵
    pass


def bayes_filter(bel, x):
    """
    :param bel: 当前置信度矩阵
    :param x:  观测得到x位置
    :return:  更新后置信度矩阵
    """
    bel_update = bel
    return bel_update


length = 20
x0 = 10
bel = np.ones(length) / length  # 初始概率都是 1/length
robot = Robot(x0, noise=1, length=length)
for _ in range(9):  # 前进9次i
    bel = bayes_filter(bel, robot.left_sense())  # 左边测量
    bel = bayes_filter(bel, robot.right_sense())  # 右边测量
    print(np.sum(bel))  # 和为1
    robot.x += 1


import matplotlib.pyplot as plt
plt.xticks(np.arange(0, 20, 1))
plt.imshow(np.expand_dims(bel, axis=0), cmap=plt.get_cmap('Greys'))
plt.show()
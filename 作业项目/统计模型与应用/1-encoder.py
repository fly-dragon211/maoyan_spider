# -*- encoding: utf-8 -*-
import random
import numpy as np
import statsmodels.api as sm
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression


# 加入高斯噪声
Y_man = np.random.normal(8000, 500, 100)  # 均值为8000，标准差为500
Y_woman = np.random.normal(6000, 500, 100)  # 均值为6000，标准差为500
X_man = np.zeros(100)
X_woman = np.ones(100)

X = np.concatenate((X_man, X_woman))
Y = np.concatenate((Y_man, Y_woman))
plt.scatter(X, Y)
plt.show()

# 对应打乱顺序
random.shuffle(X, lambda : 0.1)
random.shuffle(Y, lambda : 0.1)

X = sm.add_constant(X)  # 加入常量
model = sm.OLS(Y, X).fit()  # 构建最小二乘模型并拟合
print(model.summary())  # 输出回归结果


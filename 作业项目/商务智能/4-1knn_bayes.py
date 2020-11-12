# -*- encoding: utf-8 -*-
import numpy as np
import sklearn
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import xlwt


def saveMatrix2Excel(data, path):
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])
    f.save(path)

def knn_classify(Iris_data):
    # 最大最小规范化
    min_max_scaler = MinMaxScaler()
    X_norm = min_max_scaler.fit_transform(Iris_data.values[:, 0:4])

    X_train = X_norm[:-2, 0:4]
    y_train = Iris_data.values[:-2, 4]
    X_test = X_norm[-2:, 0:4]
    y_test = Iris_data.values[-2:, 4]
    saveMatrix2Excel(X_norm, './temp.xls')
    # 查看临近的点
    neigh = NearestNeighbors(n_neighbors=3)
    neigh.fit(X_train)
    print('临近的数据：', neigh.kneighbors(X_test, return_distance=False)+1)

    # knn分类
    knn = KNeighborsClassifier(n_neighbors=3, p=2)
    knn.fit(X_train, y_train)

    accuracy_train = np.sum((knn.predict(X_train) == y_train).astype(np.int)) / len(y_train)
    accuracy_test = np.sum((knn.predict(X_test) == y_test).astype(np.int)) / len(y_test)

    print('K 近邻对测试集分类：', knn.predict(X_test))
    print('测试样本准确率：%.4f' % accuracy_test)
    pass


Iris_data = pd.read_excel('./Iris.xlsx', sheet_name=0)

X_train = Iris_data.values[:-2, 0:4].astype(np.float)
y_train = Iris_data.values[:-2, 4]
X_test = Iris_data.values[-2:, 0:4].astype(np.float)
y_test = Iris_data.values[-2:, 4]

# knn
knn_classify(Iris_data)

# 朴素贝叶斯
clf = GaussianNB()
clf.fit(X_train, y_train)
accuracy_test = np.sum((clf.predict(X_test) == y_test).astype(np.int)) / len(y_test)
print('朴素贝叶斯对测试集分类：', clf.predict(X_test))
print('测试样本准确率：%.4f' % accuracy_test)


print('| $\mu_{}$    |', end='')
for each in X_train[0:3].mean(axis=0):
    print( '%.2f' % each, end='       |')

print('| $\sigma_{}$ |', end='')
for each in X_train[0:3].std(axis=0):
    print('%.2f'% each, end='       |')
# -*- encoding: utf-8 -*-
"""
参考：
https://blog.csdn.net/u010900574/article/details/52669072
https://www.jianshu.com/p/3c2dfd6e8e4e
"""
import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn import tree, svm, naive_bayes, neighbors, linear_model
from sklearn import metrics
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier



def shuffle_in_unison(a, b):
    """
    把 data 和 target 打乱
    :param a: data
    :param b: target
    :return:
    """
    assert len(a) == len(b)
    import numpy
    shuffled_a = numpy.empty(a.shape, dtype=a.dtype)
    shuffled_b = numpy.empty(b.shape, dtype=b.dtype)
    permutation = numpy.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
df = pd.read_csv(r'./red_wine_quality_data.csv', encoding='utf-8')

RESULT_PATH = r'D:\研究生\1-统计模型与应用\week6'

# 描述性分析
df_describe = df.describe()
df_describe.to_excel(os.path.join(RESULT_PATH, 'describe.xlsx'))
# for i, column in enumerate(df.columns):
#     print(column)
#     series = df[column]
#     print('中位数: %.4f，平均数：%.4f，众数：%.4f\n' % (series.median(),
#                                           series.mean(), series.value_counts().head(1).values[0]))



# *********************萌萌哒分割线****************************
# 2.建立二分类模型预测“普通红酒“(v12=3,4,5)和“高品质红酒”（v12=6,7,8）
def try_different_method(data, target):
    """

    :param data:
    :param target:
    :return: precision and recall
    """
    clfs = {
            'Logistic_Regression': linear_model.LogisticRegression(),
            'svm': svm.SVC(), \
            'decision_tree': tree.DecisionTreeClassifier(),
            'naive_gaussian': naive_bayes.GaussianNB(), \
            'naive_mul': naive_bayes.MultinomialNB(), \
            'K_neighbor': neighbors.KNeighborsClassifier(), \
            'bagging_knn': BaggingClassifier(neighbors.KNeighborsClassifier(), max_samples=0.5, max_features=0.5), \
            'bagging_tree': BaggingClassifier(tree.DecisionTreeClassifier(), max_samples=0.5, max_features=0.5),
            'random_forest': RandomForestClassifier(n_estimators=50), \
            'adaboost': AdaBoostClassifier(n_estimators=50), \
            'gradient_boost': GradientBoostingClassifier(n_estimators=50, learning_rate=1.0, max_depth=1,
                                                         random_state=0)
            }
    data, target = shuffle_in_unison(data, target)
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=0)
    scores = {'method': list(clfs.keys()), 'precision': [], 'recall': [],
              'f1': []}  # 记录结果
    for clf_key in clfs.keys():
        print('the classifier is :', clf_key)
        clf = clfs[clf_key]
        clf.fit(x_train, y_train.ravel())
        y_pred = clf.predict(x_test)
        score_acc = metrics.precision_score(y_test, y_pred, average='weighted')
        # score_acc = clf.score(x_test, y_test.ravel())
        score_recall = metrics.recall_score(y_test, y_pred, average='weighted')
        score_f1 = metrics.f1_score(y_test, y_pred, average='weighted')
        scores['precision'].append(score_acc)
        scores['recall'].append(score_recall)
        scores['f1'].append(score_f1)
        # print(metrics.classification_report(y_test, y_pred))
        print('the precision score is %.4f, the recall is %.4f:' % (score_acc, score_recall))
    return scores

# 把quality变成二分类
df_binary = df.copy()
series = df_binary['quality'].copy()
for i, each in enumerate(series):  # 按二分类划分
    if each in [3, 4, 5]:
        series[i] = 0
    else:
        series[i] = 1
df_binary['quality'] = series

binary_data = df_binary.iloc[:, 0:-1].values  # 转换成 numpy
binary_target = df_binary['quality'].values


binary_scores = try_different_method(binary_data, binary_target)
binary_scores = pd.DataFrame(binary_scores)
binary_scores.to_excel(os.path.join(RESULT_PATH, 'binary_result.xlsx'))

# *********************萌萌哒分割线****************************
# 3.	建立多分类模型预测红酒类别（v12）
print('建立多分类模型预测红酒类别（v12）')
data = df.iloc[:, 0:-1].values  # 转换成 numpy
target = df['quality'].values

scores = try_different_method(data, target)
scores = pd.DataFrame(scores)
scores.to_excel(os.path.join(RESULT_PATH, 'muti_result.xlsx'))
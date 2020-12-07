# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd


def get_entropy(df, key_column):
    """
    计算 df['column'] 的信息熵
    :param df:
    :param key_column:
    :return:
    """
    df_dict = {}
    df_entropy = 0
    for each in df[key_column]:
        if each in df_dict:
            df_dict[each] += 1
        else:
            df_dict[each] = 1

    for each in df_dict:
        prop = df_dict[each] / len(df[key_column])
        df_entropy += -prop*np.log2(prop)
    return df_entropy


def get_group_entropy(df, column, key_column):
    """
    得到按 column 分类后的熵
    :param df:
    :param column:
    :param key_column:
    :return:
    """
    df_entropy = 0
    for name, group in df.groupby(column):
        df_entropy += len(group) / len(df) * get_entropy(group, key_column)
    return df_entropy

def get_group_entropy1(df, column, key_column):
    """
    对 column 中的每个元素作为 threshold , 进行计算熵。
    返回最小熵 和 threshold
    :param df:
    :param column:
    :param key_column:
    :return:
    """
    df_entropy_min = 100000
    df_threshold = 0
    for each in df.sort_values(by=column)[column][0:-1]:
        threshold = each
        df_entropy = 0
        df_split0 = df[df[column] <= threshold]
        df_entropy += len(df_split0) / len(df) * get_entropy(df_split0, key_column)
        df_split0 = df_split0 = df[df[column] > threshold]
        df_entropy += len(df_split0) / len(df) * get_entropy(df_split0, key_column)
        # 小于df_entropy_min
        if df_entropy < df_entropy_min:
            df_entropy_min = df_entropy
            df_threshold = threshold

    return df_threshold, df_entropy_min


def get_group_entropy2(df, key_column, df_group_list: list):
    """
    得到按 df_group_list 分类后的熵
    eg:
    ```
    print(get_group_entropy2(df, '车型', [
    df[df['年收入'] <= 25], df[(25 < df['年收入']) & (df['年收入'] <= 50)], df[df['年收入'] > 50]
]))
```
    :param df:
    :param key_column:
    :param df_group_list:
    :return:
    """
    df_entropy = 0
    for group in df_group_list:
        df_entropy += len(group) / len(df) * get_entropy(group, key_column)
    return df_entropy

# -------------------------------------------
# 第一阶段，得到
df = pd.read_excel('./4-2.xlsx')
print(get_entropy(df, '车型'))
print('按性别分类后的熵：', get_group_entropy(df, '性别', '车型'))
print('按婚姻分类后的熵：', get_group_entropy(df, '婚姻', '车型'))

df.sort_values(by='年龄')
print('按年龄分类后的熵：', get_group_entropy1(df, '年龄', '车型'))

print(get_group_entropy2(df, '车型', [
    df[df['年收入'] <= 25], df[(25 < df['年收入']) & (df['年收入'] <= 50)], df[df['年收入'] > 50]
]))

# -------------------------------------------
# 第二阶段
df_1 = df[(25 < df['年收入']) & (df['年收入'] <= 50)]
get_entropy(df_1, '车型')
get_group_entropy(df_1, '性别', '车型')


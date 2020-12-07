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


# 第一阶段，得到
df = pd.read_excel('./8-3.xlsx')
print(get_entropy(df, '车型'))

print("%.4f" % get_group_entropy2(df, '车型', [
    df[df['年收入'] <= 25], df[df['年收入'] > 25]]))

print("%.4f" % get_group_entropy2(df, '车型', [
    df[df['年收入'] <= 30], df[df['年收入'] > 30]]))

print("%.4f" % get_group_entropy2(df, '车型', [
    df[df['年收入'] <= 50], df[df['年收入'] > 50]]))

# 第二阶段，上面计算出按30划分成两个区间，那么再进行划分
print("%.4f" % get_group_entropy2(df, '车型', [
    df[df['年收入'] <= 30]]))
print("%.4f" % get_group_entropy2(df, '车型', [
    df[df['年收入'] > 30]]))
# 所以对 df['年收入'] > 30 再进行划分
df_1 = df[df['年收入'] > 30]
print("%.4f" % get_group_entropy2(df_1, '车型', [
    df_1[df_1['年收入'] <= 50], df_1[df_1['年收入'] > 50]]))
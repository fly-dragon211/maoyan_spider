# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
df = pd.read_csv(r'D:\研究生\1-统计模型与应用\week3\cup_data.csv', encoding='GBK')


# ---------------------------------------
# 1. 缺失值处理与数据类型修改
def mean_fill(series: pd.Series):
    """
    均值填充
    :param series:
    :return:
    """
    series = pd.to_numeric(series, errors='coerce')
    s_sum = 0
    count = 0
    for i in range(len(series)):
        if pd.isna(series[i]):
            continue
        s_sum += series[i]
        count += 1
    if count > 0:
        s_mean = s_sum / float(count)
    else:
        return
    for i in range(len(series)):
        if pd.isna(series[i]):
            series[i] = s_mean
    print("%s均值：\t%f" % (series.name, s_mean))

    return series


def no_inf_fill(series: pd.Series):
    """
    因子型变量的缺失值记为“暂无信息”。
    :param series:
    :return:
    """
    for i in range(len(series)):
        if series[i] is np.nan:
            series[i] = '暂无信息'
    return series

# 以下变量存为数值型
for column in {'价格', '商品毛重', '商品评分', '服务态度', '物流速度'}:
    series = df[column].copy()
    df[column][:] = mean_fill(series)[:]
# 以下变量存为因子型/字符型
for column in set(df.columns) - {'价格', '商品毛重', '商品评分', '服务态度', '物流速度'}:
    series = df[column].copy()
    df[column][:] = no_inf_fill(series)[:]

df.to_excel('q1.xlsx')

# ---------------------------------------------------------
# 2. 计算价格大于10元样本价格的均值、方差以及四分之一分位数。
def remove_(series: pd.Series):
    removed_index = []
    for i, each in enumerate(series):
        if each <= 10:
            removed_index.append(i)
    series.drop(removed_index, inplace=True)
    return series

price = remove_(df['价格'].copy())
print('平均数：%f，方差：%f，四分之一分位数：%f。' %
      (price.mean(), price.std()**2, price.quantile(0.25)))


# ------------------------------------------
# 3. 请将价格变量进行对数变换，并绘制对数价格的频率分布直方图。
plt.figure(1)
plt.hist(np.log(price.values), normed=True, bins=100, log=True)
plt.xlabel('log(price)')
plt.ylabel('log(price_frequence)')
plt.title('对数价格的频率分布直方图')
plt.show()


# -----------------------------------------------
# 4. 统计不同材质保温杯的频数，绘制频数的柱状图。
material = df['材质'].value_counts()
plt.figure(2)
plt.title('不同材质保温杯的频数柱状图')
plt.bar(material.index, material.values)
plt.xlabel('材质')
plt.ylabel('频数')
plt.show()
for m_i, m_v in zip(material.index, material.values):
    print("%s\t%d" % (m_i, m_v))

# --------------------------------
# 5. 绘制进口保温杯和国产保温杯的对数价格箱线图。
plt.figure(3)
price_domestic = df.loc[df['国产进口'] == '国产']['价格']
price_foreign = df.loc[df['国产进口'] == '进口']['价格']
plt.subplot(121)
plt.title('国产保温杯的对数价格箱线图')
np.log(price_domestic).plot.box()
plt.subplot(122)
np.log(price_foreign).plot.box()
plt.grid(linestyle="--", alpha=0.3)
plt.title('进口保温杯的对数价格箱线图')
plt.show()

# ---------------------------------
# 6. 选出出现频数最高的6个品牌，绘制这6个品牌频数的柱状图。
plt.figure(4)
brand = df['商品品牌']
plt.bar(brand.value_counts()[:6].index, brand.value_counts()[:6].values)
plt.title('频数最高的6个品牌柱状图')
plt.show()
for m_i, m_v in zip(brand.value_counts()[:6].index, brand.value_counts()[:6].values):
    print("%s\t%d" % (m_i, m_v))

# ----------------------------------
# 根据保温杯毛重，创建新变量“重量水平”,毛重不大于300的记为“较轻重量”,大于400的记为“较重重量”,其余记为“中等重量”。
# 7. 绘制不同重量水平的对数价格箱线图。
plt.figure(5)
plt.suptitle('不同重量水平的对数价格箱线图')
indexs = ['较轻重量', '中等重量', '较重重量']
datas = [df.loc[df['商品毛重'] <= 300]['价格'],
        df.loc[(300 < df['商品毛重']) & (df['商品毛重'] <= 400)]['价格'],
        df.loc[df['商品毛重'] > 400]['价格']
        ]
for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.title(indexs[i])
    np.log(datas[i]).plot.box()
plt.show()

# ----------------------------------
# 8. 请基于该数据集自由发挥，再进行至少两项描述性统计分析，并进行简要解读。
# 8.1 价格中位数
print('价格中位数：', price.median())
# 8.2 价格众数
print('价格众数', price.value_counts().head(1).values[0])

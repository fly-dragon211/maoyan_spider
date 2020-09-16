# 爬取某一个网页所有某类型文件

爬取某一个网页所有某类型文件，使用requests库，可以添加代理，
文件头等。

[spider.py](./spider.py)给出的示例是爬取李宏毅2017年机器学习的课件。

## 爬取github一个网页的pdf文件

以爬取下面网址pdf文件示例
`https://github.com/zhanwen/MathModel/tree/master/%E5%9B%BD%E8%B5%9B%E8%AE%BA%E6%96%87/2016%E5%B9%B4%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/E`

对于github上面文件，需要进行地址替换，详情见
spider.GetOnePageGithub类。(其实我觉得直接
git clone更方便, 但是折腾一下哈哈哈)

代码见 [github_spider](./1-github_file_download.py)

## 爬取煎蛋网ooxx图像
[代码：2-jiandan_ooxx.py](./2-jiandan_ooxx.py)
[煎蛋ooxx](https://jandan.net/ooxx/MjAyMDA5MTYtMaa=#comments)

![效果图](https://gitee.com/hufanmax/image_bag/raw/master/img/20200916171300.png)

我们观察煎蛋网网址和图片存储位置不一样，图片地址类似下面：
```html
src="//ww1.sinaimg.cn/mw600/9f0b0dd5gy1giric3wgwmj20mj0u1nab.jpg"
```
所以只需要使用之前的方法下载一个网页里面全部的jpg图片就行了。

但是ooxx每一页的网址很特别，是一串随机字母：https://jandan.net/ooxx/MjAyMDA5MTYtMaa=#comments

我找到第一页网址，做了个循环，让爬虫每一次从下一页标签中寻找到下一页的网址：

![](https://gitee.com/hufanmax/image_bag/raw/master/img/20200916170108.png)


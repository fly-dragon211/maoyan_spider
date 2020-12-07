# 爬取课程慢满不满

## Requirements

```
selenium==3.141.0
webdriver_manager==3.2.2
```

## 主要思想

这个项目主要是使用自动化方法，在选课网站查找某个课程能不能选。主要是首先自己登录，记录cookie。

然后使用selenium进行爬取，找到是否满课，如果未满就给我发邮件。

![image-20200925105801536](https://gitee.com/hufanmax/image_bag/raw/master/img/20200925105801.png)



## 需要修改的地方

主要是get_course.py文件中的check_course函数。里面的东西需要自己根据网页修改！

还有get_cookie.py中的网址需要更改

# 代码

## 取得cookie并且存储到文件

```python
# get_cookie.py
# -*- encoding: utf-8 -*-
"""
获取cookie并且保存到本地
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import json


Browser_drive = ChromeDriverManager().install()
Browser = webdriver.Chrome
option = webdriver.ChromeOptions()
# option.add_argument('headless') # 设置option，后台打开


def browser_initial(log_url: str):
    """"
    进行浏览器初始化
    """
    browser = Browser(Browser_drive, chrome_options=option)

    browser.get(log_url)

    return browser


def get_cookies(browser):
    """
    获取cookies保存至本地
    """
    dictCookies = browser.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    with open('damai_cookies1.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')


if __name__ == "__main__":
    log_url = "教务网站"
    browser = browser_initial(log_url)
    time.sleep(20)  # 这时输入密码
    get_cookies(browser)
    browser.refresh()  # 刷新使输入的cookie起作用
    time.sleep(1)
    browser.quit()
```

## 发送邮件

```python
# mail.py
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail():
    # 第三方 SMTP 服务
    mail_host="mail.cn"  #设置服务器
    mail_user="user"    #用户名
    mail_pass="password"   #口令

    sender = ''  # 发送邮箱
    receivers = ['']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("server", 'utf-8')
    message['To'] =  Header("me", 'utf-8')

    subject = '可以选课了'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("无法发送邮件")
```



## 爬取课程并发送邮件

```python
# get_course.py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import sys
import time
import json
import selenium
import re
from selenium.webdriver.common.keys import Keys

# 自己的包
from mail import send_mail


Browser_drive = ChromeDriverManager().install()
Browser = webdriver.Chrome
option = webdriver.ChromeOptions()
# option.add_argument('headless') # 设置option，后台打开


def browser_initial(log_url: str):
    """"
    进行浏览器初始化
    """
    browser = Browser(Browser_drive, chrome_options=option)

    browser.get(log_url)

    return browser


def log_cookie(browser):
    """
    从本地读取cookies并刷新页面,成为已登录状态
    """
    with open('damai_cookies.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    # 往browser里添加cookies
    for cookie in listCookies:
        cookie_dict = cookie
        browser.add_cookie(cookie_dict)
    browser.refresh()  # 刷新网页,cookies才成功


def get_cookies(browser):
    """
    获取cookies保存至本地
    """
    dictCookies = browser.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    with open('damai_cookies1.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')


def check_course(name):
    while (True):
        browser.get('你的选课网址')
        time.sleep(3)

        # 点击查看课表，这里注意选择不会变化的量
        browser.find_element_by_xpath('//a[@role-title="本轮次开课课程查询"]').click()
        time.sleep(1)
        browser.find_element_by_xpath('//article[7]//input[@name="query_keyword"]'
                                      ).send_keys(name, Keys.ENTER)
        time.sleep(5)
        re_pattern = "style=\"color:rgba(255, 123, 123, 1)\">未满"
        if re.search(re_pattern, browser.page_source) is None:
            print("现在还是满的")
            print(re.search(re_pattern, browser.page_source))
        else:
            send_mail()
            break

        # 保存cookie，方便下次读取
        get_cookies(browser)
        time.sleep(5*60)


if __name__ == "__main__":
    log_url = "选课网站主页"
    course_name = '高级操作系统'
    browser = browser_initial(log_url)
    log_cookie(browser)
    check_course(course_name)
    browser.quit()
```





参考：

https://blog.csdn.net/weixin_43821172/article/details/105199481
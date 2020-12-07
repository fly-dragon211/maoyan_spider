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
    log_url = "http://yjs.ruc.edu.cn/yjsxkapp/sys/xsxkapp/index.html"
    browser = browser_initial(log_url)
    time.sleep(20)  # 这时输入密码
    get_cookies(browser)
    browser.refresh()  # 刷新使输入的cookie起作用
    time.sleep(1)
    browser.quit()
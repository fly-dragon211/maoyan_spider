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
        # cookie_dict = {
        #     'domain': 'yjs.ruc.edu.cn',
        #     'name': cookie.get('name'),
        #     'value': cookie.get('value'),
        #     "expires": '',
        #     'path': '/',
        #     'httpOnly': False,
        #     'HostOnly': False,
        #     'Secure': False
        # }
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
        browser.get('http://yjs.ruc.edu.cn/yjsxkapp/sys/xsxkapp/course.html')
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
    log_url = "http://yjs.ruc.edu.cn/yjsxkapp/sys/xsxkapp/index.html"
    course_name = '高级操作系统'
    browser = browser_initial(log_url)
    log_cookie(browser)
    check_course(course_name)
    browser.quit()
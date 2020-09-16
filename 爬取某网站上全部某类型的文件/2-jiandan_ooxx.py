# -*- encoding: utf-8 -*-
# 2020.9.16
import requests
import re
import os
import time
import random
from spider import GetOnePageFile


class JiandanImage(GetOnePageFile):
    def __init__(self, url_begin, url_head, file_type, page_num=5, wait_time=0,
                 folder=None, proxies=None):
        """

        :param url_begin: 起始网页
        :param url_head: 网址头
        :param page_num: 爬取网页数目
        :param file_type:
        :param wait_time:
        :param folder:
        :param proxies:
        """
        super().__init__(url_begin, url_head, file_type=file_type, wait_time=wait_time,
                 folder=folder, proxies=proxies)
        self.page_num = page_num

    def get_file_url(self, response):
        url_head = self.url_head
        file_url = []
        pattern_str = r'src="(.*?\.file_type)"'.replace("file_type", self.file_type)
        file_name = re.findall(pattern_str, response.text)
        for i, each in enumerate(file_name):
            file_url.append(url_head + each.replace(' ', '%20'))  # 把空格换成%20
            file_name[i] = each.split('/')[-1]

            #todo 加入随机命名，不过一般不会重复

        # print((file_url, file_name))
        return (file_url, file_name)

    def run(self):
        for i in range(self.page_num):
            # 创建新文件夹
            if not os.path.exists(str(i+1)):
                os.mkdir(str(i+1))
            # 开始爬取
            res = self.get_one_page(self.url)
            file_url_list, file_name_list = self.get_file_url(response=res)
            for file_url, file_name in zip(file_url_list, file_name_list):
                time.sleep(self.wait_time)
                self.get_file(file_url, os.path.join('./', str(i+1), file_name))
            time.sleep(self.wait_time)
            self.set_next_url(res)  # 转换页面到下一页继续爬取

    def set_next_url(self, this_response):
        url_head = 'http:'
        pattern_str = r'<a title="Newer Comments" href="(.*?)" class="next-comment-page"'
        next_url = re.search(pattern_str, this_response.text)
        next_url = url_head + next_url.group(1)
        self.url = next_url
        print(next_url)


if __name__ == '__main__':
    root_dir = r'D:\python\Spider\ooxx'
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    os.chdir(root_dir)

    url = 'https://jandan.net/ooxx/MjAyMDA5MTYtMaa=#comments'  # 1页图
    url_head = 'https:'
    file_type = 'jpg'
    a = JiandanImage(url, url_head, file_type, page_num=5, wait_time=random.uniform(1, 3))
    a.run()
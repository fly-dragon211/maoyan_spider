import requests
import re
import os
import time
from requests.exceptions import RequestException
from lxml import etree


class GetOnePageFile:
    """
    使用requests库进行下载，下载一个网页链接上所有某一个类型的文件.
    可能需要重写get_file_url函数中的pattern
    """
    def __init__(self, url, url_head, file_type, wait_time=0,
                 folder=None, proxies=None):
        if folder is not None:
            if not os.path.exists(folder):
                os.mkdir(folder)
            os.chdir(folder)
        self.file_type = file_type
        self.url = url
        self.url_head = url_head
        self.wait_time = wait_time
        self.proxies = proxies

    def run(self):
        res = self.get_one_page(self.url)
        file_url_list, file_name_list = self.get_file_url(response=res)
        for file_url, file_name in zip(file_url_list, file_name_list):
            time.sleep(self.wait_time)
            self.get_file(file_url, file_name)

    def get_file_url(self, response):
        url_head = self.url_head
        file_url = []
        pattern_str = r'href="(.*?\.file_type)"'.replace("file_type", self.file_type)
        file_name = re.findall(pattern_str, response.text)
        for i, each in enumerate(file_name):
            file_url.append(url_head + '/' + each.replace(' ', '%20'))  # 把空格换成%20
            file_name[i] = str(i) + each.split('/')[-1]

        return (file_url, file_name)

    def get_file(self, url, file_name):
        # 判断文件是否存在
        if os.path.exists(file_name):
            print("File has exist!")
            return
        res = self.get_one_page(url)
        with open(file_name, 'wb') as f:
            f.write(res.content)

        print("Sucessful to download" + " " + file_name)

    def get_one_page(self, url):
        try:
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
            response = requests.get(url, headers=headers, proxies=self.proxies)
            if response.status_code == 200:
                return response
            return None
        except RequestException as e:
            print('Requests error!: ', e)
            return None


class GetOnePageGithub(GetOnePageFile):
    """
    Github 下载文件，需要把文件头中/blob去掉，另外资源域名是https://raw.githubusercontent.com
    """
    def run(self):
        res = self.get_one_page(self.url)
        file_url_list, file_name_list = self.get_file_url(response=res)
        for file_url, file_name in zip(file_url_list, file_name_list):
            time.sleep(self.wait_time)
            file_url = file_url.replace("/blob", "")  # For github, you need to remove string "blog"
            self.get_file(file_url, file_name)


if __name__ == '__main__':
    root_dir = r'D:\python\Spider\Li_ppt'
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    os.chdir(root_dir)

    url = 'http://speech.ee.ntu.edu.tw/~tlkagk/courses_ML17_2.html'
    url_head = 'http://speech.ee.ntu.edu.tw/~tlkagk/'
    file_type = 'ppt'
    a = GetOnePageFile(url, url_head, file_type)
    a.run()
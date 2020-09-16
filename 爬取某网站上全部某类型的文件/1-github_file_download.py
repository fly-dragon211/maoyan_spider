# -*- encoding: utf-8 -*-

import spider
import os


def download_some_pages():
    root_dir = r'D:\python\Spider\国赛'
    file_type = 'pdf'
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    os.chdir(root_dir)

    url_list = [
        'https://github.com/zhanwen/MathModel/tree/master/%E5%9B%BD%E8%B5%9B%E8%AE%BA%E6%96%87/2016%E5%B9%B4%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/E',
        'https://github.com/zhanwen/MathModel/tree/master/%E5%9B%BD%E8%B5%9B%E8%AE%BA%E6%96%87/2017%E5%B9%B4%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/E'
    ]
    proxies = {
        'http': 'http://127.0.0.1:10809'
    }

    url_head = 'https://raw.githubusercontent.com'
    for i, url in enumerate(url_list):
        a = spider.GetOnePageGithub(url, url_head, file_type=file_type,
                                    folder=str(i), wait_time=2,
                                    proxies=proxies)
        a.run()
        os.chdir(root_dir)


if __name__ == '__main__':
    download_some_pages()
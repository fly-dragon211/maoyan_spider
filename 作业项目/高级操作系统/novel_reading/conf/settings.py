# -*- encoding: utf-8 -*-
# 用于存放配置文件

import os

# 获取项目根目录Novel - 1的根目录
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 获取db目录的路径
DB_PATH = os.path.join(BASE_PATH, 'db')

# 获取db.txt的根目录
DB_TXT_PATH = os.path.join(DB_PATH, 'db.txt')

# story_class文件目录路径
STORY_PATH = os.path.join(DB_PATH, 'story_class.txt')

# 小说存放目录
FICTION_DIR = os.path.join(DB_PATH, 'fictions')

# 日志文件的路径
LOG_PATH = os.path.join(BASE_PATH, 'log', 'log.txt')

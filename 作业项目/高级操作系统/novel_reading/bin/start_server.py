# -*- encoding: utf-8 -*-
# 用于存放启动文件

import os  # 导入os模块
import sys  # 导入sys模块

# 将项目的根目录，添加到sys.path中
sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from core import server  # 导入core中的src模块

if __name__ == '__main__':
    server.main()

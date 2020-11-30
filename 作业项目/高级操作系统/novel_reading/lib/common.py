# -*- encoding: utf-8 -*-
# 用于存放公共的功能

from conf import settings
import socket
from threading import Thread


# 登录认证装饰器login_auth
def login_auth(func):
    # 解决问题：循环导入问题
    from core import server

    def inner(*args, **kwargs):
        if server.login_user:
            res = func(*args, **kwargs)
            return res
        else:
            server.S_io.write('未登录，不允许使用其他功能，请先登录！')
            server.login()

    return inner


# 记录日志，应该放在公共功能中
def append_log(log_data):
    # 写入日志数据
    with open(settings.LOG_PATH, mode='at', encoding='UTF-8') as f:
        f.write(log_data + '\n')


class SocketIo:
    """
    SocketIo.write: 代替 print
    SocketIo.read: 代替 input
    """
    def __init__(self, connect: socket.socket):
        self.connect = connect

    def write(self, message, seq='\n'):
        self.connect.send(message.encode('utf-8'))
        self.connect.send(seq.encode('utf-8'))

    def read(self, message):
        self.write(message)
        return self.connect.recv(10*1024).decode('utf-8')  # 接收数据缓存大小
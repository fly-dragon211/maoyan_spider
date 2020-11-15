# -*- encoding: utf-8 -*-
import socket  # 导入 socket 模块
import time

s = socket.socket()  # 创建 socket 对象
s.settimeout(0.5)  # 设置套接字操作的超时期，2s

s.connect(('127.0.0.1', 8080))

i = 0
while True:
    try:
        i = 0
        while i < 5:
            receive = s.recv(1024*10).decode('utf-8')
            print(receive)
            time.sleep(0.1)
            i += 1
    except ConnectionAbortedError:
        print('连接关闭')
        break
    except Exception as e:  # todo  socket.timeout 的错误
        # print(e)
        pass

    inp = input()
    s.send(inp.encode('utf-8'))
    if inp == '0':
        print('退出')
        break

s.close()



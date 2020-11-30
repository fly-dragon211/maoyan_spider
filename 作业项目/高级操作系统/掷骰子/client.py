# -*- encoding: utf-8 -*-
# -*- encoding: utf-8 -*-
import socket  # 导入 socket 模块
import time

s = socket.socket()  # 创建 socket 对象
s.settimeout(0.1)  # 设置套接字操作的超时期，2s

s.connect(('127.0.0.1', 8081))

i = 0
while True:
    i = 0
    while i < 10:
        try:
            receive = s.recv(1024*10).decode('utf-8')
            print(receive, end='')
            time.sleep(0.2)
        except ConnectionAbortedError:
            print('连接关闭')
            break
        except Exception as e:  # socket.timeout 的错误
            # print(e)
            time.sleep(0.1)
            pass
        i += 1

    inp = input()
    s.send(inp.encode('utf-8'))
    if inp == 'no':
        print('退出')
        break

s.close()



# -*- encoding: utf-8 -*-
import os
import sys
import socket
from threading import Thread


class Logger(object):
    def __init__(self, connect: socket.socket, stream=sys.stdout):
        self.terminal = stream
        self.connect = connect

    def write(self, message):
        self.terminal.write(message)
        self.connect.send(message.encode('utf-8'))

    def read(self):
        return self.connect.recv(10*1024).decode('utf-8')  # 接收数据缓存大小

    def readline(self):
        return self.connect.recv(10*1024).decode('utf-8')  # 接收数据缓存大小

    def flush(self):
        pass


class Login:
    def __init__(self, S_io):
        self.user_info_file = "./user.txt"
        self.lock_info_file = "./locked.txt"
        self.running = True
        self.S_io = S_io

    def chose_cmd(self):
        msg = """
            0 退出
            1 登录
            2 注册
            """
        self.S_io.write(msg)
        cmd = self.S_io.read("请选择功能:").strip()
        if not cmd.isdigit():
            self.S_io.write("错误，请输入一个数字")
            return True
        cmd = int(cmd)
        if cmd == 0:
            self.running = False
        elif cmd == 1:
            self.login()
        elif cmd == 2:
            self.sign_in()
        return True

    def login(self):
        def lock(user, add=False, set_zero=False):
            """
            :param user: name
            :param add: Whether add the wrong number. Add=True means query
            :return: If the user is locked, return True.
            """
            lock_info_file = self.lock_info_file
            # lock_info_file不存在，创建
            if not os.path.exists(lock_info_file):
                with open(lock_info_file, "wt", encoding='utf-8') as f:
                    pass
            # 从文件中提取字典
            with open(lock_info_file, mode="r+t", encoding='utf-8') as f:
                try:
                    dic = eval(f.read())
                except:
                    dic = {}
            # 查看是否在字典中
            if user in dic:
                if add:
                    dic[user] += 1
                    self.S_io.write("密码错误!")
                    self.S_io.write("你已经输错了 %d 次, 还剩 %d 次." %
                                    (dic[user], 3 - dic[user]))
                if set_zero:
                    dic[user] = 0
            else:
                dic[user] = 0
            # 存储回文件
            with open(lock_info_file, mode="wt", encoding='utf-8') as f:
                f.write(str(dic))
            # 锁定
            if dic[user] >= 3:
                return True
            else:
                return False

        user_info_file = self.user_info_file
        self.S_io.write("欢迎来到登陆界面".center(50, '*'))
        inp_name = self.S_io.read("请输入用户名:").strip()

        # Match the password in user.txt
        with open(user_info_file, mode="rt", encoding="utf-8") as f:
            for line in f:
                if line.find(":") == -1:
                    continue
                user, password = line.strip().split(':')
                if inp_name == user:
                    inp_pwd = self.S_io.read("你的密码:").strip()
                    # Check if the user is locked
                    if lock(inp_name):
                        self.S_io.write('你的用户已经锁定!')
                        return
                    elif password != inp_pwd:
                        while not lock(inp_name, add=True):
                            inp_pwd = self.S_io.read("你的密码:").strip()
                    elif password == inp_pwd:
                        self.S_io.write("登陆成功!")
                        lock(inp_name, set_zero=True)
                        return
            # Not find the user
            self.S_io.write("没有找到用户!")

    def sign_in(self):
        self.S_io.write("欢迎来到注册界面".center(50, '*'))
        inp_name = self.S_io.read("请输入用户名:").strip()

        # Check whether your name in the file
        with open(self.user_info_file, mode="r+t", encoding="utf-8") as f:
            for line in f:
                if line.find(":") == -1:
                    continue
                user, password = line.strip().split(':')
                if inp_name == user:
                    self.S_io.write("用户名已经存在!")
                    return
            inp_pwd = self.S_io.read("你的密码:").strip()
            f.write("\n%s:%s\n" % (inp_name, inp_pwd))
            self.S_io.write("成功登录!")


def redirect(connect: socket.socket):
    sys.stdout = Logger(connect, sys.stdout)
    sys.stdin = Logger(connect, sys.stdin)

# 线程事件处理函数
def message_handle(connect, clientaddress):
    clientInfo = "%s:%d：" % (clientaddress[0], clientaddress[1])

    S_io = SocketIo(connect)
    L = Login(S_io)
    while L.running:
        L.chose_cmd()

    connect.close()  # 关闭客户机socket
    g_conn_pool.remove(connect)
    print("Info:客户端%s下线,目前在线客户端%d个。" % (clientInfo, len(g_conn_pool)))

class SocketIo:
    def __init__(self, connect: socket.socket):
        self.connect = connect

    def write(self, message, seq='\n'):
        self.connect.send(message.encode('utf-8'))
        self.connect.send(seq.encode('utf-8'))

    def read(self, message):
        self.write(message)
        return self.connect.recv(10*1024).decode('utf-8')  # 接收数据缓存大小


if __name__ == "__main__":
    g_conn_pool = [ ]  # 连接池

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务器socket,基于IPV4的TCP协议
    s.bind(("127.0.0.1", 8080))  # 绑定端口

    s.listen(5)  # 等待客户端连接
    while True:
        connect, clientaddress = s.accept()  # 建立客户端连接
        g_conn_pool.append(connect)
        print('连接地址：', clientaddress)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(connect, clientaddress))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

        # except Exception as e:
        #     print(e)



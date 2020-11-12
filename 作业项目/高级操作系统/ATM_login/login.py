# -*- encoding: utf-8 -*-
import os
import sys
import socket


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
    def __init__(self):
        self.user_info_file = "./user.txt"
        self.lock_info_file = "./locked.txt"
        self.running = True

    def chose_cmd(self):
        msg = """
            0 退出
            1 登录
            2 注册
            """
        print(msg)
        cmd = input("Please choose the command:").strip()
        if not cmd.isdigit():
            print("Error! Please input a digit!")
            return True
        cmd = int(cmd)
        if cmd == 0:
            L.running = False
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
                    print("Wrong password!")
                    print("You have input %d time, and remain %d time." %
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
        print("Welcome to login Interface".center(50, '*'))
        inp_name = input("Please input your name:").strip()

        # Match the password in user.txt
        with open(user_info_file, mode="rt", encoding="utf-8") as f:
            for line in f:
                if line.find(":") == -1:
                    continue
                user, password = line.strip().split(':')
                if inp_name == user:
                    inp_pwd = input("Your password:").strip()
                    # Check if the user is locked
                    if lock(inp_name):
                        print('The user is locked!')
                        return
                    elif password != inp_pwd:
                        while not lock(inp_name, add=True):
                            inp_pwd = input("Your password:").strip()
                    elif password == inp_pwd:
                        print("Login successfully!")
                        lock(inp_name, set_zero=True)
                        return
            # Not find the user
            print("Not find the user!")

    def sign_in(self):
        print("Welcome to sign in Interface".center(50, '*'))
        inp_name = input("Please input your name:").strip()

        # Check whether your name in the file
        with open(self.user_info_file, mode="r+t", encoding="utf-8") as f:
            for line in f:
                if line.find(":") == -1:
                    continue
                user, password = line.strip().split(':')
                if inp_name == user:
                    print("Your name has existed!")
                    return
            inp_pwd = input("Your password:").strip()
            f.write("\n%s:%s\n" % (inp_name, inp_pwd))
            print("Successfully sign in!")


def redirect(connect: socket.socket):
    sys.stdout = Logger(connect, sys.stdout)
    sys.stdin = Logger(connect, sys.stdin)


if __name__ == "__main__":
    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 5056  # 设置端口
    s.bind((host, port))  # 绑定端口

    s.listen(5)  # 等待客户端连接
    while True:
        try:
            c, addr = s.accept()  # 建立客户端连接
            print('连接地址：', addr)
            redirect(c)

            L = Login()
            while L.running:
                L.chose_cmd()
            c.close()  # 关闭连接
        except Exception as e:
            sys.stdout = sys.stdout.terminal
            print(e)



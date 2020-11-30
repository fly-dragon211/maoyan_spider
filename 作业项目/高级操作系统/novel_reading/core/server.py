# -*- encoding: utf-8 -*-
# 用于存放核心代码

import time
from db import db_handler
from lib import common
import os
from lib.common import SocketIo
import socket
from threading import Thread

# 定义login_user：若能进入该函数，证明该用户已经登录，还能获取当前用户名
login_user = None

# 定义socket 输入输出
S_io = socket.socket()

# 0 注册功能
def register():
    S_io.write('注册功能执行中...')
    while True:
        username = S_io.read('请输入用户名：(输入q退出)').strip()
        if username == 'q': break

        # 1.先校验用户是否存在
        # 涉及数据的操作：调用查看数据的功能：select
        # 给select函数传入当前输入的用户名，判断该用户是否存在
        user_data = db_handler.select(username)

        # 2.若存在，则让用户重新输入
        if user_data:
            S_io.write('当前用户已存在，请重新输入！')
            continue

        password = S_io.read('请输入密码：').strip()
        re_password = S_io.read('请确认密码：').strip()

        # 3.检测两次输入的密码是否一致
        if password == re_password:

            # 4.将当前用户的数据写入到文件中
            db_handler.save(username, password)
            S_io.write(f'用户[{username}]注册成功！')
            break

        else:
            S_io.write('两次密码不一致，请重新输入！')


# 1 登录功能
def login():
    S_io.write('登录功能执行中...')
    while True:
        username = S_io.read('请输入用户名：(输入q退出)').strip()
        if username == 'q': break

        # 1.查看当前用户是否存在
        user_data = db_handler.select(username)

        # 2.若不存在，则让用户重新输入
        if not user_data:
            S_io.write('该用户不存在，请重新输入！')
            continue

        password = S_io.read('请输入密码：').strip()

        # 3.校验用户输入的密码是否与db.txt中的密码一致
        if password == user_data[1]:

            # 4.用户登录后，记录登录状态
            global login_user
            login_user = username

            S_io.write(f'用户[{username}]登录成功！')
            break

        else:
            S_io.write('密码错误，登录失败！')


# 2 充值功能
@common.login_auth
def recharge():
    S_io.write('充值功能执行中...')
    while True:
        # 1.让用户输入充值的金额
        balance = S_io.read('请输入要充值的金额：').strip()

        # 2.判断用户输入的是否是数字
        if not balance.isdigit():
            S_io.write('请输入数字！')
            continue

        balance = int(balance)  # 将字符串类型 转换成 数字类型

        # 3.修改当前用户的金额
        # 3.1.获取当前用户数据
        user, pwd, bal = db_handler.select(login_user)  # [user, pwd, bal]

        # 3.2.先获取用户“修改前”的数据
        old_data = f'{user}:{pwd}:{bal}'

        # 3.3.修改当前用户金额，做加钱操作
        bal = int(bal)
        bal += balance  # bal是取出来的数据，balance是用户输入的要增加的数据

        # 3.4.拼接“修改后”的用户数据
        new_data = f'{user}:{pwd}:{bal}'

        # 3.5.调用修改数据的功能
        db_handler.update(old_data, new_data)
        S_io.write(f'当前用户：[{login_user}]充值金额：[{balance}]元，成功！')

        # ending：做充值日志记录
        now_time = time.strftime('%Y-%m-%d %X')
        log_data = f'时间：{now_time} 用户名：{login_user} 充值金额：{balance}'
        S_io.write(log_data)
        common.append_log(log_data)  # 将日志信息添加进去
        break


# 3 小说阅读功能
@common.login_auth
def reader():
    S_io.write('小说阅读功能执行中...')
    '''
    1.写该功能之前，先将小说数据，存放在story_class.txt文件中
    2.现将story_class.txt文件中的数据读取出来，然后解析成字典类型
    '''
    story_dic = db_handler.get_all_story()

    # 判断story_class.txt文件中是否有小说数据
    if not story_dic:
        S_io.write('没有小说，请联系管理员！')
        return

    while True:
        # 1.打印小说的种类选择信息
        S_io.write('''
        ======= 请选择小说种类 =======
        ''')
        for novel_class in story_dic.keys():
            S_io.write(novel_class.center(30, ' '))
        # 2.让用户输入小说类型编号
        choice1 = S_io.read('请输入小说类型：(输入q退出)').strip()
        if choice1 == 'q': break

        # 3.判断当前用户选择的编号是否存在
        # 若不存在，就重新输入
        if choice1 not in story_dic:
            S_io.write('输入有误，请重新输入！')
            continue

        # 4.获取当前小说类型中的所有小说
        fiction_dic = story_dic.get(choice1)

        # 5.打印当前类型的所有小说
        for number, fiction_list in fiction_dic.items():
            name, price = fiction_list
            S_io.write(f'小说编号：[{number}]  小说名字：[{name}]  小说价格：[{price}]')

        # 6.让用户选择需要购买的小说
        while True:
            choice2 = S_io.read('请输入要购买的小说编号：').strip()
            if choice2 not in fiction_dic:
                S_io.write('输入有误，请重新输入！')
                continue

            name, price = fiction_dic.get(choice2)

            # 7.让用户输入y，选择是否要购买商品
            choice3 = S_io.read(f'当前选择的小说名为：[{name}],商品单价为：[{price}],请输入 y 购买').strip()

            # 8.判断用户输入的是否是 y
            if choice3 == 'y':

                # 9.校验当前用户的余额是否大于小说单价
                # 9.1.获取当前用户的金额
                user, pwd, bal = db_handler.select(login_user)

                # 9.2.判断金额
                bal = int(bal)
                price = int(price)

                if bal < price:
                    S_io.write('余额不足')
                    break

                # 10.如果余额充足，就开始扣费
                # 10.1.拼接用户 “修改前” 的数据
                old_data = f'{user}:{pwd}:{bal}'

                # 10.2.开始扣费
                bal -= price  # bal是用户的原来余额，price是要扣去的小说的价格

                # 10.3.拼接用户 “修改后” 的数据
                new_data = f'{user}:{pwd}:{bal}'
                db_handler.update(old_data, new_data)

                S_io.write('当前小说购买成功，自动打开小说进行阅读~')

                # 11.调用获取小说的详情信息
                fiction_data = db_handler.show_fiction_data(os.path.join(choice1, name))
                S_io.write(f'''
                ======= 当前小说数据如下 =======
                {fiction_data}
                ''')

                # 12.记录购买成功的日志
                now_time = time.strftime('%Y-%m-%d %X')
                log_data = f'时间：[{now_time}] 用户名：[{login_user}] 消费金额：[{price}]'
                S_io.write(log_data)
                common.append_log(log_data)
                break


# 函数字典
func_dic = {
    '0': register,
    '1': login,
    '2': recharge,
    '3': reader,  # 这个逗号可有可无，加了也没关系
}


# 启动函数
def run():

    S_io.write('启动ing...')
    while True:
        S_io.write('''
        ======= 小说阅读器欢迎您 =======
                0 账号注册
                1 账号登录
                2 充值功能
                3 阅读小说
        ''')

        choice = S_io.read('请输入功能编号（温馨提示[输入q退出]：').strip()

        if choice == 'q':
            break

        #  判断用户输入的编号是否在函数字典中
        if choice not in func_dic:
            S_io.write('当前编号有误，请重新输入！')
            continue

        func_dic.get(choice)()


# 线程事件处理函数
def message_handle(connect, clientaddress, g_conn_pool: list):
    g_conn_pool.append(connect)
    clientInfo = "%s:%d：" % (clientaddress[0], clientaddress[1])

    global S_io
    S_io = SocketIo(connect)

    run()

    connect.close()  # 关闭客户机socket
    g_conn_pool.remove(connect)
    print("Info:客户端%s下线,目前在线客户端%d个。" % (clientInfo, len(g_conn_pool)))


def main():
    g_conn_pool = [ ]  # 连接池

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务器socket,基于IPV4的TCP协议
    s.bind(("127.0.0.1", 8080))  # 绑定端口

    s.listen(5)  # 等待客户端连接
    while True:
        connect, clientaddress = s.accept()  # 建立客户端连接
        print('连接地址：', clientaddress)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(connect, clientaddress, g_conn_pool))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

    s.close()  # 关闭服务器



main()
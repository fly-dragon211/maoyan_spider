# -*- encoding: utf-8 -*-
import time
import random
import socket
from threading import Thread


def main(S_io):
    # 让用户注册
    name = S_io.read('请填写用户名：')
    # age = S_io.read("{}您好，请输入您的年龄 : ".format(name))
    user_info = {'name': name, 'age': int(15)}  # 用户信息
    user_properties = ['X 1-5']  # 用于存放用户道具 默认道具
    properties = ['X3 (250G)', 'X1-5 (300G)']  # 道具列表 显示用
    
    # 根据用户年龄 给与不同的初始金币
    if 10 < user_info['age'] < 18:
        glod = 1000
    elif 18 <= user_info['age'] <= 30:
        glod = 1500
    else:
        glod = 500
    user_info['glod'] = glod
    
    # 输出相关提示信息
    S_io.write("{}您好，欢迎游玩本游戏，您的初始金币为：{}".format(user_info['name'], user_info['glod']))
    S_io.write("\n")
    time.sleep(1)
    S_io.write('游戏说明'.center(50, '*'))
    S_io.write("\n")
    S_io.write("电脑每次投掷三枚骰子，总点数>=10为大，否则为小".center(50, '*'))

    S_io.write('*' * 54)
    S_io.write("\n")
    
    #             开始游戏
    result = S_io.read('是否开始游戏，猜对获得100金币，猜错失去100金币 yes or no :  ')
    go = True
    if (result.lower() == 'yes'):
        while go:
            dices = []
            # 开始投掷
            for i in range(0, 3):
                dices.append(random.randint(1, 6))
            total = sum(dices)  # 计算总和
            user_input = S_io.read('请输入big OR small : ')  # 等待用户输入
            u_input = user_input.strip().lower()
            time.sleep(1)
            # 判断用户输入
            S_io.write('骰子点数为：{}'.format(dices), end=' ')
            if (total >= 10 and u_input == 'big') or (total < 10 and u_input == 'small'):
                S_io.write('您赢了!!!')
                multi = 1  # 倍数
                if len(user_properties) > 0:  # 如果用户有道具 选择是否使用道具
                    use_pro = S_io.read('是否使用道具： yes or no')
                    if use_pro.lower() == 'yes':
                        use_pro = int(S_io.read('请选择使用第几个道具{} ：'.format(user_properties)))
                        use_pro -= 1
                        # 判断道具类型
                        if user_properties[use_pro] == 'X 3':
                            multi = 3
                            S_io.write('奖金翻3倍')
                        elif user_properties[use_pro] == 'X 1-5':
                            multi = random.randint(1, 5)
                            S_io.write('奖金翻{}倍'.format(multi))
                        user_properties.remove(user_properties[use_pro])  # 删除道具
    
                user_info['glod'] += 100 * multi  # 金额增加
            else:
                S_io.write('您输了!')
                user_info['glod'] -= 100  # 错误 用户金币减 100
    
            # 判断用户金币 是否够下次玩 不够则退出程序
            if (user_info['glod'] <= 0):
                S_io.write('您的金币已经用完，感谢您的游玩')
                break
    
            if user_info['glod'] % 10 == 0:  # 用户金币 是1000的倍数是 可购买道具
                shop = S_io.read('您现在有金币:{}，是否购买道具 yes or no: '.format(user_info['glod']))
                if shop.lower() == 'yes':
                    good_num = int(S_io.read('请选择要购买第几个道具 {}'.format(properties)))
                    if good_num == 1:
                        user_properties.append('X 3')  # 给用户添加道具
                        user_info['glod'] -= 250
                        S_io.write('购买成功！消耗金币250')
                    elif good_num == 2:
                        user_properties.append('X 1-5')  # 给用户添加道具
                        user_info['glod'] -= 300  # 用户金币减 300
                        S_io.write('购买成功！消耗金币300')
                    else:
                        S_io.write('没有该道具，您失去了这次机会')
            #  一直提示 太烦
            conti = S_io.read('您现在有金币:{}，是否继续游玩,yes or no: '.format(user_info['glod']))
            if conti == 'no':
                go = False

    else:
        S_io.write('欢迎下次游玩，再见！')


class SocketIo:
    """
    SocketIo.write: 代替 S_io.write
    SocketIo.read: 代替 S_io.read
    """
    def __init__(self, connect: socket.socket):
        self.connect = connect

    def write(self, message, end='\n'):
        self.connect.send((message+end).encode('utf-8'))

    def read(self, message):
        self.write(message)
        return self.connect.recv(10*1024).decode('utf-8')  # 接收数据缓存大小


# 线程事件处理函数
def message_handle(connect, clientaddress, g_conn_pool: list):
    g_conn_pool.append(connect)
    clientInfo = "%s:%d：" % (clientaddress[0], clientaddress[1])

    S_io = SocketIo(connect)
    main(S_io)

    connect.close()  # 关闭客户机socket
    g_conn_pool.remove(connect)
    print("Info:客户端%s下线,目前在线客户端%d个。" % (clientInfo, len(g_conn_pool)))
    

if __name__ == "__main__":
    g_conn_pool = [ ]  # 连接池

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务器socket,基于IPV4的TCP协议
    s.bind(("127.0.0.1", 8081))  # 绑定端口

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
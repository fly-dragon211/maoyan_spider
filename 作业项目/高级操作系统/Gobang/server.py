import socket
from threading import Thread
import time

g_conn_pool = []  # 连接池
SERVER_HOST = "127.0.0.1"  # IP
SERVER_PORT = 8080  # Port
# 公共房间列表
public_room_list = []


def play_game(coon, clientInfo, room_no, color_count):
    if color_count == 0:
        # 获取先手操作
        updated_action = coon.recv(10 * 1024).decode("gbk")
        print("Received from client " + clientInfo, updated_action)
        status, x, y = [int(number) for number in updated_action.split(',')]
        # 更新公共图谱
        public_room_list[room_no]['db'] = "(%d,%d)" % (x, y)
        public_room_list[room_no]['updated_client'] = clientInfo
    while (True):
        # 检测对方是否下棋
        if public_room_list[room_no]['updated_client'] != clientInfo:
            print("%s 开始下棋" % (clientInfo))
            # 获取对方下棋操作
            public_dp = public_room_list[room_no]['db']
            coon.send(public_dp.encode())
            # 接收自己操作的图谱
            updated_action = coon.recv(10 * 1024).decode("gbk")
            print("Received from client " + clientInfo, updated_action)
            status, x, y = [int(number) for number in updated_action.split(',')]
            # 如果对方获胜
            if status == 3:
                # 游戏结束,房间解散
                del public_room_list[room_no]
                return
            # 自己获胜
            elif status == 1:
                public_room_list[room_no]['db'] = "(%d,%d)" % (x, y)
                public_room_list[room_no]['updated_client'] = clientInfo
                return
                # 继续游戏
            else:
                # 若游戏仍然继续，则更新自己操作棋谱
                public_room_list[room_no]['db'] = "(%d,%d)" % (x, y)
                public_room_list[room_no]['updated_client'] = clientInfo

        time.sleep(0.5)


# python client.py

# 线程事件处理函数
def message_handle(coon, clientaddress):
    clientInfo = "%s:%d：" % (clientaddress[0], clientaddress[1])
    # 设置循环，监听用户执行命令
    while True:
        # 接受用户登录信息
        action = int(coon.recv(10 * 1024).decode("gbk"))
        print("Received from client " + clientInfo, action)
        # 查找房间
        if action == 1:
            room_list_msg = "序号\t房间\t\t\t人数\n"
            for index, room in enumerate(public_room_list):
                if (len(room['member']) == 1):
                    room_list_msg += "%d\t%s\t%d\n" % (index, room['member'][0], 1)
            coon.send(room_list_msg.encode())
            room_option = int(coon.recv(10 * 1024).decode("gbk"))
            if (room_option == -1):
                break
            else:
                ok_client_msg = "%s;%d" % (public_room_list[room_option]['member'][0], 1)
                public_room_list[room_option]['member'].append(clientInfo)
                public_room_list[room_option]['updated_client'] = clientInfo
                coon.send(ok_client_msg.encode())
                # 开始对局
                while (True):
                    flag_start = int(coon.recv(10 * 1024).decode("gbk"))
                    print("Received from client " + clientInfo, flag_start)
                    if flag_start == 1:
                        play_game(coon, clientInfo, room_option, 1)
                    else:
                        break

        # 创建房间
        elif action == 2:
            # 开始创建房间
            room = {
                'member': [clientInfo],
                'db': '',
                'updated_client': ''
            }
            public_room_list.append(room)
            room_no = len(public_room_list) - 1
            # 创建房间成功
            coon.send("1".encode())
            # 每0.5s循环一次，等待其他玩家加入
            while (True):
                if (len(public_room_list[room_no]['member']) == 2):
                    ok_client_msg = "%s;%d" % (public_room_list[room_no]['member'][1], 0)
                    public_room_list[room_no]['updated_client'] = public_room_list[room_no]['member'][1]
                    coon.send(ok_client_msg.encode())
                    break
                time.sleep(0.5)
            # 开始对局
            while (True):
                flag_start = int(coon.recv(10 * 1024).decode("gbk"))
                print("Received from client " + clientInfo, flag_start)
                if flag_start == 1:
                    play_game(coon, clientInfo, room_no, 0)
                else:
                    break

        # 退出
        elif action == 3:
            break  # 结束该用户执行操作监听
    coon.close()  # 关闭客户机socket
    g_conn_pool.remove(coon)
    print("Info:客户端%s下线,目前在线客户端%d个。" % (clientInfo, len(g_conn_pool)))


# 开启服务器
def run():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务器socket,基于IPV4的TCP协议
    serversocket.bind(("127.0.0.1", 8080))  # 绑定到IP地址和端口号
    serversocket.listen(1)  # 开始侦听，队列长度为1
    print("服务器启动，等待客户端连接。")
    while True:
        coon, clientaddress = serversocket.accept()  # 使用阻塞方法accept以等待客户机连接请求
        print("Connection from client ", clientaddress)  # 打印输入客户机的信息
        g_conn_pool.append(coon)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(coon, clientaddress))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
    serversocket.close()  # 关闭服务器


if __name__ == "__main__":
    run()

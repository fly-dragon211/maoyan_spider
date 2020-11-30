'''
@Auther : gaoxin
@Date : 2019.01.01
@Version : 1.0

'''
from tkinter import *
import math
import socket
from threading import Thread

# 连接服务器
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建客户机socket

clientsocket.connect((SERVER_HOST, SERVER_PORT))  # 连接到服务器


# clientsocket.setblocking(0)

def async2(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


# 打印机器
def printMachine(output):
    ss = output.split('\n')
    str_len = len(ss[0])
    print('——' * str_len)
    print(output)
    print('——' * str_len)


# 定义棋盘类
class chessBoard():
    def __init__(self, color):
        self.window = Tk()
        self.window.title("五子棋游戏  %s方" % (color))
        self.window.geometry("660x470")
        self.window.resizable(0, 0)
        self.canvas = Canvas(self.window, bg="#EEE8AC", width=470, height=470)
        self.paint_board()
        self.canvas.grid(row=0, column=0)

    def paint_board(self):
        for row in range(0, 15):
            if row == 0 or row == 14:
                self.canvas.create_line(25, 25 + row * 30, 25 + 14 * 30, 25 + row * 30, width=2)
            else:
                self.canvas.create_line(25, 25 + row * 30, 25 + 14 * 30, 25 + row * 30, width=1)
        for column in range(0, 15):
            if column == 0 or column == 14:
                self.canvas.create_line(25 + column * 30, 25, 25 + column * 30, 25 + 14 * 30, width=2)
            else:
                self.canvas.create_line(25 + column * 30, 25, 25 + column * 30, 25 + 14 * 30, width=1)

        self.canvas.create_oval(112, 112, 118, 118, fill="black")
        self.canvas.create_oval(352, 112, 358, 118, fill="black")
        self.canvas.create_oval(112, 352, 118, 358, fill="black")
        self.canvas.create_oval(232, 232, 238, 238, fill="black")
        self.canvas.create_oval(352, 352, 358, 358, fill="black")


# 定义五子棋游戏类
# 0为黑子 ， 1为白子 ， 2为空位
class Gobang():
    # 初始化
    def __init__(self, opponent_name, color_count):

        # 16*16的二维列表，保证不会out of index
        self.db = [([2] * 16) for i in range(16)]
        # 悔棋用的顺序列表
        self.order = []
        # 棋子颜色
        self.color_list = ['black', 'white']
        self.color_count = color_count
        self.color = self.color_list[self.color_count]
        # 清空与赢的初始化，已赢为1，已清空为1
        self.flag_win = 1
        self.flag_empty = 1
        self.flag_aciton = (1 if color_count == 0 else 0)
        self.opponent_name = opponent_name
        self.board = chessBoard(self.color)
        self.game_print = StringVar()
        self.game_print.set("")
        self.options()

    # 黑白互换
    #  def change_color(self) :
    #   self.color_count = (self.color_count + 1 ) % 2
    #   if self.color_count == 0 :
    #     self.
    #     self.color = "black"
    #   elif self.color_count ==1 :
    #     self.color = "white"
    @async2
    def receiveMsg(self):

        # 等待对手下棋
        self.step = eval(clientsocket.recv(10 * 1024).decode())
        x = self.step[0]
        y = self.step[1]
        opponent_color_count = (self.color_count + 1) % 2
        self.db[y][x] = opponent_color_count
        self.board.canvas.create_oval(25 + 30 * x - 12, 25 + 30 * y - 12, 25 + 30 * x + 12, 25 + 30 * y + 12,
                                      fill=self.color_list[opponent_color_count], tags="chessman")
        if self.game_win(y, x, (self.color_count + 1) % 2):
            print(self.color_list[(self.color_count + 1) % 2], "获胜")
            self.game_print.set(self.color_list[(self.color_count + 1) % 2] + "获胜")
            clientsocket.send(("%d,%d,%d" % (3, 0, 0)).encode())
            return
        self.game_print.set("请" + self.color_list[self.color_count] + "落子")
        self.flag_aciton = 1  # 当前可对棋盘进行操作

    # 落子
    def chess_moving(self, event):
        # 不点击“开始”与“清空”无法再次开始落子，在对手下棋时间内，己方不可下棋
        if self.flag_win == 1 or self.flag_empty == 0 or self.flag_aciton == 0:
            return
        # 等待对手下棋
        if self.flag_aciton == 1:
            # 自己执行下棋
            # 坐标转化为下标
            x, y = event.x - 25, event.y - 25
            x = round(x / 30)
            y = round(y / 30)
            print("(%d,%d)" % (x, y))
            # 点击位置没用落子，且没有在棋盘线外，可以落子
            while self.db[y][x] == 2 and self.limit_boarder(y, x):
                self.db[y][x] = self.color_count
                self.order.append(x + 15 * y)
                self.board.canvas.create_oval(25 + 30 * x - 12, 25 + 30 * y - 12, 25 + 30 * x + 12, 25 + 30 * y + 12,
                                              fill=self.color, tags="chessman")
                if self.game_win(y, x, self.color_count):
                    print(self.color, "获胜")
                    self.game_print.set(self.color + "获胜")
                    clientsocket.send(("%d,%d,%d" % (1, x, y)).encode())
                    return
                    # 发送
                else:
                    #  发送自己的棋步
                    clientsocket.send(("%d,%d,%d" % (0, x, y)).encode())
                    self.flag_aciton = 0  # 在接收到对方操作之前，不可对棋盘进行操作
                    self.game_print.set("请" + self.color_list[(self.color_count + 1) % 2] + "落子")
                    # self.change_color()
                    self.receiveMsg()

    # 保证棋子落在棋盘上
    def limit_boarder(self, y, x):
        if x < 0 or x > 14 or y < 0 or y > 14:
            return False
        else:
            return True

    # 计算连子的数目,并返回最大连子数目
    def chessman_count(self, y, x, color_count):
        count1, count2, count3, count4 = 1, 1, 1, 1
        # 横计算
        for i in range(-1, -5, -1):
            if self.db[y][x + i] == color_count:
                count1 += 1
            else:
                break
        for i in range(1, 5, 1):
            if self.db[y][x + i] == color_count:
                count1 += 1
            else:
                break
                # 竖计算
        for i in range(-1, -5, -1):
            if self.db[y + i][x] == color_count:
                count2 += 1
            else:
                break
        for i in range(1, 5, 1):
            if self.db[y + i][x] == color_count:
                count2 += 1
            else:
                break
                # /计算
        for i in range(-1, -5, -1):
            if self.db[y + i][x + i] == color_count:
                count3 += 1
            else:
                break
        for i in range(1, 5, 1):
            if self.db[y + i][x + i] == color_count:
                count3 += 1
            else:
                break
                # \计算
        for i in range(-1, -5, -1):
            if self.db[y + i][x - i] == color_count:
                count4 += 1
            else:
                break
        for i in range(1, 5, 1):
            if self.db[y + i][x - i] == color_count:
                count4 += 1
            else:
                break

        return max(count1, count2, count3, count4)

    # 判断输赢
    def game_win(self, y, x, color_count):
        if self.chessman_count(y, x, color_count) >= 5:
            self.flag_win = 1
            self.flag_empty = 0
            return True
        else:
            return False

    # 悔棋,清空棋盘，再画剩下的n-1个棋子
    #  def withdraw(self ) :
    #   if len(self.order)==0 or self.flag_win == 1:
    #    return
    #   self.board.canvas.delete("chessman")
    #   z = self.order.pop()
    #   x = z%15
    #   y = z//15
    #   self.db[y][x] = 2
    #   self.color_count = 1
    #   for i in self.order :
    #    ix = i%15
    #    iy = i//15
    #    self.change_color()
    #    self.board.canvas.create_oval(25+30*ix-12 , 25+30*iy-12 , 25+30*ix+12 , 25+30*iy+12 , fill = self.color,tags = "chessman")
    #   self.change_color()
    #   self.game_print.set("请"+self.color+"落子")

    # 清空
    def empty_all(self):
        self.board.canvas.delete("chessman")
        # 还原初始化
        self.db = [([2] * 16) for i in range(16)]
        self.order = []
        self.color_count = 0
        self.color = 'black'
        self.flag_win = 1
        self.flag_empty = 1
        self.game_print.set("")

    # 将self.flag_win置0才能在棋盘上落子
    def game_start(self):
        clientsocket.send("1".encode())
        # 没有清空棋子不能置0开始
        if self.flag_empty == 0:
            return
        self.flag_win = 0
        # # 后手需要更新棋盘
        # if(self.color_count==1):
        #   self.step=eval(clientsocket.recv(10*1024).decode())
        #   x=self.step[0]
        #   y=self.step[1]
        #   self.db[y][x] = (self.color_count+1)%2
        #   self.board.canvas.create_oval(25+30*x-12 , 25+30*y-12 , 25+30*x+12 , 25+30*y+12 , fill = self.color,tags = "chessman")
        self.game_print.set("请" + self.color_list[0] + "落子")
        if self.flag_aciton == 0:
            # 等待对手下棋
            # self.step=eval(clientsocket.recv(10*1024).decode())
            # x=self.step[0]
            # y=self.step[1]
            # opponent_color_count= (self.color_count+1)%2
            # self.db[y][x] =opponent_color_count
            # self.board.canvas.create_oval(25+30*x-12 , 25+30*y-12 , 25+30*x+12 , 25+30*y+12 , fill = self.color_list[opponent_color_count],tags = "chessman")
            self.receiveMsg()

    def game_end(self):
        clientsocket.send("-1".encode())
        self.board.window.destroy()

    def options(self):
        self.board.canvas.bind("<Button-1>", self.chess_moving)
        Label(self.board.window, textvariable=self.game_print, font=("Arial", 20)).place(relx=0, rely=0, x=495, y=200)
        Button(self.board.window, text="开始游戏", command=self.game_start, width=13, font=("Verdana", 12)).place(relx=0,
                                                                                                              rely=0,
                                                                                                              x=495,
                                                                                                              y=15)
        # Button(self.board.window , text= "我要悔棋" ,command = self.withdraw,width = 13, font = ("Verdana", 12)).place(relx=0, rely=0, x=495, y=60)
        Button(self.board.window, text="清空棋局", command=self.empty_all, width=13, font=("Verdana", 12)).place(relx=0,
                                                                                                             rely=0,
                                                                                                             x=495,
                                                                                                             y=105)
        Button(self.board.window, text="结束游戏", command=self.game_end, width=13, font=("Verdana", 12)).place(relx=0,
                                                                                                            rely=0,
                                                                                                            x=495,
                                                                                                            y=420)
        self.board.window.mainloop()


def start():
    # 客户端系统提示菜单栏
    menu_bar = "1.查找房间\n2.创建房间\n3.exit"
    action = 0  # 用户操作码
    while (True):
        printMachine(menu_bar)
        print("请输入下一步的操作：")
        action = input('>')
        clientsocket.send(action.encode())
        action = int(action)
        # 查找房间
        if action == 1:
            # 接受服务器在线房间消息
            room_list_msg = clientsocket.recv(1024).decode()
            printMachine(room_list_msg)
            print("请输入你要加入的房间：（-1表示退出）")
            room_option = input('>')
            clientsocket.send(room_option.encode())
            if (int(room_option) == -1):
                break
            ok_client_msg = clientsocket.recv(1024).decode()
            client_name, color_count = ok_client_msg.split(";")
            if (ok_client_msg != "False"):
                print("与用户%s对局开始....." % (client_name))
                Gobang(client_name, int(color_count))
            else:
                print("异常错误，房间已关闭")
        # 创建房间
        elif action == 2:
            create_msg = int(clientsocket.recv(10 * 1024).decode())
            if create_msg == 1:
                print("创建成功，等待其他玩家加入：")
                ok_client_msg = clientsocket.recv(10 * 1024).decode()
                client_name, color_count = ok_client_msg.split(";")
                # while(True):
                if ok_client_msg != "False":
                    print("与用户%s对局开始....." % (client_name))
                    Gobang(client_name, int(color_count))
                else:
                    print("异常错误，房间已关闭")
            else:
                print("服务器发生异常错误")
        # 退出 
        elif action == 3:
            break
        else:
            print("输入命令有误，请重新输入。")

    clientsocket.close()  # 用户使用完毕，关闭客户机socket


if __name__ == "__main__":
    start()

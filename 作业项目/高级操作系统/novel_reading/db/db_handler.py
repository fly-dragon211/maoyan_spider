# -*- encoding: utf-8 -*-
# 用于存放数据操作代码

from conf import settings
import os


# 查看数据
def select(username):
    # 接受用户名，若存在，就返回当前用户的所有数据；若不存在，就返回None
    with open(settings.DB_TXT_PATH, mode='rt', encoding='UTF-8') as f:
        # 获取db.txt文件中的每一行数据
        for line in f:
            # 在每一行中，判断接收过来的用户名是否存在于db.txt文件中
            if username in line:
                # 若用户存在，则在当前行中，提取该用户的所有数据
                user_data = line.strip().split(':')  # 用split将:切分
                # 将当前数据，返回给调用者
                return user_data


# 保存数据
def save(username, password, balance=0):
    '''
    :param username: 注册的用户名
    :param password: 注册的密码
    :param balance: 注册时，默认余额为0
    :return:
    '''
    with open(settings.DB_TXT_PATH, mode='at', encoding='UTF-8') as f:
        # 将注册的信息添加到db.txt中
        f.write(f'{username}:{password}:{balance}\n')


# 更新数据
def update(old_data, new_data):
    '''
    :param old_data: 用户原来的数据
    :param new_data: 用户的新数据
    :return:
    '''
    # 1.拼接新的文件路径
    new_path = os.path.join(
        settings.DB_PATH, 'new.txt'
    )
    # 2.读取db.txt文件中的数据 进行修改，写入到新文件new.txt中，再更换为db.txt文件名
    with open(settings.DB_TXT_PATH, mode='rt', encoding='UTF-8') as r_f, \
            open(new_path, mode='wt', encoding='UTF-8') as w_f:
        # 2.1.新旧数据替换    尽量让代码更加简洁
        all_user_data = r_f.read()
        all_user_data = all_user_data.replace(old_data, new_data)

        # 2.2.将新的数据写入到新文件new.txt中
        w_f.write(all_user_data)

    # 3.文件名的修改  os.remove()可以不写，因为原来的db.txt会被覆盖掉
    os.replace(new_path, settings.DB_TXT_PATH)


# 获取小说字典数据
def get_all_story():
    with open(settings.STORY_PATH, mode='rt', encoding='UTF-8') as f:
        story_dic = eval(f.read())
        return story_dic


# 查看单本小说
def show_fiction_data(fiction_name):
    # 获取小说的路径
    fiction_path = os.path.join(
        settings.FICTION_DIR, fiction_name
    )

    # 打开文件，获取文件数据，并返回给用户
    with open(fiction_path, mode='rt', encoding='UTF-8') as f:
        fiction_data = f.read()

        return fiction_data

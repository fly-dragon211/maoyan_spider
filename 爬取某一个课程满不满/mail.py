# -*- encoding: utf-8 -*-
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail():
    # 第三方 SMTP 服务
    mail_host="mail.buct.edu.cn"  #设置服务器
    mail_user="2016016164"    #用户名
    mail_pass="19990225"   #口令

    sender = 'hufan@mail.buct.edu.cn'
    receivers = ['hufan_hf@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("server", 'utf-8')
    message['To'] =  Header("me", 'utf-8')

    subject = '可以选课了'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("无法发送邮件")
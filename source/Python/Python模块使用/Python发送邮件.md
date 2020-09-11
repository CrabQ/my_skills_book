# Python发送邮件

使用yagmail,无法发送附件,奇怪

```python

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import yagmail

# 使用yamail,简单
def send_mail_1():
    smtp = yagmail.SMTP(user='', password='', host='smtp.qq.com', port=465, encoding='GBK')
    subject = 'test'
    attr_2 = '1.xlsx'

    content = """你好:
        谢谢!
    """
    smtp.send('', subject=subject, contents=[ccontent, attr_2])

def send_mail_2():
    # 发送邮箱服务器
    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    # 发送邮箱用户名密码
    user = ''
    password = ''
    # 登录
    smtp.login(user, password)
    sender = user
    receives = ['']

    # 发送邮件主题和内容
    subject = 'test'
    content = """你好:
        谢谢!
    """
    # 构建发送信息
    msg = MIMEMultipart()
    # 构造对象
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    msg['subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(receives)

    # 构造附件内容：定义附件，构造附件内容
    send_file = open(r"1.xlsx", 'rb').read()
    # 调用传送附件模块，传送附件
    att = MIMEText(send_file, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    # 防止中文乱码
    att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', "新建表.xlsx"))
    msg.attach(att)

    smtp.sendmail(sender, receives, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    send_mail_2()
```

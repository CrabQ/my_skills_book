# -*- coding:utf-8 -*-
import requests
from lxml import etree

class Login():
    def __init__(self):
        super(Login, self).__init__()
        # 先访问这个url，获取会话
        self.login_url = 'https://github.com/login'
        # 使用session维持会话，并保存cookies
        self.session = requests.Session()
        # 提交用户名密码的链接
        self.session_url = 'https://github.com/session'
        # 初始化headers
        self.headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Host':'github.com',
           'Connection':'keep-alive'
        }

    def token(self):
        """
        访问登陆页面
        ：return: token
        """
        # 访问登陆页面
        login_response = self.session.get(self.login_url, headers = self.headers)
        login_html = etree.HTML(login_response.text)
        # 获取token
        token = login_html.xpath('//input[@name = "authenticity_token"]/@value')[0]
        return token

    def login(self, email, password):
        data = {
        'commit':'Sign in',
        'utf8':'✓',
        'authenticity_token': self.token(),
        'login': email,
        'password':password
        }
        self.headers['referer'] = 'https://github.com/login'
        # print(self.headers)
        # print(data)
        resp = self.session.post(self.session_url, data=data, headers=self.headers)
        print(resp)


if __name__ == '__main__':
    mylogin = Login()
    mylogin.login('18819425701@163.com', '08015417Qiu')
    print(mylogin.headers)
        
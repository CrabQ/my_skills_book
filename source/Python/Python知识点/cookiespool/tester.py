# -*- coding:utf-8 -*-

import json
import requests
from requests.exceptions import ConnectionError
from db import RedisClient
from setting import TEST_URL_MAP

class ValidTester(object):
    def __init__(self, website='default'):
        """
        父类，初始化一些对象
        :param website: 名称
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def test(self, username, cookies):
        """
        测试Cookies是否有效,子类需要重写
        :param username: 用户名
        :param cookies: cookies
        """
        raise NotImplementedError
    
    def run(self):
        """
        运行，测试所有cookies是否有效
        """
        cookies_groups = self.cookies_db.all()
        # print(cookies_groups)
        for username, cookies in cookies_groups.items():
            # print(username, cookies)
            self.test(username, cookies)

class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        """
        初始化操作
        :param website: 站点名称
        """
        super(WeiboValidTester, self).__init__(website)

    def test(self, username, cookies):
        """
        测试Cookies是否有效
        :param username: 用户名
        :param cookies: cookies
        """
        print('正在测试Cookies 用户名', username)
        try:
            cookies = json.loads(cookies)
            print(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return

        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                # print(response.url)
                print('Cookies有效', username)
                # print(response.status_code, response.headers,)
            else:
                print(response.status_code, response.headers,)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('测试Cookies发生异常', e.args)

if __name__ == '__main__':
    mytester = WeiboValidTester()
    mytester.run()
# -*- coding:utf-8 -*-

from db import RedisClient
import re

class Importer():
    def __init__(self, type, website):
        self.db = RedisClient(type, website)

    def scan(self):
        choice = input('请选择录入方式：\n输入1手动录入\t输入2以文件形式批量导入\n')
        if choice == '1':
            print('请输入账号密码组(用户名与密码中间以-分隔开)，输入quit退出：')
            while True:
                accout = input()
                if accout == 'quit':
                    break
                try:
                    username, password = accout.split('-')
                    print('用户名', username,'密码', password)
                    self.set(username, password)
                    print('请输入另一组账号密码组(用户名与密码中间以-分隔开)，输入quit退出：')
                except:
                    print('格式错误,请重新输入，输入quit退出：')

        if choice == '2':
            print('请输入文件绝对路径(用户名与密码中间以-分隔开)，输入quit退出：')
            while True:
                dir = input()
                if dir == 'quit':
                    break
                try:
                    with open(dir, 'r', encoding = 'utf-8') as f:
                        accounts = f.readlines()
                    for account in accounts:
                        try:
                            username = re.search('(.*?)-.*', account).group(1)
                            password = re.search('.*?-(.*)', account).group(1)
                            self.set(username, password)
                            
                        except:
                            print(accounts, '格式错误')
                    print('请输入另一个文件绝对路径，输入quit退出：')
                except:
                    print('文件不存在！请重新输入，输入quit退出!')

    def set(self, username, password):
        """
        设置键值对
        :param username: 用户名
        :param password: 密码
        :return:
        """
        result = self.db.set(username, password)
        print(username, '导入成功' if result else '导入失败')


if __name__ == '__main__':
    myimporter = Importer('accounts','weibo')
    myimporter.scan()
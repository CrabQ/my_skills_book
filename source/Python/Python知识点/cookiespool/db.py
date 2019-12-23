# -*- coding:utf-8 -*-

from setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
import redis
from random import choice

class RedisClient(object):
    def __init__(self, type, website):
        """
        初始化Redis连接
        :param type: 类型
        :param website: 网站
        """
        self.type = type
        self.website = website
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    def name(self):
        """
        获取redis hash名称
        : return: hash名称
        """
        return '{type}:{website}'.format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        增加一对映射关系
        :params username: 用户名
        :params value: 密码或者cookies
        : return: 添加结果
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        根据键名获取value
        :params username: 用户名
        : return: value
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        删除一对映射关系
        :params username: 用户名
        : return: 删除结果
        """
        return self.db.hdel(self.name(), username)
    
    def count(self):
        """
        获取当前hash名称的键值对总数
        : return: 返回当前hash名称的键值对总数
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机获取value，用于获取cookies
        : return: 返回当前hash名称的一个随机value
        """
        return choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取当前hash名称的所有账户信息
        : return: 返回当前hash名称的所有账户信息
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有的键值对
        : return: 返回当前hash名称的所有映射表
        """
        return self.db.hgetall(self.name())

if __name__ == '__main__':
    mydb = RedisClient('accounts', 'weibo')
    # print(mydb.set('1', '111'))
    print(mydb.usernames())
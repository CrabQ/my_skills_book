# -*- coding:utf-8 -*-
from flask import g,Flask
import json
from db import RedisClient
from setting import *

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    """
    链接redis数据库，返回链接对象
    """
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient("accounts", "' + website + '")'))
    return g
    
@app.route('/')
def index():
    """
    主页
    """
    a = get_conn()
    print(a)
    return '<h2>Welcome to Cookie Pool System</h2>'

@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookies, 访问地址如 /weibo/random
    return: 随机Cookies
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies

@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户， 访问地址如 /weibo/add/user/password
    :param website: 站点名称
    :param username: 用户名
    :param password: 密码
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})

@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
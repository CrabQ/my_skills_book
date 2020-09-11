# -*- coding:utf-8 -*-

from flask import Flask,g
from db import RedisClient

app = Flask(__name__)

def get_conn():
    """
    链接redis数据库，返回链接对象
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def route():
    """
    主页
    """
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    """
    获取代理页面
    :return : 返回一个代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    查询当前代理池代理总数页面
    :return : 返回当前代理池代理总数
    """
    conn = get_conn()
    return str(conn.count())

def main():
    app.run(
        port=5555
    )

if __name__ == '__main__':
    main()
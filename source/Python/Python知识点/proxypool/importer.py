# -*- coding:utf-8 -*-
from db import RedisClient
import re

def set(proxy):
    """
    添加代理
    :params proxy: 代理
    """    
    try:
        # 连接redis
        db = RedisClient()
        # 添加代理
        result = db.add(proxy)
        print(proxy,'导入成功!' if result else proxy,'导入失败!')
    except:
        pass

def scan():
    """
    扫面代理
    """
    proxies_dir = input('请输入要导入的代理的绝对地址: ')

    # 获取要导入的代理
    try:
        with open(proxies_dir, 'r', encoding = 'utf-8') as f:
            proxies_list = f.readlines()
    except:
        print('文件不存在！')

    # 导入代理
    try:
        print('开始导入代理！')
        for proxy in proxies_list:
            set(proxy.strip())
    except:
        print('导入错误！')


def main():
    scan()

if __name__ == '__main__':
    main()
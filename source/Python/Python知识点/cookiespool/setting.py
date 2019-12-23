# -*- coding:utf-8 -*-

# redis地址
REDIS_HOST = '127.0.0.1'
# redis端口
REDIS_PORT = '6379'
# redis密码
REDIS_PASSWORD = ''


# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，在此配置
GENERATOR_MAP = {
    'weibo': 'WeiboCookiesGenerator'
}


# 测试类，如扩展其他站点，在此配置
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}

TEST_URL_MAP = {
    'weibo': 'https://m.weibo.cn/home/setting'
}

# 产生器和验证器循环周期
CYCLE = 3600

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 6666

# 产生器开关
GENERATOR_ENABLE = True
# 测试器开关
VALID_ENABLE = True
# API开关
API_ENABLE = True
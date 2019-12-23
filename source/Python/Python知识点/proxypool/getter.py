# -*- coding:utf-8 -*-

from db import RedisClient
from crawler import Crawler
from setting import PROXIES_THRESHOLD
import sys

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到代理池数量限制
        :return : 返回判断结果
        """
        if self.redis.count() >= PROXIES_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        """
        从各大网站中获取代理
        """        
        # print('获取器开始执行!')
        for callback_label in range(self.crawler.__CrawlFuncCount__):
            # 获取Crawler里面的以 crawl 开头的函数
            callback = self.crawler.__CrawlFunc__[callback_label]
            # 判断是否达到代理池数量限制
            if not self.is_over_threshold():
                # 运行函数获取代理
                proxies_list = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                # 添加代理到数据库
                for proxy in proxies_list:
                    self.redis.add(proxy)
            else:
                print(callback, '代理池代理数量已满，不再爬取代理！')

        print('代理爬取完毕，当前代理池代理总数：', self.redis.count())

def main():
    a = Getter()
    a.run()

if __name__ == '__main__':
    main()
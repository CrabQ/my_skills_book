# -*- coding:utf8 -*-

import re
from lxml import etree
import time
import sys
import random
import json
import requests

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        # 存储以 crawl 开头的函数
        attrs['__CrawlFunc__'] = []

        for k, v in attrs.items():
            if 'crawl_' in k:
                # 如果函数以 crawl 开头，则加入列表
                attrs['__CrawlFunc__'].append(k)
                count +=1
        # 存储以 crawl 开头的函数的个数
        attrs['__CrawlFuncCount__'] = count

        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass = ProxyMetaclass):
    def get_proxies(self, callback):
        """
        :params callback: callback
        :return proxies_list: 返回爬取到的代理，列表形式
        """
        proxies_list = []
        for proxy in eval('self.{}()'.format(callback)):
            proxies_list.append(proxy)
        return proxies_list

    def crawl_xicidaili(self):
        """
        爬取代理：https://www.xicidaili.com/wt/
        :yield: 返回爬取到的代理
        """
        for i in range(1,4):
            url_full = 'https://www.xicidaili.com/wt/' + str(i)
            with open(sys.path[0] + '/user-agents.txt', 'r' , encoding = 'utf-8') as f:
                list_user_agent = f.readlines()
            user_agent = random.choice(list_user_agent).strip()
            headers = {'user-agent':user_agent}
            try:
                response = requests.get(url_full, headers = headers)
                response.encoding = 'utf-8'
                time.sleep(1)
            except:
                response = ''
            if response:
                html_proxy = etree.HTML(response.text)
                source_proxy = html_proxy.xpath('//table[@id="ip_list"]/tr')
                for proxy in source_proxy:
                    list_ip_proxy = proxy.xpath('./td[2]')
                    list_port_proxy = proxy.xpath('./td[3]')
                    judge_proxy = proxy.xpath('./td[5]')
                    if list_ip_proxy and list_ip_proxy and judge_proxy:
                        judge_proxy = judge_proxy[0].text
                        if judge_proxy == '高匿':
                            ip_proxy = list_ip_proxy[0].text
                            port_proxy = list_port_proxy[0].text
                            address_port = ip_proxy.strip()+':'+port_proxy.strip()
                            yield address_port
    
    def crawl_kuaidaili(self):
        """
        爬取代理：https://www.kuaidaili.com/free/inha/
        :yield: 返回爬取到的代理
        """
        for i in range(1, 4):
            url_full = 'https://www.kuaidaili.com/free/inha/' + str(i)
            with open(sys.path[0] + '/user-agents.txt', 'r' , encoding = 'utf-8') as f:
                list_user_agent = f.readlines()
            user_agent = random.choice(list_user_agent).strip()
            headers = {'user-agent':user_agent}
            try:
                response = requests.get(url_full, headers = headers)
                response.encoding = 'utf-8'
                time.sleep(1)
            except:
                response = ''
            if response:
                html_proxy = etree.HTML(response.text)
                source_proxy = html_proxy.xpath('//table[@class="table table-bordered table-striped"]//tr')
                for proxy in source_proxy:
                    list_ip_proxy = proxy.xpath('./td[@data-title="IP"]')
                    list_port_proxy = proxy.xpath('./td[@data-title="PORT"]')
                    if list_ip_proxy and list_ip_proxy :
                        ip_proxy = list_ip_proxy[0].text
                        port_proxy = list_port_proxy[0].text
                        address_port = ip_proxy.strip()+':'+port_proxy.strip()
                        yield address_port

    def crawl_89ip(self):
        """
        爬取代理：http://www.89ip.cn/index_1.html
        :yield: 返回爬取到的代理
        """
        for i in range(1, 4):
            url_full = 'http://www.89ip.cn/index_' + str(i) + '.html'
            with open(sys.path[0] + '/user-agents.txt', 'r' , encoding = 'utf-8') as f:
                list_user_agent = f.readlines()
            user_agent = random.choice(list_user_agent).strip()
            headers = {'user-agent':user_agent}
            try:
                response = requests.get(url_full, headers = headers)
                response.encoding = 'utf-8'
                time.sleep(1)
            except:
                response = ''
            if response:
                html_proxy = etree.HTML(response.text)
                source_proxy = html_proxy.xpath('//table[@class="layui-table"]//tr')
                for proxy in source_proxy:
                    list_ip_proxy = proxy.xpath('./td[1]')
                    list_port_proxy = proxy.xpath('./td[2]')
                    if list_ip_proxy and list_ip_proxy :
                        ip_proxy = list_ip_proxy[0].text
                        port_proxy = list_port_proxy[0].text
                        address_port = ip_proxy.strip()+':'+port_proxy.strip()
                        yield address_port

def main():
    crawler = Crawler()
    a = []
    for i in range(crawler.__CrawlFuncCount__):
        b = crawler.get_proxies(crawler.__CrawlFunc__[i])
        a.append(b)
    print(a)
if __name__ == '__main__':
    main()
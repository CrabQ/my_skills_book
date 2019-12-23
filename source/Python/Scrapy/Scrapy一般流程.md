# Scrapy一般流程

1. 新建项目

   ```python
   scrapy startproject exosomemed_spider
   ```

2. 编辑item(`/Exosomemed_spider/items.py`)

   ```python
   # -*- coding: utf-8 -*-

   import scrapy


   class ExosomemedSpiderItem(scrapy.Item):
       # 文件名字
       file_name = scrapy.Field()
       # 文章爬取结果
       result = scrapy.Field()
   ```

3. 编辑settings(`/Exosomemed_spider/settings.py`)

   ```python
   # Obey robots.txt rules
   ROBOTSTXT_OBEY = False

   DOWNLOAD_DELAY = 3

   # Disable cookies (enabled by default)
   COOKIES_ENABLED = False

   LOG_FILE = "exosomemed.log"
   LOG_LEVEL = "INFO"
   ```

4. 设置User-Agent

    settings(`/Exosomemed_spider/settings.py`)添加User-Agent并开启下载中间件

   ```python
   DOWNLOADER_MIDDLEWARES = {
      'exosomemed_spider.middlewares.RandomUserAgent':1,
   }

   USER_AGENTS = [
   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
   "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
   "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
   "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
   "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
   "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
   "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
   ]
   ```

    编写RandomUserAgent(`/Exosomemed_spider/middlewares.py`)

   ```python
   from scrapy import signals
   import random

   from scrapy.conf import settings

   class RandomUserAgent(object):
      def process_request(self, request, spider):
          user_agent = random.choice(settings['USER_AGENTS'])
          request.headers.setdefault("User-Agent", user_agent)
   ```

5. spider(`/Exosomemed_spider/spiders/exosomemed.py`)

   ```python
   #  -*- coding:utf-8 -*-

   import scrapy
   from scrapy.spiders import CrawlSpider, Rule
   from scrapy.linkextractors import LinkExtractor
   from exosomemed_spider.items import ExosomemedSpiderItem
   import re

   class Exosomemed(CrawlSpider):
       name = 'exosomemed'
       allow_domains = ['www.exosomemed.com']

       # 爬取research和专题下的所有文章
       start_urls = [
           'http://www.exosomemed.com/category/research',
           # 'http://www.exosomemed.com/category/专题',
       ]

       # 获取索引页
       research_links = LinkExtractor(allow=(r'category\/research\/page\/\d+'))
       # special_links = LinkExtractor(allow=(r'category\/%E4%B8%93%E9%A2%98\/page\/\d+'))

       # 获取文章
       article_links = LinkExtractor(allow=(r'com\/\d+.html'))
       rules = [
           Rule(research_links, callback=None, follow=True),
           # Rule(special_links, callback=None, follow=True),
           Rule(article_links, callback='parse_article', follow=False),
       ]

       def parse_article(self, response):
           # 实例化
           item = ExosomemedSpiderItem()
           try:
               # 获取文件保存名
               item['file_name'] = re.search('/(\d+\.html)', response.url).group(1)
               # 获取文章内容
               item['result'] = re.search(r'<div id="content">(.*)<div class="article-pagenavi">', response.text, re.I|re.S).group(1)
               # 判断文件属于research还是专题
               # print(response.)
               yield item
           except:
               print(response.url)
   ```

2. 编辑pipelines(`/Exosomemed_spider/pipelines.py`)

   ```python
   # -*- coding: utf-8 -*-

   import os

   class ExosomemedSpiderPipeline(object):
       def process_item(self, item, spider):
           # file_dir = r'D:/test/exosomemed/special'
           file_dir = r'D:/test/exosomemed/research'
           if not os.path.exists(file_dir):
               os.makedirs(file_dir)
           with open(file_dir +'/'+ item['file_name'], 'w', encoding='utf-8') as f:
               f.write(item['result'])

           return item
   ```

   settings(`/Exosomemed_spider/settings.py`)添加`ExosomemedSpiderPipeline`

   ```python
   ITEM_PIPELINES = {
     'exosomemed_spider.pipelines.ExosomemedSpiderPipeline': 300,
   }
   ```

# Scrapy

## 安装

```shell
pip install scrapy
```

## 流程图

![流程](https://img-blog.csdn.net/20180416224202657?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI4ODE3NzM5/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

## Scrapy一般流程

```shell
# 1. 新建项目
scrapy startproject exosomemed_spider

# 2. 新建爬虫
scrapy genspider exosomemed "exosomemed.com"

# 3. 运行
scrapy crawl exosomemed
```

## Spider

```python
import scrapy

class TestSpider(scrapy.Spider):
    name = "Test"
    allowed_domains = ["Test.com"]
    start_urls = [
        "http://www.Test.com/index.php"
    ]

    def parse(self, response):
        pass
```

### 请求传参

```python
    def parse(self, response):
        yield scrapy.Request(url=item['detail_url'],callback=self.parse_detail,meta={'item':item})

    def parse_detail(self,response):
        #通过response获取item
        item = response.meta['item']
```

### post请求发送

```python
# 对起始的url发起post请求, 重写start_requests
def start_requests(self):
        #请求的url
        post_url = 'http://fanyi.baidu.com/sug'
        # post请求参数
        formdata = {
            'kw': 'wolf',
        }
        # 发送post请求
        yield scrapy.FormRequest(url=post_url, formdata=formdata, callback=self.parse)
```

### CrawlSpider

```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TestSpider(CrawlSpider):
    name = "Test"
    allowed_domains = ["Test.com"]
    start_urls = [
        "http://www.Test.com/index.php"
    ]

    rules = (
        # 不定义callback,默认follow=True, 递归爬取
        Rule(LinkExtractor(allow=('/group?f=index_group', ), deny=('deny\.php', ))),
        # 定义了callback则不递归
        Rule(LinkExtractor(allow=('/article/\d+/\d+\.html', )), callback='parse_item'),
    )
```

## 持久化存储

### 基于终端指令的持久化存储

```shell
scrapy crawl 爬虫名称 -o xxx.json
scrapy crawl 爬虫名称 -o xxx.xml
scrapy crawl 爬虫名称 -o xxx.csv
```

### 基于管道的持久化存储

```shell
items.py       数据结构模板文件, 定义数据属性
pipelines.py   管道文件, 接收数据(items)进行持久化操作
```

流程

```shell
1. 爬虫文件爬取到数据后,需要将数据封装到items对象中
2. 使用yield关键字将items对象提交给pipelines管道进行持久化操作
3. 在管道文件中的process_item方法中接收爬虫文件提交过来的item对象,然后编写持久化存储的代码将item对象中存储的数据进行持久化存储
4. settings.py配置文件中开启管道
```

#### 基于mysql的管道存储

```python
import pymysql

class TestPipelineByMysql(object):

    conn = None
    cursor = None

    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123456',db='test')

    def process_item(self, item, spider):
        sql = 'insert into test values("%s","%s")'%(item['author'],item['content'])
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
```

## 配置

```python
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

ROBOTSTXT_OBEY = False

# 并发线程数
CONCURRENT_REQUESTS = 100

# 日志
LOG_LEVEL = 'ERROR'

LOG_FILE = 'log.txt'
```

## selenium在scrapy中的使用流程

```shell
# 在爬虫类中定义一个bro的属性,即实例化浏览器对象
# 在爬虫类重写父类的closed方法中关闭bro
# 在中间件中进行浏览器自动化操作

class WangyiSpider(RedisSpider):
    name = 'wangyi'
    start_urls = ['https://news.163.com']
    def __init__(self):
        #实例化一个浏览器对象(实例化一次)
        self.bro = webdriver.Chrome(executable_path='chromedriver')

    #必须在整个爬虫结束后,关闭浏览器
    def closed(self,spider):
        print('爬虫结束')
        self.bro.quit()

# 中间件文件
from scrapy.http import HtmlResponse

    def process_response(self, request, response, spider):
        #响应对象中存储页面数据的篡改
        if request.url in['http://news.163.com/domestic/','http://news.163.com/world/','http://news.163.com/air/','http://war.163.com/']:
            spider.bro.get(url=request.url)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            spider.bro.execute_script(js)
            time.sleep(2)  #一定要给与浏览器一定的缓冲加载数据的时间
            #页面数据就是包含了动态加载出来的新闻数据对应的页面数据
            page_text = spider.bro.page_source
            #篡改响应对象
            return HtmlResponse(url=spider.bro.current_url,body=page_text,encoding='utf-8',request=request)
        else:
            return response
```

## Scarpy下载中间件

```shell
# 引擎将请求传递给下载器过程中, 下载中间件可以对请求进行一系列处理比如设置请求的 User-Agent,设置代理等
# 在下载器完成将Response传递给引擎中,下载中间件可以对响应进行一系列处理比如进行gzip解压等

# process_request
# 篡改响应头,代理

# process_response
# 篡改响应对象
```

### 随机User-Agent

settings添加User-Agent并开启下载中间件

```python
DOWNLOADER_MIDDLEWARES = {
    'spider.middlewares.RandomUserAgent':1,
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

编写RandomUserAgent

```python
# middlewares.py
from scrapy import signals
import random

from scrapy.utils.project import get_project_settings

class RandomUserAgent(object):
    def process_request(self, request, spider):
        settings = get_project_settings()
        user_agent = random.choice(settings['USER_AGENTS'])
        request.headers.setdefault("User-Agent", user_agent)
```

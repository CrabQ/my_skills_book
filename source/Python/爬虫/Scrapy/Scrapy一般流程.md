# Scrapy

## Scrapy一般流程

```shell
# 1. 新建项目
scrapy startproject exosomemed_spider

# 2. 新建爬虫
scrapy genspider exosomemed "exosomemed.com"

# 3. 运行
scrapy crawl exosomemed
```

## selenium在scrapy中的使用流程

```shell
在爬虫类中定义一个bro的属性,即实例化浏览器对象
在爬虫类重写父类的closed方法中关闭bro
在中间件中进行浏览器自动化操作
```

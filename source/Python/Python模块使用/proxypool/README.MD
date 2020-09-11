### proxypool 说明文档

#### 目录
1. `db.py` 连接redis数据库，以及与数据库相关的各种方法
2. `importer.py` 读取文件，导入代理
3. `setting.py` 配置文件，存储各种常量参数
4. `error.py` raise各种错误
5. `crawler.py` 爬取各大网站高匿代理的类
6. `getter.py` 获取器,启动爬取代理
7. `tester.py` 测试器,测试代理是否可用
8. `api.py` 接口，通过API接口可获取随机代理
9. `scheduler.py` 调度4个模块工作
8. `run.py` 运行入口

#### 说明
代理池共分为4个模块：存储模块、获取模块、检测模块、接口模块

- 存储模块（db.py、importer.py）  
    负责存储获取模块爬取下来的代理，使用redis的sorted set进行存储。代理不重复，并通过分数标识数据库中的代理状态。通过help(RedisClient)可查看db.py中类RedisClient的各种方法，importer.py可以通过读取文件形式导入大量代理。

- 获取模块（crawler.py、getter.py）  
    负责定时从各大代理网站上爬取高匿代理，代理池设置代理总数为500，超过该数量将不会继续获取代理。新获取的代理分数标识为10。如果需要新增代理网站，只需要在crawler.py的类Crawler中添加以crawl_开头的方法即可。

- 检测模块（tester.py）  
    负责定时检测数据库中的代理，通过分数标识数据库中的代理状态。调用asyncio、aiohttp模块，通过异步携程批量测试。访问[httpbin](http://httpbin.org/get),查看返回的IP是否为该代理。当代理可用时，分数设置为50，当代理不可用时分数减1，如果分数为0，则移除该代理。

- 接口模块（api.py）   
    负责通过Web API提供对外服务的接口，访问 http://127.0.0.1:5555/random 即可随机获得数据库中所有分数为50的代理中的一个。

- 调度模块(scheduler.py、run.py)   
    负责调度其余的模块工作

#### 使用说明

- 启动代理池  
```python
# 切换python运行环境
source /home/bmnars/spider_porject/bmnars_venv/bin/activate
# 启动代理池
nohup python /home/bmnars/spider_porject/proxypool/run_proxypool.py &
```

- 获取代理  
当代理池启动时，  
访问 http://127.0.0.1:5555/random 即可获得一个当前可用的代理。  
访问 http://127.0.0.1:5555/count 可查看当前代理池的代理总数。  

- 示例  
```python
import requests
import redis

def proxy():
    """
    :return: 返回一个随机选择的proxy
    """
    try:
        response = requests.get('http://127.0.0.1:5555/random')
        return response.text
    except:
        db = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        result = db.zrangebyscore('proxies', 50, 50)
        if len(result):
            return random.choice(result)
        else:
            result = db.zrangebyscore('proxies', 0, 50)
            if len(result):
                return random.choice(result)

```
### CookiesPool 说明文档

#### 目录
1. `db.py` 连接redis数据库，以及与数据库相关的各种方法
2. `importer.py` 导入用户名密码
3. `setting.py` 配置文件，存储各种常量参数
4. `tester.py` 测试器,测试Cookies是否有效，无效则删除Cookies
5. `generator.py` 生成器，为所有账户生成Cookies
6. `api.py` 接口，通过API接口可获取随机Cookies,查询Cookies总数，添加用户等
7. `scheduler.py` 调度4个模块工作
8. `run.py` 运行入口

#### 说明
代理池共分为4个模块：存储模块、获取模块、检测模块、接口模块

- 存储模块（db.py、importer.py）  
    负责存储用户名，账号或者cookies，使用redis的hash进行存储。账号与密码、cookies一一对应，通过help(RedisClient)可查看db.py中类RedisClient的各种方法，importer.py可以通过手动输入或者读取文件形式导入账号密码。

- 生成模块（generator.py）  
    负责定时生成Cookies。

- 检测模块（tester.py）  
    负责定时检测数据库中的Cookies是否有效，无效则删除Cookies，生成器检测到账号无Cookies则会生成新的Cookies。

- 接口模块（api.py）   
    负责通过Web API提供对外服务的接口，访问 http://127.0.0.1:6666/website/random 即可随机获得数据库中对应网站的有效Cookies

- 调度模块(scheduler.py、run.py)   
    负责调度其余的模块工作

#### 使用说明

- 使用前请先导入账户密码
```
python3 run.py
```
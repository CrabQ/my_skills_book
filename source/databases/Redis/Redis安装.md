# Redis安装

## win 10安装redis

安装redis
> [redis](https://github.com/MicrosoftArchive/redis/releases)

安装RedisPy

```shell
pip install redis
```

安装RedisDump

1. 安装ruby
    > [ruby](http://www.ruby-lang.org/zh_cn/documentation/installation/)
2. 安装redis-dump

    ```shell
    gem install redis-dump
    ```

## Centos7安装Redis

```shell
# 下载解压
wget http://download.redis.io/releases/redis-5.0.7.tar.gz

# 解压
tar -zxvf redis-5.0.7.tar.gz

# 安装gcc环境
yum install -y gcc

# 进入解压目录
cd redis-5.0.7

# 编译
make

# 安装
make install PREFIX=/usr/local/redis

# 直接启动
cd /usr/local/redis/bin
./redis-server

# 使用配置文件启动(推荐)
# 复制,并修改配置文件
cp /tmp/redis-5.0.7/redis.conf /usr/local/redis/bin/
# 启动
./redis-server redis.conf

# 测试是否成功启动
ps -ef|grep redis
```

配置修改

```shell
# 守护进程方式启动
daemonize yes

# 端口
port 6379

# redis系统日志
logfile "/usr/local/redis/log/redis_log.log"

# redis工作目录
dir /usr/local/redis/rdb
```

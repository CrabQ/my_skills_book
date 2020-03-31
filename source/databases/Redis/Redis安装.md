# Redis安装

## win 10安装redis

```shell
# 安装redis
https://github.com/MicrosoftArchive/redis/releases

# 安装RedisPy
pip install redis

# 安装RedisDump
1. 安装ruby
    http://www.ruby-lang.org/zh_cn/documentation/installation/
2. 安装redis-dump
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
# 复制重命名(端口区分不同redis),并修改配置文件
cp /tmp/redis-5.0.7/redis.conf /usr/local/redis/config/
# 启动
./redis-server /config/redis-6379.conf

# 测试是否成功启动
ps -ef|grep redis
```

## 配置修改

```shell
# 守护进程方式启动
daemonize yes

# 端口
port 6379

# redis系统日志
logfile "6379.log"

# redis工作目录
dir /usr/local/redis/data
```

### RDB设置(可选)

```shell
# 关闭自动生成RDB文件
# save 900 1
# save 300 10
# save 60 10000

# RDB文件名称
dbfilename dump-6379.rdb
```

### AOF设置(可选)

```shell
# redis工作目录
dir /usr/local/redis/data

# 必须开启此项才能开启AOF
appendonly yes

# AOF文件名称
appendfilename "appendonly_6379.aof"

# AOF策略
appendfsync everysec

# 一般yes,开销没那么大
no-appendfsync-on-rewrite yes

# AOF文件重写需要的尺寸
auto-aof-rewirte-min-size 64mb

# AOF文件增长率
auto-aof-rewirte-percentage 100

aof-load-truncated yes
```

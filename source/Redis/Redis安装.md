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

目录规划

```shell
# 安装目录
/app/redis_cluster/redis_{port}/{conf, logs, pid}

# 数据目录
/data/redis_cluster/redis_{port}/redis_{port}.rdb

# 运维脚本
/root/scripts/redis_shell.sh
```

```shell
# 下载解压
wget http://download.redis.io/releases/redis-5.0.7.tar.gz
tar -zxvf redis-5.0.7.tar.gz -C /app/
ln -s /app/redis-5.0.7 /app/redis /app/redis

# 安装gcc环境
yum install -y gcc

# 进入解压目录
cd redis

# 编译安装
make && make install

# 安装
# make install PREFIX=/usr/local/redis

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

# 绑定地址
bind 内网地址

# 端口
port 6379

# pid文件和log文件保存地址
pidfile /app/redis_cluster/redis_6379/pid/redis_6379.pid
logfile /app/redis_cluster/redis_6379/logs/redis_6379.log

# 指定本地持久化文件
dbfilename redis_6379.rdb

# redis工作目录
dir /app/redis_cluster/redis_6379/
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

## 推荐配置

```shell
# 守护进程方式启动
daemonize yes

# 端口
port 6379

# redis系统日志
logfile "6379.log"

# redis工作目录
dir /usr/local/redis/data

# 慢查询
config set slowlog-max-len 1000
config set slowlog-log-slower-than 1000


# 关闭自动生成RDB文件
# save 900 1
# save 300 10
# save 60 10000

# RDB文件名称
dbfilename dump-6379.rdb


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

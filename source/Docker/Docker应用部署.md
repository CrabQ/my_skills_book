# Docker应用部署

## Centos7下MySQL部署

```shell
# 搜索镜像
docker search mysql
# 拉取
docker pull mysql

# 在/root目录下创建MySQL目录用于储存MySQL数据信息
mkdir -p ~/my_docker/mysql/3306/{config,data}
# 添加配置文件
cat > ~/my_docker/mysql/3306/config/my.cnf <<EOF
[mysqld]
datadir=/var/lib/mysql
socket=/var/run/mysqld/mysqld.sock
log_error=/var/lib/mysql/mysql.log
log_bin=/var/lib/mysql/mysql-bin
port=3306
server_id=1
EOF

# 创建容器,设置端口映射,目录映射
# 让容器的时钟与宿主机时钟同步
docker run -id \
--name=mysql_3306 \
-p 3306:3306 \
-v ~/my_docker/mysql/3306/config:/etc/mysql/conf.d \
-v ~/my_docker/mysql/3306/data:/var/lib/mysql \
-v /etc/localtime:/etc/localtime:ro \
-e MYSQL_ROOT_PASSWORD=root \
mysql:latest

# 测试是否成功
docker exec -it mysql_3306 mysql -uroot -p
```

## windows 10下MySQL部署

```shell
docker pull mysql

# 创建MySQL目录用于储存MySQL数据信息
D:\program\docker_data\mysql\3306\config
D:\program\docker_data\mysql\3306\data
# 添加配置文件
# D:\program\docker_data\mysql\3306\config\my.cnf
[mysqld]
datadir=/var/lib/mysql
socket=/var/run/mysqld/mysqld.sock
log_error=/var/lib/mysql/mysql.log
log_bin=/var/lib/mysql/mysql-bin
port=3306
server_id=1

# 创建容器,设置端口映射,目录映射
docker run -id --name=mysql_3306 -p 3306:3306 -v D:/program/docker_data/mysql/3306/config:/etc/mysql/conf.d -v D:/program/docker_data/mysql/3306/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root mysql:latest

# 测试是否成功
docker exec -it mysql_3306 mysql -uroot -p
```

## Centos8下MySQL主从复制部署

```shell
# 创建两个数据库相关目录
mkdir -p /data/docker/mysql_330{6,7}/{config,data}

# 添加配置文件
cat > /data/docker/mysql_3306/config/my.cnf <<EOF
[mysqld]
datadir=/var/lib/mysql
socket=/var/run/mysqld/mysqld.sock
log_error=/var/lib/mysql/mysql.log
log_bin=/var/lib/mysql/mysql-bin
port=3306
server_id=100
EOF

# 3307配置文件
sed 's/3306/3307/g' /data/docker/mysql_3306/config/my.cnf>/data/docker/mysql_3307/config/my.cnf
sed 's/server_id=100/server_id=101/g' -i /data/docker/mysql_3307/config/my.cnf

# 启动3306
docker run -id \
--name=mysql_3306 \
--net=host \
-v  /data/docker/mysql_3306/config:/etc/mysql/conf.d \
-v  /data/docker/mysql_3306/data:/var/lib/mysql \
-v /etc/localtime:/etc/localtime:ro \
-e MYSQL_ROOT_PASSWORD=root \
mysql:latest

# 测试
docker exec -it mysql_3306 mysql -uroot -p -P 3306 -e 'select @@version, @@server_id, @@port;'

# 启动3307
docker run -id \
--name=mysql_3307 \
--net=host \
-v  /data/docker/mysql_3307/config:/etc/mysql/conf.d \
-v  /data/docker/mysql_3307/data:/var/lib/mysql \
-v /etc/localtime:/etc/localtime:ro \
-e MYSQL_ROOT_PASSWORD=root \
mysql:latest

# 测试
docker exec -it mysql_3307 mysql -uroot -p -P 3307 -e 'select @@version, @@server_id, @@port;'

# 主库中创建复制用户
docker exec -it mysql_3306 /bin/bash
mysql -u root -p -P 3306
create user repl@'127.0.0.%' identified by '123';
grant replication slave on *.* to repl@'127.0.0.%';
# 修改加密规则
ALTER USER repl@'127.0.0.%' IDENTIFIED WITH mysql_native_password BY '123';

# 备份主库
mysqldump -u root -p -A --master-data=2 --single-transaction  -R --triggers >/var/lib/mysql/full.sql
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=653;
cp full.sql /data/docker/mysql_3307/data/

# 恢复到从库
docker exec -it mysql_3307 /bin/bash
mysql -u root -p -P 3307
source /var/lib/mysql/full.sql

# 查看
help change master to
# 告知从库关键复制信息
CHANGE MASTER TO
  MASTER_HOST='127.0.0.1',
  MASTER_USER='repl',
  MASTER_PASSWORD='123',
  MASTER_PORT=3306,
  MASTER_LOG_FILE='mysql-bin.000003',
  MASTER_LOG_POS=704,
  MASTER_CONNECT_RETRY=10;

# 开启主从专用线程
start slave;

# 检查复制状态
show slave  status \G;
```

## Centos7下Redis部署

```shell
# 拉取
docker pull redis

# 目录
mkdir -p /data/redis_6379/{conf,log,pid}

# 新建配置文件,以配置文件方式启动
cat > /data/redis_6379/conf/redis_6379.conf <<EOF
requirepass redis_6379
port 6379
logfile /log/redis_6379.log
dir /data

dbfilename redis_6379.rdb
# bgsave发生错误时是否停止写入
stop-writes-on-bgsave-error yes
# 是否压缩
rdbcompression yes
# 是否校验文件
rdbchecksum yes

# 慢查询
slowlog-max-len 1000
slowlog-log-slower-than 1000

# 必须开启此项才能开启AOF
appendonly yes
# AOF文件名称
appendfilename "appendonly_6379.aof"
# AOF策略
appendfsync everysec
# 一般yes,开销没那么大
no-appendfsync-on-rewrite yes
# AOF文件重写需要的尺寸
auto-aof-rewrite-min-size 64mb
# AOF文件增长率
auto-aof-rewrite-percentage 100
aof-load-truncated yes
EOF

# 创建容器,设置端口映射,目录映射
# 让容器的时钟与宿主机时钟同步
# 开机启动
# 以配置文件方式启动
docker run -id \
-p 6379:6379 \
--name=redis_6379 \
-v /data/redis_6379/conf/redis_6379.conf:/etc/redis/redis.conf \
-v /data/redis_6379/data:/data \
-v /data/redis_6379/log:/log \
-v /etc/localtime:/etc/localtime:ro \
--restart=always \
redis redis-server /etc/redis/redis.conf
```

## Centos8下redis sentinel部署

```shell
# redis主节点配置

# 在/root目录下创建redis目录用于储存redis数据信息
mkdir -p ~/my_docker/redis/700{0,1,2}/data

# 新建配置文件,以配置文件方式启动
cat > ~/my_docker/redis/7000/7000.conf <<EOF
port 7000
pidfile /data/redis-7000.pid
logfile "7000.log"
EOF

# 创建容器,设置端口映射,目录映射
# 让容器的时钟与宿主机时钟同步
# 开机启动
# 以配置文件方式启动
# --net=host 覆盖主机的端口
docker run -id \
--name=redis_7000 \
--net=host \
-v ~/my_docker/redis/7000/7000.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/7000/data:/data \
-v /etc/localtime:/etc/localtime:ro \
redis redis-server /etc/redis/redis.conf

# 配置2个从节点

# 配置第一个
sed 's/7000/7001/g' ~/my_docker/redis/7000/7000.conf>~/my_docker/redis/7001/7001.conf
echo 'slaveof 127.0.0.1 7000' >> ~/my_docker/redis/7001/7001.conf

docker run -id \
--name=redis_7001 \
--net=host \
-v ~/my_docker/redis/7001/7001.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/7001/data:/data \
-v /etc/localtime:/etc/localtime:ro \
redis redis-server /etc/redis/redis.conf

# 配置第二个
sed 's/7001/7002/g' ~/my_docker/redis/7001/7001.conf>~/my_docker/redis/7002/7002.conf

docker run -id \
--name=redis_7002 \
--net=host \
-v ~/my_docker/redis/7002/7002.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/7002/data:/data \
-v /etc/localtime:/etc/localtime:ro \
redis redis-server /etc/redis/redis.conf
```

配置三个sentinel

```shell
# 配置第一个
mkdir -p ~/my_docker/redis/sentinel_2638{0,1,2}/data

cat > ~/my_docker/redis/sentinel_26380/redis-sentinel-26380.conf <<EOF
port 26380
logfile "26380.log"
sentinel monitor mymaster 127.0.0.1 7000 2
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
EOF

sed 's/26380/26381/g' ~/my_docker/redis/sentinel_26380/redis-sentinel-26380.conf>~/my_docker/redis/sentinel_26381/redis-sentinel-26381.conf
sed 's/26380/26382/g' ~/my_docker/redis/sentinel_26380/redis-sentinel-26380.conf>~/my_docker/redis/sentinel_26382/redis-sentinel-26382.conf

# 启动三个sentinel
docker run -id \
--name=redis_sentinel_26380 \
--net=host \
-v ~/my_docker/redis/sentinel_26380/redis-sentinel-26380.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/sentinel_26380/data:/data \
-v /etc/localtime:/etc/localtime:ro \
redis redis-sentinel /etc/redis/redis.conf

docker run -id \
--name=redis_sentinel_26381 \
--net=host \
-v ~/my_docker/redis/sentinel_26381/redis-sentinel-26381.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/sentinel_26381/data:/data \
-v /etc/localtime:/etc/localtime:ro \
redis redis-sentinel /etc/redis/redis.conf

docker run -id \
--name=redis_sentinel_26382 \
--net=host \
-v ~/my_docker/redis/sentinel_26382/redis-sentinel-26382.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/sentinel_26382/data:/data \
-v /etc/localtime:/etc/localtime:ro \
redis redis-sentinel /etc/redis/redis.conf
```

## Centos8下redis cluster部署

```shell
mkdir -p ~/my_docker/redis/cluster_701{0,1,2,3,4,5}/data

cat > ~/my_docker/redis/cluster_7010/7010.conf <<EOF
port 7010
logfile "7010.log"
dbfilename "dump-7010.rdb"
cluster-enabled yes
cluster-config-file nodes-7010.conf
cluster-require-full-coverage no
EOF

# 配置剩余五个
sed 's/7010/7011/g' ~/my_docker/redis/cluster_7010/7010.conf>~/my_docker/redis/cluster_7011/7011.conf
sed 's/7010/7012/g' ~/my_docker/redis/cluster_7010/7010.conf>~/my_docker/redis/cluster_7012/7012.conf
sed 's/7010/7013/g' ~/my_docker/redis/cluster_7010/7010.conf>~/my_docker/redis/cluster_7013/7013.conf
sed 's/7010/7014/g' ~/my_docker/redis/cluster_7010/7010.conf>~/my_docker/redis/cluster_7014/7014.conf
sed 's/7010/7015/g' ~/my_docker/redis/cluster_7010/7010.conf>~/my_docker/redis/cluster_7015/7015.conf

# 开启
docker run -id --name=redis_cluster_7010 --net=host -v ~/my_docker/redis/cluster_7010/7010.conf:/etc/redis/redis.conf -v ~/my_docker/redis/cluster_7010/data:/data -v /etc/localtime:/etc/localtime:ro redis redis-server /etc/redis/redis.conf
docker run -id --name=redis_cluster_7011 --net=host -v ~/my_docker/redis/cluster_7011/7011.conf:/etc/redis/redis.conf -v ~/my_docker/redis/cluster_7011/data:/data -v /etc/localtime:/etc/localtime:ro redis redis-server /etc/redis/redis.conf
docker run -id --name=redis_cluster_7012 --net=host -v ~/my_docker/redis/cluster_7012/7012.conf:/etc/redis/redis.conf -v ~/my_docker/redis/cluster_7012/data:/data -v /etc/localtime:/etc/localtime:ro redis redis-server /etc/redis/redis.conf
docker run -id --name=redis_cluster_7013 --net=host -v ~/my_docker/redis/cluster_7013/7013.conf:/etc/redis/redis.conf -v ~/my_docker/redis/cluster_7013/data:/data -v /etc/localtime:/etc/localtime:ro redis redis-server /etc/redis/redis.conf
docker run -id --name=redis_cluster_7014 --net=host -v ~/my_docker/redis/cluster_7014/7014.conf:/etc/redis/redis.conf -v ~/my_docker/redis/cluster_7014/data:/data -v /etc/localtime:/etc/localtime:ro redis redis-server /etc/redis/redis.conf
docker run -id --name=redis_cluster_7015 --net=host -v ~/my_docker/redis/cluster_7015/7015.conf:/etc/redis/redis.conf -v ~/my_docker/redis/cluster_7015/data:/data -v /etc/localtime:/etc/localtime:ro redis redis-server /etc/redis/redis.conf

# 查看信息
docker exec -it redis_cluster_7010 redis-cli -p 7010 cluster nodes
# 创建集群
docker exec -it redis_cluster_7010 redis-cli -p 7010 --cluster create  127.0.0.1:7010 127.0.0.1:7011 127.0.0.1:7012 127.0.0.1:7013 127.0.0.1:7014 127.0.0.1:7015 --cluster-replicas 1
```

## Centos7下contos7部署

```shell
# --privileged=true 要加入特权
docker run -id --name=c2 --privileged=true centos:centos7

docker run -id --name=c3 --privileged=true  centos:centos7
docker run -id --name=jasper --privileged=true  centos:centos7
docker run -id --name=c5 --privileged=true -p 10005:22 centos:centos7

# 进入环境
docker exec -it c2 /bin/bash
```

## windows 10下Python部署

```shell
docker run -id --name=tornado_py3.6 -v C:\Users\CRAB\Desktop\my_docker\learn_tornado:/app python:3.6-buster
```

## windows 10下nginx部署

```shell
docker run --name stnginx -p 9000:80 -v  C:\Users\CRAB\Desktop\my_docker\docker_data\stnginx\nginx.conf:/etc/nginx/nginx.conf:ro -d nginx
```

## windows 10下MongoDB部署

```shell
docker pull mongo

# 创建容器,设置端口映射,目录映射
docker run --name=mongo_27017 -p 27017:27017  -id mongo:latest

# 测试是否成功
docker exec -it mongo_27017 mongo
```

## windows 10下elasticsearch部署

```shell
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:6.8.11
```

## windows 10下contos7部署

```shell
docker pull centos:centos7

# 创建容器,目录映射
docker run -it --name=centos7.1  centos:centos7

# 测试是否成功
docker exec -it centos7 /bin/bash
```

## windows 10下Redis部署

```shell
# 拉取
docker pull redis

# 创建目录用于储存redis数据信息
D:\program\docker_data\redis_6379{data,log, conf}

# 新建配置文件,以配置文件方式启动
D:\program\docker_data\redis_6379\conf\6379.conf
'''
port 6379
logfile /log/redis_6379.log
dbfilename redis_6379.rdb
dir /data
'''

# 创建容器,设置端口映射,目录映射
# 让容器的时钟与宿主机时钟同步
# 开机启动
# 以配置文件方式启动
docker run -id -p 6379:6379 --name=redis_6379 -v D:\program\docker_data\redis_6379\conf\6379.conf:/etc/redis/redis.conf -v D:\program\docker_data\redis_6379\data:/data -v D:\program\docker_data\redis_6379\log:/log redis redis-server /etc/redis/redis.conf
```

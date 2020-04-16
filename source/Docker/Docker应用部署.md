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
# 开机启动
docker run -id \
--name=mysql_3306 \
-v ~/my_docker/mysql/3306/config:/etc/mysql/conf.d \
-v ~/my_docker/mysql/3306/data:/var/lib/mysql \
-v /etc/localtime:/etc/localtime:ro \
-e MYSQL_ROOT_PASSWORD=root \
mysql:latest

# 测试是否成功
docker exec -it mysql_3306 mysql -uroot -p
```

## Centos7下Redis部署

```shell
# 拉取
docker pull redis

# 在/root目录下创建redis目录用于储存redis数据信息
mkdir ~/my_docker/redis/7000

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
docker run -id \
-p 7000:6379 \
--name=redis_7000 \
-v ~/my_docker/redis/7000/7000.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/6379/data:/data \
-v /etc/localtime:/etc/localtime:ro \
--restart=always \
redis redis-server /etc/redis/redis.conf
```

## Centos8下contos6部署

```shell
docker run -id \
--name=centos6 \
-v /data/docker/centos6:/data \
-v /etc/localtime:/etc/localtime:ro \
centos:6

# 进入环境
docker exec -it centos6 /bin/bash
```

## windows 10下Python部署

```shell
docker run -id --name=tornado_py3.6 -v C:\Users\CRAB\Desktop\my_docker\learn_tornado:/app python:3.6-buster
```

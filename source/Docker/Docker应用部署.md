# Docker应用部署

## Centos7下MySQL部署

```shell
# 搜索镜像
docker search mysql
# 拉取
docker pull mysql

# 在/root目录下创建MySQL目录用于储存MySQL数据信息
mkdir ~/my_docker/mysql

# 创建容器,设置端口映射,目录映射
# 让容器的时钟与宿主机时钟同步
# 开机启动
docker run -id \
-p 3306:3306 \
--name=mysql \
-v ~/my_docker/mysql/logs:/logs \
-v ~/my_docker/mysql/config:/etc/mysql/conf.d \
-v ~/my_docker/mysql/data:/var/lib/mysql \
-v /etc/localtime:/etc/localtime:ro \
-e MYSQL_ROOT_PASSWORD=54170801am+1S \
--restart=always \
mysql:latest
```

## Centos7Redis部署

```shell
# 拉取
docker pull redis

# 在/root目录下创建redis目录用于储存redis数据信息
mkdir ~/my_docker/redis

# 新建配置文件,以配置文件方式启动
my_docker/redis/config/6379.conf

# 创建容器,设置端口映射,目录映射
# 让容器的时钟与宿主机时钟同步
# 开机启动
# 以配置文件方式启动
docker run -id \
-p 6379:6379 \
--name=redis_6379 \
-v ~/my_docker/redis/config/6379.conf:/etc/redis/redis.conf \
-v ~/my_docker/redis/data:/data \
-v /etc/localtime:/etc/localtime:ro \
--restart=always \
redis redis-server /etc/redis/redis.conf
```

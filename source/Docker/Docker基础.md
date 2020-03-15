# Docker基础

## Docker概念

Docker是一个开源的应用容器引擎.

Docker是一种容器技术,解决软件跨环境迁移的问题

## Docker安装

### Centos7安装Docker

安装

```shell
# yum包更新
yum update

# 安装需要的软件包, yum-utils提供yum-config-manager功能,另外两个是devicemapper驱动依赖的
yum install -y yum-utils device-mapper-persisitent-data lvm2

# 设置yum源
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装docker,社区版
yum install -y docker-ce

# 查看版本,验证是否安装成功
docker -v
```

配置Docker加速器

```shell
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://thkvkd0a.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Docker命令

### Docker服务相关命令

```shell
# 启动
systemctl start docker

# 停止
systemctl stop docker

# 重启
systemctl restart docker

# 状态查看
systemctl status docker

开机自启动
systemctl enable docker
```

### Docker镜像相关命令

```shell
# 查看镜像
[root@izbp128jigdcjx00os4h3sz bin]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
redis               latest              f0453552d7f2        34 hours ago        98.2MB
mysql               latest              9b51d9275906        10 days ago         547MB

# 查看所有镜像id
[root@izbp128jigdcjx00os4h3sz bin]# docker images -q
f0453552d7f2
9b51d9275906

# 搜索镜像
# docker search 镜像名称
docker search redis

# 拉取镜像
# docker pull 镜像名称:版本号(不指定为最新)
docker pull redis

# 删除镜像
# docker rmi 镜像名称:版本号
docker rmi mysql:latest
# 通过ID删除
# docker rmi 9b51d9275906

# 删除所有本地镜像
docker rmi `docker images -q`
```

### Docker容器相关命令

创建容器

```shell
# -i:保持容器运行
# -t:为容器重新分配一个伪输入终端,-it,容器创建后自动进入,退出则关闭容器
# -d:以守护模式运行容器,通过docker exec进入,退出后容器不关闭

[root@izbp128jigdcjx00os4h3sz bin]# docker run -it --name=c1 centos:7 /bin/bash
Unable to find image 'centos:7' locally
7: Pulling from library/centos
ab5ef0e58194: Pull complete
Digest: sha256:4a701376d03f6b39b8c2a8f4a8e499441b0d567f9ab9d58e4991de4472fb813c
Status: Downloaded newer image for centos:7
[root@9e44af0b49c0 /]#

[root@izbp128jigdcjx00os4h3sz bin]# docker run -id --name=c2 centos:7 /bin/bash
f07547d6a854f705f8b13be0bb82152f5d0f2242117b04869a6065118a8c296b
```

查看容器

```shell
# 查看正在运行的容器
[root@izbp128jigdcjx00os4h3sz bin]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
f07547d6a854        centos:7            "/bin/bash"         15 seconds ago      Up 13 seconds                           c2

# 查看所有容器
[root@izbp128jigdcjx00os4h3sz bin]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                       PORTS               NAMES
f07547d6a854        centos:7            "/bin/bash"         47 seconds ago      Up 46 seconds                                    c2
9e44af0b49c0        centos:7            "/bin/bash"         3 minutes ago       Exited (127) 2 minutes ago                       c1

# 查看容器信息
docker inspect 容器名称

# 进入容器,退出容器不关闭
docker exec -it c1 /bin/bash

# 停止容器
[root@izbp128jigdcjx00os4h3sz bin]# docker stop c2

c2

# 启动容器
[root@izbp128jigdcjx00os4h3sz bin]# docker start c2
c2

# 删除容器,先停止运行再删除
[root@izbp128jigdcjx00os4h3sz bin]# docker rm c1
c1
```

## Docker容器的数据卷

### 概念

```shell
# 数据卷是宿主机中的一个目录或文件
# 当容器目录和数据卷目录绑定后,修改同步
# 多对多关系
```

### 作用

```shell
# 容器数据持久化
# 外部机器和容器间接通信
# 容器之间数据交换
```

### 配置

```shell
docker run -it --name=c3 -v /root/data:/root/data_container centos:7 /bin/bash
```

### 数据卷容器

```shell
# 创建数据卷容器
docker run -it --name=c3 -v /volume centos:7 /bin/bash

# 创建容器并设置数据卷
docker run -it --name=c1 --volumes-from c3 centos:7 /bin/bash
docker run -it --name=c2 --volumes-from c3 centos:7 /bin/bash
```

## Docker应用部署

### MySQL部署

```shell
# 搜索镜像
docker search mysql
# 拉取
docker pull mysql:5.6

# 在/root目录下创建MySQL目录用于储存MySQL数据信息
mkdir ~/mysql
cd ~/mysql

# 创建容器,设置端口映射,目录映射
docker run -id \
-p 3306:3306 \
--name=c_mysql \
-v $pwd/conf:/etc/mysql/conf.d \
-v $pwd/logs:/logs \
-v $pwd/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:5.6
```

## Dockerfile

### Dockerfile概念

Dockerfile是一个文本文件,包含了一条条的指令,每一条指令构建一层,基于基础镜像,最终构建出一个新的镜像

### Dockerfile构建

```shell
docker build -f Dockerfile名称 -t 镜像名称 .
```

## Docker Compose

### Docker Compose概念

Docker Compose是一个编排多容器分布式部署的工具,提供命令集管理容器化应用的完整开发周期,包括服务构建,启动和停止

使用步骤

```shell
# 利用Dockerfile定义运行环境镜像
# 使用docker-compose.yml定义组成应用的各种服务
# 运行docker-compose up启动应用
```

## Docker私有仓库

### 私有仓库搭建

```shell
# 拉取私有仓库
docker pull registry

#  创建私有仓库
docker run -id --name=registry -p 5000:5000 registry

# 浏览器输入http://私有仓库地址ip:5000/v2/_catalog测试是否搭建成功
# 信任私有仓库
vim /etc/docker/daemon.json
{"insecure-registries":["私有仓库服务器ip:5000"]}

# 重启docker服务
systemctl restart docker

# 启动私有仓库
docker start register
```

### 上传镜像至私有仓库

```shell
# 标记镜像为私有仓库的镜像
docker tag 镜像名称 私有仓库服务器ip:5000/镜像名称

# 上传
docker push 私有仓库服务器ip:5000/镜像名称
```

### 从私有仓库拉取镜像

```shell
# 拉取镜像
docker pull 私有仓库服务器ip:5000/镜像名称
```

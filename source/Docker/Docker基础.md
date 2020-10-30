# Docker基础

## Docker概念

Docker是一个开源的应用容器引擎

Docker是一种容器技术,解决软件跨环境迁移的问题

## Docker命令

### Docker服务相关命令

```shell
# 状态查看
systemctl status docker

# 开机自启动
systemctl enable docker

# 查看镜像,容器,数据卷所占用的空间
docker system df
```

### Docker的镜像基础管理

```shell
# 搜索镜像
docker search redis

# 拉取镜像
# docker pull 镜像名称:版本号(不指定为最新)
docker pull redis

# 查看镜像
docker image ls

# 查看镜像详细信息
docker image inspect centos

# 查看所有镜像id
docker image ls -q

# 导出, 删除,导入镜像
docker image save redis > redis.tar
docker image rm redis
docker image load -i redis.tar

# 添加标签, 生成新的镜像
docker image tag 62f1d3402b78 crab/redis:v1

# 通过ID删除
# docker image rm  9b51d9275906

# 删除所有本地镜像, -f强制删除
docker image rm -f `docker images -q`

# 删除虚悬镜像
docker image prune
```

### Docker容器相关命令

```shell
# 交互式容器
docker container run -it  --name=r1  redis

# 守护式容器
docker container run -id --name=c1 centos:centos7 /bin/bash

# 查看容器
docker container ls
docker container ls -a
docker container inspect c1

# 查看容器输出信息
docker container logs c1

# 启动,停止容器
docker start c2
docker stop c2

# 删除容器,先停止运行再删除, -f强制
docker rm c1

# 清理掉所有处于终止状态的容器
docker container prune
```

连接容器

```shell
docker container attach c1

# 子进程的方式登录(在已有工作容器中生成子进程,可以用于进行容器的调试,退出时也不会影响到当前容器)
docker container exec -it c1 /bin/bash
```

导入导出容器快照

```shell
docker import 容器名称
docker export 容器名称
# 容器快照文件将丢弃所有的历史记录和元数据信息，即仅保存容器当时的快照状态
# docker load 镜像存储文件将保存完整记录,体积大
```

docker容器的网络访问

```shell
# 指定映射, docker会自动添加一条iptables规则来实现端口映射
# -p hostPort:containerPort
docker container run -id --name=c1 -p 80:80 centos:centos7 /bin/bash
```

## Docker容器的数据卷

Docker 容器产生的数据,如果不`docker commit`那么容器删除后,数据也就丢失了

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

无数据卷, 从容器内拷贝文件到主机上

```shell
docker container cp <container_id>:<path> <target_path>
```

### 配置数据卷

```shell
# 可挂载多个数据卷
# docker run -it -v /宿主机绝对路径:/容器内目录:权限 <image_name>
docker container run -it --name=c3 -v /root/data:/root/data_container centos:7 /bin/bash
```

### 数据卷容器

> 命名的容器挂载数据卷, 其他的容器通过挂载这个 (父容器) 实现数据共享, 挂载数据卷的容器被称为数据卷容器

```shell
# 创建数据卷容器
docker run -it --name=c3 -v /volume centos:7 /bin/bash

# 创建容器并设置数据卷
docker run -it --name=c1 --volumes-from c3 centos:7 /bin/bash
docker run -it --name=c2 --volumes-from c3 centos:7 /bin/bash
```

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

## Docker仓库

### Docker Hub

```shell
# 登录登出
docker login
docker logout

# 推送镜像
docker push username/ubuntu:18.04
```

### 私有仓库搭建

```shell
# 拉取私有仓库
docker pull registry

#  创建私有仓库
docker run -id --name=registry -p 5000:5000 registry
# 仓库会被创建在容器的/var/lib/registry目录

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
# docker tag 镜像名称 私有仓库服务器ip:5000/镜像名称
docker tag ubuntu:latest 127.0.0.1:5000/ubuntu:latest

# 上传
docker push 私有仓库服务器ip:5000/镜像名称
```

### 从私有仓库拉取镜像

```shell
# 拉取镜像
docker pull 私有仓库服务器ip:5000/镜像名称
```

## Docker网络

```shell
# docker run network=xxx
# none : 无网络模式
# bridge ： 默认模式，相当于NAT
# host : 公用宿主机Network NameSapce
# container：与其他容器公用Network Namespace

# 创建网络
docker network create -d bridge my-net

# 连接容器
docker run -it --rm --name busybox1 --network my-net busybox sh
docker run -it --rm --name busybox2 --network my-net busybox sh

# 测试连接
ping busybox2
```

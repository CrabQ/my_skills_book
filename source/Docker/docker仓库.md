# Docker仓库

## Docker Hub

```shell
# 登录登出
docker login
docker logout

# 推送镜像
docker push username/ubuntu:18.04
```

## 私有仓库搭建

搭建

```shell
# 拉取私有仓库
docker pull registry

#  创建私有仓库
docker run -d -p 5000:5000 --restart=always --name registry -v /opt/registry:/var/lib/registry registry
# 仓库会被创建在容器的/var/lib/registry目录

# 浏览器输入http://私有仓库地址ip:5000/v2/_catalog测试是否搭建成功
curl http://127.0.0.1:5000/v2/_catalog

# 修改配置文件, 信任私有仓库
vim /etc/docker/daemon.json
{"insecure-registries":["127.0.0.1:5000"]}

# 重启docker服务
systemctl restart docker

# 启动私有仓库
docker start register
```

上传,拉取镜像至私有仓库

```shell
# 标记镜像为私有仓库的镜像
# docker tag 镜像名称 私有仓库服务器ip:5000/镜像名称
docker tag centos:centos7 127.0.0.1:5000/crab/centos7:v1

# 上传
# docker push 私有仓库服务器ip:5000/镜像名称
docker push 127.0.0.1:5000/crab/centos7:v1

# 拉取镜像
# docker pull 私有仓库服务器ip:5000/镜像名称
docker pull 127.0.0.1:5000/crab/centos7:v1
```

### 本地仓库加安全验证

```shell
# yum install -y httpd-tools

mkdir -p /opt/registry-auth/ && htpasswd -Bbc /opt/registry-auth/htpasswd crab 123

# 删除原有容器
# 创建带秘钥功能的registry容器
docker run -d -p 5000:5000 --restart=always --name registry -v /opt/registry:/var/lib/registry -v /opt/registry-auth/:/auth/ -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd"  registry

# push镜像
docker tag centos:centos7 127.0.0.1:5000/crab/centos7:v2
# 不能直接push, 需要登录
docker login 127.0.0.1:5000
docker push 127.0.0.1:5000/crab/centos7:v2

# 拉取镜像不需要登录
docker pull 127.0.0.1:5000/crab/centos7:v2
```

## harbor

搭建

```shell
# 运行docker

yum install -y docker-compose

tar -zxvf harbor-online-installer-v1.10.6.tgz

# 修改配置文件
vim harbor.cfg
# hostname: 172.16.245.27
# port: 8080

# 加载配置
./prepare

# 安装
./install.sh

# 制作镜像
docker tag centos:centos7 172.16.245.27:8080/crab/centos7:v2

# 上传, 先登录
docker login 172.16.245.27:8080
docker push 172.16.245.27:8080/crab/centos7:v2

# 拉取镜像
# docker pull 私有仓库服务器ip:8080/镜像名称
docker pull 172.16.245.27:8080/crab/centos7:v2
```

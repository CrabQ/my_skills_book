# Docker安装

## Centos7安装Docker

```shell
# 查看是否安装过
 yum list installed | grep docker
# 卸载旧版本
yum remove -y docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine \
                  docker-ce-cli.x86_64

# yum包更新
yum update

# 安装需要的软件包, yum-utils提供yum-config-manager功能,另外两个是devicemapper驱动依赖的
yum install -y yum-utils device-mapper-persistent-data lvm2

# 设置yum源
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装docker,社区版
yum install -y docker-ce

# 查看版本,验证是否安装成功
docker -v

# 查看当前 Docker 有关信息
docker info

# 帮助
docker --help

# 权限管理
# 默认只有root用户和docker组的用户才可以访问Docker引擎
# 添加docker组
groupadd docker
# 将当前用户加入组
usermod -aG docker $USER
```

配置Docker加速器

```shell
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://thkvkd0a.mirror.aliyuncs.com"]
}
EOF

# 重启服务
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## windows 10安装Docker

```shell
# 下载 Docker Desktop for Windows
# 安装
# 配置Docker加速器,设置里面修改
"registry-mirrors": ["https://thkvkd0a.mirror.aliyuncs.com"]
```

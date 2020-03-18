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

# 开启远程访问(可选)
# vi /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock
# 重新读取配置文件，重新启动docker服务
systemctl daemon-reload
systemctl restart docker

docker -H tcp://121.196.202.188:2375 images
# 帮助
docker --help
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

## windows 10安装Docker

```shell
# 下载 Docker Desktop for Windows
# 安装
# 配置Docker加速器,设置里面修改
"registry-mirrors": ["https://thkvkd0a.mirror.aliyuncs.com"]
```

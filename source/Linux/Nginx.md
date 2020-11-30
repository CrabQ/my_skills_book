# Nginx

## 安装

```shell
# 1. yum安装
yum install yum-utils -y

# 更新yum源
cat >/etc/yum.repos.d/nginx.repo<<EOF
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF

# 安装
yum install -y nginx

# 启动
systemctl start nginx


# 2. 源码包安装
wget http://nginx.org/download/nginx-1.18.0.tar.gz
```

相关目录

```shell
/etc/nginx              # 配置文件
/var/log/nginx          # 日志
/usr/bin/nginx          # 命令
/usr/share/nginx/html   # 站点目录
```

## 配置文件

配置文件解析

```shell
# master process 主进程, 管理服务能否正常运行
# worker process 工作进程, 处理用户访问请求

# 主配置文件
# /etc/nginx/nginx.conf
# 第一部分,配置文件主区域配置
user  nginx;    # 定义worker进程管理的用户
worker_processes  1;    # 定义有几个worker进行 == cpu核数|2倍核数
error_log  /var/log/nginx/error.log warn;   # 错误日志
pid        /var/run/nginx.pid;  # pid文件路径, 判断nginx服务是否开启


# 第二部分,配位置文件事件区域
events {
    worker_connections  1024;   # 一个worker进程可以同时接受1024个访问请求
}

# 第三部分, 配置http区域
http {
    include       /etc/nginx/mime.types;    # 加载一个配置文件
    default_type  application/octet-stream; # 指定默认识别文件类型
    # 日志格式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;    # 日志路径
    sendfile        on;
    #tcp_nopush     on;
    keepalive_timeout  65;  #超时时间
    #gzip  on;
    include /etc/nginx/conf.d/*.conf;   # 加载一个配置文件
}

# 扩展配置(虚拟主机配置文件)
# /etc/nginx/conf.d/default.conf
# 第四部分,server区域信息(网站==虚拟主机)
server {
    listen       80;        # 监听端口
    server_name  localhost; # 网站域名
    location / {
        root   /usr/share/nginx/html;   # 定义站点目录位置
        index  index.html index.htm;    # 首页
    }
    error_page  404              /404.html; # 错误页面

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

}
```

配置修改

```shell
# 平滑重启
systemctl reload nginx

# 只监听某个ip
    listen       127.0.0.1:80;
# 地址修改,平滑重启不生效
systemctl restart nginx

# 语法检查
nginx -t

# 禁止Ip访问
location /a {
    deny 10.0.0.0/24;       # 禁止
    allow 172.16.1.0/24;    # 允许
}
```

## 常用模块

用户访问需认证

```shell
# 1. 配置
server {
    listen       80;
    server_name  localhost;
    location / {
        root   /usr/share/nginx/html;
        index  crab.html;
        # auth_basic  "crab";
        # auth_basic_user_file password/htpasswd;
    }

# 2. 创建密码文件
htpasswd -bc ./htpasswd crab02 123456

# 3. 修改密码文件权限
chown nginx.nginx ./htpasswd && chmod 600 ./htpasswd

# 4. 重启服务
systemctl reload nginx
```

站点目录索引功能

```shell
# 模块: ngx_http_autoindex_module
# 1. 配置, 需要将首页文件删除
server {
    listen       80;
    server_name  localhost;
    location / {
        root   /usr/share/nginx/html;
        index  crab.html; # 修改为不存在页面
        # autoindex on;
    }

# 2. 修改mime.types文件,文件有配置的点击看到数据信息,无配置的点击下载
```

字符集设置

```shell
# 模块: charset
server {
    listen       80;
    server_name  localhost;
    location / {
        root   /usr/share/nginx/html;
        index  crab.html;
        # charset utf-8;
    }
```

别名

```shell
server {
    listen       80;
    # server_name  localhost, crab.com;
    location / {
        root   /usr/share/nginx/html;
        index  crab.html;
    }
```

利用nginx状态模块功能对网站进行监控

```shell
# 模块: ngx_http_stub_status_module

# 1. 配置
server {
    listen       80;
    # server_name  localhost, crab.com;
    location / {
        root   /usr/share/nginx/html;
        index  crab.html;
        stub_status;
    }

# 2. 重启
```

添加日志

```shell
server {
    listen       80;
    server_name  localhost, crab.com;
    # access_log  /var/log/nginx/localhost.log  main;    # 日志路径
    location / {
        root   /usr/share/nginx/html;
        index  crab.html;
    }

```

location作用

```shell
# 错误页面优雅显示, e.jpg放站点根目录即可
# 访问crab.com/crab/sldgj, 找不到页面显示e.jpg
location /crab {
    root /html/www;
    error_page 404 /e.jpg;
}
```

负载均衡

```shell
# ngx_http_upstream_module    -- upstream   负载均衡
# ngx_http_proxy_module       -- proxy_pass 反向代理

# 10.0.0.5 负载均衡服务器配置
upstream crab {
    server 10.0.0.7:80;
    server 10.0.0.8:80;
    server 10.0.0.9:80;
}

server {
    listen 80;
    server_name www.crab.com;
    location / {
        proxy_pass http://crab;
        proxy_set_header Host $host; # 使负载均衡服务器携带真正的访问域名给服务器
        proxy_set_header X-Forward-For $remote_addr; # 显示访问的真正服务器的IP,而非负载均衡服务器ip,用于统计
        proxy_next_upstream error timeout http_404; # 某台服务器访问错误,不返回错误页面,访问另一台服务器
    }
}


# 负载均衡几种方式
# 1. 轮训分配请求

# 2. 权重分配
upstream crab {
    server 10.0.0.7:80 weight=3;
    server 10.0.0.8:80 weight=2;
    server 10.0.0.9:80 weight=1;
}

# 3. 热备功能
upstream crab {
    server 10.0.0.7:80;
    server 10.0.0.8:80;
    server 10.0.0.9:80 backup;
}

# 4. 定义最大失败次数
max_fails=5

# 5. 定义失败之后重发的间隔时间
fail_timeout=10S

# 不同的调度算法
# 1. rr 轮训调度
# 2. wrr 权重调度
# 3. ip_hash 算法
# 4. least_conn
```

其他

```shell
# 修改默认上传文件大小
upload_max_filesize = 50M
```

## 虚拟主机配置实操

```shell
# 配置文件 /etc/nginx/gninx.conf
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server{
        listen  80;
        server_name www.qaqaqa.org
        location  / {
            root html/qaqaqa;
            index index.html index.htm;
        }
    }
}

# 创建域名对应站点
mkdir -p /etc/nginx/html/qaqaqa
echo "http://www.qaqaqa.org" > /etc/nginx/html/qaqaqa/index.html

# 语法检查
nginx -t

# 重新加载配置文件
nginx -s reload

# 查看是否重启成功
ps -ef |grep nginx
netstat -lntp|grep 80

# 添加host解析
echo "172.17.0.2 www.qaqaqa.org" >> /etc/hosts

# 测试
curl www.qaqaqa.org
```

## 运维高可用

```shell
yum install -y keepalived

# 配置文件
# vim /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email { # 邮箱相关, 收件人
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc # 链接的邮箱服务器
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id LVS_DEVEL # 高可用集群主机身份表示(不能重复)
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {        # Vrrp协议家族
    state MASTER            # 表示所在家族中的身份(MASTER/BACKUP)
    interface eth0          # 指定虚拟IP地址出现在什么网卡上
    virtual_router_id 51    # 表示家族身份信息, 多台高可用服务配置一直
    priority 100            # 优先级
    advert_int 1            # 组播包发送间隔
    authentication {        # 认证
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.200.16      # 虚拟ip地址信息
        192.168.200.17
        192.168.200.18
    }
}

```

高可用服务安全访问配置(让用户只能通过负载均衡服务器访问服务器)

```shell
# 1. 修改nginx负载均衡配置
server {
    listen ip:80; # ip: vip地址
}

# systemctl restart nginx

# 设置监听网卡上没有的地址
echo 'net.ipv4.ip_nonlocal_bind = 1' >>/etc/sysctl.conf
sysctl -p
```

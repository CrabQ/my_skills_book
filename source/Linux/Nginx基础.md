# Nginx基础

nginx通过docker安装

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

# Centos7相关命令

## Centos7防火墙相关命令

```shell
# 查看状态
systemctl status firewalld
# 开启
systemctl start firewalld

# 开启端口
[root@izbp128jigdcjx00os4h3sz data]# firewall-cmd --permanent --zone=public --add-port=6379/tcp --permanent
success

# 查看端口
[root@izbp128jigdcjx00os4h3sz data]# firewall-cmd --permanent --query-port=6379/tcp
yes

# 重启防火墙
[root@izbp128jigdcjx00os4h3sz data]# firewall-cmd --reload
success
```

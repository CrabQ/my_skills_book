# Centos7安装Mysql

## yum按照

1. 卸载默认安装的mariadb：

   ```shell
   yum remove mariadb.x86_64
   ```

2. 获取mysql官方yum源

   ```shell
   wget https://repo.mysql.com//mysql80-community-release-el7-3.noarch.rpm
   ```

3. 本地安装yum源

   ```shell
   yum localinstall mysql80-community-release-el7-3.noarch.rpm
   ```

4. 使用yum安装

   ```shell
   yum install mysql-community-server.x86_64
   ```

5. 启动mysql

   ```shell
   service mysqld start
   ```

6. 查找默认登录密码

   ```shell
   cat /var/log/mysqld.log | grep password
   ```

7. 登录修改默认密码

   ```shell
   mysql -u root -p

   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new password';
   ```

## 源码包安装

```shell
# 下载
wget http://mirrors.sohu.com/mysql/MySQL-8.0/mysql-8.0.18-el7-x86_64.tar.gz

# 解压
tar -zxvf mysql-8.0.18-el7-x86_64.tar.gz

# 移动
mv mysql-8.0.18-el7-x86_64 /usr/local/mysql

# 配置环境变量
echo 'export PATH=$PATH:/usr/local/mysql/bin' >> /etc/profile
source /etc/profile

# 建立mysql用户和组
useradd mysql

# 创建相关目录并修改权限
mkdir -p /root/mysql/3306/data
chown -R mysql.mysql /usr/local/mysql
chown -R mysql.mysql /root/mysql
chmod -R 755 /root/mysql/3306/data

# 初始化数据
/usr/local/mysql/bin/mysqld --initialize-insecure --user=root --basedir=/usr/local/mysql --datadir=/root/mysql/3306/data

# 添加mysql启动到本地服务
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql.server

# 使用systemd管理mysql
cat > /etc/systemd/system/mysqld_3306.service <<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql/bin/mysqld --defaults-file=/root/mysql/3306/my.cnf
LimitNOFILE = 5000
EOF

# 启动
systemctl start mysqld_3306.service

# 报错
# Starting MySQL.Logging to '/usr/local/mysql/data/izbp128jigdcjx00os4h3sz.err'.
# . ERROR! The server quit without updating PID file (/usr/local/mysql/data/izbp128jigdcjx00os4h3sz.pid).
```

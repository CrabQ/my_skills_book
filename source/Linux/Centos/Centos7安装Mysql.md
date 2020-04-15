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

## 安装mysql5.1.73

```shell
# 下载
wget http://dev.mysql.com/get/Downloads/MySQL-5.1/mysql-5.1.73.tar.gz
# 解压
tar -xvf mysql-5.1.73.tar.gz
cd mysql-5.1.73

# 安装相关依赖
yum install ncurses ncurses-devel
yum install -y gcc-c++*

# 编译到指定目录
# --with-unix-socket-path=/app/mysql5.1.73_data/mysql.sock 指定socket位置
./configure  '--prefix=/app/mysql5.1.73' '--without-debug' '--with-charset=utf8' '--with-extra-charsets=all' '--enable-assembler' '--with-pthread' '--enable-thread-safe-client' '--with-mysqld-ldflags=-all-static' '--with-client-ldflags=-all-static' '--with-big-tables' '--with-readline' '--with-ssl' '--with-embedded-server' '--enable-local-infile' '--with-plugins=innobase' '--with-unix-socket-path=/app/mysql5.1.73_data/mysql.sock' CXXFLAGS="-Wno-narrowing -fpermissive"
# 安装
make
make install

# 复制配置文件 自启动文件 自启动
mkdir -p /app/mysql5.1.73_data
cat > /app/mysql5.1.73_data/my.cnf <<EOF
[client]
port            = 3306
socket=/app/mysql5.1.73_data/mysql.sock

[mysqld]
port            = 3306
skip-locking
key_buffer_size = 16M
max_allowed_packet = 1M
table_open_cache = 64
sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M

basedir=/app/mysql5.1.73
datadir=/app/mysql5.1.73_data/data
user=mysql
log-error=/app/mysql5.1.73_data/mysqld.log
pid-file=/app/mysql5.1.73_data/mysqld.pid
socket=/app/mysql5.1.73_data/mysql.sock

log-bin=mysql-bin
binlog_format=mixed
server-id       = 1

[mysqldump]
quick
max_allowed_packet = 16M

[mysql]
no-auto-rehash
socket=/app/mysql5.1.73_data/mysql.sock

[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M

[mysqlhotcopy]
interactive-timeout
EOF

# 修改权限
chown -R mysql:mysql /app/mysql5.1.73 /app/mysql5.1.73_data
# 初始化mysql
/app/mysql5.1.73/bin/mysql_install_db --user=mysql --basedir=/app/mysql5.1.73 --datadir=/app/mysql5.1.73_data/data/

# 启动
/app/mysql5.1.73/bin/mysqld_safe --defaults-file=/app/mysql5.1.73_data/my.cnf &

# root添加密码
/app/mysql5.1.73/bin/mysqladmin -h localhost -u root password 'root'
# chmod a+wrx /etc/init.d/mysql
# service mysqld start

# 测试登录
/app/mysql5.1.73/bin/mysql -u root -p

# 使用systemd管理mysql
cat > /etc/systemd/system/mysqld_5.1.173.service <<EOF
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
ExecStart=/app/mysql5.1.73/bin/mysqld_safe --defaults-file=/app/mysql5.1.73_data/my.cnf
LimitNOFILE = 10000
EOF

# 启动
systemctl start mysqld_5.1.173.service
```

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
cp -r mysql-8.0.18-el7-x86_64 /app/mysql

# 配置环境变量
# echo 'export PATH=$PATH:/app/mysql/bin' >> /etc/profile
# source /etc/profile

# 建立mysql用户和组
useradd mysql

# 创建相关目录
mkdir -p /data/mysql/3306/data

# 复制配置文件
cat > /data/mysql/3306/my.cnf <<EOF
[client]
port            = 3306
socket=/data/mysql/3306/mysql.sock

[mysqld]
port            = 3306
basedir=/app/mysql
datadir=/data/mysql/3306/data
user=mysql
log-error=/data/mysql/3306/mysqld.log
pid-file=/data/mysql/3306/mysqld.pid
socket=/data/mysql/3306/mysql.sock
log-bin=/data/mysql/3306/mysql-bin
server-id = 10
EOF

# 修改权限
chown -R mysql.mysql /app/mysql  /data/mysql

# 初始化数据
/app/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/app/mysql --datadir=/data/mysql/3306/data --socket=/data/mysql/3306/mysql.sock

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
ExecStart=/app/mysql/bin/mysqld --defaults-file=/data/mysql/3306/my.cnf
LimitNOFILE = 5000
EOF

# 启动
systemctl start mysqld_3306.service

# root添加密码
/app/mysql/bin/mysqladmin -S /data/mysql/3306/mysql.sock -u root password 'root'
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
# --with-unix-socket-path=/data/mysql5.1.73_data/mysql.sock 指定socket位置
./configure  '--prefix=/app/mysql5.1.73' '--without-debug' '--with-charset=utf8' '--with-extra-charsets=all' '--enable-assembler' '--with-pthread' '--enable-thread-safe-client' '--with-mysqld-ldflags=-all-static' '--with-client-ldflags=-all-static' '--with-big-tables' '--with-readline' '--with-ssl' '--with-embedded-server' '--enable-local-infile' '--with-plugins=innobase' '--with-unix-socket-path=/data/mysql5.1.73_data/mysql.sock' CXXFLAGS="-Wno-narrowing -fpermissive"
# 安装
make
make install

# 复制配置文件
mkdir -p /data/mysql5.1.73_data
cat > /data/mysql5.1.73_data/my.cnf <<EOF
[client]
port            = 3316
socket=/data/mysql5.1.73_data/mysql.sock
[mysqld]
port            = 3316
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
datadir=/data/mysql5.1.73_data/data
user=mysql
log-error=/data/mysql5.1.73_data/mysqld.log
pid-file=/data/mysql5.1.73_data/mysqld.pid
socket=/data/mysql5.1.73_data/mysql.sock
log-bin=mysql-bin
binlog_format=mixed
server-id       = 1
[mysqldump]
quick
max_allowed_packet = 16M
[mysql]
no-auto-rehash
socket=/data/mysql5.1.73_data/mysql.sock
[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M
[mysqlhotcopy]
interactive-timeout
EOF

# 修改权限
chown -R mysql:mysql /app/mysql5.1.73 /data/mysql5.1.73_data
# 初始化mysql
/app/mysql5.1.73/bin/mysql_install_db --user=mysql --basedir=/app/mysql5.1.73 --datadir=/data/mysql5.1.73_data/data/

# 启动
# /app/mysql5.1.73/bin/mysqld_safe --defaults-file=/data/mysql5.1.73_data/my.cnf &

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
ExecStart=/app/mysql5.1.73/bin/mysqld_safe --defaults-file=/data/mysql5.1.73_data/my.cnf
LimitNOFILE = 10000
EOF

# 启动
systemctl start mysqld_5.1.173.service

# root添加密码
/app/mysql5.1.73/bin/mysqladmin -h localhost -u root password 'root'

# 测试登录
/app/mysql5.1.73/bin/mysql -u root -p
```

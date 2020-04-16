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
/app/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/app/mysql --datadir=/data/mysql/3306/data

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

# 配置环境变量
echo 'export PATH=$PATH:/app/mysql/bin' >> /etc/profile
source /etc/profile
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

## centos6升级mysql5.1.73到mysql5.7.23

centos6安装mysql5.1.73

```shell
# CentOS release 6.10 (Final)
# mysql Server version 5.7.23

# 安装
yum install -y mysql-server.x86_64

# 启动
service mysqld start

# 设置mysql开机自启
# chkconfig --list | grep mysqld
# chkconfig mysqld on

# root添加密码
/usr/bin/mysqladmin -u root password 'root'

# 创建测试库
create database genec1;

# 导入测试数据
mysql -u root -p genec1 </data/_glz_Mus_gene.sql
```

升级到5.5

```shell
# 安装依赖环境
yum install -y epel-release
# rpm -ivh https://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-15.ius.centos6.noarch.rpm
rpm -ivh https://repo.ius.io/ius-release-el6.rpm

# 创建备份路径
mkdir -p /data/mysqlupgrade/mysql51

# 备份配置文件
cp /etc/my.cnf /data/mysqlupgrade/mysql51/mysql-5.1.cnf.orig

# 跳过权限验证
cat >> /etc/my.cnf <<EOF
[client]
user=root
password=root
EOF

# 重启
service mysqld restart

# 备份数据库,用户
mysql -e 'show databases;' > /data/mysqlupgrade/mysql51/mysql-5.1.databases
mysql --silent --skip-column-names --execute "select concat('\'',User,'\'@\'',Host,'\'') as User from mysql.user;" | sort | while read u; do echo "-- $u"; mysql --silent --skip-column-names --execute "show grants for $u" | sed 's/$/;/'; done > /data/mysqlupgrade/mysql51/mysql-5.1.grants

# 导出所有数据
yum install -y xz
mysqldump --routines --all-databases | xz > /data/mysqlupgrade/mysql51/mysql-5.1.dump.sql.xz
# -- Warning: Skipping the data of table mysql.event. Specify the --events option explicitly.
# 是否备份事件表 --events

# 停止mysql
service mysqld stop
# 升级到5.5
yum --disableexcludes=all shell
remove mysql mysql-server mysql-libs
install mysql55 mysql55-server mysql55-libs mysqlclient16
ts solve
ts run
exit

# dbsake,更新配置文件
yum -y install wget
wget -O /data/mysqlupgrade/dbsake http://get.dbsake.net
chmod u+x /data/mysqlupgrade/dbsake
/data/mysqlupgrade/dbsake upgrade-mycnf --config /data/mysqlupgrade/mysql51/mysql-5.1.cnf.orig --target 5.5> /data/mysqlupgrade/mysql-5.5.cnf
mv -f /data/mysqlupgrade/mysql-5.5.cnf /etc/my.cnf

# 跳过权限验证,查看版本
sed -i 's/\[mysqld\]/[mysqld]\nskip-grant-tables\nskip-networking/' /etc/my.cnf
service mysqld start
mysql -sse "select @@version;"

# 对比
mysql -e "show databases;" > /data/mysqlupgrade/mysql51/mysql-5.5.databases
diff -U0 /data/mysqlupgrade/mysql51/mysql-5.1.databases /data/mysqlupgrade/mysql51/mysql-5.5.databases

# 更新database schema
mysql_upgrade

# 检查表,所有都OK
mysqlcheck -A

# 修改权限
sed -i '/\(skip-grant-tables\|skip-networking\)/d' /etc/my.cnf

# 重启
service mysqld restart

# 验证
mysqladmin -uroot -p version
```

升级到5.6

```shell
# 创建备份路径
mkdir -p /data/mysqlupgrade/mysql55

# 备份配置文件
cp /etc/my.cnf /data/mysqlupgrade/mysql55/mysql-5.5.cnf.orig

# 跳过权限验证
cat >> /etc/my.cnf <<EOF
[client]
user=root
password=root
EOF

# 重启
service mysqld restart

# 备份数据库,用户
mysql -e 'show databases;' > /data/mysqlupgrade/mysql55/mysql-5.5.databases
mysql --silent --skip-column-names --execute "select concat('\'',User,'\'@\'',Host,'\'') as User from mysql.user;" | sort | while read u; do echo "-- $u"; mysql --silent --skip-column-names --execute "show grants for $u" | sed 's/$/;/'; done > /data/mysqlupgrade/mysql55/mysql-5.5.grants

# 导出所有数据
mysqldump --routines --all-databases | xz > /data/mysqlupgrade/mysql55/mysql-5.5.dump.sql.xz
# -- Warning: Skipping the data of table mysql.event. Specify the --events option explicitly.
# 是否备份事件表 --events

# 停止mysql
service mysqld stop

# 升级到5.6
yum remove -y mysql55-common-5.5.61-2.ius.el6.x86_64
yum remove -y mysql55 mysql55-server mysql55-libs
yum remove -y yum remove mysqlclient16-5.1.61-4.ius.el6.x86_64
yum install -y mysql56u mysql56u-server mysql56u-libs mysqlclient16

# dbsake,更新配置文件
wget -O /data/mysqlupgrade/dbsake http://get.dbsake.net
chmod u+x /data/mysqlupgrade/dbsake
/data/mysqlupgrade/dbsake upgrade-mycnf --config /data/mysqlupgrade/mysql55/mysql-5.5.cnf.orig --target 5.6> /data/mysqlupgrade/mysql-5.6.cnf
mv -f /data/mysqlupgrade/mysql-5.6.cnf /etc/my.cnf

# 跳过权限验证,查看版本
sed -i 's/\[mysqld\]/[mysqld]\nskip-grant-tables\nskip-networking/' /etc/my.cnf
service mysqld start
mysql -sse "select @@version"
mysql -e "show databases;" > /data/mysqlupgrade/mysql55/mysql-5.6.databases
diff -U0 /data/mysqlupgrade/mysql55/mysql-5.5.databases /data/mysqlupgrade/mysql55/mysql-5.6.databases

# 更新database schema
mysql_upgrade

# 检查表,所有都OK
mysqlcheck -A

# 修改权限
sed -i '/\(skip-grant-tables\|skip-networking\)/d' /etc/my.cnf

# 重启
service mysqld restart

# 验证
mysqladmin -uroot -p version
```

升级到5.7

```shell
# 创建备份路径
mkdir -p /data/mysqlupgrade/mysql56

# 备份配置文件
cp /etc/my.cnf /data/mysqlupgrade/mysql56/mysql-5.6.cnf.orig

# 跳过权限验证
cat >> /etc/my.cnf <<EOF
[client]
user=root
password=root
EOF

# 重启
service mysqld restart

# 备份数据库,用户
mysql -e 'show databases;' > /data/mysqlupgrade/mysql56/mysql-5.6.databases
mysql --silent --skip-column-names --execute "select concat('\'',User,'\'@\'',Host,'\'') as User from mysql.user;" | sort | while read u; do echo "-- $u"; mysql --silent --skip-column-names --execute "show grants for $u" | sed 's/$/;/'; done > /data/mysqlupgrade/mysql56/mysql-5.6.grants

# 导出所有数据
mysqldump --routines --all-databases | xz > /data/mysqlupgrade/mysql56/mysql-5.6.dump.sql.xz
# -- Warning: Skipping the data of table mysql.event. Specify the --events option explicitly.
# 是否备份事件表 --events

# 停止mysql=
service mysqld stop

# 升级到5.7
yum remove -y mysqlclient16-5.1.61-4.ius.el6.x86_64
yum --disableexcludes=all shell
remove mysql56u mysql56u-server mysql56u-libs mysql56u-common
install mysql57u mysql57u-server mysql57u-libs mysqlclient16
ts solve
ts run
exit

# yum remove -y mysql55 mysql55-server mysql55-libs
# yum remove -y yum remove mysqlclient16-5.1.61-4.ius.el6.x86_64
# yum install -y mysql56u mysql56u-server mysql56u-libs mysqlclient16

# dbsake,更新配置文件
wget -O /data/mysqlupgrade/dbsake http://get.dbsake.net
chmod u+x /data/mysqlupgrade/dbsake
/data/mysqlupgrade/dbsake upgrade-mycnf --config /data/mysqlupgrade/mysql56/mysql-5.6.cnf.orig --target 5.7> /data/mysqlupgrade/mysql-5.7.cnf
mv -f /data/mysqlupgrade/mysql-5.7.cnf /etc/my.cnf

# 跳过权限验证,查看版本
sed -i 's/\[mysqld\]/[mysqld]\nskip-grant-tables\nskip-networking/' /etc/my.cnf
service mysqld start
mysql -sse "select @@version"
mysql -e "show databases;" > /data/mysqlupgrade/mysql56/mysql-5.7.databases
diff -U0 /data/mysqlupgrade/mysql56/mysql-5.6.databases /data/mysqlupgrade/mysql56/mysql-5.7.databases

# 更新database schema,报错则修复后重新运行
mysql_upgrade
# error    : Table upgrade required. Please do "REPAIR TABLE `_glz_Mus_gene`" or dump/reload to fix it!
# sys.sys_config                                     OK
# Repairing tables
# genec1._glz_Mus_gene

# 检查表,所有都OK
mysqlcheck -A

# 修改权限
sed -i '/\(skip-grant-tables\|skip-networking\)/d' /etc/my.cnf

# 重启
service mysqld restart

# 验证
mysqladmin -uroot -p version
```

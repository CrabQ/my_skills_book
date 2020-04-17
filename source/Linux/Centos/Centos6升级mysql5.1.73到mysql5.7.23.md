# Centos6升级mysql5.1.73到mysql5.7.23

centos6安装mysql5.1.73

```shell
# CentOS release 6.10 (Final)
# mysql Server version 5.1.73

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
mysql -u root -p -e 'create database genec1';

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

# 跳过权限验证
cat >> /etc/my.cnf <<EOF
[client]
user=root
password=root
EOF

# 备份配置文件
cp /etc/my.cnf /data/mysqlupgrade/mysql51/mysql-5.1.cnf.orig

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
yum remove -y remove mysql mysql-server mysql-libs
yum install -y mysql55 mysql55-server mysql55-libs mysqlclient16

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
# yum remove -y mysql55 mysql55-server mysql55-libs
# rpm -qa|grep mysql
# yum remove -y  mysqlclient16-5.1.61-4.ius.el6.x86_64
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

# 重启
service mysqld restart

# 备份数据库,用户
mysql -e 'show databases;' > /data/mysqlupgrade/mysql56/mysql-5.6.databases
mysql --silent --skip-column-names --execute "select concat('\'',User,'\'@\'',Host,'\'') as User from mysql.user;" | sort | while read u; do echo "-- $u"; mysql --silent --skip-column-names --execute "show grants for $u" | sed 's/$/;/'; done > /data/mysqlupgrade/mysql56/mysql-5.6.grants

# 导出所有数据
mysqldump --routines --all-databases | xz > /data/mysqlupgrade/mysql56/mysql-5.6.dump.sql.xz
# -- Warning: Skipping the data of table mysql.event. Specify the --events option explicitly.
# 是否备份事件表 --events

# 停止mysql
service mysqld stop

# 升级到5.7
yum remove -y  mysql56u mysql56u-server mysql56u-libs mysql56u-common
rpm -qa|grep mysql
yum install -y mysql57u mysql57u-server mysql57u-libs mysqlclient16

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
sed -i '/\(skip-grant-tables\|skip-networking\|user=root\|password=root\)/d' /etc/my.cnf

# 注意一开始添加进去配置文件的user,passowrd要删除

# 重启
service mysqld restart

# 验证
mysqladmin -uroot -p version
```

# MySQL安装及管理

## MySQL安装

### win 10安装mysql

安装（bin目录)

```shell
mysqld install
net start mysql
```

删除

```shell
net stop mysql
mysqld remove
```

my.ini(安装目录)

```shell
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8
[mysqld]
#设置3306端口
port = 3306
# 设置mysql的安装目录
basedir=D:\program\program_database\mysql-8.0.13-winx64
# 设置mysql数据库的数据的存放目录
datadir=D:\program\program_database\mysqldata
# 允许最大连接数
max_connections=200
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
# mysql导入导出数据的路径，空表示任意
secure_file_priv = ''
```

添加环境变量

```shell
D:\program\program_database\mysql-8.0.13-winx64\bin
```

#### mysql服务无法启动

```shell
mysqld --console

# 删除自己手动创建的data文件夹
mysqld -remove
# 自动创建了data文件夹以及相关的文件
mysqld --initialize-insecure
mysqld install
net start mysql
```

### Centos7安装mysql-5.7.26

```shell
# 下载
mkdir -p /application && cd /application
wget https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz

# 解压
tar -zxvf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz && mv mysql-5.7.26-linux-glibc2.12-x86_64 mysql5726

# 软件部分 /application/mysql5726
# 数据部分 /data/mysql5726/data

# 卸载默认安装的mariadb
yum remove mariadb.x86_64

# 建立mysql用户和组
useradd -s /sbin/nologin mysql5726

# 配置环境变量
# vim /etc/profile
# export PATH=/application/mysql5726/bin:$PATH
source /etc/profile

# 授权
chown -R mysql5726.mysql5726 /application/*
mkdir -p /data/mysql5726/data && chown -R mysql5726.mysql5726 /data

# 初始化(创建系统数据), 方式1
mysqld --initialize --user=mysql5726 --basedir=/application/mysql5726 --datadir=/data/mysql5726/data
# 生成临时密码, 180天过期

# 初始化方式2(无密码方式)
# mysqld --initialize-insecure --user=mysql5726 --basedir=/application/mysql5726 --datadir=/data/mysql5726/data

# 报错安装依赖
yum install -y libaio-devel

# 配置文件
cat > /etc/mysql5726.cnf <<EOF
[mysqld]
user=mysql5726
basedir=/application/mysql5726
datadir=/data/mysql5726/data
socket=/tmp/mysql.sock
server_id=5726
port=5726
log_error=/data/mysql5726/data/crabQ_err.log
log_timestamps=system
[mysql]
socket=/tmp/mysql.sock
EOF

# centos 6 启动mysql
# cp /application/mysql5726/support-files/mysql.server /etc/init.d/mysqld
# servive msqld start

# centos 7 启动mysql
cat > /etc/systemd/system/mysqld5726.service <<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql5726
Group=mysql5726
ExecStart=/application/mysql5726/bin/mysqld --defaults-file=/etc/mysql5726.cnf
LimitNOFILE = 5000
EOF

# 启动
systemctl start mysqld5726.service

# 设置初始密码
mysqladmin -uroot -p password root
```

## mysql启动关闭

```shell
# 1. 日常启动
mysql.server  start ---> mysqld_safe ---> mysqld
mysql.service start                  ---> mysqld
# 都依赖/etc/my.cnf启动

# 2. 维护性任务
mysqld_safe --skip-grant-tables
# 同样读取/etc/my.cnf, 参数冲突命令行优先
# 关闭
mysqladmin -uroot -p 123 shutdown
```

## mysql连接管理

```shell
# 查看是远程还是本地连接
# show porcesslist

# 1. TCP/IP
mysql -uroot -p -h 10.0.0.51 -P 3306

# 2. socket, -S /tmp/msyql.sock 可省略
mysql -u root -p
```

## mysql连接参数

```shell
# -e 免交互执行sql命令
mysql -u root -p -e 'select @@version;'

# < 导入数据
```

## 内置命令

```shell
help    打印命令
\c      结束上个命令运行
\q      退出mysql
\G      格式化输出
source  恢复备份文件
```

## 密码重置(忘记密码)

```shell
# 1. 关闭数据库库
/etc/init.d/mysqld stop

# 2. 维护模式启动数据库
mysqld_safe --skip-grant-tables --skip-networking &

# 3. 登录数据库修改密码
mysql> flush privileges;
mysql> alter user root@'localhost' identified by 'root';

# 4. 关闭数据库, 正常启动
pkill mysqld
systemctl start  mysqld


# 在mysql5.7.26, centos7以上方法测试不成功, 通过写入配置方式
# 1. 配置文件添加
[mysqld]
skip-grant-tables
skip-networking

# 2. 重启mysql, 输入mysql进入数据库

# 3. 登录数据库修改密码
mysql> flush privileges;
mysql> alter user root@'localhost' identified by 'root';

# 删除添加的配置, 正常启动mysql
```

## 一些错误

caching-sha2-password

```sql
# Navicat连接 Mysql 8.0.11 出现1251- Client does not support authentication protocol 错误解决方法一样

# root用户登陆,修改加密规则
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root' PASSWORD EXPIRE NEVER;
# 更新一下用户的密码
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
# 刷新权限
FLUSH PRIVILEGES;
alter user 'root'@'localhost' identified by 'root';
# 重启mysql服务
mysqld restart
```

Incorrect integer value: '' for column 'id' at row 1

```shell
mysql 5以上的版本如果是空值应该要写NULL或者0(int类型),或者:
1. 安装mysql的时候去除默认勾选的enable strict SQL mode
2. 更改mysql中的配置,重启mysql

sql-mode="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
# 修改为
sql-mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"，
```

RROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement

```shell
# mysql默认对导入导出的目录有权限限制,使用命令行进行导入导出时需在指定目录操作

# 查询mysql 的secure_file_priv值配置
show global variables like '%secure%';

# 更改mysql配置,重启
# 空表示无限制,null表示不允许
secure-file-priv=''
```

ONLY_FULL_GROUP_BY报错

```shell
# 填入查询的结果(去掉ONLY_FULL_GROUP_BY),重启mysql
vim /etc/my.cnf
sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
```

## 初始化配置

### 标签归类

```shell
# 服务器端
[mysqld]
[mysqld_safe]
# 包括上面两个
[server]

# 客户端
[mysql]
[mysqladmin]
[mysqldump]
# 包括上面3个
[client]
```

### 基础配置

```shell
[mysqld]
# 用户
user=mysql5726
# 软件安装目录
basedir=/application/mysql5726
# 数据存放目录
datadir=/data/mysql5726/data
# socket文件位置
socket=/tmp/mysql.sock
# 服务器ID, 1-65535
server_id=5726
port=5726
# 错误日志
log_error=/data/mysql5726/data/crabQ_err.log
log_timestamps=system
[mysql]
# 与服务器一致
socket=/tmp/mysql.sock
```

### 配置读取顺序

```shell
# 从左到右顺序读取, 相同会覆盖
etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf
```

### 指定读取自定义配置文件

```shell
# 启动时添加参数
--defaults-file=/etc/mysql5726.cnf
```

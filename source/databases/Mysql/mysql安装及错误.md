# mysql安装及错误

## win 10安装mysql

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

### mysql服务无法启动

```shell
mysqld --console

# 删除自己手动创建的data文件夹
mysqld -remove
# 自动创建了data文件夹以及相关的文件
mysqld --initialize-insecure
mysqld install
net start mysql
```

### 添加环境变量

```shell
D:\program\program_database\mysql-8.0.13-winx64\bin
```

### 初始设置

```sql
# root用户密码密码
mysqladmin -u root password 123456
# 新建用户
create user 'bmnars'@'localhost' identified by '123456';
# 给用户授权
grant all privileges on 想授权的数据库.* to 'user1'@'%';
# all 可以替换为 select,delete,update,create,drop
grant all privileges on bmnars.* to bmnars@localhost;
```

## 报错

关于`caching-sha2-password`问题

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

`Incorrect integer value: '' for column 'id' at row 1`

```shell
mysql 5以上的版本如果是空值应该要写NULL或者0(int类型),或者:
1. 安装mysql的时候去除默认勾选的enable strict SQL mode
2. 更改mysql中的配置`my.ini`,重启mysql
sql-mode="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
# 修改为
sql-mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"，
```

`ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement`

```shell
# mysql默认对导入导出的目录有权限限制,使用命令行进行导入导出时需在指定目录操作；
# 查询mysql 的secure_file_priv值配置
show global variables like '%secure%';
# 或者更改mysql中的配置`my.ini`,重启mysql
# 空表示无限制,null表示不允许
secure-file-priv=''
```

`mysql时区问题`
> [mysql时区](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)

`ONLY_FULL_GROUP_BY`报错

把`ONLY_FULL_GROUP_BY`从 `sql_mode`中去掉

```sql
-- 进入数据库查询
select @@sql_mode
```

```python
# 填入查询的结果(去掉ONLY_FULL_GROUP_BY),重启mysql
vim /etc/my.cnf
sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
```

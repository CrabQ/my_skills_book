# MySQL高级

## mysql连接管理

```shell
# 通过socket启动
mysql -uroot -p -S /tmp/mysql.sock
```

## 初始化配置

配置文件储存位置

```shell
/etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf
# MySQL启动时,会依次读取以上配置文件,如果有重复选项,会以最后一个文件设置的为准.

# 但是,如果启动时加入了--defaults-file=xxxx时,以上的所有文件都不会读取.
```

## SQL基础应用

常用SQL分类

```shell
DDL:数据定义语言 create alter
DCL:数据控制语言 grant revoke
DML:数据操作语言 insert update delete
DQL:数据查询语言 show select
```

## 执行计划获取及分析

```shell
获取到的是优化器选择完成的,他认为代价最小的执行计划.
作用: 语句执行前,先看执行计划信息,可以有效的防止性能较差的语句带来的性能问题.
如果业务中出现了慢语句，我们也需要借助此命令进行语句的评估，分析优化方案。
```

获取优化器选择后的执行计划

```sql
desc select * from test;
```

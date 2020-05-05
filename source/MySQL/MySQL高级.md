# MySQL高级

## mysql连接管理

```shell
# 通过socket启动
mysql -uroot -p -S /tmp/mysql.sock
```

### 初始化配置

配置文件储存位置

```shell
/etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf
# MySQL启动时,会依次读取以上配置文件
# 以最后一个文件设置的为准
# 如果以--defaults-file=xxxx启动,以上的所有文件都不会读取
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
执行计划获取到的是优化器选择完成的,他认为代价最小的执行计划

作用: 语句执行前,先看执行计划信息,可以有效的防止性能较差的语句带来的性能问题

如果业务中出现了慢语句,也需要借助此命令进行语句的评估,分析优化方案.
```

获取优化器选择后的执行计划

```sql
desc select * from test;
```

## InnoDB存储引擎

优点

```shell
事务(Transaction)
MVCC(Multi-Version Concurrency Control多版本并发控制)
行级锁(Row-level Lock)
ACSR(Auto Crash Safey Recovery)自动的故障安全恢复
支持热备份(Hot Backup)
Replication: Group Commit , GTID (Global Transaction ID) ,多线程(Multi-Threads-SQL )
```

### 存储引擎查看

```shell
SELECT @@default_storage_engine;

# 会话级别
set default_storage_engine=myisam;

# 全局级别(仅影响新会话):
set global default_storage_engine=myisam;

# 重启之后,所有参数均失效.如果要永久生效,写入配置文件
vim /etc/my.cnf
[mysqld]
default_storage_engine=myisam

# 存储引擎是表级别的,每个表创建时可以指定不同的存储引擎,建议统一为innodb.
```

`INFORMATION_SCHEMA`确认每个表的存储引擎

```sql
select table_schema,table_name ,engine from information_schema.tables where table_schema not in ('sys','mysql','information_schema','performance_schema');
```

修改一个表的存储引擎

```shell
alter table t1 engine innodb;
# 此命令我们经常用于进行innodb表的碎片整理

# 批量修改一个库的存储引擎
select concat("alter table zabbix.",table_name," engine tokudb;") from
information_schema.tables where table_schema='zabbix' into outfile '/tmp/tokudb.sql';
```

### InnoDB存储引擎物理存储结构

```shell
ibdata1:系统数据字典信息(统计信息),UNDO表空间等数据
ib_logfile0 ~ ib_logfile1: REDO日志文件,事务日志文件
ibtmp1: 临时表空间磁盘位置,存储临时表
frm:存储表的列信息
ibd:表的数据行和索引
```

### 表空间(Tablespace)

#### 共享表空间

```shell
# show variables like '%extend%';

需要将所有数据存储到同一个表空间中 ,管理比较混乱
5.5版本出现的管理模式,也是默认的管理模式
5.6版本,共享表空间保留,只用来存储数据字典信息,undo,临时表
5.7 版本,临时表被独立出来了
8.0版本,undo也被独立出去了
```

#### 独立表空间

```shell
从5.6,默认表空间不再使用共享表空间,替换为独立表空间.
主要存储的是用户数据
存储特点为:一个表一个ibd文件,存储数据行和索引信息
基本表结构元数据存储:xxx.frm
```

### MySQL的存储引擎日志

```shell
# select @@innodb_file_per_table;

Redo Log: ib_logfile0  ib_logfile1,重做日志

Undo Log: ibdata1 ibdata2(存储在共享表空间中),回滚日志

临时表:ibtmp1,在做join union操作产生临时数据,用完就自动删除
```

### 缓冲区池

```shell
select @@innodb_buffer_pool_size;
# 一般建议最多是物理内存的 75-80%
```

### innodb_flush_log_at_trx_commit(双一标准之一)

```shell
select @@innodb_flush_log_at_trx_commit;

# 主要控制了innodb将log buffer中的数据写入日志文件并flush磁盘的时间点,分别为0,1,2
# 1 每次事物的提交都会引起日志文件写入,flush磁盘的操作,确保了事务的ACID;flush到操作系统的文件系统缓存,fsync到物理磁盘
# 0 表示当事务提交时,不做日志写入操作,而是每秒钟将log buffer中的数据写入文件系统缓存并且秒fsync磁盘一次
# 2 每次事务提交引起写入文件系统缓存,但每秒钟完成一次fsync磁盘操作
```

### Innodb_flush_method=(O_DIRECT, fdatasync)

```shell
控制的是log buffer和data buffer,刷写磁盘的时候是否经过文件系统缓存
O_DIRECT 数据缓冲区写磁盘,不走OS buffer
O_DSYNC 日志缓冲区写磁盘,不走OS buffer
fsync 日志和数据缓冲区写磁盘,都走OS buffer

最高安全模式
innodb_flush_log_at_trx_commit=1
Innodb_flush_method=O_DIRECT
最高性能:
innodb_flush_log_at_trx_commit=0
Innodb_flush_method=fsync
```

### 事务的生命周期

自动提交策略

```shell
select @@autocommit;
```

### 一些定义

```shell
ibd 存储 数据行和索引
buffer pool 缓冲区池,数据和索引的缓冲
LSN  日志序列号
WAL  write ahead log 日志优先写的方式实现持久化
脏页 内存脏页,内存中发生了修改,没写入到磁盘之前,我们把内存页称之为脏页
CKPT Checkpoint,检查点,就是将脏页刷写到磁盘的动作
TXID 事务号,InnoDB会为每一个事务生成一个事务号,伴随着整个事务
```

### redo log

```shell
redo的日志文件:iblogfile0 iblogfile1
redo log buffer redo内存区域
redo的buffer 数据页的变化信息+数据页当时的LSN号
```

#### redo的刷新策略

```shell
commit;
刷新当前事务的redo buffer到磁盘
还会顺便将一部分redo buffer中没有提交的事务日志也刷新到磁盘
```

### MySQL CSR: 前滚

```shell
MySQL 在启动时,必须保证redo日志文件和数据文件LSN必须一致, 如果不一致就会触发CSR,最终保证一致

一个事务,begin;update;commit

1. 在begin ,会立即分配一个TXID=tx_01

2. update时,会将需要修改的数据页(dp_01,LSN=101),加载到data buffer中

3. DBWR线程,会进行dp_01数据页修改更新,并更新LSN=102

4. LOGBWR日志写线程,会将dp_01数据页的变化+LSN+TXID存储到redobuffer

5. 执行commit时,LGWR日志写线程会将redobuffer信息写入redolog日志文件中
基于WAL原则,在日志完全写入磁盘后,commit命令才执行成功,(会将此日志打上commit标记)

6. 假如此时宕机,内存脏页没有来得及写入磁盘,内存数据全部丢失

7. MySQL再次重启时,必须要redolog和磁盘数据页的LSN是一致的
但是,此时dp_01,TXID=tx_01磁盘是LSN=101,dp_01,TXID=tx_01,redolog中LSN=102

MySQL此时无法正常启动,MySQL触发CSR.在内存追平LSN号,触发ckpt,将内存数据页更新到磁盘,从而保证磁盘数据页和redolog LSN一值.这时MySQL正长启动

以上的工作过程,我们把它称之为基于REDO的"前滚操作"
```

### undo 回滚日志

```shell
在rollback时,将数据恢复到修改之前的状态

undo提供快照技术,保存事务修改之前的数据状态.保证了MVCC,隔离性,mysqldump的热备
```

## 日志管理

### 错误日志(log_error)

```shell
记录启动,关闭,日常运行过程中,状态信息,警告,错误

默认就是开启的

show variables like 'log_error';

# 设定
vim /etc/my.cnf
log_error=/var/log/mysql.log
log_timestamps=system
```

### binlog(binary logs):二进制日志

```sql
-- 备份恢复, 主从环境必须依赖二进制日志

-- MySQL默认是没有开启二进制日志的

-- 开关
select @@log_bin;

-- 日志路径及名字
select @@log_bin_basename;

-- 服务ID号
select @@server_id;

-- 二进制日志格式
select @@binlog_format;

双一标准之二
select @@sync_binlog;
```

### binlog内容

```shell
binlog是SQL层的功能.记录的是变更SQL语句,不记录查询语句

记录SQL语句种类
DDL: 原封不动的记录当前DDL(statement语句方式)
DCL: 原封不动的记录当前DCL(statement语句方式)
DML: 只记录已经提交的事务DML
```

DML三种记录方式

```shell
binlog_format(binlog的记录格式)参数影响
statement(5.6默认)SBR(statement based replication): 语句模式原封不动的记录当前DML
ROW(5.7 默认值) RBR(ROW based replication): 记录数据行的变化(用户看不懂,需要工具分析)
mixed(混合)MBR(mixed based replication)模式 : 以上两种模式的混合

SBR与RBR模式的对比
STATEMENT: 可读性较高,日志量少,但是不够严谨
ROW      : 可读性很低,日志量大,足够严谨

建议使用row记录模式
```

### event

```shell
二进制日志的最小记录单元
对于DDL,DCL,一个语句就是一个event
对于DML语句来讲:只记录已提交的事务
```

#### event的组成

```shell
三部分构成:
(1) 事件的开始标识
(2) 事件内容
(3) 事件的结束标识
Position:
开始标识: at 194
结束标识: end_log_pos 254
194,254: 某个事件在binlog中的相对位置号
```

查看日志的开启情况

```sql
show variables like '%log_bin%';

-- 查看一共多少个binlog
show binary logs;

-- 查看mysql正在使用的日志文件
show master status;
```

日志内容查看

```sql
show binlog events in 'mysql-bin.000003';
```

基于Position号进行日志截取

```shell
mysqlbinlog --start-position=219 --stop-position=1347 /data/binlog/mysql-bin.000003 >/tmp/bin.sql

# mysql内
set sql_Log_bin=0;
source /tmp/bin.sql
set sql_log_bin=1;
```

binlog日志的GTID新特性

```shell
Global Transaction ID
是对于一个已提交事务的编号,并且是一个全局唯一的编号

vim /etc/my.cnf
# 启用gtid类型
gtid-mode=on
# 强制GTID的一致性
enforce-gtid-consistency=true
# slave更新是否记入日志
log-slave-updates=1
```

基于GTID进行查看binlog

```shell
具备GTID后,截取查看某些事务日志
--include-gtids
--exclude-gtids
mysqlbinlog --include-gtids='dff98809-55c3-11e9-a58b-000c2928f5dd:1-6' --exclude-gtids='dff98809-55c3-11e9-a58b-000c2928f5dd:4'  /data/binlog/mysql-bin.000004
```

GTID的幂等性

```shell
开启GTID后,MySQL恢复Binlog时,重复GTID的事务不会再执行了

--skip-gtids
mysqlbinlog --skip-gtids --include-gtids='3ca79ab5-3e4d-11e9-a709-000c293b577e:6-7' /data/binlog/mysql-bin.000036 >/backup/bin.sql

set sql_log_bin=0;
source /tmp/binlog.sql
set sql_log_bin=1;

```

#### 二进制日志其他操作

自动清理日志

```shell
show variables like '%expire%';

自动清理时间按照全备周期+1
set global expire_logs_days=8;

# 永久生效
my.cnf
expire_logs_days=15;
# 至少保留两个全备周期+1的binlog
```

手工清理

```shell
PURGE BINARY LOGS BEFORE now() - INTERVAL 3 day;
PURGE BINARY LOGS TO 'mysql-bin.000010';
注意:不要手工 rm binlog文件
1. my.cnf binlog关闭掉,启动数据库
2.把数据库关闭,开启binlog,启动数据库
删除所有binlog,并从000001开始重新记录日志
```

日志滚动

```shell
flush logs;
重启mysql也会自动滚动一个新的
日志文件达到1G大小(max_binlog_size)
备份时,加入参数也可以自动滚动
```

### slow_log 慢日志

```shell
# 记录慢SQL语句的日志,定位低效SQL语句的工具日志

# vim /etc/my.cnf
# 开关
slow_query_log=1
# 文件位置及名字
slow_query_log_file=/data/mysql/slow.log
# 设定慢查询时间
long_query_time=0.1
# 没走索引的语句也记录
log_queries_not_using_indexes
```

mysqldumpslow 分析慢日志

```shell
mysqldumpslow -s c -t 10 /data/mysql/slow.log
```

## 备份恢复

备份类型

```shell
热备
在数据库正常业务时,备份数据,并且能够一致性恢复(只能是innodb)
对业务影响非常小

温备
锁表备份,只能查询不能修改(myisam)
影响到写入操作

冷备
关闭数据库业务,数据库没有任何变更的情况下,进行备份数据.
业务停止
```

备份方式及工具

```shell
逻辑备份工具
mysqldump
mysqlbinlog

物理备份工具
基于磁盘数据文件备份
xtrabackup(XBK) :percona 第三方
MySQL Enterprise Backup(MEB)
```

mysqldump (MDP)

```shell
优点:
不需要下载安装
备份出来的是SQL,文本格式,可读性高,便于备份处理
压缩比较高,节省备份的磁盘空间

缺点:
依赖于数据库引擎,需要从磁盘把数据读出
然后转换成SQL进行转储,比较耗费资源,数据量大的话效率较低

建议:
100G以内的数据量级,可以使用mysqldump
超过TB以上,我们也可能选择的是mysqldump,配合分布式的系统
```

xtrabackup(XBK)

```shell
优点:
类似于直接cp数据文件,不需要管逻辑结构,相对来说性能较高
缺点:

可读性差
压缩比低,需要更多磁盘空间

建议:
>100G<TB
```

备份策略

```shell
备份方式:
全备:全库备份,备份所有数据
增量:备份变化的数据

逻辑备份=mysqldump+mysqlbinlog
物理备份=xtrabackup_full+xtrabackup_incr+binlog或者xtrabackup_full+binlog

备份周期:
根据数据量设计备份周期
比如:周日全备,周1-周6增量
```

### mysqldump(逻辑备份的客户端工具)

```shell
# -A 全备参数

# -B db1 db2 db3 备份多个单库

# 特殊参数使用(必须要加)

# -R             备份存储过程及函数
# --triggers     备份触发器
# -E             备份事件
# -F             在备份开始时,刷新一个新binlog日志

# --master-data=2
# 以注释的形式,保存备份开始时间点的binlog的状态信息
# 在备份时,会自动记录,二进制日志文件名和位置号
      # 0 默认值
      # 1  以change master to命令形式,可以用作主从复制
      # 2  以注释的形式记录,备份时刻的文件名+postion号
# 自动锁表
# 如果配合--single-transaction,只对非InnoDB表进行锁表备份,InnoDB表进行热备,实际上是实现快照备份.

# --single-transaction
# innodb 存储引擎开启热备(快照备份)功能
# --master-data可以自动加锁
# 不加--single-transaction ,启动所有表的温备份,所有表都锁定
# 加上--single-transaction ,对innodb进行快照备份,对非innodb表可以实现自动锁表功能

# --set-gtid-purged=auto
# --set-gtid-purged=OFF,可以使用在日常备份参数中.
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
# on:在构建主从复制环境时需要的参数配置
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=ON >/data/backup/full.sql

# 备份必加参数
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
```

压缩备份并添加时间戳

```shell
例子:
mysqldump -uroot -p123 -A  -R  --triggers --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz
mysqldump -uroot -p123 -A  -R  --triggers --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F-%T).sql.gz

mysqldump备份的恢复方式(在生产中恢复要谨慎,恢复会删除重复的表)
set sql_log_bin=0;
source /backup/full_2018-06-28.sql
```

## 主从复制

```shell
基于二进制日志复制的
主库的修改操作会记录二进制日志
从库会请求新的二进制日志并回放,最终达到主从数据同步
```

主从复制核心功能

```shell
辅助备份,处理物理损坏
扩展新型的架构:高可用,高性能,分布式架构等
```

主从复制前提

```shell
两台以上mysql实例 ,server_id,server_uuid不同
主库开启二进制日志
专用的复制用户
保证主从开启之前的某个时间点,从库数据是和主库一致(补课)
告知从库,复制user,passwd,IP port,以及复制起点(change master to)
线程(三个):Dump thread  IO thread  SQL thread 开启(start slave)
```

### 主从复制原理

```shell
1. change master to 时,ip port user password binlog position写入到master.info进行记录
2. start slave 时,从库会启动IO线程和SQL线程
3. IO_T,读取master.info信息,获取主库信息连接主库
4. 主库会生成一个准备binlog DUMP线程,来响应从库
5. IO_T根据master.info记录的binlog文件名和position号,请求主库DUMP最新日志
6. DUMP线程检查主库的binlog日志,如果有新的,TP(传送)给从从库的IO_T
7. IO_T将收到的日志存储到了TCP/IP 缓存,立即返回ACK给主库 ,主库工作完成
8. IO_T将缓存中的数据,存储到relay-log日志文件,更新master.info文件binlog文件名和postion,IO_T工作完成
9. SQL_T读取relay-log.info文件,获取到上次执行到的relay-log的位置,作为起点,回放relay-log
10. SQL_T回放完成之后,会更新relay-log.info文件.
11. relay-log会有自动清理的功能.

其中:
主库一旦有新的日志生成,会发送"信号"给binlog dump ,IO线程再请求
```

### 主从复制docker搭建实操

[Centos7下MySQL主从复制部署](https://my-skills-book.readthedocs.io/en/latest/Docker/Docker%E5%BA%94%E7%94%A8%E9%83%A8%E7%BD%B2.html#centos8mysql)

### 主从复制故障处理

```sql
-- IO线程相关

-- 主库查看线程
show full processlist;

-- 从库查看主从复制状态
show slave status \G;

-- 故障处理: 主库连接不上
stop  slave
reset slave all
change master to
start slave

-- 故障处理: 二进制日志位置点不对
-- 重新搭建主从

-- SQL线程相关
-- 主要原因:从库数据修改,与主库不对应(比如自行创建数据库与主库中的冲突)
-- 设置从库只读?
show variables like '%read_only%';
```

### 主从延时

```shell
外在因素: 网络,主从硬件差异较大,版本差异,参数因素

主库
二进制日志写入不及时
主库发生了大事务,由于是串行传送,会产生阻塞后续的事务
大事务拆成多个小事务,可以有效的减少主从延时

从库
从库默认情况下只有一个SQL,只能串行回放事务SQL
```

### 延时从库

```sql
-- 人为配置从库和主库延时N小时

-- SQL线程延时:数据已写入relaylog,SQL线程"慢点"运行

CHANGE MASTER TO MASTER_DELAY = 300;

-- 延时从库状态下主库故障恢复思路
-- 主库误删除
-- 停从库SQL线程
-- 截取relaylog,起点:停止SQL线程时,relay最后应用位置. 终点:误删除之前的position(GTID)
-- 恢复截取的日志到从库
-- 从库身份解除,替代主库工作
```

### 过滤复制

```sql
-- 主库白黑名单
show master status\G;
-- Binlog_Do_DB
-- Binlog_Ignore_DB

-- 从库白黑名单
show slave status\G;
-- Replicate_Do_DB:
-- Replicate_Ignore_DB:
```

### GTID复制

```sql
-- 使用GTID构建主从
change master to
master_host='10.0.0.51',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;

start slave;

-- 在主从复制环境中,主库事务在全局由唯一GTID记录,更方便Failover
-- change master to不再需要binlog文件名和position号,MASTER_AUTO_POSITION=1;
-- 在复制过程中,从库不再依赖master.info文件,直接读取最后一个relaylog的GTID号
-- mysqldump备份时,--set-gtid-purged=auto参数默认会将备份中包含的事务操作告知从库,让从库从下一个GTID开始请求binlog
-- SET @@GLOBAL.GTID_PURGED='8c49d7ec-7e78-11e8-9638-000c29ca725d:1'
```

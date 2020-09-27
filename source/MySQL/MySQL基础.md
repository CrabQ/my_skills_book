# mysql基础

## mysqld处理sql过程

![mysqld处理sql过程.png](.assets/mysqld处理sql过程.png)

## mysql逻辑存储结构

```shell
库 表 列(字段) 数据行(记录)

表属性 列属性
```

## mysql物理存储结构

```shell
myisam
    user.frm 存储表结构(列, 列属性)
    user.MYD 存储数据记录
    user.MYI 存储索引

innodb
    time_zone.frm 存储表结构(列, 列属性)
    time_zone.ibd 存储数据记录
    ibdata1       数据字典信息
```

## innodb段,区, 页

```shell
一般情况下(非分区表)
一个表就是一个段
一个段由多个区构成
一个区由64个连续的页(16k)组成, 1M大小
```

## 字符集和校对规则

```shell
# charset
# GBK: 中文2个字符, utf8: 3, utf8mb4: 4
# utf8mb4: 支持emoji

# collation
# utf8mb4其中两个字符集校对规则
# utf8mb4_general_ci 大小写不敏感
# utf8mb4_bin        大小写敏感
```

## 用户和权限管理

### 用户

```sql
-- 用户 用户名@'白名单'

-- 新建用户
create user crab@'10.0.0.%' identified by '123';

-- 8.0之前, 同时新建和授权
grant all on *.* to crab@'10.0.0.%' identified by '123';

-- 查询用户
select user,host from mysql.user;

-- 修改密码
alter user crab@'10.0.0.%' identified by '12345';

-- 删除用户
drop user crab@'10.0.0.%';
```

### 权限

```sql
-- with grant option 是否可以给别人授权
-- grant 权限 on 作用目标 to 用户 identified by 密码 with grant option;

-- 创建一个用户ww, 通过10网段对ww库下的所有表进行select, insert, update, delete
grant select, insert, update, delete on ww.* to ww@'10.0.0.%' identified by '123';

-- 查询权限
show grants for ww@'10.0.0.%';
-- GRANT USAGE ON *.* TO 'ww'@'10.0.0.%'    可登陆
-- GRANT SELECT, INSERT, UPDATE, DELETE ON `ww`.* TO 'ww'@'10.0.0.%'

-- 回收权限
revoke delete on ww.* from 'ww'@'10.0.0.%';
```

## 数据类型

```shell
# 整数
tinyint
int

# 字符串
char(100)       未占满使用空格填充
varchar(100)    255字符内单独申请一个字符长度的空间储存字符长度,超过则申请2个
enum            枚举

# 时间
datetime
timestamp
```

## 结构化语句

常用SQL分类

```shell
DDL 数据定义语言 create alter
DCL 数据控制语言 grant revoke
DML 数据操作语言 insert update delete
DQL 数据查询语言 select show
```

### DDL 数据库定义

```sql
-- 创建数据库
create database if not exists test charset 'utf8mb4';

--查看
show databases;
show databases test;

-- 删除数据库
drop database test;

-- 修改数据库字符集
alter database test charset utf8mb4
```

数据库定义规范

```shell
库名小写
库名不能数字开头
库名不能是数据库内部关键字
必须设置字符集
```

### DDL 表定义

```sql
-- 创建表
--CREATE TABLE [IF NOT EXISTS] tbl_name(
--字段名称 字段类型 [UNSIGNED|ZEROFILL] [NOT NULL] [DEFAULT 默认值] [[PRIMARY] KEY| UNIQUE [KEY]] [AUTO_INCREMENT]
--)ENGINE=INNODB CHARSET=UTF8 AUTO_INCREMENT=1;

-- 表名小写,不能数值开头,不能是保留关键字
-- 选择合适的数据类型和长度
-- 不能为空, not null default, 要有注释
-- 必须设置存储引擎和字符集
-- 主键自增
-- emun只保存字符串类型

create table if not exists user(
    id smallint unsigned primary key auto_increment,
    username varchar(20) not null unique,
    password char(32) not null,
    age tinyint unsigned default 18,
    sex enum('男','女','保密') default '保密',
    email varchar(50) not null,
    addr varchar(200),
    birth year,
    salary float(8,2),
    tel int,
    married tinyint comment '0未婚,非0已婚',
    reg_time int unsigned,
    face char(100) not null default 'default.jpg'
) engine=innodb charset='utf8mb4';

-- 查看表定义
show create table user;

-- 删除表
drop table user;

-- 重命名表
alter table user rename to user1;
rename table user1 to user;

-- 复制表结果
create table testt like test;
```

#### 表结构修改

```sql
-- 添加字段
alter table user add test1 varchar(100) not null after username;

-- 删除字段
alter table user drop test1;

-- 修改字段属性
alter table user modify email varchar(100) not null;

-- 修改字段名称
alter table user change email eml varchar(100) not null;

-- 删除默认值
alter table user alter age drop default;

-- 修改自增长值
alter table user auto_increment=100;

-- 删除主键
alter table user modify id smallint unsigned;
alter table user drop primary key;

-- 添加主键
alter table user add primary key(id);

-- 外键,先添加联合主键,然后添加外键
ALTER TABLE gd_uniprot ADD CONSTRAINT pk_re PRIMARY KEY(disease_id, gene_id);
ALTER TABLE gd_uniprot ADD CONSTRAINT fk_dis FOREIGN KEY(disease_id) REFERENCES disease_uniprot(id);
ALTER TABLE gd_uniprot ADD CONSTRAINT fk_ge FOREIGN KEY(gene_id) REFERENCES gene_primary_uniprot(id);

-- 删除唯一索引
alter table user drop key username;

-- 添加唯一索引
alter table user add unique key(username);

-- 修改表的储存引擎为myisam
alter table user engine=myisam;

-- 在线改表结构
-- pt-osc
```

### DML 插入,更新,删除

```sql
-- 插入数据
create table if not exists user(
    id smallint unsigned primary key auto_increment,
    username varchar(20) not null unique,
    password char(32) not null,
    email varchar(50) not null,
    age tinyint unsigned default 18
) engine=innodb charset='utf8mb4';

insert into user values(1, '1', '1', '1@qq.com', 20);

insert into user set id=102, username='2', password='2', email='2@qq.com';

insert user(username, password, email) VALUES('3','3', '3@qq.com'),
('4','4', '4@qq.com');

-- 将查询结果插入到表中
create table test(
    id tinyint  primary key auto_increment,
    username varchar(20)
);

insert test select id, username from user;


-- 插入数据，唯一键已存在则更新
insert into _cs_disease_map(dis_id, gene_symbol) VALUES('2857', "A1BG")  on DUPLICATE key update source = CONCAT(source, ',abc');

-- 更新数据
update user set age=5;

-- 删除数据
delete from user where id=1;

-- 清空表, 自增值重置, delete * 自增值不变
truncate table user;
```

### DQL 查询

#### 单表

```sql
-- 查询系统参数
select @@version;

-- 查询表中记录age值为NULL
select * from cms_user where age is null;

-- 查询编号在3~10之间的用户
select * from cms_user where id between 3 and 10;

-- 查询proId为1和3的用户
select * from cms_user where proid in (1,3);

-- 查询姓张的用户
select * from cms_user where username like '张%';

-- 查询用户名为3位的用户
select * from cms_user where username like '___';

-- 去重
select DISTINCT gene_symbol FROM _cs_disease_map;

-- 先按照省份分组,再按照性别分组
select group_concat(username),proid,sex from cms_user group by proid, sex;

--COUNT(字段)不统计NULL值
select count(age) from cms_user;

-- 查询编号,性别,用户名详情,组中总人数,组中最大年龄,最小年龄,
-- 平均年龄,以及年龄总和按照性别分组
select id,sex,group_concat(username), count(*),
max(age), min(age), avg(age), sum(age) from cms_user group by sex;

-- 查询编号大于等于4的用户
select id,sex,group_concat(username), count(*),
max(age), min(age), avg(age), sum(age)
from cms_user
where id>=4
group by sex
having count(*)>2 and max(age)>60;

-- 按照年龄升序,id降序排列
select * from cms_user order by age asc, id desc;

-- 实现记录随机
select * from cms_user order by rand();

-- 查询前五条记录
select * from cms_user limit 5;

-- 查询从第二条开始一共五条记录
select * from cms_user limit 2,5;

-- 更新前3条记录，让已有年龄+10
update cms_user set age=age+10 limit 3;

-- 按照id降序排列，更新前3条
update cms_user set age=age+10 order by id desc limit 3;

-- 联合查询
select username from employee union select username from cms_user;

-- union all不会过滤重复数据, union会
select id, username from employee union all select username,sex from cms_user;

-- 语句中查询条件or in 一般用uniion改写
-- select * from city where code='chn' or code = 'usa';
select * from city where code='chn' union all select * from city where code='usa';

-- 正则
-- 查询用户名以t开始的用户
select * from cms_user where username regexp '^t';

-- 查询用户名以g结束的用户
select * from cms_user where username regexp 'g$';

-- concat
update cms_user set email=concat('email_', email);

-- group_concat
select group_concat(name) from cms_user group by dp;

-- TRIM
SELECT CONCAT('_',TRIM(' ABC '),'_'),CONCAT('_',LTRIM(' ABC '),'_'),CONCAT('_',RTRIM(' ABC '),'_');
```

#### 多表连接查询

```sql
-- 内连接
-- 查询cms_user表中id,username,email,sex
-- 查询provinces表proName
-- 条件是cms_user的性别为男的用户
-- 根据proName分组
-- 对分组结果进行筛选,选出组中人数>1的
select u.id,group_concat(u.username),u.email,u.sex, p.proname
from cms_user as u
inner join provinces as p on
p.id=u.proid
where u.sex='男'
group by p.proname
having count(*)>1;

-- 左外连接
select u.id,u.username,u.email,u.sex, p.proname
from cms_user as u
left join provinces as p on
p.id=u.proid;

-- 右外连接
select u.id,u.username,u.email,u.sex, p.proname
from cms_user as u
right join provinces as p on
p.id=u.proid;

-- 子查询
select id,username from employee where depid in (select id from department);

-- exists
select id,username from employee where exists(select id from department where id=4);
select id,username from employee where not exists(select id from department where id=4);

-- 查询获得1等奖学金的学员
select username,score from student where score >=(select level from scholarship where id=1);

-- 查询所有获得奖学金的学员
select username,score from student where score >=any(select level from scholarship);
select username,score from student where score >=some(select level from scholarship);

-- 查询所有学员中获得一等奖学金的学员
select username,score from student where score >=all(select level from scholarship);

-- 查询学员表中没有获得奖学金的学员
select username,score from student where score <all(select level from scholarship);
```

#### 字符串分割

```sql
select SUBSTRING_INDEX(image_true_path, 'dx') from img_overlap_result limit 10;
```

### 元数据

```sql
use information_schema;

-- 显示所有库和表的信息
select table_schema, group_concat(table_name)
from information_schema.tables
group by table_schema;

-- 查询所有innodb引擎的表
select  table_schema, table_name, engine
from information_schema.tables
where engine='innodb';

-- 统计world数据库数据量大小
select table_schema, sum((avg_row_length*table_rows+index_length))/1/24
from information_schema.tables
where table_schema='world';
```

## 索引

索引树高度越低越好, 一般维持在3-4最佳

### Btree索引功能上的分类

```shell
辅助索引
提取索引列的所有值进行排序
将排好序的值均匀存放在叶子节点, 进一步生成枝节点和根节点
在叶子节点中的值, 都会对应存储主键ID

聚集索引
MYSQL会自动选择主键作为聚集索引列, 没有主键则唯一键, 都没有则生成隐藏的
mysql储存数据时, 会按照聚集索引列值的顺序, 有序存储数据行
聚集索引直接将原表数据页作为叶子节点, 然后提取聚集索引列向上生成枝和根
```

### 区别

```shell
表中任何一个列都可以创建辅助索引
一张表中, 聚集索引只能有一个,一般是主键
辅助索引的叶子节点只存储索引列的有序值+聚集索引列值
聚集索引的叶子节点存储的是有序的整行数据
mysql的表数据存储是聚集索引组织表
```

### 辅助索引细分

```shell
单列辅助索引
联合索引(覆盖索引)
唯一索引
```

```sql
-- 查看索引
show index from cms_user;

-- 删除索引
drop index in_id on test4;

-- 创建普通索引
CREATE TABLE test4(
id TINYINT UNSIGNED,
username VARCHAR(20),
INDEX in_id(id),
KEY in_username(username)
);

create index in_id on test4(id);
alter table test4 add index in_id(id);

-- 唯一索引
create unique index in_id on test4(id);

-- 全文索引,innodb也可
create fulltext index full_username on test4(username);

-- 多列索引
create index mul_t1_t2_t3 on test8(test1,test2,test3);

-- 前缀索引, 仅字符串, 前5个字符
alter table city add index idx_dis(district(5));

-- 空间索引,仅myisam
CREATE TABLE test10(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
test GEOMETRY NOT NULL,
SPATIAL INDEX spa_test(test)
)ENGINE=MyISAM;

create spatial index spa_test on test10(test);
```

## 执行计划

```shell
# 执行计划获取的是优化器认为代价最小的执行计划
# 作用: 语句执行前,先看执行计划信息,可以有效的防止性能较差的语句带来的性能问题
# 如果业务中出现了慢语句,也需要借助此命令进行语句的评估,分析优化方案

# desc select * from test;
# explain select * from test;
```

### 执行计划分析

```shell
mysql> mysql> desc select user, host from mysql.user;
+----+-------------+-------+------------+-------+---------------+---------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys | key     | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+---------------+---------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | user  | NULL       | index | NULL          | PRIMARY | 276     | NULL |    3 |   100.00 | Using index |
+----+-------------+-------+------------+-------+---------------+---------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)
```

table 表名
type 类型

```shell
1. 全表扫描    all

# 从左到右, 依次性能最好
2. 索引扫描    index, range, ref, eq_ref, const(system), NULL

index 全索引扫描
# select code from city;

range 索引范围扫描 <>=, between, and, or, in, like
# select * from city where id>20;

ref 辅助索引等值查询
select * from city where code='CHN';

eq_ref 多表连接时, 子表使用主键列或唯一列作为连接
# b.y
# a join b on a.x=b.y

const(system) 主键或者唯一键的等值查询

null 找不到数据

对于辅助索引来书, != 和 not in, 等语句是不走索引的
对于主键索引来书, != 和 not in, 等语句是走的是range

like '%sd%' 不走索引
like 'sd%' 走索引
```

## 字符编码

```sql
-- 查看mysql编码
show variables like '%char%';

-- 只对当前连接有效
set names 'utf8';

-- 查看warning信息
show warnings;

-- 修改编码
alter table cms_user character set 'utf8mb4';

-- 查看会话变量
show session variables;

-- 更改会话变量,仅针对当前会话
set autocommit='off';
set @@session.autocommit='on';

-- 查看全局变量
show global variables;
select @@global.autocommit;

-- 更改全局变量
set global autocommit='on';
```

## 存储过程

```sql
-- 临时变量
use cms;
delimiter $$;
create procedure test1()
begin
declare a int default 10;
select a;
end
$$;
delimiter ;
call test1();
-- 10

-- in:输入参数
use cms;
delimiter $$;
create procedure test_int(in in_int int)
begin
select in_int;
set in_int=10;
select in_int;
end
$$;
delimiter ;
set @in_int=1;
call test_int(@in_int);
-- 1
-- 10

select @in_int;
-- 1

-- out:输出参数
use cms;
delimiter $$;
create procedure test_out(out in_out int)
begin
select in_out;
set in_out=10;
select in_out;
end
$$;
delimiter ;
set @in_out=1;
call test_out(@in_out);
-- null
-- 10

select @in_out;
-- 10

-- inout:输入输出参数
use cms;
delimiter $$;
create procedure test_in_out(inout in_out int)
begin
select in_out;
set in_out=10;
select in_out;
end
$$;
delimiter ;
set @in_out=1;
call test_in_out(@in_out);
-- 1
-- 10

select @in_out;
-- 10

-- 查看数据库下的存储过程
show procedure status where db='cms';

-- 查看存储过程的内容
show create procedure test10;

-- 删除存储过程
drop procedure test_in_out;
```

## 流程控制

```sql
-- if else
use cms
delimiter $$;
create procedure test_if(in age int)
begin
if age>60 then
select '老年人';
elseif age>18 then
select '成年人';
else
select '未成年';
end if;
end
$$;
delimiter ;
set @age=70;
call test_if(@age);

-- case
select id, username, score,
case when score>=90 then '很好'
when score>70 then '不错'
when score>55 then '合格'
else '不合格'
end
from student;

-- ifnull
select ifnull(null, 2);
-- 2
select ifnull(1,2);
-- 1

-- while
use cms;
delimiter $$;
create procedure test_while()
begin
declare i int default 1;
declare s int default 0;
while i<=100 do
set s=s+i;
set i=i+1;
end while;
select s;
end
$$;
delimiter ;
call test_while();
-- 5050


-- 定义条件和处理
delimiter $$;
create procedure test10()
begin
declare continue handler for sqlstate '42S02' set@x=1;
-- 定义条件之后不会报错,继续执行
select * from cms_user1;
select * from cms_user;
end
$$;
delimiter ;
call test10();
```

## 函数

```sql
-- 查看是否开启创建函数功能
show variables like '%fun%';

-- 开启创建函数功能
set global log_bin_trust_function_creators=1;

-- 创建函数
delimiter $$;
create function test_add(a int, b int)
returns int
begin
return a+b;
end
$$;
delimiter ;
select test_add(3,4);

-- 查看函数创建内容
show create function test_add;

-- 查看数据库下的函数
show function status;

-- 删除函数
drop function if exists test_add;
```

## 视图

```sql
create or replace view v_test
as
select * from cms_user where id>3;
select * from v_test;

-- 视图是表的查询结果,表的数据改变,视图的结果也会改变
update cms_user set age=100 where id=4;
select * from v_test;

-- 视图的增删改也会影响表
update v_test set age=83 where id=5;
select * from cms_user;

-- 查看数据库视图列表
select table_schema,table_name from information_schema.views;

-- 查看视图信息
show table status from cms like 'v%';

-- 查看删除视图权限
select drop_priv from mysql.user where user='root';

-- 删除视图
drop view if exists v_test;
```

## 触发器

```sql
-- cms_user表数据更新时,省份表的省份名称更改为user表的相应用户名
delimiter $$;
create trigger tr_test after update
on cms_user for each row
begin
    update provinces set proName=old.username where id=old.id;
end
$$;
delimiter ;

update cms_user set age=10 where id=2;

-- 查看所有触发器
show triggers;

-- 查看触发器
select * from information_schema.triggers where trigger_name='tr_test';

-- 删除触发器
drop trigger tr_test;
```

## 事务

```sql
-- 查看数据库是否支持事务
show engines;

-- 查看Mysql当前默认的存储引擎
show variables like '%engines%';

-- 修改数据库引擎
alter table cms_user engine=myisam;
```

## My ISAM表锁

```sql
-- 共享读锁,当前session可读不可写,不可读其他未锁的表,其他session可读,写的时候会等待释放锁，可以读其他表
lock table cms_user read;
select * from cms_user;
update cms_user set age=10 where id=1;
-- ERROR 1099 (HY000): Table 'cms_user' was locked with a READ lock and can't be updated
select * from cms_admin;
-- ERROR 1100 (HY000): Table 'cms_admin' was not locked with LOCK TABLES
unlock tables;

-- 查看表锁状态
show status like '%lock%';

-- 独占写锁,当前session可读可写,不可读其他未锁的表,其他session等待释放锁之后才可读写，可以读其他表
lock table cms_user write;
select * from cms_user;
update cms_user set age=20 where id=1;
select * from cms_admin;
-- ERROR 1100 (HY000): Table 'cms_admin' was not locked with LOCK TABLES
unlock tables;

-- 并发插入

-- 查看并发插入,0不允许并发插入,1无空洞(无删除的行)可插入,2都允许插入
-- 当前读锁的session获取不到另一个session的插入,释放锁之后才可以获取到
show variables like '%concurrent_insert%';

-- 设置并发插入
set global concurrent_insert=2;
```

## 慢查询

```sql
-- 慢查询
show variables like '%long_query_time%';

-- 查看数据库运行时间
show status like 'uptime';
-- 查看当前select数
show status like 'com_select';
-- 查看当前连接数
show status like 'connections';
show status like 'slow_quries';

-- 查看表的状态
show table status like 'cms_user';
```

## 分区

```sql
show variables like '%part%';
```

## 用户,权限管理

```sql
-- 创建用户,可远程访问
create user abc@'%' identified by 'sdgsdgr'
-- 只能本地访问
create user abc@'localhost' identified by 'sdgsdgr';

-- 修改用户密码
alter use abc@'%' identified by '456';

-- 删除用户
drop user abc@'%';

-- 用户授权,同时创建用户(5.6版本)
GRANT ALL PRIVILEGES ON gene_disease.* TO bmnars@"%" IDENTIFIED BY "vi93nwYV";

-- with grant option 超级管理员才具备的,给别的用户授权的功能
-- 8.0版本的授权,必须先创建用户
GRANT ALL PRIVILEGES ON my_blog.* TO 7JTZsiuI@'localhost';
```

本地管理员用户密码忘记,重置密码操作

```sql
[root@db01 ~]# mysqld_safe --skip-grant-tables --skip-networking &
mysql> flush privileges;
mysql>  alter user root@'localhost' identified by '123456';
[root@db01 ~]# pkill mysqld
[root@db01 ~]# systemctl start  mysqld
```

## show语句

```sql
-- 查看用户的权限信息
show  grants for  root@'localhost'

-- 查看字符集
show charset；

-- 查看校对规则
show collation

-- 查看数据库连接情况
show processlist;

-- 表的索引情况
show index from tables;

-- 模糊查询数据库某些状态
SHOW STATUS LIKE '%lock%';
;
-- 查看支持的所有的存储引擎
show engines;

-- 查看InnoDB引擎相关的状态信息
show engine innodb status\G;
```

## 日期时间函数

```sql
-- 返回当前日期和时间
select now();

-- 返回当前日期
select curdate();

-- 返回当前时间
select curtime();

-- 日期转换为天数
select to_days('1995-08-01');

-- 查询年龄
select (to_days(curdate())-to_days('1995-08-01'))/365;

-- 查询月份
select month(curdate());

-- 查询月份名字
select monthname(curdate());

-- 返回星期几,0表示星期一
select weekday(curdate());

-- 返回星期几的名称
select dayname(curdate());

-- 返回一周内的第几天,1是星期天
select dayofweek(curdate());

-- 星期一
select dayofweek('2020-01-06');
-- 2

-- 一年内的第几个星期
select week(curdate());
```

### 日期格式化

```sql
-- 2019-02-22 17:06:12
date_format(receiving_time, '%Y-%m')
-- 2019-02
```

### 排名

```sql
-- 按各科成绩进行行排序,并显示排名,Score重复时合并名次
select *, dense_rank() over (partition by cid order by score desc) as 排名 from sc;
-- row_number() 1 2 3 4
-- dense_rank() 1 2 2 3
-- rank() 1 2 2 4
```

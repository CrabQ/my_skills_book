
# Mysql基础语法

## 数据库与表

```sql
-- 创建数据库
create database if not exists test default character set 'utf8mb4';

-- 删除数据库
drop database test;

-- 创建表
--CREATE TABLE [IF NOT EXISTS] tbl_name(
--字段名称 字段类型 [UNSIGNED|ZEROFILL] [NOT NULL] [DEFAULT 默认值] [[PRIMARY] KEY| UNIQUE [KEY]] [AUTO_INCREMENT]
--)ENGINE=INNODB CHARSET=UTF8 AUTO_INCREMENT=1;

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

```

## 表结构

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

-- 删除唯一索引
alter table user drop key username;

-- 添加唯一索引
alter table user add unique key(username);

-- 修改表的储存引擎为myisam
alter table user engine=myisam;

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

insert user(username, password, email) VALUEs('3','3', '3@qq.com'),
('4','4', '4@qq.com');

-- 将查询结果插入到表中
create table test(
    id tinyint  primary key auto_increment,
    username varchar(20)
);

insert test select id, username from user;

-- 更新数据
update user set age=5;

-- 删除数据
delete from user where id=1;

-- 清空表
truncate table user;
```

## 查询

```sql
CREATE DATABASE IF NOT EXISTS cms DEFAULT CHARACTER SET utf8;
USE cms;
-- 管理员表cms_admin
CREATE TABLE cms_admin(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
username VARCHAR(20) NOT NULL UNIQUE,
password CHAR(32) NOT NULL,
email VARCHAR(50) NOT NULL DEFAULT 'admin@qq.com',
role ENUM('普通管理员','超级管理员') DEFAULT '普通管理员'
);
INSERT cms_admin(username,password,email,role) VALUES('admin','admin','admin@qq.com',2);

INSERT cms_admin(username,password) VALUES('king','king'),

('麦子','maizi'),

('queen','queen'),

('test','test');

-- 创建分类表cms_cate
CREATE TABLE cms_cate(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
cateName VARCHAR(50) NOT NULL UNIQUE,
cateDesc VARCHAR(200) NOT NULL DEFAULT ''
);

INSERT cms_cate(cateName,cateDesc) VALUES('国内新闻','聚焦当今最热的国内新闻'),
('国际新闻','聚焦当今最热的国际新闻'),
('体育新闻','聚焦当今最热的体育新闻'),
('军事新闻','聚焦当今最热的军事新闻'),
('教育新闻','聚焦当今最热的教育新闻');

-- 创建新闻表cms_news
CREATE TABLE cms_news(
id INT UNSIGNED AUTO_INCREMENT KEY,
title VARCHAR(50) NOT NULL UNIQUE,
content TEXT,
clickNum INT UNSIGNED DEFAULT 0,
pubTime INT UNSIGNED,
cId TINYINT UNSIGNED NOT NULL COMMENT '新闻所属分类,对应分类表中的id',
aId TINYINT UNSIGNED NOT NULL COMMENT '哪个管理员发布的,对应管理员表中的id'
);
INSERT cms_news(title,content,pubTime,cId,aId) VALUES('亚航客机失联搜救尚无线索 未发求救信号','马来西亚亚洲航空公司一架搭载155名乘客的客机28日早晨从印度尼西亚飞往新加坡途中与空中交通控制塔台失去联系,下落不明。',1419818808,1,2),
('北京新开通四条地铁线路 迎接首位客人','12月28日凌晨,随着北京地铁6号线二期、7号线、15号线西段、14号线东段的开通试运营,北京的轨道交通运营里程将再添62公里,共计达到527公里。当日凌晨5时许,北京地铁7号线瓷器口换乘站迎来新线开通的第一位乘客。',1419818108,2,1),
('考研政治题多次出现习近平讲话内容','新京报讯 （记者许路阳 (微博)）APEC反腐宣言、国家公祭日、依法治国……昨日,全国硕士研究生招生考试进行首日初试,其中,思想政治理论考题多次提及时事热点,并且多次出现习近平在不同场合的讲话内容。',1419818208,3,2),
('深度-曾雪麟：佩兰别重蹈卡马乔覆辙','12月25日是前国足主帅曾雪麟的85岁大寿,恰逢圣诞节,患有尿毒症老爷子带着圣诞帽度过了自己的生日。此前,腾讯记者曾专访曾雪麟,尽管已经退休多年,但老爷子仍旧关心着中国足球,为国足揪心,对于国足近几位的教练,他只欣赏高洪波。对即将征战亚洲杯的国足,老爷子希望佩兰不要重蹈卡马乔的覆辙',1419818308,2,4),
('国产JAD-1手枪枪架投入使用 手枪可变"冲锋枪"','日前,JAD-1型多功能手枪枪架通过公安部特种警用装备质量监督检验中心检验,正式投入生产使用。此款多功能枪架由京安盾(北京)警用装备有限公司开发研制,期间经广东省江门市公安特警支队试用,获得好评。',1419818408,4,4),
('麦子学院荣获新浪教育大奖','麦子学院最大的职业IT教育平台,获奖了',1419818508,1,5),
('麦子学院荣获腾讯教育大奖','麦子学院最大的职业IT教育平台,获奖了',1419818608,1,5),
('麦子学院新课上线','麦子学院PHP课程马上上线了,小伙伴快来报名学习哈',1419818708,1,5);

-- 创建身份表 provinces
CREATE TABLE provinces(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
proName VARCHAR(10) NOT NULL UNIQUE
);
INSERT provinces(proName) VALUES('北京'),
('上海'),
('深圳'),
('广州'),
('重庆');

-- 创建用户表cms_user
CREATE TABLE cms_user(
id INT UNSIGNED AUTO_INCREMENT KEY,
username VARCHAR(20) NOT NULL UNIQUE,
password CHAR(32) NOT NULL,
email VARCHAR(50) NOT NULL DEFAULT 'user@qq.com',
regTime INT UNSIGNED NOT NULL,
face VARCHAR(100) NOT NULL DEFAULT 'user.jpg',
proId TINYINT UNSIGNED NOT NULL COMMENT '用户所属省份'
);

INSERT cms_user(username,password,regTime,proId)

VALUES('张三','zhangsan',1419811708,1),
('张三丰','zhangsanfeng',1419812708,2),
('章子怡','zhangsan',1419813708,3),
('long','long',1419814708,4),
('ring','ring',1419815708,2),
('queen','queen',1419861708,3),
('king','king',1419817708,5),
('blek','blek',1419818708,1),
('rose','rose',1419821708,2),
('lily','lily',1419831708,2),
('john','john',1419841708,2);

-- 添加age字段
ALTER TABLE cms_user ADD age TINYINT UNSIGNED DEFAULT 18;

INSERT cms_user(username,password,regTime,proId,age)

VALUES('test1','test1',1419811708,1,NULL);

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

-- 向用户表中添加性别字段
ALTER TABLE cms_user ADD sex ENUM('男','女','保密');
UPDATE cms_user SET sex='男' WHERE id IN(1,3,5,7,9);
UPDATE cms_user SET sex='女' WHERE id IN(2,4,6,8,10);
UPDATE cms_user SET sex='保密' WHERE id IN(12,11);

-- 按照用户所属省份分组proId
select group_concat(username),proid from cms_user group by proid;
-- 先按照省份分组,再按照性别分组
select group_concat(username),proid,sex from cms_user group by proid, sex;

UPDATE cms_user SET age=11 WHERE id=1;
UPDATE cms_user SET age=21 WHERE id=2;
UPDATE cms_user SET age=33 WHERE id=3;
UPDATE cms_user SET age=44 WHERE id=4;
UPDATE cms_user SET age=25 WHERE id=5;
UPDATE cms_user SET age=77 WHERE id=6;
UPDATE cms_user SET age=56 WHERE id=7;
UPDATE cms_user SET age=88 WHERE id=8;
UPDATE cms_user SET age=12 WHERE id=9;
UPDATE cms_user SET age=32 WHERE id=10;
UPDATE cms_user SET age=65 WHERE id=11;

--COUNT(字段)不统计NULL值
select count(age) from cms_user;

-- 查询编号,性别,用户名详情,组中总人数,组中最大年龄,最小年龄,
-- 平均年龄,以及年龄总和按照性别分组
select id,sex,group_concat(username), count(*),
max(age), min(age), avg(age), sum(age) from cms_user group by sex;

-- 查询组中人数大于2的
select id,sex,group_concat(username), count(*),
max(age), min(age), avg(age), sum(age)
from cms_user
group by sex
having count(*)>2 and max(age)>60
;


-- 查询编号大于等于4的用户
select id,sex,group_concat(username), count(*),
max(age), min(age), avg(age), sum(age)
from cms_user
where id>=4
group by sex
having count(*)>2 and max(age)>60;

-- 按照年龄升序,id降序排列
UPDATE cms_user SET age=12 WHERE id=5;
select * from cms_user order by age asc, id desc;

-- 实现记录随机
select * from cms_user order by rand();

-- 查询前五条记录
select * from cms_user limit 5;

-- 查询从第二条开始一共五条记录
select * from cms_user limit 2,5;

-- 更新用户名为4位的用户，让其已有年龄-3

update cms_user set age=age-3 where username like '____';

-- 更新前3条记录，让已有年龄+10
update cms_user set age=age+10 limit 3;

-- 按照id降序排列，更新前3条
update cms_user set age=age+10 order by id desc limit 3;


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

-- 插入错误的数据
INSERT cms_user(username,password,regTime,proId)
VALUES('TEST2','TEST2','1381203974',20);

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


-- 创建部门表department(主表)
CREATE TABLE IF NOT EXISTS department(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
depName VARCHAR(20) NOT NULL UNIQUE
)ENGINE=INNODB;

INSERT department(depName) VALUES('教学部'),
('市场部'),
('运营部'),
('督导部');

-- 创建员工表employee(子表)
-- id ,username ,depId
CREATE TABLE IF NOT EXISTS employee(
id SMALLINT UNSIGNED AUTO_INCREMENT KEY,
username VARCHAR(20) NOT NULL UNIQUE,
depId TINYINT UNSIGNED,
FOREIGN KEY(depId) REFERENCES department(id) ON DELETE SET NULL ON UPDATE SET NULL
)ENGINE=INNODB;

INSERT employee(username,depId) VALUES('king',1),
('queen',2),
('张三',3),
('李四',4),
('王五',1);

-- 联合查询
select username from employee union select username from cms_user;
-- union all不会过滤重复数据
select id, username from employee union all select username,sex from cms_user;

-- 子查询
select id,username from employee where depid in (select id from department);

-- exists
select id,username from employee where exists(select id from department where id=4);
select id,username from employee where not exists(select id from department where id=4);

--　创建学员表student
-- id username score
CREATE TABLE IF NOT EXISTS student(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
username VARCHAR(20)  NOT NULL UNIQUE,
score TINYINT UNSIGNED
);

INSERT student(username,score) VALUES('king',95),
('king1',35),
('king2',45),
('king3',55),
('king4',65),
('king5',75),
('king6',80),
('king7',90),
('king8',25);
-- 创建奖学金scholarship
-- id ,level

CREATE TABLE IF NOT EXISTS scholarship(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
level TINYINT UNSIGNED
);
INSERT scholarship(level) VALUES(90),(80),(70);

-- 查询获得1等奖学金的学员
select username,score from student where score >=(select level from scholarship where id=1);

-- 查询所有获得奖学金的学员
select username,score from student where score >=any(select level from scholarship);

select username,score from student where score >=some(select level from scholarship);

-- 查询所有学员中获得一等奖学金的学员
select username,score from student where score >=all(select level from scholarship);

-- 查询学员表中没有获得奖学金的学员
select username,score from student where score <all(select level from scholarship);


-- 正则
CREATE TABLE test1 (
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
num TINYINT UNSIGNED
);
INSERT test1(id,num)

SELECT id,score FROM student;


CREATE TABLE test2 (
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
num TINYINT UNSIGNED
)SELECT id,score FROM student;

CREATE TABLE test3 (
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
score TINYINT UNSIGNED
)SELECT id,score FROM student;

-- 查询用户名以t开始的用户
select * from cms_user where username regexp '^t';

-- 查询用户名以g结束的用户
select * from cms_user where username regexp 'g$';

-- concat
update cms_user set email=concat('email_', email);

-- TRIM
SELECT CONCAT('_',TRIM(' ABC '),'_'),CONCAT('_',LTRIM(' ABC '),'_'),CONCAT('_',RTRIM(' ABC '),'_');

-- case
select id, username, score,
case when score>=90 then '很好'
when score>70 then '不错'
when score>55 then '合格'
else '不合格'
end
from student;
```

## 索引

```sql
-- 创建普通索引
CREATE TABLE test4(
id TINYINT UNSIGNED,
username VARCHAR(20),
INDEX in_id(id),
KEY in_username(username)
);

drop index in_id on test4;
create index in_id on test4(id);
alter table test4 add index in_id(id);

-- 唯一索引
create unique index in_id on test4(id);
drop index in_id on test4;

-- 全文索引,innodb也可
create fulltext index full_username on test4(username);
drop index full_username on test4;

-- 单列索引
-- 多列索引
CREATE TABLE test8(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
test1 VARCHAR(20) NOT NULL,
test2 VARCHAR(20) NOT NULL,
test3 VARCHAR(20) NOT NULL,
test4 VARCHAR(20) NOT NULL,
INDEX mul_t1_t2_t3(test1,test2,test3)
);

drop index mul_t1_t2_t3 on test8;
create index mul_t1_t2_t3 on test8(test1,test2,test3);

-- 空间索引,仅myisam
CREATE TABLE test10(
id TINYINT UNSIGNED AUTO_INCREMENT KEY,
test GEOMETRY NOT NULL,
SPATIAL INDEX spa_test(test)
)ENGINE=MyISAM;

drop index spa_test on test10;
create spatial index spa_test on test10(test);
```

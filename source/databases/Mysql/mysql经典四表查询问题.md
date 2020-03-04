# MysQL经典四表查询问题

## 初始化数据库

```sql
create database student default character set 'utf8mb4';
use student;

-- 学生表 学生编号,姓名,出生年月,性别
-- student(sid, sname, sage, ssex)
create table student(
sid int primary key auto_increment,
sname varchar(20),
sage date,
ssex enum('男','女')
)engine=innodb default charset='utf8mb4';

-- 教师表 教师编号,姓名
-- teacher(tid, tname)
create table teacher(
tid int primary key auto_increment,
tname varchar(20)
)engine=innodb default charset='utf8mb4';

-- 课程表 课程编号, 课程名称, 教师编号
-- course(cid, cname, tid)
create table course(
cid int primary key auto_increment,
cname varchar(20),
tid int,
foreign key(tid) references teacher(tid)
)engine=innodb default charset='utf8mb4';

-- 成绩表 学生编号,课程编号, 分数
-- sc(sid, cid, score)
create table sc(
sid int,
cid int,
score int,
foreign key(sid) references student(sid),
foreign key(cid) references course(cid)
)engine=innodb default charset='utf8mb4';
```

## 插入数据

```sql
insert into student values('01' , '赵雷' , '1990-01-01' , '男');
insert into student values('02' , '钱电' , '1990-12-21' , '男');
insert into student values('03' , '孙风' , '1990-05-20' , '男');
insert into student values('04' , '李云' , '1990-08-06' , '男');
insert into student values('05' , '周梅' , '1991-12-01' , '女');
insert into student values('06' , '吴兰' , '1992-03-01' , '女');
insert into student values('07' , '郑竹' , '1989-07-01' , '女');
insert into student values('08' , '王菊' , '1990-01-20' , '女');
insert into teacher values('01' , '张三');
insert into teacher values('02' , '李四');
insert into teacher values('03' , '王五');
insert into course values('01' , '语文' , '02');
insert into course values('02' , '数学' , '01');
insert into course values('03' , '英语' , '03');
insert into sc values('01' , '01' , 80);
insert into sc values('01' , '02' , 90);
insert into sc values('01' , '03' , 99);
insert into sc values('02' , '01' , 70);
insert into sc values('02' , '02' , 60);
insert into sc values('02' , '03' , 80);
insert into sc values('03' , '01' , 80);
insert into sc values('03' , '02' , 80);
insert into sc values('03' , '03' , 80);
insert into sc values('04' , '01' , 50);
insert into sc values('04' , '02' , 30);
insert into sc values('04' , '03' , 20);
insert into sc values('05' , '01' , 76);
insert into sc values('05' , '02' , 87);
insert into sc values('06' , '01' , 31);
insert into sc values('06' , '03' , 34);
insert into sc values('07' , '02' , 89);
insert into sc values('07' , '03' , 98);

```

## 问题

查询"01"课程比"02"课程成绩高的学生的信息及课程分数

```sql
select s.*, sc1.score as '课程01', sc2.score as '课程02'
from student as s
inner join sc as sc1
inner join sc as sc2
on s.sid=sc1.sid
and sc1.sid=sc2.sid
where sc2.score<sc1.score and sc1.cid=1 and sc2.cid=2;
```

查询平均成绩大于等于60分的同学的学生编号和学生姓名和平均成绩

```sql
select s.sid, s.sname, avg(sc.score) as '平均成绩'
from student as s
inner join sc
on s.sid=sc.sid
group by sc.sid
having avg(sc.score)>=60;
```

查询名字中含有"风"字的学生信息

```sql
select * from student where sname like '%风%';
```

查询课程名称为"数学",且分数低于60的学生姓名和分数

```sql
select s.sname, sc.score
from student as s
inner join sc
inner join course as c
on s.sid=sc.sid and c.cid=sc.cid
where sc.score<60 and c.cname='数学';
```

查询所有学生的课程及分数情况

```sql
select s.sname, c.cname, sc.score
from student as s
inner join sc
inner join course as c
on s.sid=sc.sid and c.cid=sc.cid;
```

查询没学过"张三"老师授课的同学的信息

```sql
select *
from student
where sid not in(
select sc.sid
from sc
inner join course as c
inner join teacher as t
on c.cid=sc.cid and t.tid=c.tid
where t.tname='张三'
);
```

查询学过"张三"老师授课的同学的信息

```sql
select s.*
from student as s
inner join sc
inner join course as c
inner join teacher as t
on c.cid=sc.cid and t.tid=c.tid and s.sid=sc.sid
where t.tname='张三';
```

查询学过编号为"01"并且也学过编号为"02"的课程的同学的信息

```sql
select s.*
from student s
inner join sc as sc1
inner join sc as sc2
on s.sid=sc1.sid and sc1.sid=sc2.sid
where sc1.cid=1 and sc2.cid=2;
```

查询学过编号为"01"但是没有学过编号为"02"的课程的同学的信息

```sql
select s.*
from student s
inner join sc as sc
on s.sid=sc.sid
where sc.cid=1 and sc.sid  in(
select sid from sc where cid=2
);
```

查询没有学全所有课程的同学的信息

```sql
select s.*
from student as s
inner join sc
on s.sid=sc.sid
group by s.sname
having count(*) != (select count(*) from course);
```

查询至少有一门课与学号为"01"的同学所学相同的同学的信息

```sql
select s.*
from student as s
inner join sc
on sc.sid=s.sid
where sc.cid in(
select cid from sc where sid=1
) and sc.sid != 1
group by s.sid;
```

查询和"01"号的同学学习的课程完全相同的其他同学的信息

```sql
select s.*, group_concat(sc.cid)
from student as s
inner join sc
on sc.sid=s.sid
where sc.sid != 1
group by sc.sid
having group_concat(sc.cid)=(
    select group_concat(sc.cid) from sc where sc.sid=1 group by sc.sid
);
```

查询没学过"张三"老师讲授的任一门课程的学生姓名

```sql
select sname
from student where sid not in(
select sc.sid
from course as c
inner join teacher as t
inner join sc
on t.tid=c.tid and sc.cid=c.cid
where t.tname='张三'
);
```

查询出只有两门课程的全部学生的学号和姓名

```sql
select s.sid,s.sname
from student as s
inner join sc
on sc.sid=s.sid
group by sc.sid
having count(*)=2;
```

查询1990年出生的学生名单

```sql
select * from student WHERE sage like '%1990%';
```

查询每门课程的平均成绩,结果按平均成绩降序排列,平均成绩相同时,按课程编号升序排列

```sql
select cid, avg(score)
from sc
group by(cid)
order by avg(score) desc, cid asc;
```

查询任何一门课程成绩在70分以上的学生姓名、课程名称和分数

```sql
select s.sname, c.cname, sc.score
from student as s
inner join sc
inner join course as c
on c.cid=sc.cid and sc.sid=s.sid
where sc.score >70;
```

查询平均成绩大于等于85的所有学生的学号、姓名和平均成绩

```sql
select s.sid, s.sname, avg(score)
from student as s
inner join sc
on sc.sid=s.sid
group by(s.sid)
having avg(score)>=85;
```

查询不及格的学生和相应课程

```sql
select s.sname, c.cname, sc.score
from student as s
inner join sc
inner join course as c
on c.cid=sc.cid and sc.sid=s.sid
where sc.score <60;
```

查询课程编号为01且课程成绩在80分以上的学生的学号和姓名

```sql
select s.sid,s.sname, c.cname, sc.score
from student as s
inner join sc
inner join course as c
on c.cid=sc.cid and sc.sid=s.sid
where sc.score>80 and sc.cid=1;
```

求每门课程的学生人数

```sql
select c.cname, count(*)
from course as c
inner join sc
on sc.cid=c.cid
group by(sc.cid);
```

统计每门课程的学生选修人数（超过5人的课程才统计）。要求输出课程号和选修人数,查询结果按人数降序排列,若人数相同,按课程号升序排列

```sql
select c.cid,c.cname, count(*)
from course as c
inner join sc
on sc.cid=c.cid
group by(sc.cid)
having count(*)>5
order by count(*) desc, c.cid asc;
```

检索至少选修两门课程的学生学号

```sql
select s.sid,s.sname
from student as s
inner join sc
on sc.sid=s.sid
group by sc.sid
having count(*)>=2;
```

查询选修了全部课程的学生信息

```sql
select s.*
from student as s
inner join sc
on sc.sid=s.sid
group by sc.sid
having count(*)=(select count(*) from course);
```

查询各学生的年龄

```sql
select s.sname, (to_days(curdate())-to_days(s.sage))/365 as age from student s;
```

查询本月过生日的学生

```sql
select * from student where month(sage)=month(curdate());
```

查询下月过生日的学生

```sql
select * from student where month(sage)=(month(curdate())+1);
```

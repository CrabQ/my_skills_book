# MySQL经典四表查询问题

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

检索"01"课程分数小于 60,按分数降序排列的学生信息

```sql
select s.*
from student as s
inner join sc
on s.sid=sc.sid
where sc.cid=1 and sc.score < 60
order by sc.score desc;
```

按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩

```sql
select s.*, avg_score
from sc as s
left join (
    select sc.sid ,avg(sc.score) as avg_score from sc group by sc.sid
   ) r
on s.sid = r.sid
order by avg_score desc ;
```

查询各科成绩最高分,最低分和平均分,以如下形式显示

课程 ID,课程 name,最高分,最低分,平均分,及格率,中等率,优良率,优秀率

及格为>=60,中等为70-80,优良为80-90,优秀为>=90

要求输出课程号和选修人数,查询结果按人数降序排列,若人数相同,按课程号升序

```sql
select sc.cid, c.cname, max(sc.score), min(sc.score), avg(sc.score),
sum(及格)/count(sc.cid) as 及格率, sum(中等)/count(sc.cid) as 中等率, sum(优良)/count(sc.cid) as 优良率, sum(优秀)/count(sc.cid) as 优秀率
from (
SELECT
    *,
    CASE
      WHEN score >= 60
      THEN 1
      ELSE 0
    END AS 及格,
    CASE
      WHEN score >= 70
      AND score < 80
      THEN 1
      ELSE 0
    END AS 中等,
    CASE
      WHEN score >= 80
      AND score < 90
      THEN 1
      ELSE 0
    END AS 优良,
    CASE
      WHEN score >= 90
      THEN 1
      ELSE 0
    END AS 优秀
  FROM
    sc) sc
inner join course as c
on c.cid=sc.cid
group by sc.cid
order by count(sc.cid) desc, cid asc;
```

按各科成绩进行排序,并显示排名, Score 重复时保留名次空缺

```sql
select *, rank() over (partition by cid order by score desc) as 排名 from sc;
```

按各科成绩进行行排序,并显示排名,Score 重复时合并名次

```sql
select *, dense_rank() over (partition by cid order by score desc) as 排名 from sc;
```

查询学生的总成绩,并进行排名,总分重复时保留名次空缺

```sql
select sid, sum(score) as 总成绩,rank() over (order by sum(score) desc) as 排名
from sc
group by sid;
```

查询学生的总成绩,并进行排名,总分重复时不保留名次空缺

```sql
select sid, sum(score) as 总成绩,dense_rank() over (order by sum(score) desc) as 排名
from sc
group by sid;
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

查询在 SC 表存在成绩的学生信息

```sql
select distinct  s.*
from student as s
inner join sc
on s.sid=sc.sid;
```

查询所有同学的学生编号、学生姓名、选课总数、所有课程的成绩总和

```sql
select  s.sid, s.sname, count(sc.cid), sum(sc.score)
from student as s
inner join sc
on s.sid=sc.sid
group by s.sid;
```

查询同名同性学生名单，并统计同名人数

```sql
select sname, count(sname) from student group by sname having count(*)>2;
```

查询「李」姓老师的数量

```sql
select count(*) from teacher where tname like '李%';
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
on sc.sid=s.sid and c.cid=sc.cid
where c.cname='数学' and sc.score<60;
```

查询所有学生的课程及分数情况(存在学生没成绩，没选课的情况)

```sql
select s.sid, s.sname, c.cname, sc.score
from student as s
inner join sc
inner join course as c
on sc.sid=s.sid and c.cid=sc.cid;
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
select s.*, group_concat(sc.cid order by sc.cid)
from student as s
inner join sc
on sc.sid=s.sid

group by sc.sid
having group_concat(sc.cid order by sc.cid) =(
    select group_concat(sc.cid order by sc.cid) from sc where sc.sid=1 group by sc.sid
) and sc.sid!=1;
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

查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩

```sql
select distinct sc1.*
from sc as sc1
inner join sc as sc2
where sc1.cid !=sc2.cid and sc1.score=sc2.score;
```

查询每门成绩最好的前两名

```sql
select * from sc where (
  select count(*) from sc as sc1 where ~~sc1~~
)
order by sc.cid asc, sc.score desc;
```

查询两门及其以上不及格课程的同学的学号,姓名及其平均成绩

```sql
select s.sid,s.sname, avg(sc.score)
from student as s
inner join (select * from sc where score<60)sc
on sc.sid=s.sid
group by sc.sid
having count(sc.sid)>=2;

select s.sid,s.sname, avg(sc.score)
from student as s
inner join sc
on sc.sid=s.sid
group by sc.sid
having sc.sid in (
    select sid from sc where score < 60 group by sid
);

```

查询出只有两门课程的全部学生的学号和姓名

```sql
select s.sid,s.sname
from student as s
inner join sc
on sc.sid=s.sid
having count(*)=2;
```

查询男生,女生人数

```sql
select ssex, count(*) from student group by ssex;
```

查询1990年出生的学生名单

```sql
select * from student WHERE sage like '1990%';
```

统计各科成绩各分数段人数:课程编号,课程名称,[100-85],[85-70],[70-60],[60-0] 及所占百分比

```sql
SELECT
  sc.cid AS 课程编号,
  cname AS 课程名称,
  SUM(
    CASE
      WHEN score >= 0
      AND score <= 60
      THEN 1
      ELSE 0
    END
  ) AS '[60-0]',
  SUM(
    CASE
      WHEN score >= 0
      AND score <= 60
      THEN 1
      ELSE 0
    END
  ) / COUNT(sid) AS '[60-0]百分比',
  SUM(
    CASE
      WHEN score >= 60
      AND score <= 70
      THEN 1
      ELSE 0
    END
  ) AS '[70-60]',
  SUM(
    CASE
      WHEN score >= 60
      AND score <= 70
      THEN 1
      ELSE 0
    END
  ) / COUNT(sid) AS '[70-60]百分比',
  SUM(
    CASE
      WHEN score >= 70
      AND score <= 85
      THEN 1
      ELSE 0
    END
  ) AS '[85-70]',
  SUM(
    CASE
      WHEN score >= 70
      AND score <= 85
      THEN 1
      ELSE 0
    END
  ) / COUNT(sid) AS '[85-70]百分比',
  SUM(
    CASE
      WHEN score >= 85
      AND score <= 100
      THEN 1
      ELSE 0
    END
  ) AS '[100-85]',
  SUM(
    CASE
      WHEN score >= 85
      AND score <= 100
      THEN 1
      ELSE 0
    END
  ) / COUNT(sid) AS '[100-85]百分比'
FROM
  sc
  JOIN course
    ON sc.cid = course.cid
GROUP BY sc.cid,
  cname ;
```

查询各科成绩前三名的记录

```sql
SELECT a.*,COUNT(b.score) +1 AS ranking
FROM sc AS a LEFT JOIN sc AS b
ON a.cid = b.cid AND a.score<b.score
GROUP BY a.cid,a.sid
ORDER BY a.cid,ranking;
```

查询每门课程的平均成绩,结果按平均成绩降序排列,平均成绩相同时,按课程编号升序排列

```sql
select cid, avg(score) from sc group by cid order by avg(score) desc, cid;
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
select s.sid, s.sname, avg(sc.score)
from student as s
inner join sc
on sc.sid=s.sid
group by sc.sid
having avg(sc.score)>=85;
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
select s.sid, s.sname, sc.score
from student as s
inner join sc
on sc.sid=s.sid
where sc.cid = 1 and sc.score >= 80;
```

求每门课程的学生人数

```sql
select cid, count(*) from sc group by cid;
```

成绩不重复，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩

```sql
select s.*, sc.score, c.cname
from student as s
inner join sc
inner join course as c
inner join teacher as t
on sc.sid=s.sid and c.cid=sc.cid and c.tid=t.tid
and t.tname='张三'
order by sc.score desc
limit 1;
```

成绩有重复的情况下，查询选修「张三」老师所授课程的学生中，成绩最高的学生

```sql
select s.*, sc.score, c.cname
from student as s
inner join sc
inner join course as c
inner join teacher as t
on sc.sid=s.sid and c.cid=sc.cid and c.tid=t.tid
and t.tname='张三' and score in (
  select max(score) from sc
  inner join course as c
  inner join teacher as t
  on c.cid=sc.cid and c.tid=t.tid
  and t.tname='张三'
);
```

统计每门课程的学生选修人数（超过5人的课程才统计）。要求输出课程号和选修人数,查询结果按人数降序排列,若人数相同,按课程号升序排列

```sql
select sc.cid, count(sc.cid) from sc group by cid having count(sc.cid)>5 order by count(sc.cid) desc, cid asc;
```

检索至少选修两门课程的学生学号

```sql
select sid,count(cid) from sc group by sid having count(cid)>=2;
```

查询没有学全所有课程的同学的信息

```sql
select s.*, count(sc.cid)
from student as s
inner join sc
on sc.sid=s.sid
group by sc.sid
having count(sc.cid)<(select count(*) from course);
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
select *, year(now())-year(sage) as '年龄' from student;
```

按照出生日期来算，当前月日 < 出生年月的月日则，年龄减一

```sql
select *,case
when (date_format(now(), '%m-%d')-date_format(sage,'%m-%d'))<0
then year(now())-year(sage)-1
else year(now())-year(sage)
end as '年龄' from student;
```

查询本周过生日的学生

```sql
select * from student where week(sage)=week(now());
```

查询下周过生日的学生

```sql
select * from student where week(sage)=week(now())+1;
```

查询本月过生日的学生

```sql
select * from student where month(sage)=month(curdate());
```

查询下月过生日的学生

```sql
select * from student where month(sage)=(month(curdate())+1);
```


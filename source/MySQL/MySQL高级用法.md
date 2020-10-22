# MySQL高级用法

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

## 分区

```sql
show variables like '%part%';
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

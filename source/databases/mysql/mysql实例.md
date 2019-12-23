# MySQL日常操作记录

## 创建数据库

```sql
create database bmnars charset=utf8;
```

## 创建表

```sql
CREATE TABLE _cs_bmnars_link_v2 (
  source_url varchar(254) UNIQUE KEY,
  local_url varchar(254) ,
  source varchar(254) ,
  update_time date ,
  id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  status varchar(128) DEFAULT 'N');

create table students(
    id int auto_increment primary key not null,
    name varchar(10) not null,
    gender bit default 1,
    birthday datetime);

CREATE TABLE disease_kegg (
  id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name varchar(255) ,
  acronym varchar(50) ,
  parent_name varchar(255) ,
  update_time date);

create table articles (
  id int(11) not null,
  title varchar(255) not null,
  content text,
  date varchar(255),
  wechat varchar(255),
  nickname varchar(255)
);
```

## 修改表名

```sql
alter table  gene_all_v2 RENAME to gene_all;
```

## 修改表结构

```sql
alter table 表名 add|change|drop 列名 类型
alter table students add isdelete bit default 0;
# 修改字段名
ALTER  TABLE gene_synonym_uniprot CHANGE pid primary_id int(11);
```

## 先添加联合主键,然后添加外键

```sql
ALTER TABLE gd_uniprot ADD CONSTRAINT pk_re PRIMARY KEY(disease_id, gene_id);
ALTER TABLE gd_uniprot ADD CONSTRAINT fk_dis FOREIGN KEY(disease_id) REFERENCES disease_uniprot(id);
ALTER TABLE gd_uniprot ADD CONSTRAINT fk_ge FOREIGN KEY(gene_id) REFERENCES gene_primary_uniprot(id);

alter table articles add constraint pk_art primary key(id);
```

## 查询外键

```sql
SELECT * FROM information_schema.KEY_COLUMN_USAGE where constraint_name='fk_ge_ctd_v2';
```

## 添加唯一约束

```sql
ALTER TABLE gene_primary_uniprot ADD unique(name);
ALTER TABLE disease_uniprot ADD unique(name);
```

## 插入数据

```sql
insert into students values(0,'郭靖',1,'1789-1-1',0);
insert into students(name) values('黄蓉');
insert into students(name) values('杨过'),('小龙女'),('郭襄');
```

## 插入查询的数据到另一个表(唯一键已存在则更新)

```sql
INSERT into disease_all(mesh_id, NAME) 
select id,name from disease_ctd_v2 on duplicate key update mesh_id = disease_ctd_v2.id;
```

## 插入数据，唯一键已存在则更新

```sql
insert into _cs_disease_map(dis_id, gene_symbol) VALUES('2857', "A1BG")  on DUPLICATE key update source = CONCAT(source, ',abc');
```

## 更新数据

```sql
update students set birthday = '1790-1-2' where id = 2;
```

## 物理删除

```sql
delete from students where id = 5;
```

## 逻辑删除

```sql
update students set isdelete = 1 where id =4;
```

## 查询

```sql
select id,name from students where id <=4;
select * from students where id in (1,3,5);
select * from students where id between 3 and 5;
```

## 一对多内链接查询

```sql
select * from gene_synonym_uniprot inner join  gene_primary_uniprot on gene_synonym_uniprot.primary_id = gene_primary_uniprot.id where gene_primary_uniprot.id = 100;
```

## 多对多内链接查询

```sql
select disease_uniprot.name,gene_primary_uniprot.name  from gd_uniprot inner join  gene_primary_uniprot on gd_uniprot.gene_id = gene_primary_uniprot.id inner join disease_uniprot on gd_uniprot.disease_id = disease_uniprot.id where gd_uniprot.gene_id = 1587;
# 以disease_id分组并且disease_id对应的gene大于1
select gd_kegg.disease_id,disease_kegg.name  from gd_kegg inner join  gene_primary_kegg on gd_kegg.gene_id = gene_primary_kegg.id inner join disease_kegg on gd_kegg.disease_id = disease_kegg.id group by gd_kegg.disease_id having count(gd_kegg.gene_id)>1;
```

## 查询（去重）

```sql
SELECT gene_symbol FROM _cs_disease_map group by gene_symbol;

select DISTINCT gene_symbol FROM _cs_disease_map;
```

## 聚合

```sql
select count(*) from students where isdelete = 1;
select max(id) from students where isdelete =1;
select min(id) from students where isdelete =1;
select sum(id) from students where isdelete =0;
select avg(id) from students where isdelete =0;
```

## 分组

```sql
select isdelete,count(*) from students group by isdelete;
select isdelete,count(*) from students group by isdelete having isdelete = 0;
```

## 备份

```sql
mysqldump -u root -p python3 > d:\bup.sql
mysqldump -u bmnars -p bmnars _cs_bmnars_vigenebio_rs > d:\rs.sql
```

## 恢复

```sql
mysql -uroot –p 数据库名 < ~/Desktop/备份文件.sql
mysql -u bmnars -p gene_disease < ./aagatlas_gene.sql
source /home/bmnars/spider_porject/vigenebio_spider/kw.sql;
```

## 导入csv数据

```sql
load data infile 'C:/Users/CRAB/Desktop/mim2gene.csv'
replace into table gene_primary_omim
fields terminated by ','
optionally enclosed by '"'
lines terminated by '\r\n'
ignore 1 lines;
```

### 基本语法

```
load data [low_priority] [local] infile 'file_name txt' [replace | ignore]
into table tbl_name
[character set gbk]
[fields
[terminated by't']
[OPTIONALLY] enclosed by '']
[escaped by'\' ]]
[lines terminated by'\n']
[ignore number lines]
[(col_name, )]
```

1. `replace` 和 `ignore` 。replace，新行将代替有相同的唯一键值的现有行。ignore，跳过有唯一键的现有行的重复行的输入。如果你不指定任何一个选项，当找到重复键时，出现一个错误，并且文本文件的余下部分被忽略。
2. `erminated by`描述字段的分隔符，默认情况下是tab字符（`\t`） 。`enclosed by`描述的是字段的括起字符，就是说字段中如果有引号，就当做是字段的一部分。 语法中还有一个是 `escaped by`，它描述的是转义字符。默认的是反斜杠（`backslash：\`）
3. `lines terminated by`是对每行进行分割，这里要注意一个问题，如果csv文件是在windows下生成，那分割用 `\r\n`，linux下用`\n`。
4. `ignore 1 lines` 是忽略第一行，因为第一行往往是字段名，后边括号中有个字段很特别 `@name`，它是说如果csv文件中有个字段我不想插进去，那就把对应字段名变成`@name`.

## 导出csv数据

```sql
select * from gene_primary_omim
into outfile 'C:/Users/CRAB/Desktop/ene.csv'
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n';
```

## 备份数据库

```sql
# 恢复时无需指定数据库
mysqldump -u bmnars -p  --databases gene_disease_all > gene_disease_all.sql  
# 恢复
mysql -u bmnars -p < ./gene_disease_all.sql

# 恢复时需要指定数据库
mysqldump –u bmnars –p   gene_disease_all > gene_disease_all.sql 
# 恢复
mysqladmin –u 用户名 –p create 数据库名     //创建数据库
mysql -u root -p gene_disease_all < ./gene_disease_all.sql
```

## 新建用户

```sql
# 可远程访问
create user bmnars@'%' identified by 'vi93nwYV'
# 只能本地访问
create user 7JTZsiuI@'localhost' identified by 'sdgsdgr';
```

## 删除用户

```sql
drop user bmnars@'localhost';
```

## 用户授权

```sql
# 某个数据库权限
GRANT ALL PRIVILEGES ON gene_disease.* TO bmnars@"%" IDENTIFIED BY "vi93nwYV";
# 8.0版本的授权
GRANT ALL PRIVILEGES ON my_blog.* TO 7JTZsiuI@'localhost' with grant option;
# 所有权限
GRANT ALL PRIVILEGES ON *.* TO bmnars@"%" IDENTIFIED BY "vi93nwYV";
```
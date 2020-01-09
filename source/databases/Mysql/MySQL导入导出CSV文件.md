# MySQL导入导出CSV文件

## 基本语法

```sql
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

-- replace和ignore replace,新行将代替有相同的唯一键值的现有行.ignore,跳过有唯一键的现有行的重复行的输入.如果你不指定任何一个选项,当找到重复键时,出现一个错误,并且文本文件的余下部分被忽略.
-- terminated by描述字段的分隔符,默认情况下是tab字符\t
-- enclosed by描述的是字段的括起字符,就是说字段中如果有引号,就当做是字段的一部分.
-- lines terminated by 对每行进行分割,如果csv文件是在windows下生成,那分割用 \r\n,linux下用\n.
-- ignore 1 lines 忽略第一行,因为第一行往往是字段名,后边括号中有个字段很特别 @name,它是说如果csv文件中有个字段我不想插进去,那就把对应字段名变成@name.
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

## 导出csv数据

```sql
select * from gene_primary_omim
into outfile 'C:/Users/CRAB/Desktop/ene.csv'
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n';
```

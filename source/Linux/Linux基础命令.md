# Linux基础命令

## 命令帮助

查看命令的简要说明

```shell
[root@izbp128jigdcjx00os4h3sz ~]# whatis ls
ls (1)               - list directory contents
```

详细说明

```shell
[root@izbp128jigdcjx00os4h3sz ~]# info ls
```

使用man

```shell
[root@izbp128jigdcjx00os4h3sz ~]# man ls
```

查看程序的binary文件所在路径

```shell
[root@izbp128jigdcjx00os4h3sz ~]# which ls
alias ls='ls --color=auto'
        /usr/bin/ls
```

查看程序的搜索路径

```shell
[root@izbp128jigdcjx00os4h3sz ~]# whereis ls
ls: /usr/bin/ls /usr/share/man/man1/ls.1.gz
```

## 文件及目录管理

### 创建和删除

```shell
# 创建
mkdir

# 删除
# rm
# 删除非空目录
rm -rf 目录
# 删除日志
rm *log
# $find ./ -name “*log” -exec rm {} ;

# 移动
mv

# 复制
cp
# 复制目录：
cp -r 目录
```

### 目录切换

```shell
# 进入路径
[root@izbp128jigdcjx00os4h3sz ~]# cd /home
[root@izbp128jigdcjx00os4h3sz home]

# 切换到上一个工作目录
[root@izbp128jigdcjx00os4h3sz home]# cd -
/root
[root@izbp128jigdcjx00os4h3sz ~]#

# 切换到home目录
cd
# cd ~

# 显示当前路径
[root@izbp128jigdcjx00os4h3sz ~]# pwd
/root
```

### 列出目录项

```shell
# 按时间排序,以列表的方式显示目录项
[root@izbp128jigdcjx00os4h3sz ~]# ls -lrt
total 22480
-rw-r--r--  1 root root 23010188 Dec 24  2018 Python-3.6.8.tgz
drwxr-xr-x  2 root root     4096 Oct 23 17:00 envs
drwxr-xr-x 18  501  501     4096 Oct 24 13:50 Python-3.6.8
```

### 查找目录及文件 find/locate

```shell
# 搜寻文件或目录
[root@izbp128jigdcjx00os4h3sz ~]# find ./ -name "python"
./.vscode-server/bin/c47d83b293181d9be64f27ff093689e8e7aed054/extensions/python
./.vscode-server/bin/9579eda04fdb3a9bba2750f15193e5fafe16b959/extensions/python
./.vscode-server/bin/26076a4de974ead31f97692a0d32f90d735645c0/extensions/python
./.vscode-server/bin/8795a9889db74563ddd43eb0a897a2384129a619/extensions/python
./.vscode-server/bin/f359dd69833dd8800b54d458f6d37ab7c78df520/extensions/python
./Python-3.6.8/python
```

查看当前目录下文件个数

```shell
[root@izbp128jigdcjx00os4h3sz ~]# find ./ | wc -l
16649
```

递归当前目录及子目录删除所有.ooo文件

```shell
find ./ -name "*.ooo" -exec rm {} \;
```

find是实时查找,如果需要更快的查询,可试试locate

locate会为文件系统建立索引数据库,如果有文件更新,需要定期执行更新命令来更新索引库

```shell
# 寻找包含有string的路径
locate string

# 更新数据库
updatedb
```

### 查看文件内容

```shell
# 显示时同时显示行号:
[root@izbp128jigdcjx00os4h3sz ~]# cat test.txt -n
     1  a
     2  b
     3  c
     4  d

# 查看前3行
[root@izbp128jigdcjx00os4h3sz ~]# head -3 test.txt
a
b
c

# 查看倒数3行
[root@izbp128jigdcjx00os4h3sz ~]# tail -3 test.txt
d
e
f
```

查看两个文件间的差别

```shell
[root@izbp128jigdcjx00os4h3sz ~]# diff test.txt test2.txt
2c2
< b
---
> db
```

动态显示文本最新信息

```shell
[root@izbp128jigdcjx00os4h3sz ~]# tail -f test.txt
a
b
c
d
e
f

```

### 查找文件内容

```shell
[root@izbp128jigdcjx00os4h3sz ~]# grep b test2.txt
db
```

### 文件与目录权限修改

```shell
# 改变文件的拥有者
chown
# 改变文件读、写、执行等属性
chmod
# 增加脚本可执行权限
chmod a+x test.py
```

### 管道和重定向

```shell
# 批处理命令连接执行
|
# 串联
;
# 前面成功则执行后面一条,否则不执行
&&
# 前面失败则后一条执行
||

[root@izbp128jigdcjx00os4h3sz ~]# ls /home && echo succ! || echo fail!
envs test.txt
succ!
```

重定向

```shell
# 将标准输出和标准错误重定向到同一文件
[root@izbp128jigdcjx00os4h3sz ~]# ls /home > result.txt 2>&1
# ls /usr &>result.txt
```

追加

```shell
[root@izbp128jigdcjx00os4h3sz ~]# echo hhhhh >> result.txt
```

清空文件

```shell
[root@izbp128jigdcjx00os4h3sz ~]# :> result.txt
```

## 文本处理

### find 文件查找

查找txt和pdf文件

```shell
# -o or
find . \( -name "*.txt" -o -name "*.pdf" \) -print
```

查找所有非txt文本

```shell
find . ! -name "*.txt" -print
```

指定搜索深度,打印出当前目录的文件(深度为1)

```shell
# -type 文件类型 f代表文件 d代表文件夹 l代表链接
find . -maxdepth 1 -type f
```

查询7天前被访问过的所有文件

```shell
# -atime 访问时间,单位是天.分钟单位则是-amin
# -mtime 修改时间,内容被修改
# -ctime 变化时间,元数据或权限变化
find . -atime +7 -type f -print
```

寻找大于2k的文件

```shell
find . -type f -size +2k
```

查询具有可执行权限的所有文件

```shell
find . -type f -perm 644 -print
```

用户weber所拥有的文件

```shell
find . -type f -user weber -print
```

找到之后删除当前目录下所有的swp文件

```shell
find . -type f -name "*.swp" -delete
```

将找到的文件全都copy到另一个目录

```shell
# {}是一个特殊的字符串,对于每一个匹配的文件,{}会被替换成相应的文件名
find . -type f -mtime +10 -name "*.txt" -exec cp {} OLD \;
```

### grep 文本搜索

```shell
# -c 统计文件中包含文本的次数
# -i 搜索时忽略大小写
grep -c -i 'my' result.txt
```

匹配多个模式

```shell
# -n 打印匹配的行号
[root@izbp128jigdcjx00os4h3sz ~]# grep -e 'my' -e 'envs' -n result.txt
1:envs
2:my_blog
3:my_blog.log
4:my_blog_sql
```

### xargs 命令行参数转换

将多行输出转化为单行输出

```shell
[root@izbp128jigdcjx00os4h3sz ~]# cat result.txt | xargs
envs my_blog my_blog.log my_blog_sql hhhhh
```

将单行转化为多行输出

```shell
# -n指定每行显示的字段数
[root@izbp128jigdcjx00os4h3sz ~]# cat result.txt | xargs -n 2
envs my_blog
my_blog.log my_blog_sql
hhhhh
```

### sort排序

```shell
# -n 按数字进行排序
# -d 按字典序进行排序
# -r 逆序排序
# -k N 指定按第N列排序
[root@izbp128jigdcjx00os4h3sz ~]# sort result.txt  -r -d
my_blog_sql
my_blog.log
my_blog
hhhhh
envs
```

### uniq 消除重复行

消除重复行

```shell
[root@izbp128jigdcjx00os4h3sz ~]# cat result.txt | uniq
envs
my_blog
my_blog.log
my_blog_sql
hhhhh
```

统计各行在文件中出现的次数

```shell
[root@izbp128jigdcjx00os4h3sz ~]# cat result.txt | uniq -c
      1 envs
      1 my_blog
      1 my_blog.log
      1 my_blog_sql
      1 hhhhh
```

找出重复行

```shell
[root@izbp128jigdcjx00os4h3sz ~]# cat result.txt | uniq -d
```

### 用tr进行转换

加解密转换,替换对应字符

```shell
[root@izbp128jigdcjx00os4h3sz ~]# echo 12345 | tr '0-9' '9876543210'
87654
```

删除所有数字(对结果而言)

```shell
[root@izbp128jigdcjx00os4h3sz ~]# cat result.txt |tr -d '0-9'
envs
my_blog
my_blog.log
my_blog_sql
hhhhh

hhhhh
```

### paste 按列拼接文本

```shell
[root@izbp128jigdcjx00os4h3sz ~]# paste result.txt result_2.txt -d '|'
envs|envs
my_blog|my_blog
my_blog.log|my_blog.log
my_blog_sql|my_blog_sql
hhhhh|hhhhh
123|123
hhhhh|hhhhh
```

### wc 统计行和字符的工具

```shell
# 统计行数
[root@izbp128jigdcjx00os4h3sz ~]# wc -l result.txt
7 result.txt

# 统计单词数
[root@izbp128jigdcjx00os4h3sz ~]# wc -w result.txt
7 result.txt

# 统计字符数
[root@izbp128jigdcjx00os4h3sz ~]# wc -c result.txt
53 result.txt
```

### sed 文本替换利器

首处替换

```shell
# 替换每一行的第一处匹配的my
[root@izbp128jigdcjx00os4h3sz ~]# sed 's/hhh/new/' result.txt
envs
my_blog
my_blog.log
my_blog_sql
newhh
123
newhh
```

全局替换

```shell
[root@izbp128jigdcjx00os4h3sz ~]# sed 's/l/z/g' result.txt
envs
my_bzog
my_bzog.zog
my_bzog_sqz
hhhhh
123
hhhhh
```

移除空白行

```shell
[root@izbp128jigdcjx00os4h3sz ~]# sed '/^$/d' result.txt
```

默认替换后,输出替换后的内容,如果需要直接替换原文件,使用-i

```shell
[root@izbp128jigdcjx00os4h3sz ~]# sed -i 's/hhh/new/g' result.txt
```

### awk 数据流处理工具

awk脚本结构

```shell
awk ' BEGIN{ statements } statements2 END{ statements } '
# 1.执行begin中语句块
# 2.从文件或stdin中读入一行,然后执行statements2,重复这个过程,直到文件全部被读取完毕
# 3.执行end语句块
```

使用不带参数的print时,会打印当前行

```shell
[root@izbp128jigdcjx00os4h3sz ~]# echo -e "line1\nline2" | awk 'BEGIN{print "start"} {print } END{ print "End" }'
start
line1
line2
End
```

特殊变量`NR NF $0 $1 $2`

```shell
# NR:表示记录数量,在执行过程中对应当前行号
# NF:表示字段数量,在执行过程总对应当前行的字段数
# $0:这个变量包含执行过程中当前行的文本内容
# $1:第一个字段的文本内容
# $2:第二个字段的文本内容

[root@izbp128jigdcjx00os4h3sz ~]# echo -e "line1 f2 f3\n line2 \n line 3" | awk '{print NR":"$0"-"$1"-"$2}'
1:line1 f2 f3-line1-f2
2: line2 -line2-
3: line 3-line-3
```

统计文件的行数

```shell
[root@izbp128jigdcjx00os4h3sz ~]# awk 'END {print NR}' result.txt
8
```

累加每一行的第一个字段

```shell
[root@izbp128jigdcjx00os4h3sz ~]# echo -e "1\n 2\n 3\n 4\n" | awk 'BEGIN{num = 0 ;
> print "begin";} {sum += $1;} END {print "=="; print sum }'
begin
==
10
```

传递外部变量

```shell
[root@izbp128jigdcjx00os4h3sz ~]# var=1000
[root@izbp128jigdcjx00os4h3sz ~]# echo | awk '{print vara}' vara=$var
1000
```

用样式对awk处理的行进行过滤

```shell
# 行号小于5
[root@izbp128jigdcjx00os4h3sz ~]# awk 'NR < 5' result.txt

# 包含new的行
[root@izbp128jigdcjx00os4h3sz ~]# awk '/new/' result.txt
newhh
newhh

# 不包含new的行
[root@izbp128jigdcjx00os4h3sz ~]# awk '!/new/' result.txt

envs
my_blog
my_blog.log
my_blog_sql
123
```

以下字符串，打印出其中的时间串

```shell
# 使用-F来设置定界符(默认为空格)
[root@izbp128jigdcjx00os4h3sz ~]# echo '2015_04_02 20:20:08: mysqli connect failed, please check connect info'|awk -F':' '{print $1 ":" $2 ":" $3; }'
2015_04_02 20:20:08
```

打印指定列

```shell
[root@izbp128jigdcjx00os4h3sz ~]# ls -lrt | awk '{print $6}'

Dec
Oct
Oct
Mar
```

### 磁盘管理

#### 查看磁盘空间

磁盘空间利用大小

```shell
# -h 易读的方式
[root@izbp128jigdcjx00os4h3sz mysql]# df -h
```

当前目录所占空间大小

```shell
# -s 递归
[root@izbp128jigdcjx00os4h3sz mysql]# du -sh
211M    .
```

查看当前目录下所有子文件夹排序后的大小

```shell
[root@izbp128jigdcjx00os4h3sz mysql]# du -sh `ls` | sort
211M    data
4.0K    logs
8.0K    config
```

#### 打包,压缩

打包, 多个文件归并到一个

```shell
# -c :打包选项
# -v :显示打包进度
# -f :使用档案文件
[root@izbp128jigdcjx00os4h3sz mysql]# tar -cvf config.tar ./config
./config/
./config/my.cnf
```

压缩

```shell
[root@izbp128jigdcjx00os4h3sz mysql]# gzip 1.txt
# 1.txt.gz
```

解包

```shell
-x 解包
[root@izbp128jigdcjx00os4h3sz test]# tar -xvf config.tar
./config/
./config/my.cnf
```

解压后缀为`.tar.gz`的文件

```shell
[root@izbp128jigdcjx00os4h3sz test]# gunzip config.tar.gz
# 然后解包
```

### 进程管理工具

```shell
[root@izbp128jigdcjx00os4h3sz ~]# ps -ef
```

查询归属于用户root的进程

```shell
ps -ef|grep root
# ps -lu root
```

显示进程信息,并实时更新

```shell
# P 根据CPU使用百分比大小进行排序
# M 根据驻留内存大小进行排序
top
```

查看端口占用的进程状态

```shell
netstat -an
```

杀死指定PID的进程

```shell
kill PID
```

杀死相关进程

```shell
kill -9 3306
```

分析线程栈

```shell
pmap PID
```

### 性能监控

查看CPU使用率

```shell
# 每秒采样一次,总共采样2次
sar -u 1 2
```

查看CPU平均负载

```shell
# ar指定-q后,就能查看运行队列中的进程数,系统上的进程大小,平均负载等
sar -q 1 2
```

查看内存使用状况

```shell
sar -r 1 2
```

查看内存使用量

```shell
free -m
```

查询页面交换

```shell
sar -W 1 3
```

## 网络工具

列出所有端口(包括监听和未监听的)

```shell
-t tcp端口
netstat -a
```

使用netstat工具查询端口

```shell
netstat -antp | grep 6379
```

查看路由状态

```shell
route -n
```

发送ping包到地址IP

```shell
ping IP
```

探测前往地址IP的路由路径

```shell
traceroute IP
```

DNS查询，寻找域名domain对应的IP

```shell
host IP
```

直接下载文件或者网页

```shell
wget url
–limit-rate 下载限速
-o 指定日志文件,输出都写入日志,
-c 断点续传
```

SSH登陆

```shell
ssh ID@host
```

ftp/sftp文件传输

```shell
# get filename 下载文件
# put filename 上传文件
# ls 列出host上当前路径的所有文件
# cd 在host上更改当前路径
# lls 列出本地主机上当前路径的所有文件
# lcd 在本地主机更改当前路径
sftp ID@host
```

将本地localpath指向的文件上传到远程主机的path路径

```shell
scp localpath ID@host:path
```

以ssh协议，遍历下载path路径下的整个文件系统，到本地的localpath

```shell
scp -r ID@site:path localpath
```

## 定时任务crontab

```sh
# 创建.sh文件
#!/bin/sh
/home/bmnars/spider_porject/spider_venv/bin/python /home/bmnars/spider_porject/biotech_org_spider/biotech_org_spider_mysql.py >>/home/bmnars/spider_porject/biotech_org_spider/log/$(date +%Y-%m-%d).log 2>&1

# 设置定时任务
crontal -e
#每天4点执行脚本
0 16 * * * sh /home/bmnars/spider_porject/crontab/biotech_org_spider.sh

# 使用Python虚拟环境,所以执行路径为虚拟环境的Python路径/home/bmnars/spider_porject/spider_venv/bin/python
# 字符%是一个可被crontab识别的换行符所以通过调用.sh文件执行Python脚本
```

## 查看CPU和内存使用情况

```shell
top
　　PID：进程的ID
　　USER：进程所有者
　　PR：进程的优先级别,越小越优先被执行
　　NInice：值
　　VIRT：进程占用的虚拟内存
　　RES：进程占用的物理内存
　　SHR：进程使用的共享内存
　　S：进程的状态。S表示休眠,R表示正在运行,Z表示僵死状态,N表示该进程优先值为负数
　　%CPU：进程占用CPU的使用率
　　%MEM：进程使用的物理内存和总内存的百分比
　　TIME+：该进程启动后占用的总的CPU时间,即占用CPU使用时间的累加值。
　　COMMAND：进程启动命令名称
```

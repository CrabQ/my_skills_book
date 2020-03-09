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
# 按时间排序，以列表的方式显示目录项
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

指定搜索深度,打印出当前目录的文件（深度为1）

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

加解密转换，替换对应字符

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

## 定时任务crontab

```sh
# 创建.sh文件
#!/bin/sh
/home/bmnars/spider_porject/spider_venv/bin/python /home/bmnars/spider_porject/biotech_org_spider/biotech_org_spider_mysql.py >>/home/bmnars/spider_porject/biotech_org_spider/log/$(date +%Y-%m-%d).log 2>&1

# 设置定时任务
crontal -e
#每天4点执行脚本
0 16 * * * sh /home/bmnars/spider_porject/crontab/biotech_org_spider.sh

# 使用Python虚拟环境，所以执行路径为虚拟环境的Python路径/home/bmnars/spider_porject/spider_venv/bin/python
# 字符%是一个可被crontab识别的换行符所以通过调用.sh文件执行Python脚本
```

## 查看CPU和内存使用情况

```shell
top
　　PID：进程的ID
　　USER：进程所有者
　　PR：进程的优先级别，越小越优先被执行
　　NInice：值
　　VIRT：进程占用的虚拟内存
　　RES：进程占用的物理内存
　　SHR：进程使用的共享内存
　　S：进程的状态。S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值为负数
　　%CPU：进程占用CPU的使用率
　　%MEM：进程使用的物理内存和总内存的百分比
　　TIME+：该进程启动后占用的总的CPU时间，即占用CPU使用时间的累加值。
　　COMMAND：进程启动命令名称
```

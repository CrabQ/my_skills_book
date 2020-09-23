# Linux基础命令

## 命令帮助

命令行快捷键

```shell
# ctrl + a 光标回到行首
# ctrl + e 光标回到行尾
# ctrl + u 剪切光标到行首字符
# ctrl + k 剪切光标到行尾字符
# ctrl + insert 复制命令行内容
# shift + insert 粘贴命令行内容
```

查看命令的简要说明

```shell
whatis ls
ls (1)               - list directory contents
```

使用man

```shell
man ls
# --help
```

### 关机相关命令

```shell
# 立即关机
shutdown -h now
# 10分钟关机或者11:00
shutdown -h +10

# 重启
reboot
# shutdown -r now
```

## 文件和目录

### pwd: 显示当前路径

```shell
# 显示当前路径
pwd
```

### cd: 目录切换

```shell
# 进入路径
cd /home

# 切换到上一个工作目录
cd -

# 切换到home目录
cd
# cd ~
```

### ls: 显示目录下内容

```shell
# 显示所有文件,按照修改时间反向排序
ls -art
# -l 长格式
# -h 人性化显示
```

### tree: 树结构显示目录下内容

```shell
# 只显示目录
tree -d /root

# 遍历目录的最大层数
tree -L 2 /root
```

### mkdir: 创建目录

```shell
# 创建
mkdir test

# 递归创建
mkdir -p test/t/s

# 同时创建多个
mkdir test/{1,2}/{3,4}
```

### touch: 创建空文件

```shell
touch test.py
```

### cp: 复制文件和目录

```shell
# 复制目录
cp -r 目录
```

### mv: 移动或重命名文件

```shell
# -f 强制覆盖
```

### rm: 删除文件或目录

```shell
# -f 强制删除
# -r 递归删除目录及其内容
rm -rf 目录
# 删除日志
rm *log
# $find ./ -name “*log” -exec rm {} ;
```

### rmdir: 删除空目录

### ln: 硬连接和软连接

```shell
# 无参数,创建硬链接
# -s 创建软链接(符号链接)
ln 源文件 目标文件
# 软链接相当于快捷方式,硬链接相当于复制一份
```

### readlink: 查看符号链接文件的内容

### find: 查找文件

```shell
# 查看当前目录下文件个数
find ./ | wc -l
16649

# -o or
# 查找txt和pdf文件
find . \( -name "*.txt" -o -name "*.pdf" \) -print

# 查找所有非txt文本
find . ! -name "*.txt" -print

# -type 文件类型 f代表文件 d代表文件夹 l代表链接
# -maxdepth levels 查找级数
find . -maxdepth 1 -type f

# -atime 访问时间,单位是天.分钟单位则是-amin
# -ctime 变化时间,元数据或权限变化
# -mtime [-n|+n|n] 通过文件修改时间
# 查询7天前被访问过的所有文件
find . -atime +7 -type f -print

# 寻找大于2k的文件
find . -type f -size +2k

# 查询具有可执行权限的所有文件
find . -type f -perm 644 -print

# 用户weber所拥有的文件
find . -type f -user weber -print

# 找到之后删除当前目录下所有的swp文件
find . -type f -name "*.swp" -delete

# {}是一个特殊的字符串,对于每一个匹配的文件,{}会被替换成相应的文件名
# 将找到的文件全都copy到另一个目录
find . -type f -mtime +10 -name "*.txt" -exec cp {} OLD \;

# 递归当前目录及子目录删除所有.ooo文件
find ./ -name "*.ooo" -exec rm {} \;
```

### xargs: 将标准输入转换成命令行参数

```shell
# -d 自定义分隔符
# 当前目录下所有.log文件移动到dir1下
find . -name "*.log" | xargs -i mv {} dir1/

# -i {}代替前面的结果

# 将多行输出转化为单行输出
cat result.txt | xargs
envs my_blog my_blog.log my_blog_sql hhhhh

# -n指定每行显示的字段数
# 将单行转化为多行输出
cat result.txt | xargs -n 2
envs my_blog
my_blog.log my_blog_sql
hhhhh
```

### rename: 重命名文件

### basename: 显示文件名或目录名

### dirname: 显示文件或者目录路径

### chattr: 改变文件的扩展属性

### lsattr: 查看文件扩展属性

### file: 显示文件类型

### md5sum: 计算和校验文件的MD5值

```shell
# 生成文件md5值
md5sum test.py >md5.log
# -c 从指定文件中读取MD5校验值,并进行校验
md5sum -c md5.log
```

### chown: 改变文件或者目录的用户和用户组

```shell
# -R 递归改变
# chown 用户:组 test.py
chown -R mysql.mysql /root/mysql/*

```

### chmod: 改变文件或目录权限

```shell
# -R 递归改变
chmod 753 test.py
# 增加脚本可执行权限
chmod a+x test.py
```

更改文件,目录读写权限

```shell
chmod userMark(+|-)PermissionsMark

# userMark取值
# u 用户
# g 组
# o 其它用户
# a 所有用户

# PermissionsMark取值
# r 读
# w 写
# x 执行
```

### chgrp: 更改文件用户组

### umask: 显示或设置权限掩码

## 文件过滤及内容编辑处理命令

### cat: 合并文件或查看文件内容

```shell
cat >>file1.txt<<EOF
hi
EOF

# 显示时同时显示行号:
cat test.txt -n
     1  a
     2  b
     3  c
     4  d
# -b 和-n一样,忽略空白行

cat | mysql -u root -p << EOF
CHANGE MASTER TO
  MASTER_HOST='127.0.0.1',
  MASTER_USER='repl',
  MASTER_PASSWORD='123',
  MASTER_PORT=3306,
  MASTER_LOG_FILE='mysql-bin.000003',
  MASTER_LOG_POS=704,
  MASTER_CONNECT_RETRY=10;
EOF
```

### tac: 反向显示文件内容

### more: 分页显示文件内容

```shell
# +n 从n行开始显示
# 空格 向下滚动一屏
# b 返回上一屏
```

### less: 分页显示文件内容

```shell
# -N 显示行号
# 空格 向下滚动一屏
# b 返回上一屏
```

### head: 显示文件内容头部

```shell
# -n 显示行号
```

### tail: 显示文件内容尾部

```shell
# -n 显示行号
# -f 实时显示文件追加的数据
tail -f a.log
```

### tailf: 跟踪日志文件

```shell
# -n 显示行号
# 相当于tail -f ,不同的是文件不增长则不访问
```

### cut: 从文本中提取一段文字并输出

```shell
-c 以字符为单位
-d 自定义分隔符,默认tab
-f 与-d一起,指定显示哪个区域
```

### split: 分割文件

### paste: 合并文件

```shell
paste result.txt result_2.txt -d '|'
envs|envs
my_blog|my_blog
my_blog.log|my_blog.log
my_blog_sql|my_blog_sql
hhhhh|hhhhh
123|123
hhhhh|hhhhh
```

### sort: 文本排序

```shell
# -n 按照数值大小进行排序
# -r 倒序
# -t 指定分隔符
# -k 按指定区间排序
# -d 按字典序进行排序
# -k N 指定按第N列排序

sort result.txt -r -d
my_blog_sql
my_blog.log
my_blog
hhhhh
envs
```

### join: 按两个文件的相同字段合并

### uniq: 去除重复行

```shell
-c 去除重复行,并计算每行出现的次数
```

消除重复行

```shell
cat result.txt | uniq
envs
my_blog
my_blog.log
my_blog_sql
hhhhh
```

统计各行在文件中出现的次数

```shell
cat result.txt | uniq -c
      1 envs
      1 my_blog
      1 my_blog.log
      1 my_blog_sql
      1 hhhhh
```

找出重复行

```shell
cat result.txt | uniq -d
```

### wc: 统计文件的行数,单词书或字节数

```shell
-l 统计行数
-L 打印最长行的长度
```

```shell
# 统计行数
wc -l result.txt
7 result.txt

# 统计单词数
wc -w result.txt
7 result.txt

# 统计字符数
wc -c result.txt
53 result.txt
```

### iconv: 转换文件的编码格式

### dos2unix: 将DOS格式文件转换成UNIX格式

### diff: 比较两个文件的不同

### vimdiff: 可视化比较工具

### rev: 反向输出文件内容

### tr:替换或删除字符

```shell
# -d 删除字符
```

加解密转换,替换对应字符

```shell
echo 12345 | tr '0-9' '9876543210'
87654
```

删除所有数字(对结果而言)

```shell
cat result.txt |tr -d '0-9'
envs
my_blog
my_blog.log
my_blog_sql
hhhhh

hhhhh
```

### od: 按不同进制显示文件

### tee: 多重定向

### vi/vim: 纯文本编辑器

## 文本处理三剑客

重定向

```shell
# 将标准输出和标准错误重定向到同一文件
ls /home > result.txt 2>&1
# ls /usr &>result.tx
```

追加

```shell
echo hhhhh >> result.txt
```

清空文件

```shell
:> result.txt
```

### grep: 文本过滤工具

```shell
# -v 过滤
# -n 显示行号
# -i 不区分大小写
# -c 统计匹配的行数
# -e 匹配多个
# -E 使用扩展的egrep命令

# 过滤空行和注释行
grep -Ev "^$|#" nginx.conf
```

### sed: 字符流编辑器

```shell
# -i 直接修改文件内容,默认替换后,输出替换后的内容
sed -i 's/hhh/new/g' result.txt

# 内置命令
# i 指定行前追加文本
# a 指定行后追加文本
sed '2a hi' result.txt
# 第二行后加上一行hi

# d 删除匹配行
sed '2,5d' result.txt
# 删除第二到第五行
```

首处替换

```shell
# 替换每一行的第一处匹配的my
sed 's/hhh/new/' result.txt
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
sed 's/l/z/g' result.txt
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
sed '/^$/d' result.txt
```

### awk: 数据流处理工具

awk脚本结构

```shell
awk ' BEGIN{ statements } statements2 END{ statements } '
# 1.执行begin中语句块
# 2.从文件或stdin中读入一行,然后执行statements2,重复这个过程,直到文件全部被读取完毕
# 3.执行end语句块

# 使用不带参数的print时,会打印当前行
echo -e "line1\nline2" | awk 'BEGIN{print "start"} {print } END{ print "End" }'
start
line1
line2
End

# 特殊变量`NR NF $0 $1 $2`
# NR: 当前行号
# NF: 字段数
# $0: 整行内容
# $1: 第一个字段的文本内容
# $2: 第二个字段的文本内容
# $NF: 最后一列
# 行号小于5
awk 'NR < 5' result.txt

echo -e "line1 f2 f3\n line2 \n line 3" | awk '{print NR":"$0"-"$1"-"$2}'
1:line1 f2 f3-line1-f2
2: line2 -line2-
3: line 3-line-3

# 统计文件的行数
awk 'END {print NR}' result.txt
8

# 累加每一行的第一个字段
echo -e "1\n 2\n 3\n 4\n" | awk 'BEGIN{num = 0 ;
> print "begin";} {sum += $1;} END {print "=="; print sum }'
begin
==
10

# 传递外部变量
var=1000
echo | awk '{print vara}' vara=$var
1000

# 包含new的行
awk '/new/' result.txt
newhh
newhh

# 不包含new的行
awk '!/new/' result.txt
envs
my_blog
my_blog.log
my_blog_sql
123

# 使用-F来设置定界符(默认为空格)
# 以下字符串,打印出其中的时间串
echo '2015_04_02 20:20:08: mysqli connect failed, please check connect info'|awk -F':' '{print $1 ":" $2 ":" $3; }'
2015_04_02 20:20:08

# 打印指定列
ls -lrt | awk '{print $6}'
Dec
Oct
Oct
Mar
```

使用awk和chkconfig关闭不需要的开机自启服务

```shell
chkconfig --list|grep 3:on|grep -vE "crond|sshd|network|rsyslog|stsstat|" | awk '{print "chkconfig " $1 " off"}'|bash
```

## Linux信息显示与搜索文件命令

### uname: 显示系统信息

```shell
# -r 显示内核发行版本号
uname -r

# 显示操作系统
uname -m

# -a 显示系统所有相关信息
uname -a
lsb_release -a

```

### hostname: 显示或设置系统的主机名

```shell
# -I 显示主机所有IP地址,不依赖DNS解析
# 临时修改为test
hostname test

# 永久修改
vim /etc/hostname
```

### dmesg: 系统启动异常诊断

### stat: 显示文件或文件系统状态

### du: 统计磁盘空间使用情况

```shell
# -h 可读方式查看
# -s 递归
du -sh
211M    .

# 查看当前目录下所有子文件夹排序后的大小
du -sh `ls` | sort
211M    data
4.0K    logs
8.0K    config
```

### date: 显示与设置系统时间

```shell
# -d 显示指定字符串的时间
# -s 设置系统时间
date
```

### echo: 显示一行文本

```shell
# -n 不要自动换行
```

### watch: 监视命令执行情况

```shell
# -n 命令执行的间隔时间,默认2s
```

### which: 显示命令的全路径

查看程序的binary文件所在路径

```shell
which ls
alias ls='ls --color=auto'
        /usr/bin/ls
```

### whereis: 显示命令及其相关文件全路径

```shell
whereis ls
ls: /usr/bin/ls /usr/share/man/man1/ls.1.gz
```

### locate: 快速定位文件路径

locate会为文件系统建立索引数据库,如果有文件更新,需要定期执行更新命令来更新索引库

```shell
# 寻找包含有string的路径
locate string

# 更新数据库
updatedb
```

### updatedb: 更新mlocate数据库

## 文件备份与压缩命令

### tar: 打包备份

```shell
# z 通过gzip压缩或者解压
# c 创建新的tar包
# x 解开tar包
# v 显示过程
# f 指定压缩文件的名字
# t 不解压查看tar包内容
# C 指定解压的目录路径
# --exclude=PATTERN 打包时排除不需要的文件或目录
# -h 打包软连接文件指向的真实源文件

# 打包
tar -zcf new.tar.gz ./new/

# 解包
tar -zxvf new.tar.gz
```

### gzip: 压缩或解压文件

只能压缩文件,目录需要先打包

压缩,解压都会会删除源文件

```shell
# 压缩
gzip *.html

# -c 将内容输出到标准输出,不改变原始文件
# 压缩,不删除源文件
gzip -c 1.html>1.gz

# -d 解开压缩文件
# 解压
gzip -dv *.gz
```

### zip: 打包和压缩文件

```shell
# -r 压缩指定目录下所有文件和路径
# -x 压缩文件时排除某个文件
zip -r test.zip ./test/ -x test/1.html
```

### unzip: 解压zip文件

```shell
# -l 不解压查看tar包内容
unzip -l test.zip

# -d 指定解压的目录路径
unzip -d /test test.zip
```

### scp: 远程文件复制

```shell
# -P port 端口
# -p 传输后保留文件原始属性
# -r 递归复制整个目录

# 将本地localpath指向的文件上传到远程主机的path路径
scp localpath ID@host:path
scp -rp ./testc root@121.196.202.188:/tmp

# 以ssh协议,遍历下载path路径下的整个文件系统,到本地的localpath
# scp -r ID@site:path localpath
# 相同文件会覆盖
scp -rp cnda@192.168.9.122:/home/cnda/new /home/cnda/12new
```

### rsync: 文件同步工具

### 查看文件内容

```shell


# 查看前3行
head -3 test.txt
a
b
c

# 查看倒数3行
tail -3 test.txt
d
e
f
```

查看两个文件间的差别

```shell
diff test.txt test2.txt
2c2
< b
---
> db
```

动态显示文本最新信息

```shell
tail -f test.txt
a
b
c
d
e
f

```

## 用户管理及用户信息查询命令

### useradd: 创建用户

```shell
# -g 指定用户对应的用户组,组需已存在

# -s shell 用户登入后使用的shell名称
# -M 不建立用户家目录
useradd nginx -s /sbin/nologin -M
```

### usermod: 修改用户信息

### userdel: 删除用户

```shell
# -f 强制删除用户，即使用户已登录
# -r 同时删除与用户相关的所有文件
```

### groupadd: 创建新的用户组

### groupdel: 删除用户组

### groups: 用户分组

```shell
# 查看用户分组
groups jack
```

### gpasswd: 添加用户到分组

```shell
# 添加用户jack到分组mike
gpasswd -a jack mike

# 从mike分组剔除jack
gpasswd -d jack mike
```

### passwd: 修改用户密码

### chage: 修改用户密码有效期

### chpasswd: 批量更新用户密码

### su: 切换用户

```shell
# su - 用户名 切换的同时将登录后的环境变量一并切换
```

### visudo: 编辑sudoers文件

```shell
# 添加管理用户
visudo
test ALL=(ALL) /usr/sbin/useradd,/usr/sbin/userdel
```

### sudo: 以另一个用户身份执行命令

```shell
# 查看当前用户被授予的sudo权限集合
sudo -l
```

### id: 显示用户与用户组的信息

### w: 显示已登录用户信息

### who: 显示已登录用户信息

### users: 显示已登录用户

### whoami: 显示当前登录的用户名

### last: 显示用户登录列表

### lastb: 显示用户登录失败的记录

### lastlog: 显示所有用户的最近登录记录

## 磁盘与文件系统管理命令

### fdisk: 磁盘分区工具

受mbr分区表的限制,fdisk工具只能给小于2TB的磁盘划分分区

```shell
# -l 显示所有磁盘分区的信息
```

### partprobe: 更新内核的磁盘分区表信息

### tune2fs: 调整ext2/ext3/ext4 文件系统参数

### parted: 磁盘分区工具

```shell
# -l 显示所有磁盘分区的信息
```

### mkfs: 创建Linux文件系统

```shell
# -t 指定要创建的文件体统类型
```

### dumpe2fs: 导出ext2/ext3/ext4文件系统信息

### resize2fs: 调整ext2/ext3/ext4文件系统大小

### fsck: 检查并修复Linux文件系统

文件系统必须是卸载的

不要对正常的分区使用fsck

### dd: 转换或复制文件

```shell
# if=<输入文件> 从指定文件中读取
# of=<输出文件> 写入到指定文件
# bs=<字节数> 一次读写的字节数
# count=<块数> 指定复制block块的个数
```

### mount: 挂载文件系统

```shell
# -o 后接一些挂载的选项,是安全性能优化的重要选项
# -t 指定挂载的文件系统类型

# 查看当前挂载信息
mount
# 光盘挂载到/mnt
mount /dev/cdrom /mnt
```

### umount: 卸载文件系统

```shell
# -f 强制卸载
# -l 懒惰卸载,清楚对文件系统的所有引用,一般和-f参数配合使用
umount /mnt
```

### df: 报告文件系统磁盘空间的使用情况

```shell
# -h 人性化显示
# -i 显示文件提醒的inode信息
df -h

# 文件系统的inode数限制
df -i
```

### mkswap: 创建交换分区

### swapon: 激活交换分区

### swapoff: 关闭交换分区

### sync: 刷新文件系统缓冲区

## 进程管理命令

### ps: 查看进程

```shell
# a 显示与终端相关的所有进程,包含每个进程的完整路径
# x 显示与终端无关的所有进程
# u 显示指定用户相关的进程信息
ps -aux

# -e 显示所有进程
# -f 额外显示UID,PPID,C与STIME栏位
ps -ef| grep mysql
```

### pstree: 显示进程状态树

### pgrep: 查找匹配条件的进程

### kill: 终止进程

```shell
kill 3436
# 强制终止
kill -9 3436
```

### killall: 通过进程名终止进程

### pkill: 通过进程名终止进程

```shell
# -t 终端 杀死指定终端的进程
# -u 用户 杀死指定用户的进程
```

### top: 实时显示系统中各个进程的资源占用状况

```shell
# 默认以CPU负载排序
top
```

### nice: 调整程序运行时的优先级

### renice: 调整运行中的进程的优先级

### nohup: 用户退出系统进程继续工作

```shell
nohup ping www.baidu.com &
```

### strace: 跟踪进程的系统调用

### ltrace: 跟踪进程调用库函数

### runlevel: 输出当前运行级别

```shell
# 3: 多用户模式
runlevel
N 3
```

### init: 初始化Linux进程

```shell
# 关机
init 0
# 重启
init 6
```

### service: 管理系统服务

```shell
# centos7: systemctl
systemctl status docker
```

## 网络管理命令

```shell
# 查看dns
cat /etc/resolv.conf
```

### ifconfig: 配置或显示网络接口信息

```shell
# up 激活指定的网络接口
# down 关闭指定的网络接口
# 查看ip
ifconfig eth0
```

### ifup: 激活网络接口

### ifdown: 禁用网络接口

### route: 显示或管理路由表

```shell
-n 直接使用IP地址,不进行DNS解析主机名
add 添加路由信息
del 删除路由信息
-net 到一个网络的路由,后接一个网络号地址
-host 到一个主机路由,后接一个主机地址
netmask NM 为添加的路由指定网路掩码
gw GW 为发往目标网络/主机的任何分组执行网关
# 查看默认网关
route -n
```

### arp: 管理系统的arp缓存

```shell
-n 显示数字IP地址
-s <主机> <MAC 地址> 设置指定主机的IP地址与MAC地址的静态映射
-d <主机> 从arp缓存区中删除指定主机的arp条目
```

### ip: 网络配置工具

### netstat: 查看网络状态

```shell
-n 显示数字形式的地址而不是去解析主机,端口或用户名
-a 显示处于监听状态和非监听状态的socket信息
-t 显示所有TCP连接情况
-u 显示所有UDP连接情况
-p 显示socket所属进程的PID和名称
```

列出所有端口(包括监听和未监听的)

```shell
# -t tcp端口
# -n 显示数字形式的地址
netstat -an

# 使用netstat工具查询端口
netstat -antp | grep 6379
```

### ss: 查看网络状态

### ping: 测试主机之间的网络连通性

### traceroute: 追踪数据传输路由状况

### arping:　发送arp请求

### telnet: 远程登录主机

```shell
# 测试ssh端口是否开放
telnet 127.0.0.1 22
```

### nc: 多功能网络工具

```shell
-l 指定监听端口,然后等待网络连接
-z 表示zero,扫描时不发送任何数据
-v 详细数据
-w 设置超时时间,对-l无效
```

### ssh: 安全地远程登录主机

```shell
ssh -p 22 root@127.0.0.1
```

### wget: 命令行下载工具

```shell
# -O 指定名称
# -c 断点续传
# -limit-rate 限速
# -b 后台执行

wget http://download.redis.io/releases/redis-5.0.7.tar.gz
```

### ftp/sftp: 文件传输

```shell
# get filename 下载文件
# put filename 上传文件
# ls 列出host上当前路径的所有文件
# cd 在host上更改当前路径
# lls 列出本地主机上当前路径的所有文件
# lcd 在本地主机更改当前路径
sftp user@host
```

### mailq: 显示邮件传输队列

### mail: 发送和接受邮件

```shell
-s 指定邮件主题
-a 发送附件
```

### nslookup: 域名查询工具

### dig: 域名查询工具

```shell
# +trace从根域开始查询结果
dig +trace www.baidu.com
```

### host: 域名查询工具

### nmap: 网络探测工具和安全/端口扫描器

### tcpdump: 监听网络流量

## 系统管理命令

### lsof: 查看进程打开的文件

```shell
# -i 通过监听指定的协议,端口和主机等信息查看进程状态
lsof -i:80
```

### uptime: 显示系统的运行时间及负载

### free: 显示系统内存信息

### iftop: 动态显示网络接口流量信息

### vmstat: 虚拟内存统计

### mpstat: CPU信息统计

### iostat: IO信息统计

### iotop: 动态显示磁盘I/O统计信息

### sar: 收集系统信息

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

查询页面交换

```shell
sar -W 1 3
```

### chkconfig: 管理开机服务

```shell
# 原理: /etc/rd*.d/目录中对应的软连接(SK开头表示开关)

# --add 添加一个系统服务
# --del 删除一个系统服务

# 显示不同运行级别下服务的启动状态
chkconfig --list
```

### ntsysv: 管理开机服务

### setup: 管理开机服务

### ethool: 查询网卡参数

### mii-tool: 管理网络接口状态

### dmidecode: 查询系统硬件信息

### lspci: 显示所有PCI设备

### ipcs: 显示进程间通信设施的状态

### ipcrm: 清楚ipc相关信息

### rpm: RPM包管理器



![image-20200922131022465](C:\Users\CRAB\Desktop\MY\my_skills_book\source\Linux\Linux基础命令.assets\image-20200922131022465.png)

```shell
# -q 查询
# -i info|install
# -l 显示软件包中的所有文件列表
# -R 显示软件包的依赖环境
# -v 详细信息
# -h #显示安装进度
# -a 查询所有软件包
# -e 卸载
# -f 查询文件或者命令属于哪个软件包

# 查询mysql相关
rpm -qa|grep mysql

# 安装
rpm -ivh a.rpm
```

### yum: 自动化RPM包管理工具

```shell
# -y 确认

# 列出所有安装包
yum list installed

# 检查更新
yum check-update

# 安装
yum install httpd

# 卸载
yum remove httpd

# 更新
yum update httpd

# 列出软件包
yum list httpd

# 搜索
yum search httpd

# 列出所有可用软件
yum list

# 更新系统
yum update

# 列出启用yum源
yum repolist

# 列出所有yum源
yum repolist all

# 清理所有缓存
yum clean all

# 历史
yum history
```

## 系统常用内置命令

```shell
# alias: 显示和创建已有命令的别名
# unalias: 取消已有命令的别名
# bg: 把任务放到后台
# fg: 把后台任务放到前台
# echo: 显示一行文本
# eval: 读入参数,并将它们组合成一个新的命令,然后执行
# export: 设置或显示环境变量
```

## 环境变量

bashrc与profile都用于保存用户的环境信息,bashrc用于交互式non-loginshell,而profile用于交互式login shell

```shell
# /etc/profile,/etc/bashrc 是系统全局环境变量设定
# ~/.profile,~/.bashrc用户目录下的私有环境变量设定
```

## 程序构建

一般源代码提供的程序安装需要通过配置,编译,安装三个步骤

- 配置做的工作主要是检查当前环境是否满足要安装软件的依赖关系,以及设置程序安装所需要的初始化信息,比如安装路径,需要安装哪些组件.配置完成,会生成makefile文件供第二步make使用
- 编译是对源文件进行编译链接生成可执行程序
- 安装做的工作就简单多了,就是将生成的可执行文件拷贝到配置时设置的初始路径下

查询可用的配置选项

```shell
./configure --help
```

编译使用make编译

```shell
# make -f myMakefile
make
```

安装

```shell
make install
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

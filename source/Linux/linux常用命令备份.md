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
# -d 显示目录
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
# cp -r 目录 /d1/d2/d3
cp -r /d1/ /c1
# /c1不存在--> /c1/d2/d3
# /c1存在--> /c1/d1/d2/d3

# 强行覆盖
\cp -r /d1/ /c1
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
# find ./ -name “*log” -exec rm {} ;
```

### rmdir: 删除空目录

### readlink: 查看符号链接文件的内容

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

## Linux信息显示与搜索文件命令

### dmesg: 系统启动异常诊断

### stat: 显示文件或文件系统状态

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

### updatedb: 更新mlocate数据库

## 文件备份与压缩命令

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

### ss: 查看网络状态

### ping: 测试主机之间的网络连通性

### traceroute: 追踪数据传输路由状况

### arping:　发送arp请求

### nc: 多功能网络工具

```shell
-l 指定监听端口,然后等待网络连接
-z 表示zero,扫描时不发送任何数据
-v 详细数据
-w 设置超时时间,对-l无效
```

### wget: 命令行下载工具

```shell
# -O 指定名称
# -c 断点续传
# -limit-rate 限速
# -b 后台执行

wget http://download.redis.io/releases/redis-5.0.7.tar.gz
```

### mailq: 显示邮件传输队列

### mail: 发送和接受邮件

```shell
-s 指定邮件主题
-a 发送附件
```

### nslookup: 域名查询工具

### host: 域名查询工具

### nmap: 网络探测工具和安全/端口扫描器

### tcpdump: 监听网络流量

## 系统管理命令

### lsof: 查看进程打开的文件

```shell
yum install -y lsof
# -i 通过监听指定的协议,端口和主机等信息查看进程状态
lsof -i:80
```

### uptime: 显示系统的运行时间及负载

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

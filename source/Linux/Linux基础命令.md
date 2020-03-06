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

## 目录切换

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

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

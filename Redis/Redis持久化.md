# Redis持久化

## 什么是持久化

redis所有数据保持在内存中

对数据的更新将异步地保存在磁盘上

## 持久化的方式

```shell
# 快照 MySQL Dump|Redis RDB
# 写日志 MySQL Binlog|Redis AOF
```

## RDB文件(二进制)

RDB是Redis内存到硬盘的快照,用于持久化

### 触发机制

```shell
# save(同步),老文件会被替换,时间复杂度O(n),阻塞,不消耗额外内存,但阻塞客户端命令
save
# OK

# bgsave(异步),老文件会被替换,时间复杂度O(n),阻塞(发生在fork),不阻塞客户端命令,但需要fork,消耗额外内存
bgsave
# Background saving started

# 自动(不推荐),以下满足任一就会执行
# save 900 1
# save 300 10
# save 60 10000
```

相关配置

```shell
# 默认生成文件名
dbfilename dump.rdb

# 生成文件存放目录
dir ./

# bgsave发生错误时是否停止写入
stop-writes-on-bgsave-error yes

# 是否压缩
rdbcompression yes

# 是否校验文件
rdbchecksum yes
```

推荐配置

```shell
# 关闭自动生成rdb文件

# 通过端口区分不同redis生成的文件
dbfilename dump-${port}.rdb

# 选择大容量目录
dir /bigdiskpath

# bgsave发生错误时是否停止写入
stop-writes-on-bgsave-error yes
```

### 自动触发的机制-不容忽略的方式

```shell
# 全量复制(主从)
# debug reload
# shutdown
```

### RDB问题

```shell
耗时,耗性能
不可控,丢失数据
```

## AOF

### AOF的三种策略

```shell
# always, redis(写命令刷新缓冲区)-缓冲(always:每条命令fsync到硬盘)-AOF文件
# 不丢失数据,IO开销大

# everysec, redis(写命令刷新缓冲区)-缓冲(everysec:每秒把缓冲区fsync到硬盘)-AOF文件,默认配置
# 每秒一次fsync,丢一秒数据

# no, 系统决定写不写到硬盘
# 不用管,不可控
```

### AOF重写

```shell
减少硬盘占用量
加快恢复速度
```

### 两种实现方式

命令行fork

```shell
bgrewriteaof
# Background append only file rewriting started
```

配置AOF重写

```shell
# 配置

# AOF文件重写需要的尺寸
auto-aof-rewirte-min-size

# AOF文件增长率
auto-aof-rewirte-percentage

# 统计
# AOF当前尺寸(单位:字节)
aof_current_size

# AOF上次启动和重写的尺寸(单位:字节)
aof_base_size
```

AOF重写需要同时满足以下两个条件才会自动触发

```shell
aof_current_size > auto-aof-rewirte-min-size
aof_current_size - aof_base_size / aof_base_size > auto-aof-rewirte-percentage
```

### AOF相关配置

```shell
# 必须开启此项才能开启AOF
appendonly yes

# AOF文件名
appendfilename "appendonly-${port}.aof"

# AOF策略
appendfsync everysec

# 文件存放目录
dir /bigdiskpath

# 一般yes,开销没那么大
no-appendfsync-on-rewrite yes

# AOF文件重写需要的尺寸
auto-aof-rewirte-min-size 64mb

# AOF文件增长率
auto-aof-rewirte-percentage 100
```

## AOF和RDB的选择

```shell
RDB 启动优先级低,体积小,恢复速度快,会丢失数据,重
AOF 高,大,慢,根据策略决定,轻
```

### RDB最佳策略

```shell
自动 关
集中管理(备份)
主从,从开(备份)
```

### AOF最佳策略

```shell
开 缓存和存储
AOF重写集中管理
everysec
```

### 最佳策略

```shell
小分片
缓存或者存储
监控(硬盘,内存,负载,网络)
足够的内存
```

## 持久化的优化

### fork操作

```shell
同步操作
与内存量息息相关:内存越大,耗时越长(与机器类型有关)
info:latest_fork_usec
```

改善

```shell
优先使用物理机或者高效支持fork操作的虚拟化技术
控制redis实例最大可用内存:maxmemory
合理配置Linux内存分配策略: vm.overcommit_memory=1
降低fork频率: 例如放宽AOF重写自动触发时机,不必要的全量复制
```

### 子进程开销与优化

cpu

```shell
开销: RDB和AOF文件生成,属于CPU密集型
优化: 不做CPU绑定,不和CPU密集型部署
```

内存

```shell
开销: fork内存开销,copy-on-write
优化: echo never >　/sys/kernel/mm/transparent_hugepage/enabled
```

硬盘

```shell
开销: RDB和AOF文件写入,可以结合iostat,iotop分析
优化:
不要和高硬盘负载服务部署一起:存储服务,消息队列等
no-appendfsync-on-rewrite = yes
根据写入量决定磁盘类型: 例如SSD
单机多实例持久化文件目录可以考虑分盘
```

### AOF追加阻塞

```shell
定位: redis日志,info persistence
优化: 参考硬盘优化
```

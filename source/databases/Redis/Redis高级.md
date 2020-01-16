# Redis高级

## Redis特性

- 速度快,内存型
- 持久化,断电不丢数据,对数据的更新将异步保存到磁盘上
- 多种数据结构
- 支持多种编程语言
- 功能丰富
- 简单
- 主从复制
- 高可用,分布式

### Redis典型应用场景

- 缓存系统
- 计数器
- 消队列系统
- 排行榜

## Redis功能

### 慢查询

#### 命令执行的生命周期

> 发送命令-排队-执行命令(慢查询发生的阶段)-返回结果
> 客户端超时不一定慢查询

#### 慢查询定义

- 先进先出队列
- 固定长度
- 保存在内存中

#### 慢查询配置

```shell
# 慢查询固定长度,默认128
slowlog-max-len

# 慢查询阀值(单位:微秒),默认10000
slowlog-log-slower-than
# =0 记录所有命令
# <0 不记录任何命令

# 获取慢查询队列
slowlog get [n]

# 获取慢查询队列长度
slowlog len

# 清空慢查询队列
slowlog reset
```

两种配置方法

```shell
# 修改配置文件重启,第一次配置,平时不推荐

# 动态配置
config set slowlog-max-len 1000
config set slowlog-log-slower-than 1000
```

#### 慢查询运维经验

```shell
# slowlog-max-len 1000
# slowlog-log-slower-than 1000
# 理解生命周期
# 定期持久化慢查询,通过开源软件等导入到MySQL
```

### pipeline

pipeline操作非原子

#### 使用建议

```shell
# 注意每次pipeline携带数据量
# pipeline每次只能作用在一个Redis节点上
# M操作与pipeline区别
```

### 发布订阅

无法收到历史消息

#### 角色

- 发布者(publisher)
- 订阅者(subscriber)
- 频道(channel)

#### 发布订阅API

```shell
# 发布命令
# publish channel message
publish sohu:tv 'hello world'
# (integer) 1 订阅者个数

# 订阅
# subscribe [channel] 一个或多个
subscribe sohu:tv
# Reading messages... (press Ctrl-C to quit)
# 1) "subscribe"
# 2) "sohu:tv"
# 3) (integer) 1

# 发布者发布之后收到的信息
# 1) "message"
# 2) "sohu:tv"
# 3) "hello world"

# 取消订阅
# unsubscribe [channel] 一个或多个
unsubscribe sohu:tv
# 1) "unsubscribe"
# 2) "sohu:tv"
# 3) (integer) 0

# psubscribe [pattern...] 订阅模式
# punsubscribe [pattern...] 退订指定的模式
# pubsub channels 列出至少有一个订阅者的频道
# pubsub numsub [channel...] 列出给定频道的订阅者数量
```

#### 发布订阅与消息队列

- 发布订阅 所有的订阅者都收到消息
- 消息队列 通过列表,阻塞的方式,只有抢到的客户端能收到信息

### BitMap(位图)

8个bit可以组成一个Byte,储存1亿用户只要大概12.5MB

```shell
# 给位图指定索引设置值
setbit key offset value

# 获取位图指定索引的值
getbit key offset

# 获取位图指定范围(start到end,单位为字节,如果不指定则为全部)位值为1的个数
bitcount key [start end]

# 将多个bitmap的and(交集),or(并集),not(非),xor(异或)操作并将结果保存在destkey中
bitop op destkey key [key...]

计算位图指定范围(start到end,单位为字节,如果不指定则为全部)第一个偏移量对应的值等于targetBit的位置
bitpos key targetBit [start end]
```

#### BitMap使用经验

```shell
type=string,最大512MB
注意setbit的偏移量,可能有较大耗时
```

### HyperLogLog

基于HyperLogLog算法:极小空间完成独立数量统计
本质还是字符串
内存消耗超小

#### HyperLogLog API

```shell
# 向HyperLogLog添加元素
pfadd key element [element...]

# 计算HyperLogLog的独立总数
pfcount key [key ...]

# 合并多个HyperLogLog
pfmerge destkey sourcekey [sourcekey ...]
```

#### HyperLogLog使用经验

- 能否容忍错误(错误率:0.81%)
- 是否需要单条数据(无法获取单条数据)

### GEO

- since 3.2+
- type geoKey = zet
- 没有删除API: zrem key member

```shell
# 增加地理位置信息
geoadd key longitude latitude member [longitude latitude member ...]

# 获取地理位置信息
geopos key member [member...]

# 获取两个地理位置的距离
geolist key member1 member2 [unit]
# unit: m,km,mi(英里),ft(尺)
```

## Redis持久化

### 什么是持久化

redis所有数据保持在内存中,对数据的更新将异步地保存在磁盘上

### 持久化的方式

```shell
# 快照 MySQL Dump|Redis RDB
# 写日志 MySQL Binlog|Redis AOF
```

### RDB文件(二进制)

RDB是Redis内存到硬盘的快照,用于持久化

#### 触发机制

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

#### 自动触发的机制-不容忽略的方式

```shell
# 全量复制(主从)
# debug reload
# shutdown
```

#### RDB问题

- 耗时,耗性能
- 不可控,丢失数据

### AOF

#### AOF的三种策略

```shell
# always, redis(写命令刷新缓冲区)-缓冲(always:每条命令fsync到硬盘)-AOF文件
# 不丢失数据,IO开销大

# everysec, redis(写命令刷新缓冲区)-缓冲(everysec:每秒把缓冲区fsync到硬盘)-AOF文件,默认配置
# 每秒一次fsync,丢一秒数据

# no, 系统决定写不写到硬盘
# 不用管,不可控
```

#### AOF重写

- 减少硬盘占用量
- 加快恢复速度

##### 两种实现方式

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

#### AOF相关配置

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

### AOF和RDB的选择

- RDB 启动优先级低,体积小,恢复速度快,会丢失数据,重
- AOF 高,大,慢,根据策略决定,轻

#### RDB最佳策略

- 自动 关
- 集中管理(备份)
- 主从,从开(备份)

#### AOF最佳策略

- 开 缓存和存储
- AOF重写集中管理
- everysec

#### 最佳策略

- 小分片
- 缓存或者存储
- 监控(硬盘,内存,负载,网络)
- 足够的内存

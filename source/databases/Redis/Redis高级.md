# Redis高级

## Redis特性

```shell
速度快,内存型
持久化,断电不丢数据,对数据的更新将异步保存到磁盘上
多种数据结构
支持多种编程语言
功能丰富
简单
主从复制
高可用,分布式
```

### Redis典型应用场景

```shell
缓存系统
计数器
消息队列系统
排行榜
```

## Redis功能

### 慢查询

#### 命令执行的生命周期

```shell
发送命令-排队-执行命令(慢查询发生的阶段)-返回结果
客户端超时不一定慢查询
```

#### 慢查询定义

```shell
先进先出队列
固定长度
保存在内存中
```

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

```shell
发布者(publisher)
订阅者(subscriber)
频道(channel)
```

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

```shell
发布订阅 所有的订阅者都收到消息
消息队列 通过列表,阻塞的方式,只有抢到的客户端能收到信息
```

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

# 计算位图指定范围(start到end,单位为字节,如果不指定则为全部)第一个偏移量对应的值等于targetBit的位置
bitpos key targetBit [start end]
```

#### BitMap使用经验

```shell
type=string,最大512MB
注意setbit的偏移量,可能有较大耗时
```

### HyperLogLog

```shell
基于HyperLogLog算法:极小空间完成独立数量统计

本质还是字符串

内存消耗超小
```

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

能否容忍错误(错误率:0.81%)
是否需要单条数据(无法获取单条数据)

### GEO

```shell
since 3.2+
type geoKey = zet
没有删除API: zrem key member
```

```shell
# 增加地理位置信息
geoadd key longitude latitude member [longitude latitude member ...]

# 获取地理位置信息
geopos key member [member...]

# 获取两个地理位置的距离
geolist key member1 member2 [unit]
# unit: m,km,mi(英里),ft(尺)
```

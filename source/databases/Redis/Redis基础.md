# Redis基础

## Redis特性

- 速度快,内存型
- 持久化,断电不丢数据,对数据的更新将异步保存到磁盘上
- 多种数据结构
- 支持多种编程语言
- 功能丰富
- 简单
- 主从复制
- 高可用,分布式

## Redis典型应用场景

- 缓存系统
- 计数器
- 消队列系统
- 排行榜

## 通用命令

以下命令的时间复杂度,无说明则为O(1)

获取所有key,时间复杂度O(n)

```shell
# 通常不在生产环境使用
keys *
# 1) "hello"
```

获取所有key总数

```shell
# 计算key总数
dbsize
# (integer) 1
```

判断key是否存在

```shell
exists key hello
# (integer) 1
```

删除一个key

```shell
del hello
# (integer) 1
```

设置key的过期时间

```shell
# 设置过期时间,20秒
expire hello 20
# (integer) 1

# 查看key过期时间
ttl hello
# (integer) 6
# (integer) -2 key已不存在
# (integer) -1 无过期时间

# 去掉key的过期时间
persist hello
# (integer) 1
```

返回key的类型

```shell
type hello
# string
```

### 字符串

#### 字符串应用场景

- 缓存
- 分布式锁
- 计数器

#### 字符串基本语法

设置

```shell
set hello world
# OK
```

获取

```shell
get hello
# "world"
```

删除

```shell
del hello
# (integer) 1
```

自增

```shell
incr count
# (integer) 1

incr count
# (integer) 2

incrby count 10
# (integer) 12

# 浮点
set float 10
# OK
incrbyfloat float 0.5
# "10.5"

decr count
# (integer) 11

decrby count 11
# (integer) 0

decr count
# (integer) -1

get count
# "-1"
```

设置字符串,key不存在才设置

```shell
setnx count hi
# (integer) 0 key已存在

setnx hi hi
# (integer) 1 key不存在
```

设置字符串,key存在才设置

```shell
set hi world xx
# OK key已存在

set nihao world xx
# (nil) key不存在
```

批量操作,时间复杂度O(n)

```shell

mset hi hi hello hello nihao nihao
# OK
mget hi hello nihao
# 1) "hi"
# 2) "hello"
# 3) "nihao"
```

设置新值并返回旧值

```shell
getset hi hello
# "hi"
```

追加

```shell
append hi ',hi'
# (integer) 8
```

返回字符串长度

```shell
strlen hi
# (integer) 8

get hi
# "hello,hi"

set hi '嗨'
# OK
get hi
# "\xe5\x97\xa8"
strlen hi
# (integer) 3
```

通过下标获取,设置字符串

```shell
get hi
# "hello,hi"
getrange hi 6 7
# "hi"
setrange hi 7 0
# (integer) 8
get hi
# "hello,h0"
```

#### 字符串实际应用

记录网站每个用户个人主页的访问量

```shell
# 单线程,无竞争
incr userid:pageview
```

缓存视频的基本信息(数据源在MySQL中)

### hash

#### hash基本语法

设置

```shell
hset user:1:info name mike age 23
# (integer) 2
```

获取

```shell
hget user:1:info name
# "mike"
```

获取所有,时间复杂度O(n)

```shell
hgetall user:1:info
# 1) "name"
# 2) "mike"
# 3) "age"
# 4) "23"
```

获取所有键,时间复杂度O(n)

```shell
hkeys user:1:info
# 1) "name"
# 2) "age"
```

获取所有值,时间复杂度O(n)

```shell
hvals user:1:info
# 1) "mike"
# 2) "23"
```

删除

```shell
hdel user:1:info age
# (integer) 1
```

判断是否存在

```shell
hexists user:1:info name
# (integer) 1
```

获取长度

```shell
hlen user:1:info
# (integer) 1
```

批量操作,时间复杂度O(n)

```shell
hmset user:1:info name mike age 23
# OK

hmget user:1:info name age
# 1) "mike"
# 2) "23"
```

自增

```shell
hincrby user:1:info pageview 1
# (integer) 1
```

#### hash实际应用

记录网站每个用户个人主页的访问量

```shell
hincrby user:1:info pageview count
```

### list

#### list基本语法

右端插入,时间复杂度O(1~n)

```shell
rpush listkey c b a
# (integer) 3
```

获取整个列表

```shell
lrange listkey 0 -1
# 1) "c"
# 2) "b"
# 3) "a"
```

左端插入,时间复杂度O(1~n)

```shell

lpush listkey c b a
# (integer) 3
# 1) "a"
# 2) "b"
# 3) "c"
```

在值前后插入,时间复杂度O(n)

```shell
linsert listkey before b 1
# (integer) 4
# a1bc

linsert listkey after b 2
# (integer) 5
# a1b2c
```

左边弹出

```shell
lpop listkey
# "a"
```

右边弹出

```shell
rpop listkey
# "c"
```

批量删除某个值,时间复杂度O(n)

```shell
# abcabcabc,从左开始,删除两个b
lrem listkey 2 b
# (integer) 2
#  acacabc

# abcabcabc,从右开始,删除两个c
lrem listkey -2 c
# (integer) 2
# abcabab

# abcabcabc,删除所有a
lrem listkey 0 a
# (integer) 3
# bcbcbc
```

修剪列表,时间复杂度O(n)

```shell
# abcdefg
ltrim listkey 1 3
# OK
# bcd
```

根据索引获取item,时间复杂度O(n)

```shell
lindex listkey 0
# "b"
```

获取长度

```shell
llen listkey
# (integer) 3
```

根据索引设置值,时间复杂度O(n)

```shell
# bcd
lset listkey 0 h
# OK
# hcd
```

blpop, brpop

```shell
blpop key timeout
# lpop阻塞版本,timeout是阻塞超时时间,为0永远不阻塞,brpop相同
```

#### list实际应用

- 时间轴,新内容lpush

```shell
# lpush + lpop = Stack
# lpush + rpop = Queue
# lpush + ltrin = Capped Collection
# lpush + Brpop = Message Queue
```

### set

#### set基本语法

添加

```shell
sadd user:1:follow it sport
# (integer) 2
```

删除

```shell
srem user:1:follow it
# (integer) 1
```

长度

```shell
scard user:1:follow
# (integer) 1
```

获取所有

```shell
smembers user:1:follow
# 1) "music"
# 2) "movie"
# 3) "sport"
```

判断是否存在

```shell
sismember user:1:follow sport
# (integer) 1
```

随机获取

```shell
# 随机获取两个
srandmember user:1:follow 2
# 1) "it"
# 2) "movie"
```

随机弹出

```shell
# 弹出的元素已不在集合中
spop user:1:follow
# "it"
```

集合间的API

```shell
sadd user:1:follow it music his sports
sadd user:2:follow it news ent sports

# 差集
sdiff user:1:follow user:2:follow
# 1) "music"
# 2) "his"

# 交集
sinter user:1:follow user:2:follow
# 1) "sports"
# 2) "it"

# 并集
sunion user:1:follow user:2:follow
# 1) "ent"
# 2) "music"
# 3) "it"
# 4) "news"
# 5) "his"
# 6) "sports"
```

#### set实际应用

- 用户like,赞,踩
- 抽奖系统
- 标签
- 共同关注

### zset

#### zset基本语法

添加,时间复杂度O(logN)

```shell
zadd user:1:ranking 1 kris 225 tom
# (integer) 2
```

删除

```shell
zrem user:1:ranking 1 kris
# (integer) 1
```

返回分数

```shell
zscore user:1:ranking tom
# "225"
```

加减分数

```shell
zincrby user:1:ranking -10 tom
# "215"
zincrby user:1:ranking 10 mike
# "10"
```

返回元素个数

```shell
zcard user:1:ranking
# (integer) 2
```

返回排名

```shell
zrank user:1:ranking tom
# (integer) 1
zrank user:1:ranking mike
# (integer) 0
```

返回指定索引范围内的元素(升序),时间复杂度O(log(n)+m)

```shell
zrange user:1:ranking 0 -1 withscores
# 1) "mike"
# 2) "10"
# 3) "tom"
# 4) "215"
```

返回指定分数范围内的元素(升序),时间复杂度O(log(n)+m)

```shell
zrangebyscore user:1:ranking 200 225
# 1) "tom"
```

返回指定分数范围内的元素个数,时间复杂度O(log(n)+m)

```shell
zcount user:1:ranking 200 225
# (integer) 1
```

删除指定索引范围内的元素(升序),时间复杂度O(log(n)+m)

```shell
zremrangebyrank user:1:ranking 0 1
# (integer) 2
```

删除指定分数范围内的元素(升序),时间复杂度O(log(n)+m)

```shell
zremrangebyscore user:1:ranking 1 10
# (integer) 1
```

#### 实际应用

- 排行榜

## Redis功能

### 慢查询

####　命令执行的生命周期

> 发送命令-排队-执行命令(慢查询发生的阶段)-返回结果
> 客户端超时不一定慢查询

####　慢查询定义

- 先进先出队列
- 固定长度
- 保存在内存中

####　慢查询配置

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

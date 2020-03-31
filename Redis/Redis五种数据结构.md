# Redis五种数据结构

## 基础

### Redis 是一个基于内存的高性能key-value数据库

### 为什么Redis是单线程的

```shell
Redis是基于内存的操作,CPU不是Redis的瓶颈,Redis的瓶颈最有可能是机器内存的大小或者网络带宽.既然单线程容易实现,而且CPU不会成为瓶颈,那就顺理成章地采用单线程的方案了
```

### Redis是单线程的,但Redis为什么这么快

```shell
1、完全基于内存,绝大部分请求是纯粹的内存操作,非常快速.数据存在内存中,类似于HashMap,HashMap的优势就是查找和操作的时间复杂度都是O(1)

2、数据结构简单,对数据操作也简单,Redis中的数据结构是专门进行设计的

3、采用单线程,避免了不必要的上下文切换和竞争条件,也不存在多进程或者多线程导致的切换而消耗 CPU,不用去考虑各种锁的问题,不存在加锁释放锁操作,没有因为可能出现死锁而导致的性能消耗

4、使用多路I/O复用模型,非阻塞IO;这里"多路"指的是多个网络连接,"复用"指的是复用同一个线程

5、使用底层模型不同,它们之间底层实现方式以及与客户端之间通信的应用协议不一样,Redis直接自己构建了VM 机制
```

### Redis相比memcached有哪些优势

```shell
memcached所有的值均是简单的字符串,redis作为其替代者,支持更为丰富的数据类型

redis的速度比memcached快很多

redis可以持久化其数据
```

### redis通讯协议

```shell
RESP 是redis客户端和服务端之前使用的一种通讯协议;

RESP 的特点：实现简单、快速解析、可读性好
```

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

Redis info查看命令

```shell
info memory
```

清空数据库

```shell
flushall
```

## 字符串

### 字符串应用场景

```shell
缓存
分布式锁
计数器
```

### 字符串基本语法

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

### 字符串实际应用

```shell
记录网站每个用户个人主页的访问量
# 单线程,无竞争
# incr userid:pageview

缓存视频的基本信息(数据源在MySQL中)
```

## hash

### hash基本语法

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

### hash实际应用

```shell
记录网站每个用户个人主页的访问量
# hincrby user:1:info pageview count
```

## list

### list基本语法

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

### list实际应用

```shell
时间轴,新内容lpush

# lpush + lpop = Stack
# lpush + rpop = Queue
# lpush + ltrin = Capped Collection
# lpush + Brpop = Message Queue
```

## set

### set基本语法

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

### set实际应用

```shell
用户like,赞,踩
抽奖系统
标签
共同关注
```

## zset

### zset基本语法

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

### 实际应用

```shell
排行榜
```

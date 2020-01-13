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

以下命令的时间复杂度,除`keys`为O(n)外,其他都为O(1)

```shell
# 通常不在生产环境使用
keys *
# 1) "hello"

# 计算key总数
dbsize
# (integer) 1

exists key hello
# (integer) 1

del hello
# (integer) 1

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

# 返回key的类型
type hello
# string
```

## 字符串

### 应用场景

- 缓存
- 分布式锁
- 计数器

### 基本语法

```shell
set hello world
# OK

get hello
# "world"

del hello
# (integer) 1

# 自增
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

# key不存在才设置
setnx count hi
# (integer) 0 key已存在

setnx hi hi
# (integer) 1 key不存在

# key存在才设置
set hi world xx
# OK key已存在

set nihao world xx
# (nil) key不存在

# 批量操作(O(n))
mset hi hi hello hello nihao nihao
# OK
mget hi hello nihao
# 1) "hi"
# 2) "hello"
# 3) "nihao"

# 设置新值并返回旧值
getset hi hello
# "hi"

# 追加
append hi ',hi'
# (integer) 8

# 返回字符串长度
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

get hi
# "hello,hi"
getrange hi 6 7
# "hi"
setrange hi 7 0
# (integer) 8
get hi
# "hello,h0"
```

### 实际应用

记录网站每个用户个人主页的访问量

```shell
# 单线程,无竞争
incr userid:pageview
```

缓存视频的基本信息(数据源在MySQL中)

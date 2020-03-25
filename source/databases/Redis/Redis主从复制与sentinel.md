# Redis主从复制与sentinel

## 主从复制

1. 数据副本
2. 扩展读性能

```shell
一个master可以有多个slave
一个slave只能有一个master
数据流向是单向的,master到slave
```

### 主从复制的实现

可以通过命令或者修改配置文件实现

#### slaveof命令

```shell
# 成为127.0.0.1 6379的从节点
slaveof 127.0.0.1 6379

# 取消从节点,数据不会删除,重新成为从节点时会清除当前所有数据
slaveof no one
```

####　配置

```shell
slaveof ip port
# 只读
slave-read-only yes
```

### 单机实现

```shell
# 复制配置文件
[root@izbp128jigdcjx00os4h3sz config]# cp redis-6379.conf

# 修改端口等信息为6380
[root@izbp128jigdcjx00os4h3sz config]# sed 's/6379/6380/g' -i redis-6380.conf redis-6380.conf

# 启动6380服务器(6379已启动)
[root@izbp128jigdcjx00os4h3sz config]# ../bin/redis-server redis-6380.conf

# 进入6380客户端
[root@izbp128jigdcjx00os4h3sz bin]# ./redis-cli -p 6380

# 查看分片
127.0.0.1:6380> info replication
# Replication
role:master
connected_slaves:0

# 添加一个key
127.0.0.1:6380> sadd test a b c d e
(integer) 5

# 设置为6379的slave
127.0.0.1:6380> slaveof 127.0.0.1 6379
OK

# 再次查看分片
127.0.0.1:6380> info replication
# Replication
role:slave
master_host:127.0.0.1
master_port:6379
master_link_status:up
master_last_io_seconds_ago:4
master_sync_in_progress:0
slave_repl_offset:56
slave_priority:100
slave_read_only:1
connected_slaves:0

# 原6380上的keys已清除
127.0.0.1:6380> smembers test
(empty list or set)

# 6379的数据已复制
127.0.0.1:6380> dbsize
(integer) 11

# replica-read-only yes 配置为这个,6380无法写入数据
127.0.0.1:6380> set a aa
(error) READONLY You can't write against a read only replica.

# 查看6379
127.0.0.1:6379> info replication
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6380,state=online,offset=756,lag=1
master_replid:25e95610a7c14b74ab86f253cf63d7a23451cb53
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:756
```

### 全量复制

runid: 每次启动分配的id,重启会改变,(即可能引发全量复制)

主从复制的同时,这期间写入的数据会在缓冲区记录下来,同样发送给从节点,保证数据一致

全量复制的开销

```shell
bgsave时间
RDB文件网络传输时间
从节点清除数据时间
从节点加载RDB的时间
可能的AOF重写时间(如果开启)
```

### 主从复制常见问题

#### 读写分离

读写分析: 读流量分摊到从节点
可能遇到的问题

- 复制数据延迟
- 读到过期数据
- 从节点故障

#### 配置不一致

1. 例如maxmemory不一致:丢失数据
2. 例如数据结构优化参数(例如hash-max-ziplist-entries):内存不一致

#### 规避全量复制

1. 第一次全量复制
    - 第一次不可避免
    - 小主节点,低峰

2. 节点运行ID不匹配
    - 主节点重启(运行ID变化)
    - 故障转移,例如哨兵或集群

3. 复制积压缓冲区不足
    - 网络中断,部分复制无法满足
    - 增大复制缓冲区配置rel_backlog_size,网络增强

#### 规避复制风暴

单主节点复制风暴

```shell
问题: 主节点重启,多从节点复制
解决: 更换复制拓扑
```

单机器复制风暴

```shell
机器宕机后,大量全量复制
主节点分散多机器
```

## sentinel

### 主从复制是否高可用

主从复制问题

```shell
故障只能手动转移
写能力和存储能力受限
```

### Redis sentinel架构

### Redis sentinel故障转移

```shell
多个sentinel发现并确认master有问题
选举出一个sentinel作为领导
选出一个slave作为master
通知其余slave成为新的master的slave
通知客户端主从变化
等待老的master复活成为新master的slave
```

### Redis sentinel配置

1. 配置开启主从节点
2. 配置开启sentinel监控主节点(sentinel是特殊的redis)

```shell
# sentinel主要配置
port ${port}
dir "/opt/soft/redis/data/"
logfile "${port}.log"
# 主节点,2表示客观下线的sentinel投票数量
sentinel monitor mymaster 172.0.0.1 7000 2
# 判断时限,30秒
sentinel down-after-milliseconds mymaster 30000
# 故障转移时新master同一时间传输快照给slave数量
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
```

### Redis sentinel三个定时任务

1. 每10秒每个sentinel对master和slave执行info
   1. 发现slave节点
   2. 确认主从关系

2. 每2秒每个sentinel通过master节点的channel交换信息(pub/sub)
   1. 通过__sentinel__:hello频道交互
   2. 交互对节点的'看法'和自身信息

3. 每1秒每个sentinel对其他sentinel和redis执行ping

### 主观下线和客观下线

```shell
sentinel monitor <mastername> <ip> <port> <quorum>
sentinel down-after-milliseconds <mastername> <timeout>
# 主观下线: 每个sentinel节点对redis节点失败的'偏见'
# 客观下线: 所有sentinel节点对redis节点失败'达成共识'(超过quorum个统一)
```

### 领导者选举

```shell
原因:只有一个sentinel节点完成故障转移
选举:通过sentinel is-master-down-by-addr命令都希望成为领导者
每个做主观下线的sentinel节点向其他sentinel节点发送命令,要求将它设置为领导者
收到命令的sentinel节点如果没有同意其他sentinel节点发送的命令,那么将同意该请求,否则拒绝
如果该sentinel节点发现自己的票数已经超过sentinel集合半数而且超过quorum,那么它将成为领导者
如果此过程有多个sentinel节点成为了领导者,那么将等待一段时间重新进行选举
```

### 故障转移(sentinel领导者节点完成)

```shell
从slave节点中选出一个合适的节点作为新的master节点
对上面的slave节点执行slaveof no one命令让其成为master节点
向剩余的slave节点发送命令,让它们成为新master节点的slave节点,复制规则和parallel-syncs参数有关
更新对原来master节点配置为slave,并保持着对其'关注',当恢复后命令它去复制新的master节点
```

#### 选择'合适的'slave节点

```shell
选择slave-priority(slave节点优先级)最高的slave节点,如果存在则返回,不存在则继续
选择复制偏移量最大的slave节点(复制的最完整),如果存在则返回,不存在则继续
选择runid最小的slave节点
```

### 节点运维

```shell
从节点:临时下线还是永久下线,是否做一些清理工作,要考虑读写分离的情况
sentinel节点:同上
```

#### 节点上线

```shell
主节点: sentinel failover 进行替换
从节点: slaveof即可,sentinel节点可以感知
sentinel节点: 参考其他sentinel节点启动即可
```

### sentinel实操

redis主节点配置

```shell
cd /usr/local/redis/config
tee redis-7000.conf <<-'EOF'
port 7000
daemonize yes
pidfile /var/run/redis-7000.pid
logfile "7000.log"
dir "/usr/local/redis/data"
EOF
```

配置2个从节点

```shell
# 配置第一个
sed 's/7000/7001/g' redis-7000.conf>redis-7001.conf
echo 'slaveof 127.0.0.1 7000' >> redis-7001.conf

# 配置第二个
sed 's/7001/7002/g' redis-7001.conf>redis-7002.conf
```

开启三个redis节点

```shell
/usr/local/redis/bin/redis-server redis-7000.conf
/usr/local/redis/bin/redis-server redis-7001.conf
/usr/local/redis/bin/redis-server redis-7002.conf
```

配置三个sentinel

```shell
# 配置第一个
tee redis-sentinel-26379.conf <<-'EOF'
port 26379
daemonize yes
dir "/usr/local/redis/data"
logfile "26379.log"
sentinel monitor mymaster 127.0.0.1 7000 2
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
EOF

# 配置另外两个
sed 's/26379/26380/g' redis-sentinel-26379.conf>redis-sentinel-26380.conf
sed 's/26379/26381/g' redis-sentinel-26379.conf>redis-sentinel-26381.conf
```

开启sentinel

```shell
/usr/local/redis/bin/redis-sentinel redis-sentinel-26379.conf
/usr/local/redis/bin/redis-sentinel redis-sentinel-26380.conf
/usr/local/redis/bin/redis-sentinel redis-sentinel-26381.conf
```

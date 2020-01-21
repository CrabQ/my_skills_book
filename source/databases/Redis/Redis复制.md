# Redis复制

## 主从复制

1. 数据副本
2. 扩展读性能

```shell
一个master可以有多个slave
一个slave只能有一个master
数据流向是单向的,master到slave
```

### 主从复制的实现

slaveof命令

```shell
# 成为127.0.0.1 6379的从节点
slaveof 127.0.0.1 6379

# 取消从节点,数据不会删除,重新成为从节点时会清除当前所有数据
slaveof no one
```

配置

```shell
slaveof ip port
# 只读
slave-read-only yes
```

### 全量复制

主从复制的同时,这期间写入的数据会在缓冲区记录下来,同样发送给从节点,保证数据一致

全量复制的开销

```shell
bgsave时间
RDB文件网络传输时间
从节点清楚数据时间
从节点夹在RDB的时间
可能的AOF重写时间
```

部分复制

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
# 判断时限
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
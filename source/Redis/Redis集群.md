# Redis集群

## 数据分布概论

### 哈希分区

#### 节点取余:hash(key)%nodes

```shell
客户端分片方式: 哈希 + 取余
节点伸缩: 数据节点关系变化,导致数据迁移
迁移数量和添加节点数量有关,建议翻倍扩容
# 不推荐这种方式
```

#### 一致性哈希

```shell
客户端分片方式: 哈希 + 顺时针(优化取余)
节点伸缩: 只影响临近节点,但还是有数据迁移
翻倍伸缩: 保证最小迁移数据和负载均衡(不翻倍的话节点承载的数据量大小会不一致)
```

#### 虚拟槽分区

```shell
预设虚拟槽: 每个槽映射一个数据子集,一般比节点数大
良好的哈希函数: 例如CRC16
服务端管理节点,槽,数据: 例如Reids Cluster
```

## Redis Cluster架构

```shell
节点
meet
指派槽
复制
```

### Redis Cluster 特性

```shell
复制
高可用
分片
```

## Redis Cluster 安装

### 原生命令安装

配置开启redis

```shell
port ${port}
daemonize yes
dir "/opt/soft/redis/data/"
dbfilename "dump-${port}.rdb"
logfile "${port}.log"
cluster-enabled yes
cluster-config-file nodes-${port}.conf

# redis-server redis-700[0-5].conf
```

meet

```shell
# cluster meet ip port
redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 700[1-5]
```

Cluster节点主要配置

```shell
cluster-enabled yes
cluster-node-timeout 15000
cluster-config-file  "nodes.conf"
# 是否全部没问题才判断集群为正常
cluster-require-full-coverage yes
```

分配槽

```shell
# cluster addslots slot [slot...]
redis-cli -h 127.0.0.1 -p 7000 cluster addslots {0..5461}
redis-cli -h 127.0.0.1 -p 7001 cluster addslots {5462..10922}
redis-cli -h 127.0.0.1 -p 7002 cluster addslots {10923..16383}
```

设置主从

```shell
#   node-id
redis-cli -h 127.0.0.1 -p 7003   ${node-id-7000}
redis-cli -h 127.0.0.1 -p 7004   ${node-id-7001}
redis-cli -h 127.0.0.1 -p 7005   ${node-id-7002}
```

### 原生命令安装实操

redis节点配置并开启

```shell
cd /usr/local/redis/config
tee redis-7000.conf <<-'EOF'
port 7000
daemonize yes
logfile "7000.log"
dbfilename "dump-7000.rdb"
dir "/usr/local/redis/data"
cluster-enabled yes
cluster-config-file nodes-7000.conf
cluster-require-full-coverage no
EOF

# 开启第一个节点
/usr/local/redis/bin/redis-server redis-7000.conf

# 配置剩余五个
sed 's/7000/7001/g' redis-7000.conf>redis-7001.conf
sed 's/7000/7002/g' redis-7000.conf>redis-7002.conf
sed 's/7000/7003/g' redis-7000.conf>redis-7003.conf
sed 's/7000/7004/g' redis-7000.conf>redis-7004.conf
sed 's/7000/7005/g' redis-7000.conf>redis-7005.conf

# 开启剩余五个
/usr/local/redis/bin/redis-server redis-7001.conf
/usr/local/redis/bin/redis-server redis-7002.conf
/usr/local/redis/bin/redis-server redis-7003.conf
/usr/local/redis/bin/redis-server redis-7004.conf
/usr/local/redis/bin/redis-server redis-7005.conf
```

meet

```shell
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7001
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7002
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7003
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7004
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7005

# 查看信息
../bin/redis-cli -p 7003 cluster nodes
../bin/redis-cli -p 7003 cluster info
```

分配槽

```shell
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster addslots {0..5461}
../bin/redis-cli -h 127.0.0.1 -p 7001 cluster addslots {5462..10922}
../bin/redis-cli -h 127.0.0.1 -p 7002 cluster addslots {10923..16383}

# 查看槽
 ../bin/redis-cli -p 7003 cluster slots
```

分配主从

```shell
# 查看信息,获取node id
../bin/redis-cli -p 7003 cluster nodes

# 设置主从关系
 ../bin/redis-cli -h 127.0.0.1 -p 7003   a41fdbabdcc54537ec1d7c2ff50b57040805115e
 ../bin/redis-cli -h 127.0.0.1 -p 7004   4fdec72ee9a578a75c46f680eabbde8561787905
 ../bin/redis-cli -h 127.0.0.1 -p 7005   8dd8e77d53c59030596f6fd5a97d52e1b6aa9746
```

检验是否开启成功

```shell
 ../bin/redis-cli -c -p 7003
127.0.0.1:7003>  set hi hello
-> Redirected to slot [16140] located at 127.0.0.1:7002
OK
```

### 官方工具安装

`redis-trib.rb`已弃用,直接使用`redis-cli --cluster`即可

```shell
# 配置同上
# 开启6个服务器
/usr/local/redis/bin/redis-server redis-7000.conf
/usr/local/redis/bin/redis-server redis-7001.conf
/usr/local/redis/bin/redis-server redis-7002.conf
/usr/local/redis/bin/redis-server redis-7003.conf
/usr/local/redis/bin/redis-server redis-7004.conf
/usr/local/redis/bin/redis-server redis-7005.conf

# 创建集群
# --cluster-replicas 1 主节点数/从节点数的比例,按照命令中IP:PORT的顺序,先3主,后3从
/usr/local/redis/bin/redis-cli --cluster create  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1
```

#### docker方式部署

[Centos8下redis cluster部署](https://my-skills-book.readthedocs.io/en/latest/Docker/Docker%E5%BA%94%E7%94%A8%E9%83%A8%E7%BD%B2.html#centos8redis-cluster)

## 集群伸缩

集群伸缩远离

```shell
集群伸缩=槽和数据在节点之间的移动
```

### 扩展集群

准备新节点

```shell
集群模式启动
配置和其他节点统一
启动后是孤儿节点
redis-server conf/redis-7006.conf
```

加入集群

```shell
# redis-cli --cluster add-node new_host:new_port existing_host:existing_port --salve --master-id <arg>
redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000
```

迁移槽和数据

原理

```shell
1. 对目标节点发送 cluster setslot {slot} importing {sourceNodeId} 命令,让目标节点准备导入槽的数据
2. 对源节点发送 cluster setslot {slot} migrating {targetNdoeId} 命令,让源节点准备迁出槽的数据
3. 源节点循环执行 cluster getkeysinslot {slot} {count} 命令,每次获取count个属于槽的键
4. 在源节点执行 migrate {targetIp} {targetPort} key 0 {timeout} 命令把指定key迁移
5. 重复执行步骤3-4直到槽下所有数据迁移到目标节点
6. 向集群所有节点发送 cluster setslot {slot} node {targetNodeId} 命令,通知槽分配给目标节点
```

#### 扩展集群实操

```shell
# 添加两个节点7006, 7007(从节点)
# 添加两个配置文件
cd /usr/local/redis/config
sed 's/7000/7006/g' redis-7000.conf>redis-7006.conf
sed 's/7000/7007/g' redis-7000.conf>redis-7007.conf

# 启动
/usr/local/redis/bin/redis-server redis-7006.conf
/usr/local/redis/bin/redis-server redis-7007.conf

# 查看7006为孤儿节点
../bin/redis-cli -p 7006 cluster nodes

# 添加到集群
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7006
../bin/redis-cli -h 127.0.0.1 -p 7000 cluster meet 127.0.0.1 7007

# 添加主从
../bin/redis-cli -h 127.0.0.1 -p 7007 cluster replicate a6ec55d7c47c17a294436923190fec898cb2fb11

# 分配槽
../bin/redis-cli --cluster reshard 127.0.0.1:7000
# 输入分配槽个数 4096
# 7006的node id
# all 所有槽重新分配
```

### 收缩集群

```shell
下线迁移槽
忘记节点 cluster forget {downNodeId}
关闭节点
```

#### 收缩集群实操

```shell
# 下线节点7006,7007

# 迁移7006的槽到7000,7001,7002
../bin/redis-cli --cluster reshard  --cluster-from a6ec55d7c47c17a294436923190fec898cb2fb11 --cluster-to 9e47369e0d3760e86478e0f59cba5bbb020d3b46 --cluster-slots 1366 127.0.0.1 7006

../bin/redis-cli --cluster reshard  --cluster-from a6ec55d7c47c17a294436923190fec898cb2fb11 --cluster-to 3beb178f1f60ad27cc3a87640f2257dd29be5551 --cluster-slots 1366 127.0.0.1 7006

../bin/redis-cli --cluster reshard  --cluster-from a6ec55d7c47c17a294436923190fec898cb2fb11 --cluster-to 04aea196f8c76cd988c6225309b16a92eea55a9d --cluster-slots 1366 127.0.0.1 7006

# 删除节点,先从后主,不然会触发故障转移
../bin/redis-cli --cluster del-node 127.0.0.1:7000 6f5b25d89a75f38cca23bb896e3e86bcf1047db8

../bin/redis-cli --cluster del-node 127.0.0.1:7000 a6ec55d7c47c17a294436923190fec898cb2fb11
```

### moved重定向

```shell
# 设置键值时,如果当前键的槽不在对应节点,返回moved重定向(moved 槽 槽对应节点)
# 计算槽
cluster keyslot php
# redis-cli -c 使用集群模式,槽未命中时自动切换,不使用则会报错
# 槽已确定迁移
```

### ask重定向

```shell
# 客户端获取键值时,键对应的槽已迁移至其他节点,会返回ask重定向
# 槽还在迁移过程中(不确定是否迁移)
```

### smart客户端:追求性能

### 批量操作优化

```shell
# mget mset操作
1. 串行mget 即相当于for循环一个个操作 网络IO O(keys)
2. 串行IO 先本地计算槽 O(nodes)
3. 并行IO 2基础上并行 一次网络时间O(max_slow(node))
4. hash_tag 全部key包装成hash,一次发送给一个节点 O(1)
```

## 故障转移

### 故障发现

```shell
通过ping/pong消息实现故障发现,不需要sentinel
主观下线: 某个节点认为另一个节点不可用, '偏见'
客观下线: 当半数以上持有槽的主节点都标记某节点主观下线

客观下线作用:
通过集群内所有节点标记故障节点为客观下线
通过故障节点的从节点触发故障转移流程
```

### 故障恢复

资格检查

```shell
每个从节点检查与故障主节点的断线时间
超过cluster-node-timeout * cluster-slave-validity-factor取消资格
cluster-slave-validity-factor 默认是10
```

准备选举时间

```shell
断线时间越短,偏移量越大的从节点,选举时间越短,越有可能成为主节点
```

选举投票

```shell
超过半数+1即为选举成功
```

替换主节点

```shell
1. 当前从节点取消复制变为主节点(slaveof no one)
2. 执行clusterDelSlot撤销故障主节点负责的槽,并执行clusterAddSlot把这些槽分配给自己
3. 向集群广播自己的pong消息,表明已经替换了故障从节点
```

## Redis Cluster开发运维常见问题

### 集群完整性

```shell
cluster-require-full-coverage默认为yes
集群中16384个槽全部可用:保证集群完整性
节点故障或故障转移中:
(error)CLUSTERDOWN The cluster is down
```

### 带宽消耗

官方建议:1000个节点

三个方面

```shell
消息发送频率: 节点发现与其他节点最后通信时间超过cluster-node-timeout/2时会直接发送ping消息
消息数据量: slots槽数组(2KB空间)和整个集群1/10的状态数据(10个节点状态数据约1KB)
节点部署的机器规模: 集群分布的机器越多且每台机器划分的节点数越均匀,则集群内整体的可用带宽越高
```

一个例子

```shell
规模: 节点200个,20台物理机(每台10个节点)
cluster-node-timeout=15000, ping/pong带宽为25Mb
cluster-node-timeout=20000, ping/pong带宽低于15Mb
```

优化

```shell
避免'大'集群: 避免多业务使用一个集群,大业务可以多集群
cluster-node-timeout: 带宽和故障转移速度的均衡
尽量均匀分配到多机器上: 保证高可用和带宽
```

### Pub/Sub广播

```shell
问题: publish在集群每个节点广播:加重带宽
解决: 单独走一套Redis Sentinel
```

### 数据倾斜

节点和槽分配不均

```shell
redis-cli --cluster info ip:port 查看节点,槽,键值分布
redis-cli --cluster rebalance ip:port 进行均衡(谨慎使用)
```

不同槽对应键值数量差异较大

```shell
CRC16正常情况下比较均匀
可能存在hash_tag
cluster countkeysinslot {slot} 获取槽对应键值个数
```

包含bigkey

```shell
bigkey: 例如大字符串,几百万的元素的hash,set等
从节点: redis-cli --bigkeys
优化: 优化数据结构
```

内存相关配置不一致

```shell
hast-max-ziplist-value, set-max-intest-entries等
优化: 定期'检查'配置一致性
```

### 请求倾斜

```shell
热点key: 重要的key或者bigkey
优化:
避免bigkey
热键不要用hash_tag
当一致性不高时,可以用本地缓存+MQ
```

### 读写分离

```shell
只读连接: 集群模式的从节点不接受任何读写请求
重定向到负责槽的主节点
readonly命令可以读:连接级别命令(争对当前连接)

读写分离:更加复杂
复制延迟,读取过期数据,从节点故障
修改客户端: cluster slaves {NodeId}
不建议
```

### 数据迁移

```shell
官方迁移工具: rdis-cli --cluster import
只能从单机迁移到集群
不支持在线迁移: source需要停写
不支持断电续传
单线程迁移: 影响速度

在线迁移:
唯品会 redis-migrate-tool
豌豆荚 redis-port
```

### 集群vs单机

集群限制

```shell
key批量操作支持有限: 例如mget,mset必须在一个slot
key事务和Lua支持有限: 操作的key必须在一个节点
key是数据分区的最小粒度: 不支持bigkey分区
不支持多个数据库: 集群模式下只有一个db 0
复制只支持一层: 不支持树形复制结构
```

分布式redis不一定好

```shell
1. Redis Cluster: 满足容量和性能的扩展性,很多业务'不需要'
大多数客户端性能会'降低'
命令无法跨节点使用: mget,keys,scan,flush,sinter等
Lua和事务无法跨节点使用
客户端维护更复杂: SDK和应用本身消耗(例如更多的连接池)

2. 很多场景Redis Sentinel已经足够好
```

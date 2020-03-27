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
# cluster replicate node-id
redis-cli -h 127.0.0.1 -p 7003 cluster replicate ${node-id-7000}
redis-cli -h 127.0.0.1 -p 7004 cluster replicate ${node-id-7001}
redis-cli -h 127.0.0.1 -p 7005 cluster replicate ${node-id-7002}
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
 ../bin/redis-cli -h 127.0.0.1 -p 7003 cluster replicate a41fdbabdcc54537ec1d7c2ff50b57040805115e
 ../bin/redis-cli -h 127.0.0.1 -p 7004 cluster replicate 4fdec72ee9a578a75c46f680eabbde8561787905
 ../bin/redis-cli -h 127.0.0.1 -p 7005 cluster replicate 8dd8e77d53c59030596f6fd5a97d52e1b6aa9746
```

检验是否开启成功

```shell
 ../bin/redis-cli -c -p 7003
127.0.0.1:7003>  set hi hello
-> Redirected to slot [16140] located at 127.0.0.1:7002
OK
```

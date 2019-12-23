# Redis实例

```python
import redis

# decode_responses=True写入的键值对中的value为str类型,False为字节类型。
db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
```

## List操作

列表内的元素可以重复，可以从两端存储

```python
# 向列表尾添加元素
db.rpush(REDIS_KEY, dumps(request))

# 返回并删除列表头元素
db.lpop(REDIS_KEY)

# 返回列表长度
db.llen(REDIS_KEY)
```

## Sorted Set操作

有序集合,集合中的元素都是不重复的,且有分值

```python
# 返回proxy分数
db.zscore(REDIS_KEY, proxy)

# 返回集合REDIS_KEY里的元素个数
db.zcard(REDIS_KEY)

# 添加分数为score的proxy
db.zadd(REDIS_KEY, {proxy:SCORE})

# 添加proxy，分数为-1，如果已存在proxy，则score=score+(-1)
db.zincrby(REDIS_KEY, -1, proxy)

# 删除proxy元素
db.zrem(REDIS_KEY, proxy)

# 返回分数为1-10之间的元素
db.zrangebyscore(REDIS_KEY, 1, 10)

# 返回第1到100个元素，(按score从大到小排序)
db.zrevrange(REDIS_KEY, 0, 99)
```

## Hash操作

```python
# 增加一对映射
db.hset(key, username, value)

# 获取value
db.hget(key, username)

# 删除映射
db.hdel(key, username)

# 获取映射个数
db.hlen(key)

# 获取所有keys
db.hkeys(key)

# 获取所有values
db.hvals(key)

# 获取所有映射键值对
db.hgetall(key)
```

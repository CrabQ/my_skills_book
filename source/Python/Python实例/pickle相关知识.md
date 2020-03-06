# pickle相关知识

## TypeError: can't pickle _thread.RLock objects

参考[TypeError: can't pickle _thread.lock objects](https://blog.csdn.net/qq_38765321/article/details/88376031)
写爬虫时，打算把requests对象序列化之后存入redis,报错

```python
# 此句报错
self.db.rpush(REDIS_KEY, dumps(request))
TypeError: can't pickle _thread.lock objects
```

原因如下：
> pickle模块要对内部的成员变量进行序列化，但不支持对自定义对象加锁，所以会抛出类型异常的错误。

因为我初始化了自定义的类，导致错误

```python
class Spider():
    def __init__(self):
        # RedisQueue()为自定义的类
        self.queue = RedisQueue()
```

去掉初始化就可以了：

```python
class Spider():
    queue = RedisQueue()
```

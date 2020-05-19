# Python基础

## python的垃圾回收机制

```shell
# 1. 循环引用导致的内存泄露

l1 = [1]
l2 = [2]

l1.append(l2)
# l1 = [值1的内存地址, l2的内存地址]
print(id(l2))
print(id(l1[1]))

l2.append(l1)
# l2 = [值2的内存地址, l1的内存地址]
print(id(l1))
print(id(l2[1]))

del l1
del l2
# l1, l2循环引用,并没有被回收

# 2. 标记清除,解决循环引用
# 3. 隔代回收
```

## 整形之整数进制转换

```shell
# 转换为二进制
print(bin(10))
print(int('0b1010', 2))

# 转换为八进制
print(oct(10))
print(int('0o12', 8))

# 转换为十六进制
print(hex(10))
print(int('0xa', 16))

a = list({'1':1,'2':2})
print(a)
```

## 装饰器

```shell
import time
from functools import wraps

# 无参装饰器

def timer(func):
    # 将原函数的属性赋值给wrap函数
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'time:{time.time()-start}')
        return res
    return wrap

@timer
def run():
    time.sleep(1)
    print('running')

run()
print(run.__name__)

# 有参装饰器
def outer(name):
    def timer(func):
        # 将原函数的属性赋值给wrap函数
        @wraps(func)
        def wrap(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            print(f'{name}, time:{time.time()-start}')
            return res
        return wrap
    return timer

@outer('first')
def run():
    time.sleep(1)
    print('running')

run()
```

## 迭代器与生成器

```shell
# 迭代器
def my_iter(obj):
    iter_obj = obj.__iter__()
    while True:
        try:
            print(iter_obj.__next__())
        except StopIteration:
            break

my_iter((1,2,3,4))

# 自定义迭代器:生成器
def my_range(start, stop, step):
    while start<stop:
        yield start
        start += step

print(list(my_range(1, 10, 2)))

# send
def f1():
    l = []
    while True:
        k = yield 'aa'
        l.append(k)
        print(l)
        k = yield 'bb'
        l.append(k)
        print(l)

g = f1()
g.send(None)
print(g.send('1'))
print(g.send('2'))
```

## 三元表达式

```shell
print(1 if 1<2 else 2)
print(1 if 1>2 else 2)
```

## 列表生成式

```shell
l = [1,2,3,4,5]
print([x for x in l if x%2==1])
```

## 函数递归

```shell
# 函数递归

def f(n):
    if n == 1 or n ==2:
        return 1
    else:
        return f(n-1)+f(n-2)

print(f(5))
```

## 匿名函数lambda

```shell
# 匿名函数lambda以及max以及map以及filter
d = {'c':1, 'b':2, 'a':3}
print(max(d, key=lambda x: d[x]))
print(list(map(lambda x: x+100, [1,2,3])))
print(list(filter(lambda x: x>1, [1,2,3])))
```

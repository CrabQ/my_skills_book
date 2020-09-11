# Python并发编程

## 多进程

进程间的数据互相隔离

开启进程的两种方式

```python
# 方式1
from multiprocessing import Process
import os


def f():
    print(os.getpid(), os.getppid())


if __name__ == '__main__':
    p_list = []
    for i in range(10):
        target = Process(target=f)
        target.start()
        p_list.append(target)
    for p in p_list:
        p.join()
    print('master', os.getpid())

# 方式2
from multiprocessing import Process
import os


class f(Process):
    def run(self):
        print(os.getpid(), os.getppid())


if __name__ == '__main__':
    p_list = []
    for i in range(10):
        target = f()
        target.start()
        p_list.append(target)
    for p in p_list:
        p.join()
    print('master', os.getpid())
```

### 守护进程

```python
# 会随主进程结束而结束

# 守护进程内无法再开启子进程, 否则抛出异常AssertionError: daemonic processes are not allowed to have children

target = Process(target=f)
# 守护进程需要在start前设置
target.daemon = True
target.start()
```

### 使用多进程实现socket聊天并发

```python
# server
from multiprocessing import Process
from socket import *

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 13614))
server.listen(5)


def talk(conn):
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            conn.send(msg.upper())
        except:
            break


if __name__ == '__main__':
    while True:
        conn, client_addr = server.accept()
        p = Process(target=talk, args=(conn, client_addr))
        p.start()

# client
from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 13614))

if __name__ == '__main__':
    while True:
        msg = input('>>>: ').strip()
        if not msg:
            continue
        client.send(msg.encode('utf-8'))
        msg = client.recv(1024)
        print(msg.decode('utf-8'))
```

### 进程加锁

```python
import os
import random
import time
from multiprocessing import Process, Lock

def work(lock):
    lock.acquire()
    print(f'{os.getpid()} is running')
    time.sleep(random.randint(1,3))
    print(f'{os.getpid()} is done')
    lock.release()

if __name__ == '__main__':
    lock = Lock()
    for i in range(3):
        target = Process(target=work, args=(lock,))
        target.start()
```

### 进程间通信

#### 队列

管道和锁定实现

```shell
q.get_nowait() 同q.get(False)方法

q.qsize q.empty q.full 不太可靠
```

生产者消费者模型

```python
# 生产者消费者模式是通过一个容器来解决生产者和消费者的强耦合问题
# 生产者和消费者彼此之间不直接通讯, 而通过阻塞队列来进行通讯
import time
import random
import multiprocessing


def consumer(q):
    while True:
        time.sleep(random.randint(1, 3))
        res = q.get()
        if not res:
            break
        print('取出: ', res)


def producer(q):
    for i in range(5):
        q.put(f'包子{i}')
        print(f'生产: 包子{i}')


if __name__ == '__main__':
    queue = multiprocessing.Queue(3)

    c_list = []
    p = multiprocessing.Process(target=producer, args=(queue,))
    p.start()
    for i in range(2):
        c = multiprocessing.Process(target=consumer, args=(queue,))
        c.start()
        c_list.append(c)

    p.join()

    # 发送信号让消费者停止, 几个消费者就应该发送几次结束信号None
    queue.put(None)
    queue.put(None)
```

##### JoinableQueue

```python
# 与Queue对象基本相同, 还有如下方法
# q.task_done(): 使用者使用此方法发出信号, 表示q.get()返回的项目已经被处理
# q.join(): 生产者将使用此方法进行阻塞, 直到队列中所有项目均被处理, 阻塞将持续到为队列中的每个项目均调用q.task_done()方法为止

import time
import random
import multiprocessing


def consumer(q):
    while True:
        time.sleep(random.randint(1, 3))
        res = q.get()
        if not res:
            break
        print('取出: ', res)
        # 向q.join()发送一次信号, 表示一个数据被取走
        q.task_done()


def producer(q):
    for i in range(5):
        q.put(f'包子{i}')
        print(f'生产: 包子{i}')

    # 生产完毕, 阻塞主进程, 直到队列所有项目都被处理
    q.join()


if __name__ == '__main__':
    queue = multiprocessing.JoinableQueue(3)

    c_list = []
    p = multiprocessing.Process(target=producer, args=(queue,))
    p.start()
    for i in range(2):
        c = multiprocessing.Process(target=consumer, args=(queue,))
        c.daemon = True
        c.start()
        c_list.append(c)

    # p结束, 则表示消费者处理完毕, 可设置消费者为守护进程, 随主线程结束
    p.join()
```

## 多线程

```shell
两种开启方式: 与多进程类似
同一进程内的线程之间共享进程内的数据
```

### 使用多线程实现socket聊天并发

```python
# server
from socket import *
from threading import Thread

server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 12333))
server.listen(5)


def talk(conn):
    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        try:
            conn.send(msg.upper())
        except:
            break


if __name__ == '__main__':
    while True:
        conn, client_addr = server.accept()
        t = Thread(target=talk, args=(conn,))
        t.start()

# client
from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 12333))

if __name__ == '__main__':
    while True:
        msg = input(">>>: ")
        if not msg:
            continue
        client.send(msg.encode('utf-8'))
        msg = client.recv(1024)
        print(msg.decode('utf-8'))
```

## concurrent.futures

```shell
concurrent.futures模块提供了高度封装的异步调用接口

ThreadPoolExecutor: 线程池, 提供异步调用

ProcessPoolExecutor: 进程池, 提供异步调用
```

### ProcessPoolExecutor与ThreadPoolExecutor

```python
# ProcessPoolExecutor与ThreadPoolExecutor用法一致
from concurrent.futures import ProcessPoolExecutor
import os
import time
import random


def task(n):
    print(f"{os.getpid()} is running")
    time.sleep(random.randint(1, 3))
    return n * 2

def result(res):
    # result(timeout=None): 取得结果
    print(res.result())

if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers=3)
    for i in range(11):
        # 异步提交任务
        future = executor.submit(task, i).add_done_callback(result)

    # 取代for循环submit的操作
    # executor.map(task, range(1, 12))

    # shutdown(wait=True): 相当于进程池的pool.close()+pool.join()操作
    # wait=True, 等待池内所有任务执行完毕回收完资源后才继续, False立即返回,不等待池内的任务执行完毕
    # 不管wait参数为何值整个程序都会等到所有任务执行完毕, submit和map必须在shutdown之前
    executor.shutdown(True)
```

## 携程

### gevent

```python
# gevent模块先打补丁
from gevent import monkey;monkey.patch_all()

import gevent
import time

```

#### 单线程的套接字服务端并发

```python
# server
from gevent import monkey;monkey.patch_all()

from socket import *
import gevent


def talk(conn):
    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        try:
            conn.send(msg.upper())
        except:
            break


def run(ip, port):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    while True:
        conn, client_addr = server.accept()
        gevent.spawn(talk, conn=conn)


if __name__ == '__main__':
    g = gevent.spawn(run, ip='127.0.0.1', port=12333)
    g.join()


# client
from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 12333))

if __name__ == '__main__':
    while True:
        msg = input(">>>: ")
        if not msg:
            continue
        client.send(msg.encode('utf-8'))
        msg = client.recv(1024)
        print(msg.decode('utf-8'))
```

### 单线程+多任务异步携程

```python
# 携程: 在函数定义的时候使用async修饰,函数调用后返回一个携程对象,函数内部的语句不会立即执行

# 任务对象: 对协程对象的进一步封装,必须注册到事件循环中,绑定回调

# 事件循环: 相当于容器,存放任务对象,启动后异步执行任务对象


import asyncio
import time

# 回调函数
def callback(task):
    print('callback', task.result())

async def test(num):
    print(f'test{num}')
    await asyncio.sleep(3)
    return f'test{num}'

start_time = time.time()

tasks = []
for i in range(3):
    t = test(i)
    # 封装一个任务对象
    task = asyncio.ensure_future(t)
    # 添加回调
    task.add_done_callback(callback)
    tasks.append(task)

# 创建一个事件循环的对象
loop = asyncio.get_event_loop()
# 任务对象注册
loop.run_until_complete(asyncio.wait(tasks))

print('all:', time.time()-start_time)

# test0# test1
# test2
# callback test0
# callback test1
# callback test2
# all: 3.0028576850891113
```

### aiohttp

```python
# 支持异步
import aiohttp

async def test(url):
    async with aiohttp.ClientSession() as s:
        async with await s.get(url) as response:
            page_text = await response.text()
    return page_text
```

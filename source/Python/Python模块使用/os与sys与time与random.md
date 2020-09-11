# os与sys与time与random

## os

```python
import os

# 执行系统命令
os.system('dir c:')

# 获取环境变零
print(os.environ)

# 获取当前路径
print(os.path.dirname(__file__))

# 获取当前文件名称
print(os.path.basename(__file__))

# 判断路径是否存在
print(os.path.exists('c:/dgs'))

# 判断文件是否存在
print(os.path.isfile('c:/sldj'))

# 组合路径
print(os.path.join('c:/', 'a.txt'))
```

## sys

```python
import sys

# 添加搜索路径
sys.path.append('./')
print(sys.path)

# 接收用户运行时输入的参数 test.py a b c
print(sys.argv)
# ['C:\\Users\\CRAB\\Desktop\\MY\\my_skills_book\\test.py', 'a', 'b', 'c']

# 打印进度条
def programs(percentage):
    if percentage > 1:
        percentage = 1
    res = int(50*percentage) * '#'
    import time
    time.sleep(0.1)
    print('\r[%-50s] %d%%'%(res, int(percentage*100)), end='')
    # print(f"\r[{res.ljust(100, ' ')}] {int(percentage*100)}%", end='')

start_size = 0
total_size = 101011
while start_size < total_size:
        start_size += 1024
        percentage = start_size / total_size
        programs(percentage)
```

## time

```python
import time

# 秒
print(time.time())
# 结构化时间
print(time.localtime())
# 字符串
print(time.strftime('%Y-%m-%d %H:%M:%S'))

# 结构化时间->字符串
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
# 字符串->结构化时间
print(time.strptime('2020-05-19 22:58:05', '%Y-%m-%d %H:%M:%S'))

# 结构化时间->秒
print(time.mktime(time.localtime()))
# 秒->结构化时间
print(time.localtime(time.time()))


import datetime

print(datetime.datetime.now())

# 时间加3天
print(datetime.datetime.now()+datetime.timedelta(days=3))
```

## random

```python
import random

# [1,10]之间的整数
print(random.randint(1, 10))
# (0,1)之间的小数
print(random.random())

l = [1,2,3,4,5]
random.shuffle(l)
print(l)

# 验证码
def random_code(size=4):
    res = []
    for _ in range(size):
        res.append(random.choice((chr(random.randint(65, 90)), str(random.randint(0, 9)))))
    return ''.join(res)

print(random_code())
```

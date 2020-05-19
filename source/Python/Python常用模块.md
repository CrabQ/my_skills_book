# Python常用模块

## sys

```shell
import sys

sys.path.append('./')
print(sys.path)
```

## os

```shell
import os

print(os.path.dirname(__file__))
```

## time

```shell
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

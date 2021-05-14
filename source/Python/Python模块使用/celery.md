# celery

安装

```shell
pip install celery
# windows平台需要
pip install eventlet
```

## 模块方式使用

```python
# celery_server.py
from celery import Celery

broker = 'redis://:redis_6379@121.196.202.188:6379/1'
backend = 'redis://121.196.202.188:6379/2'

app = Celery(__name__, broker=broker, backend=backend, )


@app.task
def add(a, b):
    return a+b

```

模块使用方式

```shell
celery -A celery_server worker --loglevel=info -P eventlet
```

另一个python文件, 右键运行

```python
from celery_server import add

add.delay(1,2)
```

## 包管理(推荐)

```shell
celery -A celery_app worker --loglevel=info -P eventlet
# windows系统需要eventlet支持
# 必须在这个包下建一个celery.py的文件，将Celery(...)产生对象的语句放在该文件中, 或者直接在__init__中写
```

```python
# 包名 script/celery_task

# script/celery_task/__init__.py
from celery import Celery

broker = 'redis://:redis_6379@121.196.202.188:6379/1'
backend = 'redis://:redis_6379@121.196.202.188:6379/2'

app = Celery(__name__, broker=broker, backend=backend, )


app.autodiscover_tasks(['celery_task.task'])


# 任务
# script/celery_task/task.py
from . import app


@app.task
def add(x, y):
    return x + y


@app.task
def low(x, y):
    return x - y


# 添加任务
# script/t_add_task.py
from celery_task import task

def add_task():
    # 添加立即执行任务
    res1 = task.add.delay(5, 3)
    res2 = task.low.delay(5, 3)

    # 添加延时任务
    from datetime import datetime, timedelta
    eta = datetime.utcnow() + timedelta(minutes=1)
    res3 = task.add.apply_async(args=(10,10), eta=eta)

    return res1,res2, res3


# 获取结果
# script/t_get_result.py
from celery.result import AsyncResult

from celery_task import app
from t_add_task import add_task

if __name__ == '__main__':
    for i in add_task():
        async = AsyncResult(id=i.id, app=app)
        if async.successful():
            print(async.get())
        else:
            print(async.status)
```

```shell
# 运行celery
celery -A celery_task worker -l info -P eventlet

# 运行script/t_get_result.py
```

执行定时任务

```python
# script/celery_task/__init__.py


# 命令行执行
# celery -A celery_app worker --loglevel=info -P eventlet
# celery  -A celery_task  beat -l info

# 添加如下内容
# 任务的定时配置
from datetime import timedelta
from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-task': {
        'task': 'celery_task.tasks.add',
        'schedule': timedelta(seconds=6),
        # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
        'args': (300, 10),
    }
}
```

## django中使用

```python
# 根目录下
# celery_task/__init__.py
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

# 加载django环境
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
django.setup()

backend = 'redis://:redis_6379@121.196.202.188:6379/2'
broker = 'redis://:redis_6379@121.196.202.188:6379/1'

app = Celery(__name__, backend=backend, broker=broker)
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False

app.autodiscover_tasks(packages=['celery_task.update_banner'])

app.conf.beat_schedule = {
    'update_banner': {
        'task': 'celery_task.update_banner.update_banner',
        'args': (),
        'schedule': timedelta(seconds=60)
    }
}

# celery_task/update_banner.py
from . import app


@app.task
def update_banner():
    from django.core.cache import cache
    from apps.home.models import Banner
    from apps.home.serializer import BannerSerializer
    queryset_banner = Banner.objects.filter(is_delete=False, is_show=True).order_by('orders').all()
    serializer_banner = BannerSerializer(instance=queryset_banner, many=True).data
    for i in serializer_banner:
        i['image'] = 'http://127.0.0.1:8000' + i['image']
    cache.set('home_banner_cache', serializer_banner, 60 * 60 * 3)
```

执行定时任务

```shell
# 启动worker
celery -A celery_task worker -l info
# 启动beat
celery -A celery_task beat -l info
```

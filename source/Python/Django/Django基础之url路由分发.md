# Django基础之url路由分发

url路由分发的本质是url与要为该url调用的视图函数之间的映射表

```python
def index():
    pass

def home():
    pass

# 定义一个url和函数的对应关系
URL_LIST = [
    ("/index/", index),
    ("/home/", home),
]
```

## 路由匹配与分发

```python
# 2.0之后写法
from django.urls import path

urlpatterns = [
    path('articles/2003/', views.special_case_2003),

    path('articles/<int:year>/<int:month>/', views.month_archive, name='articles'),
]
```

## 路由分发

```python
# 2.0之后写法
from django.urls import path

urlpatterns = [
    # url分发,每个应用创建自己的urls
    path(r'app1/', include('app01.urls')),
]
```

## 默认参数

```python
# urls.py
from django.conf.urls import path

from . import views

urlpatterns = [
    upath(r'articles/', views.articles),
    upath(r'articles/<int:id>/', views.articles),
]

# views.py
def articles(request, id=1):
    pass
```

## 传递额外参数给视图函数

```python
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive, {'foo': 'bar'}),
]

# /blog/2005/请求，Django将调用views.year_archive(request, year='2005', foo='bar')
```

## 命名URL和URL的反向解析

```python
# 别名
path('articles/<int:year>/<int:month>/', views.month_archive, name='articles'),

# 模板引用
{% url 'articles' 2020 9 %}

# 反向解析,views视图引用
from django.urls import reverse

reverse("articles", args=('2020', '9'))
```

## 命名空间

```python
# 路由分发时加上命名空间
    path(r'app1/', include('app01.urls', namespace='app01')),

# 模板引用时加上命名空间避免冲突, 其他也是同样写法
{% url 'app01:articles' 2020 9 %}
```

## 其他

### APPEND_SLASH

url取消自动加斜杠

```shell
# settings.py, 默认为True
APPEND_SLASH = False
```

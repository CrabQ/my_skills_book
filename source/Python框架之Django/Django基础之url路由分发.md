# Django基础之url路由分发

## 路由分发的本质

url与调用的视图函数之间的映射

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

## 路由匹配

```python
# 2.0之后写法
from django.urls import path

urlpatterns = [
    path('articles/2003/', views.special_case_2003),

    path('articles/<int:year>/<int:month>/', views.month_archive, name='articles'),
]
```

### 路由转换器

```shell
str     匹配除了路径分隔符 / 之外的非空字符串, 默认
int     匹配正整数, 包含0
slug    匹配字母, 数字以及横杠, 下划线组成的字符串
uuid    匹配格式化的uuid, 如 075194d3-6885-417e-a8a8-6c931e272f00
path    匹配任何非空字符串, 包含了路径分隔符
```

## 路由分发

```python
# 2.0之后写法
from django.urls import path, include

urlpatterns = [
    # url分发,每个应用创建自己的urls
    path(r'app1/', include('app01.urls')),
]
```

## 默认参数

如果想让两个路由指向同一个视图函数, 视图函数需要设置默认值

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(r'articles/', views.articles),
    path(r'articles/<int:id>/', views.articles),
]

# views.py
from django.http.response import HttpResponse

def articles(request, id=1):
    return HttpResponse(str(id))
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
# url设置别名
path('articles/<int:year>/<int:month>/', views.month_archive, name='articles'),

# 模板引用
{% url 'articles' 2020 9 %}

# 反向解析, views视图引用
reverse("articles", args=('2020', '9'))
```

## 命名空间

```python
# 路由分发时加上命名空间
path(r'app1/', include('app01.urls', namespace='app01')),

# 模板引用时加上命名空间避免冲突
{% url 'app01:articles' 2020 9 %}
```

## 其他

### url取消自动加斜杠

```shell
# settings.py, 默认为True
APPEND_SLASH = False
```

# Django基础之url路由分发

```python
# 2.0之后写法
from django.urls import path

urlpatterns = [
    path('articles/2003/', views.special_case_2003),

    # 默认参数, def year_archive(request,year='2010')
    path('articles/<int:year>/', views.year_archive),

    path('articles/<int:year>/<int:month>/', views.month_archive, name='articles'),

    # url分发,每个应用创建自己的urls
    path(r'app1/', include('app01.urls')),
]
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
# url分发时加上命名空间
    path(r'app1/', include('app01.urls', namespace='app01')),

# 模板引用时加上命名空间避免冲突
{% url 'app01:articles' 2020 9 %}
```

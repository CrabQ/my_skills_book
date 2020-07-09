# Django基础之_views视图函数

## 请求相关的属性方法(request--HttpRequest对象)

```python
# request-> def index(request)
<WSGIRequest: GET '/app1/index/'>
# request.body
b''
# request.GET
<QueryDict: {}>
# request.POST
<QueryDict: {}>
# request.path
'/app1/index/'
# request.path_info
'/app1/index/'
# request.get_full_path()
'/app1/index/'
```

## FBV和CBV

```python
# CBV  -- class based view
# 正常写法

# FBV -- function based view
# views
from django.http import HttpResponse
from django.views import View

class HomeView(View):
    def get(self, request):
        return HttpResponse('ok')

# urls
from django.urls import path
from . import views

urlpatterns = [
    path(r'home/', views.HomeView.as_view()),
]
```

### CBV的dispatch方法

```python
class HomeView(View):

    def dispatch(self, request, *args, **kwargs):
        print('来了')
        ret =  super().dispatch(request, *args, **kwargs)
        print('走了')
        return ret

    def get(self, request):
        print('get')
        return HttpResponse('ok')

# 来了
# get
# 走了
# [07/Jul/2020 11:24:48] "GET /app1/home/ HTTP/1.1" 200 2
```

### 装饰器

```python
def add_info(f):
    def inner(*args, **kwargs):
        print('add 1')
        res = f(*args, **kwargs)
        print('add 2')
        return res
    return inner

@add_info
def home1(request):
    print('get')
    return HttpResponse('ok')

# add 1
# get
# add 2


from django.utils.decorators import method_decorator

# 方式3:单独给get加装饰器
@method_decorator(add_info, name='get')
class HomeView(View):

    # 方式2:所有方法都加装饰器
    # @method_decorator(add_info)
    def dispatch(self, request, *args, **kwargs):
        ret =  super().dispatch(request, *args, **kwargs)
        return ret

    # 方式1:单独给get加装饰器
    # @method_decorator(add_info)
    def get(self, request):
        print('get')
        return HttpResponse('ok')
```

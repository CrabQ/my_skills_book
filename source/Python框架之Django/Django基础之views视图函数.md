# Django基础之views视图函数

## request--HttpRequest对象

```python
# request-> def index(request)
# <WSGIRequest: GET '/app1/index/'>

request.body
# b''

request.GET
# <QueryDict: {}>

request.POST
# <QueryDict: {}>

request.path
# '/app1/index/'

request.path_info
# '/app1/index/'

request.get_full_path()
# '/app1/index/'

# 文件数据
request.FILES
# FILES仅在请求方法为POST且提交的<form>带有enctype="multipart/form-data"下才会包含数据
```

## Response

### Response对象

```python
from django.http import HttpResponse

response['Content-Type'] = 'text/html; charset=UTF-8'
response = HttpResponse("hi")

# HttpResponse.content: 响应内容
# HttpResponse.charset: 响应内容的编码
# HttpResponse.status_code: 响应的状态码
```

### JsonResponse对象

```python
from django.http import JsonResponse

response = JsonResponse({'foo': 'bar'})
print(response.content)
# b'{"foo": "bar"}'

# 默认只能传递字典类型, 如果要传递非字典类型需要设置一下safe关键字参数
# response = JsonResponse([1, 2, 3], safe=False)
```

## Django shortcut functions

### render

```python
from django.shortcuts import render

def my_view(request):
    return render(request, 'myapp/index.html', {'foo': 'bar'})
```

### redirect

```python
# 参数:
# 一个模型, 将调用模型的get_absolute_url() 函数
# 一个视图, 可带参数, 将使用urlresolvers.reverse来反向解析名称
# 一个绝对的或相对的URL, 将原封不动的作为重定向的位置

# 默认返回一个临时的重定向, 传递permanent=True可返回一个永久的重定向

# A页面临时重定向(302)到B页面, 那搜索引擎收录的就是A页面
# A页面永久重定向(301)到B页面，那搜索引擎收录的就是B页面
```

## FBV和CBV

```python
# views.py
# FBV -- function based view
def articles(request, id=1):
    return HttpResponse(str(id))

# CBV  -- class based view
from django.http import HttpResponse
from django.views import View

class HomeView(View):
    # 对应不同的请求方法
    def get(self, request):
        return HttpResponse('ok')

    def post(self, request):
        return HttpResponse('ok')


# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(r'home/', views.HomeView.as_view()),
]
```

### CBV的dispatch方法

通过反射执行各种请求方法

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

#### FBV加装饰器

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
```

#### CBV加装饰器

```python
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

## 一些实例

### 读取文件数据

```python
# 保存上传文件前, 当上传文件小于2.5M时,django会将上传文件的全部内容读进内存, 从内存读取一次, 写磁盘一次
# 当上传文件很大时, django会把上传文件写到临时文件中, 然后存放到系统临时文件夹中

def index(request):
    file_obj = request.FILES.get('file')
    with open(file_obj.name, 'wb') as f:
        for line in file_obj.chunks():
            f.write(line)
```

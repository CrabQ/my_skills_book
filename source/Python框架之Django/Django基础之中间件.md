# Django基础之中间件

用于在全局范围内改变Django的输入和输出

```python
# 自带的中间件, settings.py
# 从上往下执行process_request, 从下往上执行process_response
# 即第一个中间件的process_request, 第二个中间件的process_request, 走一圈
# 然后到第一个中间件的process_view, 第二个中间件的process_view

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## 中间件的五个方法

```python
process_request(self,request)
# 中间件列表顺序执行
# 在执行视图函数之前执行

# 返回值是None --> 下一个中间件process_request处理
# 如果是HttpResponse对象 --> 对应中间件的process_response, 然后倒序执行下一个中间件的process_response


process_view(self, request, view_func, view_args, view_kwargs)
# 中间件列表顺序执行
# view_func是Django即将使用的视图函数, 是实际的函数对象, 而不是函数的名称作为字符串

# process_view方法是在Django路由系统之后, 视图系统之前执行的
# 所有中间件的process_request执行完毕之后 --> process_view

# 返回None --> 下一个中间件process_view处理, 然后在执行相应的视图
# HttpResponse --> 不继续往下执行, 倒序执行一个个process_response方法, 最后返回给浏览器


process_template_response(self,request,response)
# 中间件列表倒序执行
# 在视图函数执行完成后立即执行

# 前提视图函数返回的对象有一个render()方法(或者表明该对象是一个TemplateResponse对象或等价方法)

process_exception(self, request, exception)
# 中间件列表倒序执行
# 只有在视图函数中出现异常了才执行

# 返回None --> 下一个中间件process_exception
# HttpResponse --> 倒序执行一个个process_response方法, 最后返回给浏览器

process_response(self, request, response)
# 中间件列表倒序执行
# 在视图函数之后执行
```

![执行顺序示意图](https://images2018.cnblogs.com/blog/1342004/201806/1342004-20180626145605311-893859640.png)

![执行顺序示意图2](https://images2018.cnblogs.com/blog/1342004/201806/1342004-20180626145540139-490623235.png)

## 自定义中间件

```python
# 应用下创建一个文件夹，文件夹下面创建一个xx.py文件
# 在settings.py中MIDDLEWARE配置里加上自定义的中间件 *.xx.MD1
from django.utils.deprecation import MiddlewareMixin

class MD1(MiddlewareMixin):
    def process_request(self,request):
        return None
    def process_response(self,request,response)
        return response
```

## 解决跨域问题

安装模块

```shell
pip install django-cors-headers
```

使用

```python
# settings.py
# 1. 添加app
INSTALLED_APPS = [
    'corsheaders',
]

# 2. 添加中间件
# 在SessionMiddleware后面以及CommonMiddleware前面
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware'
    'django.middleware.common.CommonMiddleware',
]

# 3. 添加配置参数
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://ops.xxx.com',
    'http://ops.xxx.com:8001',
)
CORS_ALLOW_METHODS = ('DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'VIEW',)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'x-token',
)
```

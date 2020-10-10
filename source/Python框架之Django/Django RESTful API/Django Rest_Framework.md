# Django Rest_Framework

## 安装

```shell
pip install djangorestframework
```

## 序列化组件

前期准备

```python
# settings.py注册

INSTALLED_APPS = [
    'app01',
    'rest_framework',
]
```

模型类

```python
# app01/models.py

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField()
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE, null=True)
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.name
```

路由

```python
# app01/urls.py

from django.urls import path
from app01 import views

urlpatterns = [
    path('books/', views.BookView.as_view(), ),
    path('books/<int:pk>/', views.BookDetailView.as_view(), )
]

```

### 序列化与反序列化, 基于APIView和Serializer

为模型类添加一个序列化器

```python
# app01/ser.py

from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from . import models


# validators, 通过函数补充验证手段
def about_django(value):
    if 'django' in value:
        raise ValidationError("书名不能包括django")


class BookSerializer(serializers.Serializer):
    # read_only=True仅用于序列化输出
    # write_only=True仅用于反序列化输入
    id = serializers.IntegerField(read_only=True)

    # validators, 数据验证
    title = serializers.CharField(max_length=30, validators=[about_django])

    # default 反序列化时使用的默认值
    price = serializers.IntegerField(default=10)

    # 高级用法 source, 返回给前端的数据字段名可以和数据库不一致
    # source 后可跟方法(如模型中定义了一个方法, 可以直接指定在source执行
    pub = serializers.DateField(source='pub_date')
    publish = serializers.CharField(default="", source="publish.id")

    # SerializerMethodField,执行方法, 方法为 get_字段名
    authors = serializers.SerializerMethodField()

    # 返回书籍所有作者
    def get_authors(self, obj):
        temp = []
        for author in obj.authors.all():
            temp.append(author.name)
        return temp

    # 反序列化时进行数据验证, 局部钩子
    def validate_title(self, value):
        if '三国' in value:
            raise ValidationError("书名不能包括三国")
        return value

    # 反序列化时进行数据验证, 全局钩子
    def validate(self, attrs):
        return attrs

    # 验证数据成功后,我们可以使用序列化器来完成数据反序列化的过程.
    # 这个过程可以把数据转成模型类对象
    # 通过create和update方法实现
    # 创建序列化器对象的时候, 没有传递instance实例, 则调用save()方法时, create()被调用
    # 相反, 如果传递了instance实例, 则调用save()方法时, update()被调用

    def create(self, validated_data):
        # return models.Book(**validated_data)

        # 获取出版社ID
        publish_id = validated_data.get('publish')
        if publish_id:
            publish_id = publish_id.get('id', '')
        del validated_data['publish']

        # 获取作者列表
        authors = validated_data.get('authors', [])
        del validated_data['authors']

        # 返回数据对象的同时保存到数据库
        b_obj = models.Book.objects.create(publish_id=publish_id, **validated_data)

        # 添加书籍作者
        for author in authors:
            b_obj.authors.add(models.Author.objects.filter(pk=author).first())
        return b_obj

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.pub_date = validated_data.get('pub', instance.pub_date)

        # 获取出版社ID
        publish = validated_data.get('publish')
        if publish:
            instance.publish_id = publish.get('id')

        # 更新书籍作者
        authors = validated_data.get('authors', [])
        a_list = []
        for author in authors:
            a_list.append(models.Author.objects.filter(pk=author).first())
        instance.authors.set(a_list)

        instance.save()
        return instance

```

构造序列化器对象, 获取序列化数据

```python
# app01/views.py

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .ser import BookSerializer


class BookView(APIView):
    def get(self, request):
        b_obj = models.Book.objects.all()

        # 如果转换多个模型对象数据,则需要加上many=True
        serializer = BookSerializer(instance=b_obj, many=True)
        res = {"status": 200, "msg": "ok", "data": serializer.data}

        return JsonResponse(res)

    def post(self, request):
        bs = BookSerializer(data=request.data)
        if bs.is_valid():
            # 在对序列化器进行save()保存时, 可以额外传递数据
            # 在create()和update()中的validated_data参数获取到
            bs.save(authors=request.data.get('authors'))
            res = {"status": 200, "msg": "ok", "data": bs.data}
        else:
            res = {"status": 400, "msg": bs.errors}

        return Response(res)


class BookDetailView(APIView):
    def get(self, request, pk):
        b_obj = models.Book.objects.filter(pk=pk).first()
        b_ser = BookSerializer(instance=b_obj)
        res = {"status": 200, "msg": "ok", "data": b_ser.data}
 
        return JsonResponse(res)

    def delete(self, request, pk):
        models.Book.objects.filter(pk=pk).delete()
        res = {"status": 200, "msg": "ok", "data": ''}

        return JsonResponse(res)

    def put(self, request, pk):
        b_obj = models.Book.objects.filter(pk=pk).first()

        # partial=True, 允许部分更新
        b_ser = BookSerializer(instance=b_obj, data=request.data, partial=True)

        # raise_exception=True, 验证失败时抛出异常serializers.ValidationError
        # 会向前端返回HTTP 400 Bad Request响应
        b_ser.is_valid(raise_exception=True)

        b_ser.save(authors=request.data.get('authors'))
        res = {"status": 200, "msg": "ok", "data": b_ser.data}

        return JsonResponse(res)
```

### 模型类序列化器ModelSerializer

```shell
基于模型类自动生成一系列字段
基于模型类自动为Serializer生成validators
包含默认的create()和update()的实现
```

```Python
# 只需要修改序列化器, 其他不用修改
# app01/ser.py

from rest_framework import serializers

from . import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        # 指明模型
        model = models.Book

        # fields = "__all__"
        # 指定字段
        fields = ("title", "price", "id", "publish", "authors", "pub_date")

        # 排除字段, 与fields不能同用
        # exclude = ('id')

        # 额外字段
        extra_kwargs = {
            'price': {'min_value': 0, 'required': True, 'write_only': True},
        }
```

### 请求与相应

#### Request

```shell
request.data            返回解析之后的请求体数据
request.query_params    与Django标准的request.GET相同
```

#### Response

```shell
Response(data, status=None, template_name=None, headers=None, content_type=None)

response.data
# 传给response对象的序列化后, 但尚未render处理的数据

response.status_code
# 状态码的数字

response.content
# 经过render处理后的响应数据
```

状态码

```python
from rest_framework import status
```

Renderer 渲染器, 跟据请求头中的Accept来自动转换响应数据到对应格式

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
    )
}
```

## 视图组件

```shell
REST framework 提供了众多的通用视图基类与扩展类, 以简化视图的编写

控制序列化器的执行(检验, 保存, 转换数据)
控制数据库查询的执行
```

### 2个视图基类

#### APIView

```shell
rest_framework.views.APIView

APIView是REST framework提供的所有视图的基类,继承自Django的View父类

传入到视图方法中的是REST framework的Request对象,而不是Django的HttpRequeset对象
在进行dispatch()分发前,会对请求进行身份认证、权限检查、流量控制


支持定义的类属性
    authentication_classes  列表或元祖,身份认证类
    permissoin_classes      列表或元祖,权限检查类
    throttle_classes        列表或元祖,流量控制类
```

#### GenericAPIView[通用视图类]

```shell
rest_framework.generics.GenericAPIView

继承自APIVIew,主要增加了操作序列化器和数据库查询的方法,
作用是为下面Mixin扩展类的执行提供方法支持。通常在使用时,可搭配一个或多个Mixin扩展类
```

属性

```shell
serializer_class    指明视图使用的序列化器
queryset            指明使用的数据查询集
pagination_class    指明分页控制类
filter_backends     指明过滤控制后端
```

方法

```python
# get_serializer_class(self)
# 控制视图方法执行不同的序列化器对象
# 返回序列化器类,默认返回serializer_class, 可重写
def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer

# get_serializer(self, args, *kwargs)
# 返回序列化器对象,主要用来提供给Mixin扩展类使用

# get_queryset(self)
# 返回视图使用的查询集,主要用来提供给Mixin扩展类使用
# 是列表视图与详情视图获取数据的基础,默认返回queryset属性

# get_object(self)
# 返回详情视图所需的模型类数据对象,主要用来提供给Mixin扩展类使用
# get_object()方法根据pk参数查找queryset中的数据对象, 传递参数名需指定为PK
```

```python
# 序列化器为上边 模型类序列化器ModelSerializer 中的代码
# app01/views.py

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from . import models
from .ser import BookSerializer


class BookView(GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        b_ser = self.get_serializer(instance=self.get_queryset(), many=True)
        res = {"status": 200, "msg": "ok", "data": b_ser.data}

        return Response(res)

    def post(self, request):
        b_ser = self.get_serializer(data=request.data)
        b_ser.is_valid(raise_exception=True)
        b_ser.save()
        res = {"status": 200, "msg": "ok", "data": b_ser.data}

        return Response(res)


class BookDetailView(GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        b_ser = self.get_serializer(instance=self.get_object())
        res = {"status": 200, "msg": "ok", "data": b_ser.data}

        return Response(res)

    def put(self, request, pk):
        b_ser = self.get_serializer(instance=self.get_object(), data=request.data, partial=True)

        b_ser.is_valid(raise_exception=True)
        b_ser.save()
        res = {"status": 200, "msg": "ok", "data": b_ser.data}

        return Response(res)
```

### 5个视图扩展类

```shell
提供几种后端视图处理流程的实现
即对数据资源进行增删查改, 减少代码量

五个扩展类需要搭配GenericAPIView父类
因为五个扩展类的实现需要调用GenericAPIView提供的序列化器与数据库查询方法
```

#### ListModelMixin

```python
# 列表视图扩展类,提供list(request, *args, **kwargs)方法快速实现列表视图,返回200状态码

class BookView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)
```

#### CreateModelMixin

```python
# 创建视图扩展类,提供create(request, *args, **kwargs)方法快速实现创建资源的视图,成功返回201状态码

# 如果序列化器对前端发送的数据验证失败,返回400错误

class BookView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
```

#### RetrieveModelMixin

```python
# 详情视图扩展类,提供retrieve(request, *args, **kwargs)方法,可以快速实现返回一个存在的数据对象

# 状态码 200 or 400

class BookDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request)
```

#### UpdateModelMixin

```python
# 更新视图扩展类,提供update(request, *args, **kwargs)方法,可以快速实现更新一个存在的数据对象

# 同时也提供partial_update(request, *args, **kwargs)方法,可以实现局部更新

# 状态码 200 or 400

class BookDetailView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.partial_update(request)
```

#### DestroyModelMixin

```python
# 删除视图扩展类,提供destroy(request, *args, **kwargs)方法,可以快速实现删除一个存在的数据对象

# 状态码 200 or 400

class BookDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.partial_update(request)

    def delete(self, request, pk):
        return self.destroy(request)
```

### GenericAPIView的视图子类

```shell
CreateAPIView
继承自：GenericAPIView、CreateModelMixin
提供 post 方法

ListAPIView
继承自：GenericAPIView、ListModelMixin
提供 get 方法

RetrieveAPIView
继承自: GenericAPIView、RetrieveModelMixin
提供 get 方法

DestoryAPIView
继承自：GenericAPIView、DestoryModelMixin
提供 delete 方法

UpdateAPIView
继承自：GenericAPIView、UpdateModelMixin
提供 put 和 patch 方法

RetrieveUpdateAPIView
继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin
提供 get、put、patch方法

RetrieveUpdateDestoryAPIView
继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin
提供 get、put、patch、delete方法
```

### 视图集ViewSet

```shell
使用视图集ViewSet, 可以将一系列逻辑相关的动作放到一个类中

list() 提供一组数据
retrieve() 提供单个数据
create() 创建数据
update() 保存数据
destory() 删除数据

ViewSet视图集类不再实现get(), post()等方法,而是实现动作 action 如 list() 、create() 等

视图集只在使用as_view({"get":"list"})方法的时候,才会将action动作与具体请求方式对应上
```

#### ViewSet

```python
# 继承自APIView与ViewSetMixin,作用也与APIView基本类似,提供了身份认证、权限校验、流量管理等

# ViewSet主要通过继承ViewSetMixin来实现在调用as_view()时传入字典（如{‘get’:’list’}）的映射处理工作

# 在ViewSet中,没有提供任何动作action方法,需要我们自己实现action方法

# app01/urls.py
from django.urls import path
from app01 import views

urlpatterns = [
    path('books/', views.BookViewSet.as_view({"get": "list"}), ),
]

# app01/views.py
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from . import models
from .ser import BookSerializer

class BookViewSet(ViewSet):
    def list(self, request):
        book = models.Book.objects.all()
        ser = BookSerializer(instance=book, many=True)
        return Response(ser.data)

```

#### GenericViewSet

```python
# 继承自GenericAPIView与ViewSetMixin
# 提供GenericAPIView提供的基础方法,可以直接搭配Mixin扩展类使用

# url 如上ViewSet
class BookViewSet(GenericViewSet, ListModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer
```

#### ModelViewSet

```shell
继承自GenericViewSet
同时包括了五个视图扩展类
ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin
```

#### ReadOnlyModelViewSet

```shell
继承自GenericViewSet
同时包括了ListModelMixin、RetrieveModelMixin
```

#### 视图集中定义附加action动作

```python
# {"get": "list", "post": "create"}
# {"get": "retrieve","put":"update","delete":"destroy"}

# urls.py
    path('books/', views.BookViewSet.as_view({"get": "login"}), ),

class BookViewSet(GenericViewSet, ListModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def login(self, request):
        # 获取本次请求的视图方法名
        print(self.action)
```

## 路由组件

```shell
对于视图集ViewSet, 除了可以自己手动指明请求方式与动作action之间的对应关系外
还可以使用Routers来帮助我们快速实现路由信息

REST framework提供了两个router
SimpleRouter
DefaultRouter

DefaultRouter会多附带一个默认的API根视图
返回一个包含所有列表视图的超链接响应数据
```

```python
# urls.py
from django.urls import path
from rest_framework import routers
from app01 import views

# router对象, 注册视图集
router = routers.SimpleRouter()
# prefix 该视图集的路由前缀  viewset 视图集  basename 路由别名的前缀
router.register('books', views.BookViewSet, basename='book')

urlpatterns = [
    # path('books/', views.BookViewSet.as_view({"get": "list", "post": "create"}), ),
    # path('books/', views.BookView.as_view(), ),
    # path('books/<int:pk>/', views.BookDetailView.as_view(), )
]


# 添加路由数据
urlpatterns += router.urls


# 自动生成路由地址[增/删/改/查一条/查多条的功能]
# 不会自动生成在视图集自定义方法的路由, 需要进行action动作的声明
```

### 视图集中附加action的声明

```python
from rest_framework.decorators import action

from . import models
from .ser import BookSerializer


class BookView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    # action装饰器, 生成对应路由
    # detail=True 表示路径格式是xxx/<pk>/action方法名/
    # False 表示路径格式是xxx/action方法名/
    @action(["get", "post"], detail=False)
    def get_1(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
```

## 认证权限频率

### 认证Authentication

```python
# 1. 编写自定义认证类, 继承BaseAuthentication, 重写authenticate
from rest_framework.authentication import BaseAuthentication

class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        pass

# 2. 视图函数导入认证类使用或者全局使用
# 局部禁用 authentication_classes = []

# settings.py
# 全局使用
REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":["app01.app_auth.TokenAuth",]
}

# 局部使用
# 视图函数在视图类中添加
authentication_classes = [TokenAuth, ]

# 认证失败会有两种可能的返回值
# 401 Unauthorized 未认证
# 403 Permission Denied 权限被禁止
```

实例

```python
# 修改模型, 添加用户
# app01/models.py
class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    user_type=models.IntegerField(choices=((1,'超级用户'),(2,'普通用户'),(3,'二笔用户')))

class UserToken(models.Model):
    user=models.OneToOneField(to='User')
    token=models.CharField(max_length=64)


# 1. 编写自定义认证类 app01/app_auth.py
from rest_framework.authentication import BaseAuthentication

class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
    # 认证逻辑: 认证通过则返回两个值
    # 失败则抛出AuthenticationFailed异常
        token = request.GET.get('token')
        # 用户登录时生成token, 存入数据库, 同时返回给用户, 让用户携带token访问资源
        token_obj = models.UserToken.objects.filter(token=token).first()
        if token_obj:
            return token_obj.user, token
        else:
            raise AuthenticationFailed('认证失败')


# 2. 视图函数导入认证类使用
from app_auth import TokenAuth

class Course(APIView):
    authentication_classes = [TokenAuth, ]
```

#### 内置认证方案(需要配合权限使用)

```python
# 开启SessionAuthentication可用内置权限认证
class Course(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAdminUser,]

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # session认证
        'rest_framework.authentication.BasicAuthentication',   # 基本认证
    )
}
```

### 权限Permissions

```Python
# 权限在认证之后, 基本和认证差不多

# 权限控制可以限制用户对于视图的访问和对于具体数据对象的访问
# 在执行视图的dispatch()方法前会先进行视图访问权限的判断
# 在通过get_object()获取具体对象时会进行模型对象访问权限的判断

# 全局使用
REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":["app01.service.auth.Authentication",],
    "DEFAULT_PERMISSION_CLASSES":["app01.service.permissions.SVIPPermission",]
}

# 局部使用
# 视图函数在视图类中添加
permission_classes = [UserPermission,]

# 自定义权限需继承rest_framework.permissions.BasePermission父类并实现以下两个任何一个方法或全部
# has_permission(self, request, view)
#   是否可以访问视图, view表示当前视图对象

# has_object_permission(self, request, view, obj)
#   是否可以访问数据对象, view表示当前视图, obj为数据对象
```

实例

```python
# 限制只有超级用户能访问
from rest_framework.permissions import BasePermission
class UserPermission(BasePermission):
    message = '不是超级用户,查看不了'
    def has_permission(self, request, view):
        user_type = request.user.user_type
        if user_type == 1:
            return True
        else:
            return False
```

#### 内置权限

```python
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
# AllowAny 允许所有用户
# IsAuthenticated 仅通过认证的用户
# IsAdminUser 仅管理员用户
# IsAuthenticatedOrReadOnly 已经登陆认证的用户可以对数据进行增删改操作,没有登陆认证的只能查看数据

# 全局配置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
# 未配置则采用AllowAny
```

### 限流Throttling

```python
# 全局使用
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES':['app01.utils.MyThrottles',],
}

# 局部使用
# 视图函数在视图类中添加
throttle_classes = [MyThrottles,]
```

#### 内置频率类

```python
#写一个类,继承自SimpleRateThrottle（根据ip限制）
from rest_framework.throttling import SimpleRateThrottle
class VisitThrottle(SimpleRateThrottle):
    scope = 'luffy'
    def get_cache_key(self, request, view):
        return self.get_ident(request)

#在setting里配置：（一分钟访问三次）
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES':{
        'luffy':'3/m'  # key要跟类中的scop对应
    }
}


# 根据用户ip限制
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/m',
    }
}
# 使用 `second`, `minute`, `hour` 或`day`来指明周期
# 可以全局使用, 局部使用

# 限制匿名用户每分钟访问3次
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/m',
    }
}

# 限制登陆用户每分钟访问10次
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '10/m'
    }
}
```

## 过滤Filtering

安装

```shell
pip install django-filter
```

配置

```python
INSTALLED_APPS = [
    'django_filters',  # 需要注册应用,
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}


# 视图中添加filter_fields属性, 指定过滤字段
# 需要是继承GenericAPIView的视图函数
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_fields = ('age', 'sex')
# 127.0.0.1:8000/four/students/?sex=1
```

## 排序

```python
from django_filters.rest_framework import DjangoFilterBackend

class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [OrderingFilter]
    # 如果同时需要过滤和排序, 先过滤再排序
    # filter_backends = [DjangoFilterBackend, OrderingFilter]

    ordering_fields = ('id', 'age')

# 127.0.0.1:8000/books/?ordering=-age
# -id 表示针对id字段进行倒序排序
# id  表示针对id字段进行升序排序
```

## 自定义异常处理

```python
from rest_framework.views import exception_handler

# 1. 自定义异常处理函数
def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is None:
        if isinstance(exc, DatabaseError):
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            response = Response({'detail': '未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response

# 2. 声明
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

## 分页

```python
# 全局分页
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':  'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100  # 每页数目
}

# 局部分页
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    pagination_class = LargeResultsSetPagination

# 局部禁用
pagination_class = None
```

### PageNumberPagination

```shell
GET  http://127.0.0.1:8000/students/?page=4

page_size               每页数目
page_query_param        前端发送的页数关键字名, 默认为 page
page_size_query_param   前端发送的每页数目关键字名,默认为None
max_page_size           前端最多能设置的每页数量
```

```python
# APIView
from rest_framework.pagination import PageNumberPagination
class  Pager(APIView):
    def get(self,request,*args,**kwargs):
        # 获取所有数据
        ret=models.Book.objects.all()
        # 创建分页对象
        page=PageNumberPagination()
        # 在数据库中获取分页的数据
        page_list=page.paginate_queryset(ret,request,view=self)
        # 对分页进行序列化
        ser=BookSerializer1(instance=page_list,many=True)
        return Response(ser.data)


#ListAPIView
# 127.0.0.1/four/students/?p=1&size=5

# 声明分页的配置类
from rest_framework.pagination import PageNumberPagination

class StandardPageNumberPagination(PageNumberPagination):
    # 默认每一页显示的数据量
    page_size = 2
    # 允许客户端通过get参数来控制每一页的数据量
    page_size_query_param = "size"
    max_page_size = 10
    # 自定义页码的参数名
    page_query_param = "p"

class StudentAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    pagination_class = StandardPageNumberPagination
```

### LimitOffsetPagination

```shell
GET http://127.0.0.1/four/students/?limit=100&offset=400

default_limit       默认限制, 默认值与PAGE_SIZE设置一致
limit_query_param   limit参数名, 默认 limit
offset_query_param  offset参数名, 默认 offset
max_limit           最大limit限制, 默认None
```

```python
# http://127.0.0.1:8000/pager/?offset=4&limit=3

# APIView
from rest_framework.pagination import LimitOffsetPagination

class  Pager(APIView):
    def get(self,request,*args,**kwargs):
        # 获取所有数据
        ret=models.Book.objects.all()
        # 创建分页对象
        page=LimitOffsetPagination()
        # 在数据库中获取分页的数据
        page_list=page.paginate_queryset(ret,request,view=self)
        # 对分页进行序列化
        ser=BookSerializer1(instance=page_list,many=True)
        # return page.get_paginated_response(ser.data)
        return Response(ser.data)


#ListAPIView
from rest_framework.pagination import LimitOffsetPagination

class StandardLimitOffsetPagination(LimitOffsetPagination):
    # 默认每一页查询的数据量,类似上面的page_size
    default_limit = 2
    limit_query_param = "size"
    offset_query_param = "start"

class StudentAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    # 调用页码分页类
    # pagination_class = StandardPageNumberPagination
    # 调用查询偏移分页类
    pagination_class = StandardLimitOffsetPagination
```

### CursorPagination

```shell
GET http://127.0.0.1/four/students/?cursor=cD0xNQ%3D%3D

cursor_query_param  默认查询字段, 不需要修改
page_size           每页数目
ordering            按什么排序, 需要指定
```

```python
#APIView

from rest_framework.pagination import CursorPagination

# 看源码,是通过sql查询,大于id和小于id
class  Pager(APIView):
    def get(self,request,*args,**kwargs):
        # 获取所有数据
        ret=models.Book.objects.all()
        # 创建分页对象
        page=CursorPagination()
        page.ordering='nid'
        # 在数据库中获取分页的数据
        page_list=page.paginate_queryset(ret,request,view=self)
        # 对分页进行序列化
        ser=BookSerializer1(instance=page_list,many=True)
        # 可以避免页码被猜到
        return page.get_paginated_response(ser.data)


# ListAPIView

class MyCursorPagination(CursorPagination):
    page_size=2
    ordering='-id'

from rest_framework.generics import ListAPIView
class AuthorListView(ListAPIView):
    serializer_class = serializers.AuthorModelSerializer
    queryset = models.Author.objects.filter(is_delete=False)
    pagination_class =MyCursorPagination
```

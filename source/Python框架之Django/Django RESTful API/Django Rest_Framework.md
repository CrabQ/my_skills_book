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
# models.py

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
# urls.py

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
# ser.py

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
    xxx_pub = serializers.CharField(source='publish.email')

    # SerializerMethodField,执行方法, 方法为 get_字段名
    xxx_aut = serializers.SerializerMethodField()

    # 返回书籍所有作者
    def get_xxx_aut(self, instance):
        tmp = []
        for i in instance.authors.all():
            tmp.append(i.name)
        return tmp

    # 反序列化时进行数据验证, 局部钩子
    def validate_title(self, value):
        if '三国' in value:
            raise ValidationError("书名不能包括三国")
        return value

    # 反序列化时进行数据验证, 全局钩子
    def validate(self, attrs):
        if attrs.get('title') == attrs.get('authors'):
            raise ValidationError('不能同名')
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
# views.py

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
# ser.py

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

#### 基于ModelSerializer和APIView实现增删查改

模型类

```python
from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(choices=((0, '未删除'), (1, '删除')), default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 抽象类,不在数据库实现
        abstract = True


class Book(BaseModel):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pub_date = models.DateField(null=True)
    publish = models.ForeignKey("Publish", on_delete=models.DO_NOTHING, db_constraint=False)
    authors = models.ManyToManyField("Author", db_constraint=False)

    def publish_name(self):
        return self.publish.name

    def authors_list(self):
        authors = self.authors.all()
        return [{'name': aut.name, 'sex': aut.sex} for aut in authors]

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    sex = models.IntegerField(choices=((1, '男'), (2, '女')), default=1)
    detail = models.OneToOneField('AuthorDetail', on_delete=models.CASCADE, db_constraint=False)

    def __str__(self):
        return self.name
```

路由

```python
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookView.as_view()),
    path('books/<int:pk>/', views.BookView.as_view()),
]
```

序列化器

```python
from rest_framework.serializers import ModelSerializer, ListSerializer
from .models import Book


# 重写BookSerializer的ListSerializer的update方法,实现批量修改
class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        print(instance, validated_data)
        return [
            self.child.update(instance=instance[i], validated_data=attrs) for i, attrs in enumerate(validated_data)
        ]


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'price', 'pub_date', 'publish', 'authors', 'publish_name', 'authors_list')

        extra_kwargs = {
            'publish': {'write_only': True},
            'authors': {'write_only': True},
            'publish_name': {'read_only': True},
            'authors_list': {'read_only': True}
        }
        # 指定为自定义的类, many=True时触发
        list_serializer_class = BookListSerializer
```

视图函数

```python
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book
from .ser import BookSerializer


# 自定义response
class CustomerResponse(Response):
    def __init__(self, code=200, msg='ok', data=None, headers=None, status=None, **kwargs):
        dic = {
            'code': code,
            'msg': msg,
        }
        if data:
            dic['data'] = data
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)


class BookView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有
        obj = Book.objects.all()
        bs = BookSerializer(instance=obj, many=True)
        # 获取单条
        pk = kwargs.get('pk')
        if pk:
            obj = obj.filter(pk=pk).first()
            bs = BookSerializer(instance=obj)
        return CustomerResponse(data=bs.data)

    def post(self, request, *args, **kwargs):
        # 单增
        if isinstance(request.data, dict):
            bs = BookSerializer(data=request.data)
        # 批量增
        elif isinstance(request.data, list):
            bs = BookSerializer(data=request.data, many=True)
        else:
            return CustomerResponse(code=400, msg='error')
        bs.is_valid(raise_exception=True)
        bs.save()
        return CustomerResponse(data=bs.data)

    def put(self, request, *args, **kwargs):
        # 单改
        if kwargs.get('pk'):
            obj = Book.objects.filter(pk=kwargs.get('pk')).first()
            bs = BookSerializer(instance=obj, data=request.data, partial=True)
        # 批量改
        else:
            obj_list = []
            data_list = []
            for i in request.data:
                obj = Book.objects.filter(pk=i.pop('pk')).first()
                obj_list.append(obj)
                data_list.append(i)
            # 通过重写BookSerializer的list_serializer_class对应的类的update方法
            bs = BookSerializer(instance=obj_list, data=data_list, partial=True, many=True)
        bs.is_valid(raise_exception=True)
        bs.save()
        return CustomerResponse(data=bs.data)

    def delete(self, request, *args, **kwargs):
        # 单或者批量删
        pk_list = []
        if kwargs.get('pk'):
            pk_list.append(kwargs.get('pk'))
        else:
            pk_list = request.data.get('pks')
        Book.objects.filter(pk__in=pk_list).update(is_delete=True)
        return CustomerResponse()
```

### 请求与相应

#### Request

```shell
request.data            返回解析之后的请求体数据, 无论什么根式的post都可以
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

##### 自定义response

```python
from rest_framework.response import Response


class CustomerResponse(Response):
    def __init__(self, code=200, msg='ok', data=None, status=None, headers=None, **kwargs):
        dic = {'code': code, 'msg': msg}
        if data:
            dic['data'] = data
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)
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
# 使用自定义Response返回数据

# views.py
from rest_framework.generics import GenericAPIView

from .ser import BookSerializer
from . import models

class BooksDetailView_2(GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        bs = self.get_serializer(instance=self.get_object())
        return CustomerResponse(data=bs.data)


class BooksView_2(GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        bs = self.get_serializer(instance=self.get_queryset(), many=True)
        return CustomerResponse(data=bs.data)


# urls.py
urlpatterns = [
    path(r'books_2/<int:pk>/', views.BooksDetailView_2.as_view()),
    path(r'books_2/', views.BooksView_2.as_view()),
]
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

### 视图集

```shell
使用视图集, 可以将一系列逻辑相关的动作放到一个类中

list() 提供一组数据
retrieve() 提供单个数据
create() 创建数据
update() 保存数据
destory() 删除数据

视图集类不再实现get(), post()等方法,而是实现动作 action 如 list() 、create() 等

视图集只在使用as_view({"get":"list"})方法的时候,才会将action动作与具体请求方式对应上
```

#### ViewSet

```python
# 继承自APIView与ViewSetMixin,作用也与APIView基本类似,提供了身份认证、权限校验、流量管理等

# ViewSet主要通过继承ViewSetMixin来实现在调用as_view()时传入字典（如{‘get’:’list’}）的映射处理工作

# 在ViewSet中,没有提供任何动作action方法,需要我们自己实现action方法

# views.py
from rest_framework.viewsets import ViewSet

from . import models
from .ser import BookSerializer

class BooksViewSet(ViewSet):

    def get_all(self, request):
        obj = models.Book.objects.all()
        bs = BookSerializer(instance=obj, many=True)
        return CustomerResponse(data=bs.data)


# 视图集中定义附加action动作
# urls.py
from django.urls import path
from app01 import views

urlpatterns = [
    path(r'books_4/', views.BooksViewSet.as_view(actions={'get': 'get_all'})),
]
```

#### GenericViewSet

```python
# 继承自GenericAPIView与ViewSetMixin
# 提供GenericAPIView提供的基础方法,可以直接搭配Mixin扩展类使用

# views.py
class BooksViewSet_2(GenericViewSet, mixins.ListModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer


# urls.py
urlpatterns = [
    path(r'books_5/', views.BooksViewSet_2.as_view(actions={'get': 'list'})),
]
```

#### ModelViewSet

```shell
继承自GenericViewSet
同时包括了五个视图扩展类
ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin

只需要路由对应相应方法, 可直接使用一个视图(如获取多个和获取一个)
```

```python
# views.py
class BooksViewSet_3(ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer


# urls.py
urlpatterns = [
    path(r'books_6/', views.BooksViewSet_3.as_view(actions={'get': 'list'})),
    path(r'books_6/<int:pk>/', views.BooksViewSet_3.as_view(actions={'get': 'retrieve'})),
]
```

#### ReadOnlyModelViewSet

```shell
继承自GenericViewSet
同时包括了ListModelMixin、RetrieveModelMixin
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
routers.register('books_7', views.BooksViewSet_4, )

urlpatterns = [
    ...
]

# 添加路由数据
urlpatterns += routers.urls
# routers.urls
# [<URLPattern '^books_7/$' [name='book-list']>, <URLPattern '^books_7/get_1/$' [name='book-get-1']>, <URLPattern '^books_7/(?P<pk>[^/.]+)/$' [name='book-detail']>, <URLPattern '^books_7/(?P<pk>[^/.]+)/get_2/$' [name='book-get-2']>]

# 自动生成路由地址[增/删/改/查一条/查多条的功能]
# 不会自动生成在视图集自定义方法的路由, 需要进行action动作的声明


# views.py
# 下方 --> 视图集中附加action的声明
```

## 视图集中附加action的声明

```python
# views.py
class BooksViewSet_4(ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    # action装饰器, 生成对应路由
    # False 表示路径格式是xxx/action方法名/
    # 127.0.0.1:8000/api/app01/books_7/get_1/
    @action(['get'], detail=False)
    def get_1(self, request):
        return self.list(request)

    # detail=True 表示路径格式是xxx/<pk>/action方法名/
    # 127.0.0.1:8000/api/app01/books_7/3/get_2/
    @action(['get'], detail=True)
    def get_2(self, request, pk):
        return self.retrieve(request)
```

## 认证权限频率

认证权限频率使用方式

```python
# 三者相同, 认证举例


# 1. 局部使用
# views.py
from .app_auth import TokenAuthentication

class BrowserView(APIView):
    authentication_classes = [TokenAuthentication]


# 2. 局部禁用
# views.py
class BrowserView(APIView):
    authentication_classes = []


# 3. 全局使用
# settings.py
REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":["app01.app_auth.TokenAuthentication",]
}
```

### 认证Authentication

```python
编写自定义认证类, 继承BaseAuthentication, 重写authenticate

认证失败会有两种可能的返回值
401 Unauthorized 未认证
403 Permission Denied 权限被禁止
```

实例

```python
# 修改模型, 添加用户
# models.py
class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    user_type=models.IntegerField(choices=((1,'超级用户'),(2,'普通用户'),(3,'二笔用户')))

class UserToken(models.Model):
    user=models.OneToOneField(to='User')
    token=models.CharField(max_length=64)


# 1. 编写自定义认证类
# app_auth.py
from rest_framework.authentication import BaseAuthentication

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = UserToken.objects.filter(token=token).first()
        if obj:
            return obj.user, token
        else:
            raise AuthenticationFailed('用户未认证')


# 2. 视图函数导入认证类使用
# views.py
from uuid import uuid4

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, UserToken
from .app_auth import TokenAuthentication, AppPermission


class CustomerResponse(Response):
    def __init__(self, code=200, msg='ok', data=None, headers=None, status=None, **kwargs):
        dic = {'code': code, 'msg': msg}
        if data:
            dic['data'] = data
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)


class UserLoginView(APIView):
    def post(self, request):
        user = request.data.get('user')
        password = request.data.get('password')
        user_obj = User.objects.all().filter(user=user, password=password).first()
        if user_obj:
            token = uuid4()
            UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
            return CustomerResponse(data={'token': token})
        else:
            return CustomerResponse(code=400, msg='用户名或者密码错误!')


class BrowserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AppPermission]

    def get(self, request):
        return CustomerResponse(data=request.user.user)
```

#### 内置认证方案(需要配合权限使用)

```python
# 认证为权限铺垫,二者结合使用, 认证: request.user, 权限: request.user.is_staff, return True
# 开启SessionAuthentication可用内置权限认证
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
权限在认证之后, 基本和认证差不多

权限控制可以限制用户对于视图的访问和对于具体数据对象的访问
在执行视图的dispatch()方法前会先进行视图访问权限的判断
在通过get_object()获取具体对象时会进行模型对象访问权限的判断


自定义权限需继承rest_framework.permissions.BasePermission父类并实现以下两个任何一个方法或全部
has_permission(self, request, view)
是否可以访问视图, view表示当前视图对象

has_object_permission(self, request, view, obj)
是否可以访问数据对象, view表示当前视图, obj为数据对象
```

实例

```python
# 模型为上边认证模型
# 配合自定义认证类从request.user获取用户类型作判断
# app_auth.py
from rest_framework.permissions import BasePermission

class AppPermission(BasePermission):
    def has_permission(self, request, view):
        user_type = request.user.user_type
        if user_type == 1:
            return True
        else:
            return False


# 限制只有用户类型为1的用户才能访问
# views.py
class BrowserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AppPermission]

    def get(self, request):
        return CustomerResponse(data=request.user.user)
```

#### 内置权限

```python
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
# AllowAny 允许所有用户
# IsAuthenticated 仅通过认证的用户
# IsAdminUser 仅管理员用户
# IsAuthenticatedOrReadOnly 已经登陆认证的用户可以对数据进行增删改操作,没有登陆认证的只能查看数据

# 配合SessionAuthentication使用
# views.py
class Course(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAdminUser,]
```

### 限流Throttling

#### 内置频率类(配合内置认证权限)

```python
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

#### 自定义频率

限制每个ip每分钟访问3次

```python
# app_auth.py
class IpThrottle(SimpleRateThrottle):
    scope = 'ip'

    def get_cache_key(self, request, view):
        # return self.get_ident(request)
        return request.META.get('REMOTE_ADDR')


# settings.py
REST_FRAMEWORK = {
    # key要跟类中的scop对应
    'DEFAULT_THROTTLE_RATES': {
        'ip': '3/m',
    }


# views.py
class BrowserView(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [AppPermission]
    throttle_classes = [IpThrottle]

    def get(self, request):
        return CustomerResponse(data=request.user.user)
```

## 过滤Filtering

安装

```shell
pip install django-filter
```

配置

```python

# 全局配置
# settings.py
INSTALLED_APPS = [
    'django_filters',  # 需要注册应用,
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}


# 视图中添加filter_fields属性, 指定过滤字段
# 需要继承GenericAPIView的视图函数
# views.py
from django_filters.rest_framework import DjangoFilterBackend


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('user',)

# http://127.0.0.1:8000/api/app02/users/?user=test1
```

## 排序

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 如果同时需要过滤和排序, 先过滤再排序
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_fields = ('user',)
    ordering_filter = ('id',)


# http://127.0.0.1:8000/api/app02/users/?ordering=-id
# -id 倒序
# id  升序
```

## 自定义异常处理

```python
# 1. 自定义异常处理函数
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def app_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    # response=None, drf未处理异常
    # response=Response, drf捕获异常, 不符合自定义规范
    response = exception_handler(exc, context)
    if not response:
        if isinstance(exc, ZeroDivisionError):
            code = 777
            msg = '除数不能为0'
        else:
            code = 999
            msg = str(exc)
        return Response(data={'code': code, 'msg': msg}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={'code': 888, 'msg': response.data.get('detail')}, status=status.HTTP_400_BAD_REQUEST)


# 2. 声明
# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

## 分页

### PageNumberPagination

```shell
page_size               每页数目
page_query_param        前端发送的页数关键字名, 默认为 page
page_size_query_param   前端发送的每页数目关键字名,默认为None
max_page_size           前端最多能设置的每页数量
```

```python
# ListAPIView
# http://127.0.0.1:8000/api/books2/?ppage=1&ssize=4

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "ssize"
    max_page_size = 4
    page_query_param = "ppage"


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardPageNumberPagination


# APIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class BookListView(APIView):

    def get(self, request, *args, **kwargs):
        obj_list = Book.objects.all()

        # 创建分页对象
        page_obj = PageNumberPagination()
        page_obj.page_size = 2
        page_obj.page_query_param = 'ppage'
        page_obj.max_page_size = 4
        page_obj.page_size_query_param = 'ssize'
        # 筛选数据
        obj_list = page_obj.paginate_queryset(queryset=obj_list, request=request, view=self)
        # 获取上一页
        previous_url = page_obj.get_previous_link()
        # 获取下一页
        next_url = page_obj.get_next_link()

        ser = BookSerializer(instance=obj_list, many=True)
        return CustomerResponse(data=ser.data, previous_url=previous_url, next_url=next_url)
```

### LimitOffsetPagination

```shell
default_limit       默认限制, 默认值与PAGE_SIZE设置一致
limit_query_param   limit参数名, 默认 limit
offset_query_param  offset参数名, 默认 offset
max_limit           最大limit限制, 默认None
```

```python
# ListAPIView
# "http://127.0.0.1:8000/api/books2/?llimit=2&ooffset=2"

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = "llimit"
    offset_query_param = "ooffset"
    max_limit = 4

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardLimitOffsetPagination
```

### CursorPagination

```shell
cursor_query_param  默认查询字段, 不需要修改
page_size           每页数目
ordering            按什么排序, 需要指定
```

```python
# ListAPIView
# http://127.0.0.1:8000/api/books2/?ccuror=cD02

from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination


class StandardCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-id'
    cursor_query_param = 'ccuror'


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardCursorPagination


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
```

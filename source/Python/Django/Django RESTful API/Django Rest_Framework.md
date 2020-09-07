# Django Rest_Framework

## 安装

```shell
pip install djangorestframework
```

## 基本使用

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

        # 如果转换多个模型对象数据，则需要加上many=True
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

## 请求与相应

### Request

```shell
request.data            返回解析之后的请求体数据
request.query_params    与Django标准的request.GET相同
```

### Response

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

APIView是REST framework提供的所有视图的基类，继承自Django的View父类

传入到视图方法中的是REST framework的Request对象，而不是Django的HttpRequeset对象
在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制


支持定义的类属性
    authentication_classes  列表或元祖，身份认证类
    permissoin_classes      列表或元祖，权限检查类
    throttle_classes        列表或元祖，流量控制类
```

#### GenericAPIView[通用视图类]

```shell
rest_framework.generics.GenericAPIView

继承自APIVIew，主要增加了操作序列化器和数据库查询的方法，
作用是为下面Mixin扩展类的执行提供方法支持。通常在使用时，可搭配一个或多个Mixin扩展类
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
# 返回序列化器类，默认返回serializer_class, 可重写
def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer

# get_serializer(self, args, *kwargs)
# 返回序列化器对象，主要用来提供给Mixin扩展类使用

# get_queryset(self)
# 返回视图使用的查询集，主要用来提供给Mixin扩展类使用
# 是列表视图与详情视图获取数据的基础，默认返回queryset属性

# get_object(self)
# 返回详情视图所需的模型类数据对象，主要用来提供给Mixin扩展类使用
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
# 列表视图扩展类，提供list(request, *args, **kwargs)方法快速实现列表视图，返回200状态码

class BookView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)
```

#### CreateModelMixin

```python
# 创建视图扩展类，提供create(request, *args, **kwargs)方法快速实现创建资源的视图，成功返回201状态码

# 如果序列化器对前端发送的数据验证失败，返回400错误

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
# 详情视图扩展类，提供retrieve(request, *args, **kwargs)方法，可以快速实现返回一个存在的数据对象

# 状态码 200 or 400

class BookDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request)
```

#### UpdateModelMixin

```python
# 更新视图扩展类，提供update(request, *args, **kwargs)方法，可以快速实现更新一个存在的数据对象

# 同时也提供partial_update(request, *args, **kwargs)方法，可以实现局部更新

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
# 删除视图扩展类，提供destroy(request, *args, **kwargs)方法，可以快速实现删除一个存在的数据对象

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
使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中

list() 提供一组数据
retrieve() 提供单个数据
create() 创建数据
update() 保存数据
destory() 删除数据

ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等

视图集只在使用as_view({"get":"list"})方法的时候，才会将action动作与具体请求方式对应上
```

#### ViewSet

```python
# 继承自APIView与ViewSetMixin，作用也与APIView基本类似，提供了身份认证、权限校验、流量管理等

# ViewSet主要通过继承ViewSetMixin来实现在调用as_view()时传入字典（如{‘get’:’list’}）的映射处理工作

# 在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法

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
# 提供GenericAPIView提供的基础方法，可以直接搭配Mixin扩展类使用

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
# urls.py
    path('books/', views.BookViewSet.as_view({"get": "login"}), ),

class BookViewSet(GenericViewSet, ListModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    def login(self, request):
        # 获取本次请求的视图方法名
        print(self.action)
        pass
```

```python
from rest_framework.decorators import action

from . import models
from .ser import BookSerializer


class BookView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer

    # action装饰器, 生成对应路由, detail=False,生成的路由是否带ID
    @action(["get", "post"], detail=False)
    def get_1(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
```

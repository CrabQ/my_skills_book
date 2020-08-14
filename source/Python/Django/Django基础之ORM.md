# Django基础之ORM

Object Relational Mapping

## 字段

```python
from django.db import models
from multiselectfield import MultiSelectField

sex_type = (('1', '男'), ('0', '女'))

class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学院报名后,请改为真实姓名!')
    sex = models.CharField('性别', choices=sex_type, max_length=1, default='1', blank=True, null=True)
    introduce_from = models.ForeignKey('self', verbose_name='转介绍自学员', blank=True, null=True, on_delete=models.CASCADE)
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    date = models.DateTimeField("咨询日期", auto_now_add=True)
    consultant = models.ForeignKey('UserInfo', verbose_name='销售', related_name='customers', blank=True, null=True, on_delete=models.CASCADE)
    class_list = models.ManyToManyField('ClassList', verbose_name='已报班级', blank=True, null=True)

    class Meta:
        # 排序
        ordering = ['id', ]
        # 后台显示名称
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表'
```

### multiselectfield

```python
pip install django-multiselectfield
```

## 配置MySQL

```python
# 修改settings.py文件

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'HOST':'127.0.0.1',
           'PORT':'3306',
           'NAME': 'test_dj',
           'USER':'root',
           'PASSWORD':'123',
       }
   }

# 项目文件夹下的init文件中,写上下面两句
import pymysql
pymysql.install_as_MySQLdb()

# 时区关闭,MySQL时区会有问题
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

```

## 数据库同步指令

```python
python manage.py makemigrations
python manage.py migrate
```

## ORM单表操作

```python
# 增
Book(title='title1', price=2.33, pub_date=datetime.datetime.now(), publish='publish').save()
Book.objects.create(title='title2', price=3.22, pub_date=datetime.datetime.now(), publish='publish1')

# 增加或者更新, defaults填写新字段
Book.objects.update_or_create(id=100, defaults={'title':'update'})
# 返回一个元祖,对象,以及是否create
# (<Book: update>, False)

# 删
Book.objects.filter(id=100).delete()
# (1, {'app1.Book': 1})
Book.objects.get(id=101).delete()
# (1, {'app1.Book': 1})

# 改
Book.objects.filter(id=102).update(title='update102')
# 1

# 查
Book.objects.all()

Book.objects.filter(id=103)
# <QuerySet [<Book: titel4>]>

Book.objects.get(id=103)
# <Book: titel4>

Book.objects.exclude(id=103)

Book.objects.order_by('-id')

Book.objects.order_by('-id').reverse()

Book.objects.order_by('-id').reverse().count()
# 101

Book.objects.first()
# <Book: update102>

Book.objects.last()
# <Book: update>

Book.objects.filter(id=1).exists()
# False

Book.objects.filter(id=110).values('id', 'title')
# <QuerySet [{'id': 110, 'title': 'titel11'}]>

Book.objects.filter(id=110).values_list('id', 'title')
# <QuerySet [(110, 'titel11')]>

Book.objects.values_list('title').distinct().count()
# 98
Book.objects.values_list('title').count()
# 101

Book.objects.filter(id__gt=199)
# <QuerySet [<Book: update>, <Book: update>, <Book: update>]>

# 大于等于
Book.objects.filter(id__gte=199)
# <QuerySet [<Book: update>, <Book: update>, <Book: update>, <Book: update>]>

Book.objects.filter(id__in = [199, 200])
# <QuerySet [<Book: update>, <Book: update>]>

Book.objects.filter(id__range = [199, 200])
# <QuerySet [<Book: update>, <Book: update>]>

Book.objects.filter(title__contains='update')
# <QuerySet [<Book: update102>, <Book: update>, <Book: update>, <Book: update>, <Book: update>]>

# 不区分大小写
Book.objects.filter(title__icontains='update')

Book.objects.filter(title__startswith='update')
# <QuerySet [<Book: update102>, <Book: update>, <Book: update>, <Book: update>, <Book: update>]>

Book.objects.filter(title__endswith='update')
# <QuerySet [<Book: update>, <Book: update>, <Book: update>, <Book: update>]>

Book.objects.filter(pub_date__year__gt=2018)
```

## ORM多表操作

```python
# 一对一
models.OneToOneField(to='表名',to_field='字段名',on_delete=models.CASCADE)

# 一对多
models.ForeignKey(to='表名',to_field='字段名',on_delete=models.CASCADE)

# 多对多,自动创建第三表
models.ManyToManyField(to='另外一个表名')

from app1.models import Book, Author, AuthorDetail, Publish
# Author一对一AuthorDetail
# Publish一对多Book
# Author多对多Book
```

### 增

```python
new_ad = AuthorDetail.objects.create(birthday='2020-08-08', tel='1882932482', addr='广州市')

Author.objects.create(name='小明', age=40, author_detail=new_ad)

Author.objects.create(name='小明', age=40, author_detail_id=new_ad.id)

# 一对多
new_p = Publish.objects.create(name='小明出版社', email='m@qq.com', city='广州')
Book.objects.create(title='小明的故事', price=28.8, pub_date=datetime.now(), pub=new_p)
Book.objects.create(title='小明的故事2', price=28.8, pub_date=datetime.now(), pub_id=new_p.id)

# 多对多
# 方式1
book1 = Book.objects.get(id=1)
book1.aut.add(*[3,4])

# 方式2
au1 = Author.objects.get(id=3)
au2 = Author.objects.get(id=4)
book2 = Book.objects.get(id=2)
book2.aut.add(*[au1, au2])
```

### 删

```python
# 一对一与一对多一致
# 表1外键关联表2, 表1删除不影响表2, 表2删除影响表1
Publish.objects.get(id=1).delete()

# 多对多
book_obj = Book.objects.get(id=3)
book_obj.aut.remove(1)
# 全清
book_obj.aut.clear(1)
```

### 更新

```python

# 删除然后更新
book_obj.aut.set(['2','3'])
```

## 基于对象的跨表查询

```python
# 关系属性(字段)写在哪个类(表)里面,从当前类(表)的数据去查询它关联类(表)的数据叫做正向查询,反之叫做反向查询

# 一对一正向, 对象.关联属性名称
Author.objects.filter(name='小明').first().author_detail.tel
# 反向, 对象.小写类名
AuthorDetail.objects.filter(tel='222').first().author.name

# 一对多正向
Book.objects.filter(title='小明的故事').first().pub.name
# 反向, 对象.类名小写_set
Publish.objects.filter(name="小明出版社").first().book_set.all()

# 多对多正向
Book.objects.filter(title='小明的故事').first().aut.all()
# 反向
Author.objects.filter(name='小明').first().book_set.all()
```

## 基于双下划线的跨表查询

```python
# 一对一正向
Author.objects.filter(name='小明').values('author_detail__tel')
# 反向
AuthorDetail.objects.filter(author__name='小明').values('author__age')

# 一对多正向
Book.objects.filter(title='小明的故事').values('pub__name')
# 反向, 对象.类名小写_set
Publish.objects.filter(name="小明出版社").values('book__title')

# 多对多正向
Book.objects.filter(title='小明的故事').values('aut__name')
# 反向
Author.objects.filter(name='小明').values('book__title')
```

## 聚合

```python
from django.db.models import Avg,Max,Min,Sum,Count

Author.objects.filter(name='小明').values('book__price').aggregate(a=Avg('book__price'), c=Count('book__price'), s=Sum('book__price'))
```

## 分组

```python
# annotate

# Publish.objects作为分组依据
# Publish.objects.annotate(a = Avg('book__price')).values('name','a')

# pub_id作为分组依据
# Book.objects.values('pub_id').annotate(a=Avg('price')).values('pub_id','a')
```

## F查询和Q查询

```python
from django.db.models import F,Q

# F  针对自己单表中字段的比较和处理
Book.objects.filter(id__gt=F('pub_id'))
Book.objects.all().update(price=F('price')+100)

# filter()等方法中的逗号是与操作
# Q    &  |  非~
# &优先级高
Book.objects.filter(Q(Q(id=4)|Q(id=6))&Q(price__gt=140))
```

### Q对象高级操作

```python
# 将查询条件的左边也变成字符串的形式
from django.db.models import Q

q = Q()
q.connector = 'or'
q.children.append(('name', 'hi'))
q.children.append(('price__lt', 600))
models.Book.objects.filter(q)
```

### 字符串拼接

```python
from django.db.models.functions import Concat
from django.db.models import Value

models.Product.objects.update(name=Concat(F('name'),Value('新款')))
```

## QuerySet方法

### update()与save()的区别

两者都是对数据的修改保存操作, 但是save()函数是将数据列的全部数据项全部重新写一遍

而update()则是针对修改的项进行更新, 效率高耗时少

推荐对数据的修改保存用update()

### bulk_create批量插入数据

```python

# 批量增
obj_list = []
for i in range(1,100):
    obj_list.append(Book(title=f'title{i}', price=i+.33, pub_date=datetime.datetime.now(), publish=f'publish{i}'))

Book.objects.bulk_create(obj_list)
```

## 执行原生sql

```python
Publish.objects.raw('select * from app1_publish;')
# <RawQuerySet: select * from Publish>

from django.db import connection
cursor = connection.cursor()
cursor.execute(sql,)
cursor.fetchall()

# 展示sql
# connection.queries
```

## 事务和锁

```python
# django开启事务
# 1. 全局开启(settings.py)
DATABASES = {
    'default': {
            #全局开启事务，绑定的是http请求响应整个过程
            "ATOMIC_REQUESTS": True,
                }
            }

# 2. 局部使用事务
# 2.1. 用法1
from django.db import transaction

@transaction.atomic
def viewfunc(request):
    do_stuff()

# 2.2. 用法2
from django.db import transaction

def viewfunc(request):
    do_stuff()

    with transaction.atomic():   #保存点
        do_more_stuff()

    do_other_stuff()

# 在事物里面加锁,直至事务结束
# select * from t1 where id=1 for update;
models.T1.objects.select_for_update().fitler(id=1)
```

## 创建超级用户

```python
python manage.py createsuperuser
```

## 外部文件操作django的models

```python
#外部文件使用django的models,需要配置django环境

import os

if __name__ == '__main__':
    # manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'four_pro.settings')
    import django
    django.setup()

    from app01 import models
```

## 字段合集

```python
复制代码
AutoField(Field)
        - int自增列，必须填入参数 primary_key=True

BigAutoField(AutoField)
    - bigint自增列，必须填入参数 primary_key=True

    注：当model中如果没有自增列，则自动会创建一个列名为id的列
    from django.db import models

SmallIntegerField(IntegerField):
    - 小整数 -32768 ～ 32767

PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField)
    - 正小整数 0 ～ 32767
IntegerField(Field)
    - 整数列(有符号的) -2147483648 ～ 2147483647

PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField)
    - 正整数 0 ～ 2147483647

BigIntegerField(IntegerField):
    - 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807

BooleanField(Field)
    - 布尔值类型

NullBooleanField(Field):
    - 可以为空的布尔值

CharField(Field)
    - 字符类型
    - 必须提供max_length参数， max_length表示字符长度

TextField(Field)
    - 文本类型

EmailField(CharField)：
    - 字符串类型，Django Admin以及ModelForm中提供验证机制

IPAddressField(Field)
    - 字符串类型，Django Admin以及ModelForm中提供验证 IPV4 机制

GenericIPAddressField(Field)
    - 字符串类型，Django Admin以及ModelForm中提供验证 Ipv4和Ipv6
    - 参数：
        protocol，用于指定Ipv4或Ipv6， 'both',"ipv4","ipv6"
        unpack_ipv4， 如果指定为True，则输入::ffff:192.0.2.1时候，可解析为192.0.2.1，开启此功能，需要protocol="both"

URLField(CharField)
    - 字符串类型，Django Admin以及ModelForm中提供验证 URL

SlugField(CharField)
    - 字符串类型，Django Admin以及ModelForm中提供验证支持 字母、数字、下划线、连接符（减号）

CommaSeparatedIntegerField(CharField)
    - 字符串类型，格式必须为逗号分割的数字

UUIDField(Field)
    - 字符串类型，Django Admin以及ModelForm中提供对UUID格式的验证

FilePathField(Field)
    - 字符串，Django Admin以及ModelForm中提供读取文件夹下文件的功能
    - 参数：
            path,                      文件夹路径
            match=None,                正则匹配
            recursive=False,           递归下面的文件夹
            allow_files=True,          允许文件
            allow_folders=False,       允许文件夹

FileField(Field)
    - 字符串，路径保存在数据库，文件上传到指定目录
    - 参数：
        upload_to = ""      上传文件的保存路径
        storage = None      存储组件，默认django.core.files.storage.FileSystemStorage

ImageField(FileField)
    - 字符串，路径保存在数据库，文件上传到指定目录
    - 参数：
        upload_to = ""      上传文件的保存路径
        storage = None      存储组件，默认django.core.files.storage.FileSystemStorage
        width_field=None,   上传图片的高度保存的数据库字段名（字符串）
        height_field=None   上传图片的宽度保存的数据库字段名（字符串）

DateTimeField(DateField)
    - 日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]

DateField(DateTimeCheckMixin, Field)
    - 日期格式      YYYY-MM-DD

TimeField(DateTimeCheckMixin, Field)
    - 时间格式      HH:MM[:ss[.uuuuuu]]

DurationField(Field)
    - 长整数，时间间隔，数据库中按照bigint存储，ORM中获取的值为datetime.timedelta类型

FloatField(Field)
    - 浮点型

DecimalField(Field)
    - 10进制小数
    - 参数：
        max_digits，小数总长度
        decimal_places，小数位长度

BinaryField(Field)
    - 二进制类型
```

### 与mysql字段对应关系

```python
'AutoField': 'integer AUTO_INCREMENT',
'BigAutoField': 'bigint AUTO_INCREMENT',
'BinaryField': 'longblob',
'BooleanField': 'bool',
'CharField': 'varchar(%(max_length)s)',
'CommaSeparatedIntegerField': 'varchar(%(max_length)s)',
'DateField': 'date',
'DateTimeField': 'datetime',
'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
'DurationField': 'bigint',
'FileField': 'varchar(%(max_length)s)',
'FilePathField': 'varchar(%(max_length)s)',
'FloatField': 'double precision',
'IntegerField': 'integer',
'BigIntegerField': 'bigint',
'IPAddressField': 'char(15)',
'GenericIPAddressField': 'char(39)',
'NullBooleanField': 'bool',
'OneToOneField': 'integer',
'PositiveIntegerField': 'integer UNSIGNED',
'PositiveSmallIntegerField': 'smallint UNSIGNED',
'SlugField': 'varchar(%(max_length)s)',
'SmallIntegerField': 'smallint',
'TextField': 'longtext',
'TimeField': 'time',
'UUIDField': 'char(32)',
```

### 字段参数

```python
null 用于表示某个字段可以为空

unique 如果设置为unique=True 则该字段在此表中必须是唯一的

db_index 如果db_index=True 则代表着为此字段设置索引

default 默认值

DateField和DateTimeField
auto_now_add 配置auto_now_add=True n创建数据记录的时候会把当前时间添加到数据库
auto_now     配置上auto_now=True 每次更新数据记录的时候会更新该字段
```

### 关系字段

ForeignKey

```python
外键类型在ORM中用来表示外键关联关系, 一般把ForeignKey字段设置在 '一对多'中'多'的一方

ForeignKey可以和其他表做关联关系, 也可以和自身做关联关系

字段参数
to 设置要关联的表

to_field 设置要关联的表的字段

on_delete 当删除关联表中的数据时,当前表与其关联的行的行为
models.CASCADE 删除关联数据,与之关联也删除

db_constraint 是否在数据库中创建外键约束,默认为True
```

OneToOneField

```python
通常一对一字段用来扩展已有字段. (简单的信息一张表, 隐私的信息另一张表, 之间通过一对一外键关联)
```

## Django终端打印SQL语句

```python
# obj.query 可以查看sql语句

# settings.py 添加配置即可
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}
```

## 序列化

```python
from django.core import serializers

def ser(request):
    user_list=models.User.objects.all()

    ret=serializers.serialize('json',user_list)

    return HttpResponse(ret)
```

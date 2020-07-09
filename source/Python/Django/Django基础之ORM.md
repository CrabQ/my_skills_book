# Django基础之ORM

Object Relational Mapping

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

# 批量增
obj_list = []
for i in range(1,100):
    obj_list.append(Book(title=f'title{i}', price=i+.33, pub_date=datetime.datetime.now(), publish=f'publish{i}'))

Book.objects.bulk_create(obj_list)

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

# 增
from app1.models import Book, Author, AuthorDetail, Publish
# Author一对一AuthorDetail
# Publish一对多Book
# Author多对多Book

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

# 删
# 一对一与一对多一致
# 表1外键关联表2, 表1删除不影响表2, 表2删除影响表1
Publish.objects.get(id=1).delete()

# 多对多
book_obj = Book.objects.get(id=3)
book_obj.aut.remove(1)
# 全清
book_obj.aut.clear(1)
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

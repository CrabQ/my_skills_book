# Python进阶

## Python高级

### Python的函数参数传递

传地址,传递的是内存中对对象的引用(可变对象与不可变对象的区别)

### Python中的元类(metaclass)

type可以动态的创建类,即Python用来创建所有类的元类

```Python
a = type('test', (), {})
a
<class '__main__.test'>
a()
<__main__.test object at 0x000002EDB1362048>
```

#### 作用

- 拦截类的创建
- 修改类
- 返回修改之后的类

自定义元类,修改方法名为大写

```python
class UpperAttrMetaClass(type):
    def __new__(cls,  future_class_name, future_class_parents, future_class_attr):
        new_attr = {}
        for k, v in future_class_attr.items():
            if not k.startswith('__'):
                new_attr[k.upper()] = v

        return super(UpperAttrMetaClass, cls).__new__(cls, future_class_name, future_class_parents, new_attr)

class Test(metaclass=UpperAttrMetaClass):
    def test(self):
        pass

if __name__ == '__main__':
    print(hasattr(Test, 'test'))
    # False
    print(hasattr(Test, 'TEST'))
    # True
```

### 类变量和实例变量

类变量是可在类的所有实例之间共享的值(也就是说,它们不是单独分配给每个实例的)

实例变量是实例化之后,每个实例单独拥有的变量

```Python
class Test():
    num = 0

    def __init__(self, name):
        self.name = name
        Test.num += 1

if __name__ == '__main__':
    a = Test('a')
    print(a.name, a.num) # a 1

    b = Test('b')
    print(b.name, b.num) # b 2
```

### Python自省

自省就是面向对象的语言所写的程序在运行时,所能知道对象的类型.

简单一句就是运行时能够获得对象的类型.

比如`type(),dir(),getattr(),hasattr(),isinstance()`

### 字典推导式

```python
{k:v for k, v in ((1, 11), (2, 22))}
{1: 11, 2: 22}
```

### Python中单下划线和双下划线

`__foo__`:一种约定,Python内部的名字,用来区别其他用户自定义的命名,以防冲突,就是例如`__init__(),__del__(),__call__()`这些特殊方法

`_foo`:一种约定,用来指定变量私有.程序员用来指定私有变量的一种方式.不能用`from module import *`导入,其他方面和公有一样访问

`__foo`:这个有真正的意义:解析器用`_classname__foo`来代替这个名字,以区别和其他类相同的命名,它无法直接像公有成员一样随便访问,通过对象名._类名__xxx这样的方式可以访问.

### 字符串格式化:%和.format

更喜欢`f'this is {name}'`

### 迭代器和生成器

生成器(generator):一边循环一边计算的机制

凡是可作用于 for 循环的对象都是 Iterable 类型

凡是可作用于 next() 函数的对象都是 Iterator 类型

集合数据类型如 list 、 dict 、 str 等是 Iterable 但不是 Iterator,不过可以通过 iter() 函数获得一个 Iterator 对象

```shell
isinstance((x for x in range(3)), Iterable)
True
isinstance((x for x in range(3)), Iterator)
True

isinstance([], Iterable)
True
isinstance([], Iterator)
False
```

### `*args` and `**kwargs`

`*args`被打包成tuple
`**kwargs` 被打包成dict

### 闭包

闭包(closure)是函数式编程的重要的语法结构,指的是一个内嵌函数引用其外部作作用域的变量.

- 必须有一个内嵌函数
- 内嵌函数必须引用外部函数中的变量
- 外部函数的返回值必须是内嵌函数

```shell
def line_conf(a, b):
    def inner(x):
        return a*x+b
    return inner
```

### 面向切面编程AOP和装饰器

装饰器的作用就是为已经存在的对象添加额外的功能

- 引入日志
- 函数执行时间统计
- 执行函数前预备处理
- 执行函数后清理功能
- 权限校验等场景
- 缓存

### Python中重载

> [引自知乎](http://www.zhihu.com/question/20053359)

函数重载主要是为了解决两个问题.

- 可变参数类型
- 可变参数个数

另外,一个基本的设计原则是,仅仅当两个函数除了参数类型和参数个数不同以外,其功能是完全相同的,此时才使用函数重载,如果两个函数的功能其实不同,那么不应当使用重载,而应当使用一个名字不同的函数.

好吧,那么对于情况 1 ,函数功能相同,但是参数类型不同,python 如何处理？答案是根本不需要处理,因为 python 可以接受任何类型的参数,如果函数的功能相同,那么不同的参数类型在 python 中很可能是相同的代码,没有必要做成两个不同函数.

那么对于情况 2 ,函数功能相同,但参数个数不同,python 如何处理?大家知道,答案就是缺省参数.对那些缺少的参数设定为缺省参数即可解决问题.因为你假设函数功能相同,那么那些缺少的参数终归是需要用的.

好了,鉴于情况 1 跟 情况 2 都有了解决方案,python 自然就不需要函数重载了.

### 新式类和旧式类

Python3里的类全部都是新式类

```python
class A():
    pass

class B(A):
    pass

class C():
    pass

class D(B, C):
    pass
```

按照经典类的查找顺序从左到右深度优先的规则,在访问`D.foo1()`的时候,先找到B,没有,深度优先,访问A,找到了foo1(),所以这时候调用的是A的foo1()

### Python中的作用域

本地作用域(Local)→当前作用域被嵌入的本地作用域(Enclosing locals)→全局/模块作用域(Global)→内置作用域(Built-in)

### GIL线程全局锁

线程全局锁(Global Interpreter Lock),即Python为了保证线程安全而采取的独立线程运行的限制,说白了就是一个核只能在同一时间运行一个线程.匿名函数

```shell

```

对于io密集型任务,python的多线程起到作用,但对于cpu密集型任务,python的多线程几乎占不到任何优势,还有可能因为争夺资源而变慢.

### 协程

协程其实可以认为是比线程更小的执行单元.自带CPU上下文,在合适的时机,我们可以把一个协程切换到另一个协程.只要这个过程中保存或恢复 CPU上下文那么程序还是可以运行的.

线程切换从系统层面远不止保存和恢复CPU上下文这么简单.操作系统为了程序运行的高效性每个线程都有自己缓存Cache等等数据,操作系统还会帮你做这些数据的恢复操作.所以线程的切换非常耗性能.

但是协程的切换只是单纯的操作CPU的上下文,所以一秒钟切换个上百万次系统都抗的住.

简单点说协程是进程和线程的升级版,进程和线程都面临着内核态和用户态的切换问题而耗费许多切换时间,而协程就是用户自己控制切换的时机,不再需要陷入系统的内核态

### lambda函数

匿名函数

```Python
map( lambda x : x + 1, [1, 2, 3] )
```

### Python函数式编程

```Python
filter(lambda x: x > 5, [4,5,6])
map( lambda x : x + 1, [1, 2, 3] )
```

### Python里的拷贝

```shell
# 浅拷贝: 仅拷贝顶层对象的引用
# 深拷贝: 子对象也拷贝
```

### Python的List

```shell
# is是对比地址
# ==是对比值
```

### read,readline和readlines

```shell
# read 读取整个文件
# readline 读取下一行,使用生成器方法
# readlines 读取整个文件到一个迭代器以供我们遍历
```

### Python2和3的区别

Python3改进

```shell
print成为函数
编码问题,Python3不再有Unicode对象,默认str就是Unicode
除法变化,Python3除号返回浮点数
类型注解(type hint).帮助IDE实现类型检查
优化的super()方便直接调用父类函数
高级解包操作. a, b, *rest = range(10)
Keyword only arguments.限定关键字参数
Chained exceptions. Python3重新抛出异常不会丢失栈信息
一切返回迭代器range, zip, map, dict.values, ect.are all iterators
yield from 链接子生成器
asyncio内置库,async/await原生协程支持异步编程
新的内置库enum, mock, asyncio, ipaddress, concurrent.futures等
生成的pyc文件统一放到__pycache__
一些内置库的修改. urllib, selector等
性能优化等
```

### 整数进制转换

```python
# 转换为二进制
bin(10)
Out[12]: '0b1010'
int("0b1010", 2)
Out[14]: 10

# 转换为八进制
oct(10)
Out[2]: '0o12'
int("0o12", 8)
Out[3]: 10

# 转换为十六进制
hex(10)
Out[4]: '0xa'
int("0xa", 16)
Out[5]: 10
```

## Python垃圾回收机制

```shell
Python变量地址为栈区, 变量指向的值的地址存放位置为堆区

引用计数为主, 某个值的地址引用计数(从栈区->堆区)为0, 则回收地址

为解决循环引用问题, 引入 标记-清除
每次内存空间将要耗尽时扫描栈区, 标记所有可直接或间接访问到的对象为存活对象, 清除无标记对象

为提升 标记-清除 效率, 引入 分代回收
一个变量多次扫描都被引用, 变量权重增加, 从新生代->青春代

新生代->青春代->老年代, 等级越高, 被垃圾回收机制扫描的频率越低
以空间换时间(如果某个变量刚移入青春代就解除关联, 则无法及时清除)
```

## 装饰器

```python
import time
# 留原函数的文档和函数名属性
from functools import wraps

# 无参装饰器
def timer(func):
    # 将原函数的属性赋值给wrap函数
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'time:{time.time()-start}')
        return res
    return wrap

@timer
def run():
    time.sleep(1)
    print('running')

run()
print(run.__name__)

# 有参装饰器, 即在外面再包一层
def outer(name):
    def timer(func):
        # 将原函数的属性赋值给wrap函数
        @wraps(func)
        def wrap(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            print(f'{name}, time:{time.time()-start}')
            return res
        return wrap
    return timer

@outer('first')
def run():
    time.sleep(1)
    print('running')

run()
```

### 类装饰器

```python
import time

class LogTime():
    # 装饰器加参数
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        def _log(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            print(f'run: {time.time()-start}')
            return  res
        return _log

@LogTime()
def sleep():
    time.sleep(2)
```

## 迭代器与生成器

### 迭代器

```shell
# 可迭代对象(Iterable): 内置有__iter__方法的对象都是可迭代对象

# 迭代器对象(Iterator): 调用obj.iter()方法

# for循环本质就是调用可迭代对象内置的iter方法生成迭代器对象, 再调用该迭代器对象的next方法将取值, 直到捕捉StopIteration异常，结束迭代

>>> s={1,2,3}
>>> i = iter(s) # 本质就是在调用s.__iter__(),返回s的迭代器对象i
>>> i
<set_iterator object at 0x000002D0F6EFB778>
>>> next(i) # 本质就是在调用i.__next__()
1
>>> next(i)
2
>>> next(i)
3
>>> next(i)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

```python
# 迭代器
def my_iter(obj):
    iter_obj = obj.__iter__()
    while True:
        try:
            print(iter_obj.__next__())
        except StopIteration:
            break

my_iter((1,2,3,4))

```

## 生成器

```shell
# 函数体包含yield关键字, 调用函数不会执行函数体代码, 得到的返回值即生成器对象

# 生成器内置有__iter__和__next__方法, 生成器是迭代器

def my_range(start, stop, step):
    print('start')
    while start<stop:
        yield start
        start += step

>>> g = my_range(1, 4, 1)
>>> next(g)  # 触发函数执行,遇到yield停止,将yield后的值返回并在当前位置挂起函数
start
1
>>> next(g)
2
>>> next(g)
3
>>> next(g)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

```python
# send
def f1():
    l = []
    while True:
        k = yield '第一次yield'
        l.append(k)
        print('第一次yield', l)
        k = yield '第二次yield'
        l.append(k)
        print('第二次yield', l)

>>> g = f1()
# 需要初始化一次,让函数挂起在food=yield等待调用g.send()方法为其传值
# g.send(None) = next(g)
>>> g.send(None)
'第一次yield'

>>> g.send(1)
第一次yield [1]
'第二次yield'

>>> g.send(2)
第二次yield [1, 2]
'第一次yield'

>>> g.send(3)
第一次yield [1, 2, 3]
'第二次yield'

>>> g.send(4)
第二次yield [1, 2, 3, 4]
'第一次yield'
```

通过装饰器为yield生成器初始化

```python
if __name__ == '__main__':

    def init(func):
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            next(res)
            return res
        return inner

    @init
    def eat():
        print('ready to eat')
        l = []
        while True:
            food = yield l
            l.append(food)

    e = eat()
    print(e.send('棉花糖'))
    print(e.send('奶茶'))
    print(e.send('炸鸡'))

# ready to eat
# ['棉花糖']
# ['棉花糖', '奶茶']
# ['棉花糖', '奶茶', '炸鸡']
```

## 三元表达式

```shell
# res = 条件成立时返回的值 if 条件 else 条件不成立时返回的值
>>> 1 if 1<2 else 2
1
>>> 1 if 1>2 else 2
2

## 列表生成式
>>> [x for x in [1,2,3]]
[1, 2, 3]

# 生成器表达式
# yield关键字或者()
>>> (x for x in [1,2,3])
<generator object <genexpr> at 0x000002D0F6EED2C8>
>>>
```

## 函数递归

```shell
# sys.getrecursionlimit()查看递归深度,默认1000

# sys.setrecursionlimit()设定该值, 但受限于主机操作系统栈大小

# python不是一门函数式编程语言, 无法对递归进行尾递归优化

def f(n):
    if n == 1 or n ==2:
        return 1
    else:
        return f(n-1)+f(n-2)

print(f(5))


# 要求打印嵌套多层的列表的所有元素
items=[[1,2],3,[4,[5,[6,7]]]]

def print_list(l):
    for i in l:
        if isinstance(i, list):
            print_list(i)
        else:
            print(i, end="")

print_list(items)
```

## 包

```shell
导入包实际上就是执行包中的__init__.py

使用 from 包 import *, 由__init__.py下的__all__变量控制导入内容
单个Python文件导入也一样
```

## 封装

```python
    class Student():
        def __init__(self, name):
            self.__name = name

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, val):
            self.__name = val

        @name.deleter
        def name(self):
            del self.__name

    s = Student('hong')
    s.name = 'ming'
    del s.name
```

## 继承与派生

### super

```python
class A:
    def test(self):
        super().test()

class B:
    def test(self):
        print('from B')

class C(A,B):
    pass

>>> C.mro() #属性查找时按照顺序C->A->B->object, B就相当于A的父类
[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,<class ‘object'>]
>>> obj=C()
>>> obj.test() # 属性查找的发起者是类C的对象obj,所以中途发生的属性查找都是参照C.mro()
from B
```

### 组合

## 多态与鸭子类型

### 多态

```python
# 多态性的本质在于不同的类中定义有相同的方法名

# 父类指定子类继承后一定要实现的方法(定义抽象类)

from abc import ABCMeta, abstractmethod

# 指定metaclass属性将类设置为抽象类
# 抽象类本身只是用来约束子类的, 不能被实例化
class A(metaclass=ABCMeta):
    # 限制子类必须定义有一个名为b的方法
    @abstractmethod
    def b(self):
        pass


class B(A):
    def b(self):
        pass
```

### 鸭子类型

```shell
当看到一只鸟走起来像鸭子,游泳起来像鸭子,叫起来也像鸭子,这只鸟就可以被称为鸭子

关注点在对象的行为,而不是类型(duck typing)

比如 file, String, socket对象都支持read/write方法(file like object)

又比如list.extend()方法中,我们并不关心它的参数是不是list,只要它是可迭代的,所以它的参数可以是list/tuple/dict/字符串/生成器等

鸭子类型在动态语言中经常使用,非常灵活,使得python不像java那样专门去弄一大堆的设计模式
```

## 绑定方法与非绑定方法

```python
# @classmethod 绑定方法
# @staticmethod 非绑定方法

class MySQL:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.id = self.create_id()

    @classmethod
    def from_conf(cls): # 从配置文件中读取配置进行初始化
        return cls(settings.HOST,settings.PORT)

    @staticmethod
    def create_id():
        return uuid.uuid4()

>>> MySQL.from_conf # 绑定到类的方法, 对象也可以调用, 不过自动传入的第一个参数仍然是类, 也就是说这种调用是没有意义的
<bound method MySQL.from_conf of <class ‘__main__.MySQL'>>
>>> conn=MySQL.from_conf() # 调用类方法，自动将类MySQL当作第一个参数传给cls
```

## 反射

```python
>>> class Student():
...     def name(self):
...         pass
>>>
>>> s = Student()
>>> hasattr(s, 'name')
True

>>> getattr(s, 'name')
<bound method Student.name of <__main__.Student object at 0x0000021DF9B4B408>>

>>> setattr(s, 'age', 18)
>>> s.__dict__
{'age': 18}

>>> delattr(s, 'age')
>>> s.__dict__
{}
```

## 内置方法

```python
>>> class Student():
...     def __str__(self):
...         return 'print'
...     def __del__(self):
...         print('del')
...
>>> s = Student()
>>> print(s)
print
>>>
>>> s = 1
del
```

## 元类

### class 关键字

```shell
class关键字定义的类本身也是一个对象
负责产生该对象的类称之为元类
内置的元类为type

class关键字创建类
    1. 获取类型 class_name = 'People'
    2. 获取基类 class_bases = (object,)
    3. 执行类体代码,获取类名称空间 class_dict = {...}
    # exec('class_body', {}, class_dict)
    4. 调用元类获取类 People = type(class_name, class_bases, class_dict)


控制类的产生:
    __new__  生成空对象
    __init__ 初始化__new__生成的对象

控制类的调用(生成类的对象):
    __call__ 控制类的调用
    # class People() --> people的元类('People',class_bases, class_dict) --> 即调用type.__call__生成people的对象
```

在元类中控制把自定义类的数据属性都变成大写

```python
# 继承了type的才是元类
class UpMeta(type):
    # 生成空的对象
    def __new__(cls, name, class_bases, class_dict):
        up_arrts = {}
        # 排除双下划线,以及方法
        for k, v in class_dict.items():
            if callable(v) or k.startswith('__'):
                up_arrts[k] = v
            else:
                up_arrts[k.upper()] = v
        return type.__new__(cls, name, class_bases, up_arrts)


class Student(metaclass=UpMeta):
    school = 'qinghua'
    sex = 'man'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        print(self.name)


if __name__ == '__main__':
    print(Student.__dict__)
    # {'__module__': '__main__', 'SCHOOL': 'qinghua', 'SEX': 'man', '__init__': <function Student.__init__ at 0x00000196381B34C8>, 'get_name': <function Student.get_name at 0x00000196381B3288>, '__dict__': <attribute '__dict__' of 'Student' objects>, '__weakref__': <attribute '__weakref__' of 'Student' objects>, '__doc__': None}
```

在元类中控制自定义的类无需__init__方法

```python
# 在元类中控制自定义的类无需__init__方法
# 1. 元类帮其完成创建对象以及初始化操作
#
# 2. 要求实例化时传参必须为关键字形式, 否则抛出异常TypeError: must use keyword argument
#
# 3. key作为用户自定义类产生对象的属性, 且所有属性变成大写

class UpMeta(type):
    def __call__(self, *args, **kwargs):
        if args:
            raise TypeError('must use keyword argument for key function')

        # __call__, 类调用时触发, 即生成对象
        # 1. 调用__new__生成空对象, 类本身无此方法, 则按照类.mro()顺序查找, 最终为object.__new__()
        # obj = self.__new__(self)
        obj = object.__new__(self)

        # 2. 调用__init__初始化对象
        # self.__init__(obj, *args, **kwargs)

        # 控制的是Student对象的属性大写, 即s.__dict__ : {'NAME': 'hong', 'AGE': 18}
        obj.__dict__ = {k.upper(): v for k, v in kwargs.items()}

        # 3. 返回生成的对象
        return obj


class Student(metaclass=UpMeta):
    school = 'qinghua'

    def get_name(self):
        if hasattr(self, 'name'):
            print(getattr(self, 'name'))


if __name__ == '__main__':
    s = Student(name='hong', age=18)
    print(s.__dict__)
    # {'NAME': 'hong', 'AGE': 18}
```

在元类中控制自定义的类产生的对象相关的属性全部为隐藏属性

```python

class UpMeta(type):
    def __call__(self, *args, **kwargs):
        # __call__, 类调用时触发, 即生成对象
        # 1. 调用__new__生成空对象, 类本身无此方法, 则按照类.mro()顺序查找, 最终为object.__new__()
        obj = self.__new__(self)

        # 2. 调用__init__初始化对象
        self.__init__(obj, *args, **kwargs)

        # 控制的是Student对象的属性大写, 即s.__dict__ : {'NAME': 'hong', 'AGE': 18}
        obj.__dict__ = {f'_{self.__name__}__{k}': v for k, v in obj.__dict__.items()}

        # 3. 返回生成的对象
        return obj


class Student(metaclass=UpMeta):
    school = 'qinghua'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        if hasattr(self, 'name'):
            print(getattr(self, 'name'))


if __name__ == '__main__':
    s = Student(name='hong', age=18)
    print(s.__dict__)
    # {'_Student__name': 'hong', '_Student__age': 18}
```

### 单例模式

```python
# 单例: 即单个实例, 指的是同一个类实例化多次的结果指向同一个对象, 用于节省内存空间

# 1. 作为模块导入

# 2. 通过元类控制
class UpMeta(type):
    def __init__(self, class_name, class_bases, class_dict):
        self.__instance = object.__new__(self)

    def __call__(self, *args, **kwargs):
        self.__init__(self.__instance, *args, **kwargs)
        return self.__instance


class Student(metaclass=UpMeta):
    school = 'qinghua'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        if hasattr(self, 'name'):
            print(getattr(self, 'name'))


if __name__ == '__main__':
    s1 = Student('1', 1)
    s2 = Student('2', 2)
    print(s1 is s2)
    print(s1, s1.__dict__)

# 3. 通过类方法控制
class Student():
    school = 'qinghua'
    __instance = None

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        if hasattr(self, 'name'):
            print(getattr(self, 'name'))

    @classmethod
    def singleton(cls):
        if not cls.__instance:
            cls.__instance = cls('3', 3)
        return cls.__instance

if __name__ == '__main__':
    s1 = Student('1', 1)
    s2 = Student('2', 2)
    print(s1 is s2)
    s3 = Student.singleton()
    s4 = Student.singleton()
    print(s3 is s4)

# 4. 通过装饰器控制
def singleton(func):
    __instance = func('3', 3)

    def wrapper(*args, **kwargs):
        return __instance

    return wrapper


@singleton
class Student():
    school = 'qinghua'
    __instance = None

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        if hasattr(self, 'name'):
            print(getattr(self, 'name'))


if __name__ == '__main__':
    s1 = Student('1', 1)
    s2 = Student('2', 2)
    print(s1 is s2)  # True
    print(s1.__dict__)  # {'name': '3', 'age': 3}
```

### 属性查找

```shell
从对象发起, 按照类.mro找起
从类发起, 按照类.mro找起, object没有, 查找元类
```

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

### @staticmethod和@classmethod

都可以通过Class.method()的方式使用

classmethod第一个参数是cls,可以引用类变量

staticmethod使用起来和普通函数一样,只不过放在类里去组织

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

### 鸭子类型

当看到一只鸟走起来像鸭子,游泳起来像鸭子,叫起来也像鸭子,这只鸟就可以被称为鸭子

关注点在对象的行为,而不是类型(duck typing)

比如 file, String, socket对象都支持read/write方法(file like object)

又比如list.extend()方法中,我们并不关心它的参数是不是list,只要它是可迭代的,所以它的参数可以是list/tuple/dict/字符串/生成器等.

鸭子类型在动态语言中经常使用,非常灵活,使得python不像java那样专门去弄一大堆的设计模式.

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

### `__new__`和``__init__``的区别

```shell
# __new__是一个静态方法,而__init__是一个实例方法.
# __new__ 是在__init__之前被调用的特殊方法.
# __new__方法会返回一个创建的实例,而__init__什么都不返回.
# 只有在__new__返回一个cls的实例时后面的__init__才能被调用.
# 当创建一个新实例时调用__new__,初始化一个实例时用__init__.
```

### 单例模式

单例模式是一种常用的软件设计模式.在它的核心结构中只包含一个被称为单例类的特殊类.通过单例模式可以保证系统中一个类只有一个实例而且该实例易于外界访问.

```shell
class SingleTon():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingleTon, cls).__new__(cls, *args, **kwargs)
        return cls._instance

if __name__ == '__main__':
    a = SingleTon()
    b = SingleTon()
    a.name = 'mike'
    print(a.name , b.name) # mike mike
    print(a is b) # True

```

### Python中的作用域

本地作用域（Local）→当前作用域被嵌入的本地作用域（Enclosing locals）→全局/模块作用域（Global）→内置作用域（Built-in）

### GIL线程全局锁

线程全局锁(Global Interpreter Lock),即Python为了保证线程安全而采取的独立线程运行的限制,说白了就是一个核只能在同一时间运行一个线程.

对于io密集型任务,python的多线程起到作用,但对于cpu密集型任务,python的多线程几乎占不到任何优势,还有可能因为争夺资源而变慢.

### 协程

协程其实可以认为是比线程更小的执行单元.自带CPU上下文,在合适的时机,我们可以把一个协程切换到另一个协程.只要这个过程中保存或恢复 CPU上下文那么程序还是可以运行的.

线程切换从系统层面远不止保存和恢复CPU上下文这么简单.操作系统为了程序运行的高效性每个线程都有自己缓存Cache等等数据,操作系统还会帮你做这些数据的恢复操作.所以线程的切换非常耗性能.

但是协程的切换只是单纯的操作CPU的上下文,所以一秒钟切换个上百万次系统都抗的住.

简单点说协程是进程和线程的升级版,进程和线程都面临着内核态和用户态的切换问题而耗费许多切换时间,而协程就是用户自己控制切换的时机,不再需要陷入系统的内核态

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

### 面向切面编程AOP和装饰器

### 鸭子类型

### Python中重载

### 新式类和旧式类

### __new__和init的区别

### 单例模式

### Python中的作用域

### GIL线程全局锁

### 协程

### 闭包

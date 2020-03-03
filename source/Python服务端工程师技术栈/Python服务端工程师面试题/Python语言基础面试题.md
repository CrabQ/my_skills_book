# Python语言基础面试题

## 基础

列出5个常用python标准库

```python
os,time,random,threading,sys,queue,shutil
```

如何知道一个 Python 对象的类型

```python
type()
```

pprint 模块是干什么的

```python
# 输出一个整齐美观的Python数据结构
import pprint
a = [str(i)*10 for i in range(6)]
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(a)
print(a)
# [   '0000000000',
#     '1111111111',
#     '2222222222',
#     '3333333333',
#     '4444444444',
#     '5555555555']
# ['0000000000', '1111111111', '2222222222', '3333333333', '4444444444', '5555555555']
```

简述你对 input()函数的理解

```python
获取标准输入,字符串类型
```

python 中的 is 和==

```python
is 判断内存id是否相等
== 值是否相等
值比较时用==, 判断是否同一对象用is
```

在 Python 中如何使用多进制数字

```python
# bin转化为二进制,0b前缀表示二进制
print(bin(10), int(0b1010))
# 0b1010 10

# 0o表示八进制
print(oct(8), int(0o10))
# 0o10 8

# 0x表示16进制
print(hex(16))
# 0x10
```

怎样声明多个变量并赋值

```python
a, b = 1, 2
```

什么是负索引

```python
用负数作为索引,-1表示数组最后一位
```

python内建数据类型有哪些

```python
Python3 中有六个标准的数据类型:字符串（String）、数字（Digit）、列表（List）、元组（Tuple）、集合（Sets）、字典（Dictionary）
string, number(int, folat, complex, bool), bytes, set, list, dict, tuple
```

Python 交换两个变量的值

```python
a,b = b,a
```

三元运算写法和应用场景

```python
a = 1
b = 2
c = 'add' if a>b else 'less'
print(c)
```

解释一下 python 中 pass 语句的作用

```python
空语句,保持结构完整
```

了解 enumerate 么

```python
a = ['a','b','c','d']
for i in enumerate(a, start=8):
    print(i)
# (8, 'a')
# (9, 'b')
# (10, 'c')
# (11, 'd')
```

Python 中递归的最大次数,那如何突破呢

```python
最大次数为1000次
```

isinstance 作用以及应用场景

```python
判断对象是否是一个已知的类型
判断对象的数据类型
判断类的继承关系
```

lambda 表达式格式以及应用场景

```python
# lambda表达式: lambda 参数1, 参数2, : 参数表达式
应用场景
简单功能的函数实现
不需要关注函数命名
复用性不高或者只用一次的函数
# 输出1到100内的奇数
print(list(filter(lambda x: x%2 == 1, range(1, 101))))
```

新式类和旧式类的区别

```python
python3取消了经典类,默认都是新式类,并且不必显式的继承object.
区别: 继承搜索顺序的变化
新式类:广度优先
经典类:深度优先
```

dir()是干什么用的

```python
# dir()不带参数时,返回当前范围内的变量、方法和定义的类型列表；
# 带参数时,返回参数的属性、方法列表
# 如果参数包含方法__dir__(),该方法将被调用
class A():
    def b(self):
        pass

if __name__ == '__main__':
    print(dir())
    print(dir(A))
# ['A', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'b']

```

解释一下 Python 中的赋值运算符

解释一下 Python 中的逻辑运算符

解释一下 Python 中的位运算符

一个包里有三个模块,demo1.py, demo2.py, demo3.py,但使用 from tools import *导入模块时,如何保证只有 demo1、demo3 被导入了

```python
# 在包中设置__init__.py
import demo1
import demo3
```

copy 和 deepcopy 的区别是什么

```python
copy仅拷贝对象本身,不拷贝对象中引用的其他对象
deepcopy除拷贝对象本身,还拷贝对象中引用的其他对象（子对象）
copy不会为子对象额外创建新的内存空间,当子对象被修改之后,这个子对象的引用都会发生改变
deepcopy是一个新对象的创建,只是用了和被拷贝对象相同的值,子对象改变不会影响被拷贝对象
```

代码中经常遇到的*args, **kwargs 含义及用法

```python
args(arguments): 位置参数
kwars(keyword arguments): 关键字参数
```

Python 中会有函数或成员变量包含单下划线前缀和结尾,和双下划线前缀结尾,区别是什么

```python
单下划线开头的命名方式被常用于模块中,在一个模块中以单下划线开头的变量和方法会被默认划入模块内部范围.当使用 from my_module import * 导入时,单下划线开头的变量和方法是不会被导入的.但使用 import my_module 导入的话,仍然可以用 my_module._var 这样的形式访问属性或方法
单下划线结尾的命名方式也存在,但是不常用,其实也不推荐用.这种命名方式的作用就是为了和 python 的一些内置关键词区分开来,假设我们想给一个变量命名为 class,但是这会跟 python 的关键词 class 冲突,所以我们只好退一步使用单下划线结尾命名,也就是 class_
双下划线开头和结尾的是一些 python 的“魔术”对象,如类成员的 __init__、__del__、__add__、__getitem__ 等,以及全局的__file__、__name__ 等
```

Python 中的作用域

```python
locals -> enclosing function -> globals -> builtins
locals,当前所在命名空间（如函数、模块）,函数的参数也属于命名空间内的变量
enclosing,外部嵌套函数的命名空间（闭包中常见）
globals,全局变量,函数定义所在模块的命名空间
builtins,内建模块的命名空间
```

列出 Python 中可变数据类型和不可变数据类型,为什么

```python

不可变对象 bool/int/float/tuple/str/frozenset
可变对象 list/set/dict
默认参数只计算一次
id() 方法进行内存地址的检测
```

谈谈对 Python 和其他语言的区别

```python
python是一门强类型的动态语言,不会发生隐式转换.解释型语言,在运行时才确定类型.跟java这类编译型的语言不一样.
```

简述解释型和编译型编程语言

```python
解释型语言: 不用声明变量类型,运行时确定,边解释边运行
编译形语言: 需要声明变量类型,先编译后运行,运行速度快
```

Python 的解释器种类以及相关特点

```python
CPython c语言开发的,使用最广的解释器
IPython 基于 cPython 之上的一个交互式计时器,交互方式增强,功能和 cPython 一样
PyPy 目标是执行效率,采用 JIT 技术.对 Python 代码进行动态编译,提高执行效率
JPython 运行在 Java 上的解释器,直接把 Python 代码编译成 Java 字节码执行
IronPython 运行在微软 .NET 平台上的解释器,把 Python 编译成 . NET 的字节码
```

## Python3 和 Python2

Python3 和 Python2 之间的区别

```python
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

Python3 和 Python2 中 int 和 long 区别

```python
Python2 有 int 和 long 类型.int 类型最大值不能超过 sys.maxint,而且这个最大值是平台相关的.可以通过在数字的末尾附上一个Ｌ来定义长整型,显然,它比 int 类型表示的数字范围更大.在 Python3 里,只有一种整数类型 int,大多数情况下,和 Python２中的长整型类似
```

xrange 和 range 的区别

```python
xrange 是在 Python2 中的用法,Python3 中只有 range, xrange 用法与 range 完全相同,所不同的是生成的不是一个 list 对象,而是一个生成器
```

## Python代码规范

什么是 PEP8

```python
《Python Enhancement Proposal #8》（8 号 Python 增强提案）又叫 PEP8,他针对的 Python 代码格式而编订的风格指南
```

了解 Python 之禅么

```python
通过 import this 语句可以获取其具体的内容.它告诉大家如何写出高效整洁的代码
```

了解 docstring 么

```python
DocStrings 文档字符串是一个重要工具,用于解释文档程序,帮助你的程序文档更加简单易懂.主要是解释代码作用的
print(datetime.datetime.now())
```

了解类型注解么

```python
PEP 484 引入了类型提示,这使得可以对 Python 代码进行静态类型检查. 在使用 Ide 的时候可以获取到参数的类型,更方便传入参数.使用格式如下

def foo(num: int) -> None:
    print(f"接收到的数字是:{num}")
介绍下这个简单例子,我们可以在函数的参数部分使用参数名+:+类型,来指定参数可以接受的类型,这里的话就是 num 参数为 int 类型,然后后面->接的是返回值的类型.这里返回值为 None,然后通过 fstring 格式化字符串输出传入的数字
```

例举你知道 Python 对象的命名规范,例如方法或者类等

```python
类:总是使用首字母大写单词串,如 MyClass.内部类可以使用额外的前导下划线
变量:小写,由下划线连接各个单词
方法名:小写,由下划线连接各个单词
常量:常量名所有字母大写
```

Python 中的注释有几种

```python
单行注释在行首是 #
多行注释可以使用三个单引号或三个双引号,包括要注释的内容
```

如何优雅的给一个函数加注释

```python
可以使用 docstring 配合类型注解
```

如何给变量加注释

```python
可以通过变量名:类型的方式如下

a: str = "this is string type"
```

Python 代码缩进中是否支持 Tab 键和空格混用

```python
不允许 tab 键和空格键混用,一般推荐使用 4 个空格替代 tab 键
```

是否可以在一句 import 中导入多个库

```python
不推荐.因为一次导入多个模块可读性不是很好,所以一行导入一个模块会比较好.同样的尽量少用 from modulename import *,因为判断某个函数或者属性的来源有些困难,不方便调试,可读性也降低了
```

在给 Py 文件命名的时候需要注意什么

```python
不要和标准库库的一些模块重复,比如 abc. 另外名字要有意义,不建议数字开头或者中文命名
```

例举几个规范 Python 代码风格的工具

```python
pylint 和 flake8
```

单双引号三引号表示什么

```python
单双引号都表示字符串,三引号表示注释
```

下面代码会存在什么问题,如何改进

```python
def strappend(num): # 无注释
    str = 'frist'   # 不能使用关键字'str'做变量名
    for i in range(num):    # i意义不明
        str+=str(i) # 不能使用关键字'str'做变量名,报错
    return str

# 修改
def strappend(append_count:int)->str:
    """字符串修改

    遍历append_count. 将遍历的值转为str添加到字符串
    :param append_count: 遍历次数
    :return: 最终得到的字符串
    """
    append_str = 'frist'
    # 遍历获取time的次数int类型
    for time in range(append_count):
        append_str += str(time)
    return append_str

print(strappend(10))
```

## 字符串

统计字符串每个单词出现的次数

```python
a = 'sldjgslsljhgowegpwjrho[pjdglsj'
for i in set(a):
    print(f'{i}:{str(a.count(i))}')
```

将"hello world"转换为首字母大写"Hello World"

```python
s = "hello world"
' '.join(x.capitalize() for x in s.split(' '))
# Hello World
```

如何检测字符串中只含有数字

```python
print('294859'.isdigit())
print('sljd0248jlg'.isdigit())
```

将字符串"ilovechina"进行反转

```python
'i love china'[::-1]
```

Python 中的字符串格式化方式你知道哪些

```python
 %-formatting、str.format 和 f-string
```

有一个字符串开头和末尾都有空格,比如“ adabdw ”,要求写一个函数把这个字符串的前后空格都去掉

```python
print(' adabdw '.strip())
```

获取字符串”123456“最后的两个字符

```python
'123456'[-2:]
```

一个编码为 GBK 的字符串 S,将其转成 UTF-8 编码的字符串

```python
"S".encode("gbk").decode("utf-8",'ignore')
```

s="info:xiaoZhang 33 shandong",用正则切分字符串输出['info', 'xiaoZhang', '33', 'shandong']

```python
import  re
re.split('[:\s]','info:xiaoZhang 33 shandong')
```

"你好 中国 ",去除多余空格只留一个空格

```python
"你好 中国 ".strip()
```

怎样将字符串转换为小写

```python
'SJLsdgJDG'.lower()

```

a="hello"和 b="你好"编码成 bytes 类型

```python
a="hello"
b="你好"
a.encode()
b.encode()
```

## 列表与元祖

已知 AList = [1,2,3,1,2],对 AList 列表元素去重

```python
AList = [1,2,3,1,2]
list(set(AList))
```

如何实现 "1,2,3" 变成 ["1","2","3"]

```python
"1,2,3".split(',')
```

给定两个 list,A 和 B,找出相同元素和不同元素

```python
a = list('12345abcde')
b = list('12345678abcdefg')
set(a)&set(b)
set(a)^set(b)
```

\[[1,2],[3,4],[5,6]]一行代码展开该列表,得出[1,2,3,4,5,6]

```python
print([x for g in [[1,2],[3,4],[5,6]] for x in g])
```

合并列表[1,5,7,9]和[2,2,6,8]

```python
[1,5,7,9]+[2,2,6,8]
```

如何打乱一个列表的元素

```python
import random
a = [1,5,7,9]
random.shuffle(a)
```

举例 sort 和 sorted 的区别

```python
a = [1,4,7,2,4,23,9]
# sorted是一个函数,返回一个新的list
new_a = sorted(a)
print(new_a)
# [1, 2, 4, 4, 7, 9, 23]
# sort是实例方法,直接作用在list本身,不会返回新的list
a.sort()
print(a)
# [1, 2, 4, 4, 7, 9, 23]
```

按照字典内的年龄排序

```python
d = [
    {'name':'a', 'age':1},
    {'name':'b', 'age':12},
    {'name':'c', 'age':15645},
    {'name':'d', 'age':134},
]
d.sort(key=lambda x: x['age'])
```

Python 里面如何实现 tuple 和 list 的转换

```python
a = (1,2,3,4,5,6,6)
print(list(a))
```

下面的代码输出结果

```python
a = (1,2,3,[4,5,6,7],8)
a[3][0] = 2
print(a)
# (1, 2, 3, [2, 5, 6, 7], 8)
```

filter 方法求出列表所有奇数并构造新列表,a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

```python
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list(filter(lambda x: x%2 ==1, (i for i in a))))
```

下面的代码输出结果是什么

```python
a = (1,2,3,[4,5,6,7],8)
a[2] = 2
# TypeError: 'tuple' object does not support item assignment
```

简述 any()和 all()方法

```python
any() 空列表和空元祖返回False
有一不为空,则True
all() 空列表和空元祖返回True
有一空则False
```

## 字典

字典操作中 del 和 pop 有什么区别

```python
# del   只删除不返回
# pop   删除指定键值对,返回值
```

请合并下面两个字典 a = {"A":1,"B":2},b = {"C":3,"D":4}

```python
a = {"A":1,"B":2}
b = {"C":3,"D":4}
a.update(b)
```

如何使用生成式的方式生成一个字典,写一段功能代码

```python
a = {name:'age' for name in ['a','b','c']}
```

如何把元组("a","b")和元组(1,2),变为字典{"a":1,"b":2}

```python
dict(zip(('a','b'), (1,2))))
```

如何交换字典 {"A":1,"B":2}的键和值

```python
{v:k for k,v in {'A': 1, 'B': 2}.items()}
```

## 生成器

我们知道对于列表可以使用切片操作进行部分元素的选择,那么如何对生成器类型的对象实现相同的功能呢

```python
import itertools

def fbnq(num):
    a, b = 1, 1
    for _ in range(num):
        a, b = b, a+b
        yield b

if __name__ == '__main__':
    f = fbnq(20)
    f_list = itertools.islice(f, 10,20)
    for i in f_list:
        print(i)

range(10)[:5]
```

请将[i for i in range(3)]改成生成器

```python
(i for i in range(3))
```

## 文件读取

w、a+、wb 文件写入模式的区别

```python
r : 读取文件,若文件不存在则会报错
w: 写入文件,若文件不存在则会先创建再写入,会覆盖原文件
a : 写入文件,若文件不存在则会先创建再写入,但不会覆盖原文件,而是追加在文件末尾
rb,wb:分别于r,w类似,用于读写二进制文件
r+ : 可读、可写,文件不存在也会报错,写操作时会覆盖
w+ : 可读,可写,文件不存在先创建,会覆盖
a+ :可读、可写,文件不存在先创建,不会覆盖,追加在末尾
```

在读文件操作的时候会使用 read、readline 或者 readlines,简述它们各自的作用

```python
# read 读取整个文件
# readline 读取下一行
# readlines 以迭代器形式读取整个文件
```

有两个磁盘文件 A 和 B,各存放一行字母,要求把这两个文件中的信息合并(按字母顺序排列),输出到一个新文件 C 中

```python
with open('./A.txt', 'r', encoding='utf-8') as f:
    a = f.readline()
with open('./B.txt', 'r', encoding='utf-8') as f:
    b = f.readline()
c = list(a + b)
c.sort()
with open('./C.txt', 'w', encoding='utf-8') as f:
    f.write(''.join(c))
```

简述with方法打开文件帮我们做了什么

```python
执行
finally:
    f.close()
```

用 python 删除文件和用 linux 命令删除文件方法

```python
import os

os.remove(file)
# linux
rm -rf file
```

## json

json序列化时,可以处理的数据类型有哪些?如何定制支持 datetime 类型

```python
# 列表、字典、字符串、数值、bool、None
# 定制支持 datetime 类型
from datetime import datetime
import json
from json import JSONEncoder

class DatetimeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super(DatetimeEncoder, self).default(o)

if __name__ == '__main__':
    a = {'age':18, 'date':datetime.now()}
    print(json.dumps(a, cls=DatetimeEncoder))
```

json 序列化时,默认遇到中文会转换成 unicode,如果想要保留中文怎么办

```python
import json

a = '你送挂机了ksjdglj'
print(json.dumps(a, ensure_ascii=False))
```

python 字典和 json 字符串相互转化方法

```python
import json

a = {'age':13, 'name':'小米'}
json_a = json.dumps(a, ensure_ascii=False)
print(type(json_a))
dict_a = json.loads(json_a)
print(type(dict_a))

```

## 日期时间

python获取当前日期

```python
import time
time.localtime()

import datetime
datetime.datetime.now()
```

如果当前的日期为 20190530,要求写一个函数输出 N 天后的日期,(比如 N 为 2,则输出 20190601)

```python
from datetime import datetime, timedelta

def get_date(now, num):
    a = datetime.strptime(now, '%Y%m%d').date()
    offset_day = timedelta(days=num)
    return (a+offset_day).strftime('%Y-%m-%d')

print(get_date('20190912', 3))
print(get_date('20190912', 23))
print(get_date('20190912', 123))
```

## 异常

写一段自定义异常代码

```python
class MyExcepiton(Exception):

    def __init__(self, info):
        super(MyExcepiton, self).__init__()
        self.info = info

    def __str__(self):
        return self.info

if __name__ == '__main__':
    try:
        raise MyExcepiton('test my exception')
    except MyExcepiton as e:
        print(e)
```

举例说明异常模块中 try except else finally 的相关意义

```python
def test(a, b):
    try:
        c = a/b
    except ZeroDivisionError:
        print('除数不能为0')
    else:
        print(c)
    finally:
        print('done')

if __name__ == '__main__':
    test(10,3)
    test(2,0)

# 3.3333333333333335
# done
# 除数不能为0
# done
```

遇到 bug 如何处理

```python
可以使用python自带的异常处理或自定义异常抛出,查找问题可以看看官方文档,或者百度,谷歌
```

什么是断言应用场景

```python
# 断言语句是将调试断言插入程序的便捷方式
# 在condition为True时不触发,为False时触发AssertionError错误
assert condition
assert 1 == 1
assert 1 == 0
# AssertionError

应用场景:
防御性的编程
运行时对程序逻辑的检测
合约性检查
程序中的常量
检查文档
```

列举 5 个 Python 中的异常类型以及其含义

```python
BaseException  # 所有异常的基类
 +-- SystemExit  # 解释器请求退出
 +-- KeyboardInterrupt  # 用户中断执行(通常是输入^C)
 +-- GeneratorExit  # 生成器(generator)发生异常来通知退出
 +-- Exception  # 常规异常的基类
      +-- StopIteration  # 迭代器没有更多的值
      +-- StopAsyncIteration  # 必须通过异步迭代器对象的__anext__()方法引发以停止迭代
      +-- ArithmeticError  # 各种算术错误引发的内置异常的基类
      |    +-- FloatingPointError  # 浮点计算错误
      |    +-- OverflowError  # 数值运算结果太大无法表示
      |    +-- ZeroDivisionError  # 除(或取模)零 (所有数据类型)
      +-- AssertionError  # 当assert语句失败时引发
      +-- AttributeError  # 属性引用或赋值失败
      +-- BufferError  # 无法执行与缓冲区相关的操作时引发
      +-- EOFError  # 当input()函数在没有读取任何数据的情况下达到文件结束条件(EOF)时引发
      +-- ImportError  # 导入模块/对象失败
      |    +-- ModuleNotFoundError  # 无法找到模块或在在sys.modules中找到None
      +-- LookupError  # 映射或序列上使用的键或索引无效时引发的异常的基类
      |    +-- IndexError  # 序列中没有此索引(index)
      |    +-- KeyError  # 映射中没有这个键
      +-- MemoryError  # 内存溢出错误(对于Python 解释器不是致命的)
      +-- NameError  # 未声明/初始化对象 (没有属性)
      |    +-- UnboundLocalError  # 访问未初始化的本地变量
      +-- OSError  # 操作系统错误,EnvironmentError,IOError,WindowsError,socket.error,select.error和mmap.error已合并到OSError中,构造函数可能返回子类
      |    +-- BlockingIOError  # 操作将阻塞对象(e.g. socket)设置为非阻塞操作
      |    +-- ChildProcessError  # 在子进程上的操作失败
      |    +-- ConnectionError  # 与连接相关的异常的基类
      |    |    +-- BrokenPipeError  # 另一端关闭时尝试写入管道或试图在已关闭写入的套接字上写入
      |    |    +-- ConnectionAbortedError  # 连接尝试被对等方中止
      |    |    +-- ConnectionRefusedError  # 连接尝试被对等方拒绝
      |    |    +-- ConnectionResetError    # 连接由对等方重置
      |    +-- FileExistsError  # 创建已存在的文件或目录
      |    +-- FileNotFoundError  # 请求不存在的文件或目录
      |    +-- InterruptedError  # 系统调用被输入信号中断
      |    +-- IsADirectoryError  # 在目录上请求文件操作(例如 os.remove())
      |    +-- NotADirectoryError  # 在不是目录的事物上请求目录操作(例如 os.listdir())
      |    +-- PermissionError  # 尝试在没有足够访问权限的情况下运行操作
      |    +-- ProcessLookupError  # 给定进程不存在
      |    +-- TimeoutError  # 系统函数在系统级别超时
      +-- ReferenceError  # weakref.proxy()函数创建的弱引用试图访问已经垃圾回收了的对象
      +-- RuntimeError  # 在检测到不属于任何其他类别的错误时触发
      |    +-- NotImplementedError  # 在用户定义的基类中,抽象方法要求派生类重写该方法或者正在开发的类指示仍然需要添加实际实现
      |    +-- RecursionError  # 解释器检测到超出最大递归深度
      +-- SyntaxError  # Python 语法错误
      |    +-- IndentationError  # 缩进错误
      |         +-- TabError  # Tab和空格混用
      +-- SystemError  # 解释器发现内部错误
      +-- TypeError  # 操作或函数应用于不适当类型的对象
      +-- ValueError  # 操作或函数接收到具有正确类型但值不合适的参数
      |    +-- UnicodeError  # 发生与Unicode相关的编码或解码错误
      |         +-- UnicodeDecodeError  # Unicode解码错误
      |         +-- UnicodeEncodeError  # Unicode编码错误
      |         +-- UnicodeTranslateError  # Unicode转码错误
      +-- Warning  # 警告的基类
           +-- DeprecationWarning  # 有关已弃用功能的警告的基类
           +-- PendingDeprecationWarning  # 有关不推荐使用功能的警告的基类
           +-- RuntimeWarning  # 有关可疑的运行时行为的警告的基类
           +-- SyntaxWarning  # 关于可疑语法警告的基类
           +-- UserWarning  # 用户代码生成警告的基类
           +-- FutureWarning  # 有关已弃用功能的警告的基类
           +-- ImportWarning  # 关于模块导入时可能出错的警告的基类
           +-- UnicodeWarning  # 与Unicode相关的警告的基类
           +-- BytesWarning  # 与bytes和bytearray相关的警告的基类
           +-- ResourceWarning  # 与资源使用相关的警告的基类.被默认警告过滤器忽略
```

## 闭包与装饰器

写一个函数,接收整数参数 n,返回一个函数,函数的功能是把函数的参数和 n 相乘并把结果返回

```python
def sum(n):
    def inner(a):
        return n*a
    return inner

a = sum(4)
b = sum(10)
print(a(3))
print(b(3))
```

函数装饰器有什么作用请列举说明

```python
在不修改代码的前提下进行功能扩展,满足面对对象的开闭原则
引入日志
函数执行时间统计
执行函数前预备处理
执行函数后清理功能
权限校验等场景
缓存
事务处理
```

## 函数

如何在函数中设置一个全局变量

```python
global a
```

一行代码输出 1-100 之间的所有偶数

```python
print([x for x in range(2, 101, 2)])
```

请写一个 Python 逻辑,计算一个文件中的大写字母数量

```python
with open('./A.txt', 'r', encoding='utf-8') as f:
    result = f.readlines()

count = list()
for i in result:
    for j in i:
        if j.isupper():
            count.append(j)
print(count)
print(len(count))
```

pathlib 的用法举例

```python
pathlib 模块提供了一组面向对象的类,这些类可代表各种操作系统上的路径,程序可通过这些类操作路径
```

魔法函数 __call__怎么使用

```python
# __call__允许一个类的实例像函数一样被调用
class Entity():
    def __init__(self, size, x, y):
        self.x = x
        self.y = y
        self.size = size

    def __call__(self, x, y):
        # 改变实例属性
        self.x = x
        self.y = y

    def run(self):
        print(self.x, self.y, self.size)

if __name__ == '__main__':
    demo = Entity(1,2,3)
    demo.run()
    demo(4,5)
    demo.run()
```

如何判断一个对象是函数还是方法

```python
在类外声明为方法
类中声明为函数,通过类调用也为函数,使用实例化对象调用为方法
```

@classmethod 和@staticmethod 用法和区别

```python
@classmethod 类方法:访问和修改类属性,进行类的相关操作,通过类或实例对象调用,传递cls
@staticmethod 静态方法:不访问类属性和实例属性,通过类或实例对象调用,相当于普通函数
```

metaclass 作用以及应用场景

```python
元类
```

hasattr() getattr() setattr()的用法

```python
class Test():
    name = 'xiao'

    def run(self):
        print('run')

if __name__ == '__main__':
    demo = Test()
    print(hasattr(demo, 'name'))
    print(hasattr(demo, 'run'))
    print(getattr(demo, 'name'))
    getattr(demo, 'run')()
    setattr(demo, 'sexy', '男')
    print(hasattr(demo, 'sexy'))
```

请列举你知道的 Python 的魔法方法及用途

```python
__new__ 创建类并返回类的实例
__init__ 初始化实例
__del__ 销毁实例化对象
__call__ 让类像函数一样被调用
__getattr__ 访问对象不存在的属性时调用,用于定义访问行为
__setattr__ 设置对象属性时调用
__delattr__ 删除对象属性时调用
__next__ 返回迭代器的下一个元素
```

Python 的传参是传值还是传址

```python
# 对可变对象传址,不可变对象传值(其实都是传地址)
def test(param):
    if isinstance(param, int):
        param += 1
    if isinstance(param, list):
        param.append(1)
    print(param)

if __name__ == '__main__':
    a = 1
    test(a)
    print(a)
    b = [2,3]
    test(b)
    print(b)
# 2
# 1
# [2, 3, 1]
# [2, 3, 1]
```

## Python 垃圾回收机制

```python
python采用的是引用计数机制为主,标记-清除和分代收集两种机制为辅的策略
Python 对小整数的定义是 [-5, 257) 这些整数对象是提前建立好的,不会被垃圾回收.在一个 Python 的程序中,所有位于这个范围内的整数使用的都是同一个对象.
同理,单个字母也是这样的

但是当定义2个相同的字符串时,引用计数为0,触发垃圾回收
```

## 面对对象编程

Python 中的接口如何实现

```python
通过类、函数定义接口
```

Python 中的反射了解么

什么是猴子补丁

```python
程序功能的追加或者变更
```

在 Python 中是如何管理内存的

```python
内存池,pymalloc,
小于256bits,pymalloc在内存池申请空间,大于256bits,直接执行new/malloc的行为来申请内存空间
```

当退出 Python 时是否释放所有内存分配

```python
循环引用其它对象或引用自全局命名空间的对象的模块,在 Python 退出时并非完全释放
```

什么是面向对象的 mro

```python
MRO就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表
MRO 是在Python多继承和钻石继承问题上的核心内容,它规定了如何,什么时候,怎么样去 调用父类的方法
```

## 正则

使用正则表达式匹配出 `<html><h1><div>a="张明 98 分"</div></html>` 中的地址 a="张明 98 分"

```python
import  re

re.search('.*>(.*")<.*', '<html><h1><div>a="张明 98 分"</div></html>').group(1)
```

正则表达式匹配中`(.*)和(.*?)`匹配区别

```python
贪婪和非贪婪
```

写一段匹配邮箱的正则表达式

```python
import  re

a = '192sojdg_lr@163.com'
b = '_234slg@gma.cn'
result = re.search(r'[a-zA-Z0-9_]+@\w+\.\w+', b)
print(result)
```

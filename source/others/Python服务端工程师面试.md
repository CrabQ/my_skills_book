# Python技术栈

## Python服务端工程师面试

### 面试流程

#### 一面问基础

#### 二面问项目

#### 三面问设计

### 后端技术栈

#### Python语言基础知识

    语言特点
    语法基础
    高级特性

#### 算法与数据结构

    常用算法和数据结构
    分析时间/空间复杂度
    实现常用算法和数据结构

#### 编程范式知识

    面对对象编程
    常用设计模式
    函数式编程

#### 操作系统

    常用Linux命令
    进程/线程
    内存管理

#### 网络编程

    常用协议 TCP/IP/HTTP
    Socket编程基础
    Python并发库

#### 数据库

    Mysql,索引优化
    关系型和NoSql的使用场景
    Redis缓存

#### Python Web框架

    常用框架对比, RESTful
    WSGI原理
    Web安全问题

#### 系统设计

    设计原则
    后端系统常用组件(缓存,数据库,消息队列等)
    技术选型和实现(短网址服务, Feed流系统)

### Python初/中级工程师技能要求

#### 初级工程师

    扎实的计算机理论基础
    代码规范,风格良好
    能在指导下靠谱地完成业务需求

#### 中级工程师

    扎实的计算机理论基础和丰富的项目经验
    能独立设计和完成项目需求
    熟悉常用的web组件(缓存,消息队列等)
    具备一定的系统设计能力

### 简历

#### 简历内容

    基本信息(姓名,学校,学历,联系方式等)
    职业技能(编程语言,框架,数据库,开发工具等)
    关键项目经验(担任职责,用到哪些技术)

#### 简历自我评价

    可有可无
    有则真诚简洁

#### 简历加分项

    知名项目经验
    技术栈比较匹配
    开源项目(github/技术blog/Linux/UNIX geek)

#### 简历注意事项

    内容精简,突出重点,不超过两页
    注意格式,推荐PDF
    信息真实,技能和岗位匹配,无太多无关内容

#### 自我介绍

    个人信息
    掌握的技术,参与的项目
    应聘的岗位,看法和兴趣

#### 自我介绍模板

    您好,我叫xx,毕业于xx,所学专业是xx
    之前就职于xx公司,担任后端工程师,负责xx项目,对xx技术比较熟悉
    我的工作经验和目前这个岗位较为匹配,希望能够应聘到这个岗位

## Python技术栈知识点

### Python语言基础

#### Python语言特性

    动态强类型语言
    动静态指的是运行期还是编译期确定类型
    强类型指的是不会发生隐式类型转换

#### Python作为后端语言优缺点

    胶水语言,轮子多,应用广泛
    语言灵活,生产力高
    性能问题,代码维护问题,Python2/3兼容问题

#### 什么是鸭子类型

当看到一只鸟走起来像鸭子,游泳起来像鸭子,叫起来也想鸭子,这只鸟就可以被称为鸭子

    关注点在对象的行为,而不是类型(duck typing)
    比如 file, String, socket对象都支持read/write方法(file like object)
    再比如定义了 __iter__ 魔术方法的对象可以用for迭代
    鸭子类型更关注接口而非类型

#### 什么是monkey patch

什么是 monkey patch?那些地方用到了,自己如何实现?

    所谓的monkey patch 就是运行时替换
    比如gevent库需要修改内置的socket
    from gevent import monkey; monkey.patch_socket()

#### 什么是自省

运行时判断一个对象的类型的能力

    Python一切皆对象,用type,id,isinstance获取对戏那个类型信息
    Inspect模块提供了更多获取对象信息的函数

#### 什么是列表和字典推导

    比如[i for i in range(10) if i%2==0]
    一种快速生成list/dict/set的方式,用来代替map/filter等
    (i for i in range(10) if i%2==0)返回生成器

### Python2/3差异

#### Python3改进

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

#### Python2/3工具

    熟悉一些兼容2/3的工具
    six模块
    2to3等工具转换代码
    \__future\__

### Python函数

#### Python如何传递参数

    唯一支持的参数传递是共享传参
    Call by Object(Call by Object Reference or Call by Sharing)
    Call by sharing(共享传参).函数形参获得实参中各个引用的副本

#### Python可变/不可变对象

    不可变对象 bool/int/float/tuple/str/frozenset
    可变对象 list/set/dict
    默认参数只计算一次

#### Python *args, **kwargs

用来处理可变参数

    *args 被打包成tuple
    **kwargs 被打包成dict

### Python异常机制

#### 使用异常的常见场景

    网络请求(超时,连接错误等)
    资源访问(权限问题,资源不存在)
    代码逻辑(越界访问,KeyError等)

#### 如何自定义异常

    继承Exception 实现自定义异常(不是BaseException)
    给异常加上一些附件信息
    处理一些业务相关的特定异常

### Python性能分析与优化

#### 什么是Cpython GIL

GIL, Global Interpreter Lock

    Cpython解释器的内存管理并不是线程安全的
    保护多线程情况下对Python对象的访问
    Cpython使用简单的锁机制避免多个线程同时执行字节码

#### GIL的影响

限制了程序的多核执行

    同一个时间只能有一个线程执行字节码
    CPU密集程序难以利用多核优势
    IO期间会释放GIL,对IO密集程序影响不大

#### 如何规避GIL影响

区分CPU和IO密集程序

    CPU密集可以使用多进程+进程池
    IO密集使用多线程/协程
    cpython扩展

#### 为了什么有了GIL还要关注线程安全

Python中什么操作才是原子的?一步到位执行完

    一个操作如果是一个字节码指令可以完成的就是原子的
    原子的是可以保证线程安全的
    使用dis操作来分析字节码

#### 如何剖析程序性能

    使用各种profile工具(内置或第三方)
    二八定律,大部分时间耗时在少量代码上
    内置的profile/cprofile等工具
    使用pyflame(uber开源)的火焰图工具

#### 服务端性能优化措施

Web应用一般语言不会成为瓶颈

    数据结构和算法优化
    数据库层:索引优化,慢查询消除,批量操作减少IO,NoSQL
    网络IO:批量操作,pipeline操作减少IO
    缓存:使用内存数据库 redis/memcached
    异步:asyncio, celery
    并发:gevent/多线程

### Python生成器与协程

#### 什么是生成器Generator

    生成器就是可以生成值得函数
    当一个函数里有了yield关键字就成了生成器
    生成器可以挂起执行并且保持当前执行的状态

#### 基于生成器的协程

    Python3之前没有原生协程,只有基于生成器的协程
    pep 342(Coroutines via Enhanced Generators)增强生成器功能
    生成器可以通过yield暂停执行和产出数据
    同时支持send()向生成器发送数据和throw()向生成器抛出异常

#### 协程的注意点

    协程需要使用send(None)或者next(coroutine)来预激(prime)才能启动
    在yield处协程会暂停执行
    单独的yield value会产出值给调用方
    可以通过coroutine.send(value)来给协程发送值,发送的值会赋值给yield表达式左边的变量value=yield
    协程执行完成之后(没有遇到下一个yield语句)会抛出StopIteration异常

#### Python3原生协程

    Python3.5引入async/await支持原生协程(native coroutine)

### Python单元测试

#### 什么是单元测试

Unit Testing

    针对程序模块进行正确性检验
    一个函数,一个类进行验证
    自底向上保证程序正确性

#### 为什么要写单元测试

三无代码不可取(无文档,无注释,无单测)

    保证代码逻辑的正确性(甚至有些采用测试驱动开发(TDD))
    单测影响设计,易测的代码往往是高内聚低耦合的
    回归测试,防止改一处整个服务不可用

#### 单元测试相关的库

    nose/pytest较为常用
    mock模块用来模拟替换网络请求等
    coverage统计测试覆盖率

## 编程范式

### 面对对象基础以及Python类

#### 什么是面对对象编程

Object Oriented Programming(OOP)

    把对象作为基本单元,把对象抽象成类(Class),包含成员和方法
    数据封装,继承,多态
    Python中使用类来实现.过程式编程(函数),OOP(类)

#### 组合与继承

优先使用组合而非继承

    组合是使用其他的类实例作为自己的一个属性(Has-a 关系)
    子类继承父类的属性和方法(Is a 关系)
    优先使用组合保持代码简单

#### 类变量和实例变量的区别

    类变量有所有实例共享
    实例变量由实例单独享有,不同实例之间不影响
    当我们需要在一个类的不同实例之间共享变量的时候使用类变量

#### classmethod/staticmethod区别

    都可以通过Class.method()的方式使用
    classmethod第一个参数是cls,可以引用类变量
    staticmethod使用起来和普通函数一样,只不过放在类里去组织

#### 什么是元类?使用场景

元类(Meta Class)是创建类的类

    元类允许我们控制类的生成,比如修改类的属性等
    使用type来定义元类
    元类最常见的一个使用场景就是ORM框架

### Python装饰器

#### 什么是装饰器Decorator

    Python中一切皆对象,函数也可以当做参数传递
    装饰器是接受函数作为参数,添加功能后返回一个新函数的函数(类)
    Python中通过@使用装饰器


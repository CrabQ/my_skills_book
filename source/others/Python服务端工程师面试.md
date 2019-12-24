# Python技术栈

## Python服务端工程师面试

### 面试流程

1. 一面问基础
2. 二面问项目
3. 三面问设计

### 后端技术栈

1. Python语言基础
    - 语言特点
    - 语法基础
    - 高级特性

2. 算法与数据结构
    - 常用算法和数据结构
    - 分析时间/空间复杂度
    - 实现常用算法和数据结构

3. 编程范式
    - 面对对象编程
    - 常用设计模式
    - 函数式编程

4. 操作系统
    - 常用Linux命令
    - 进程/线程
    - 内存管理

5. 网络编程
    - 常用协议 TCP/IP/HTTP
    - Socket编程基础
    - Python并发库

6. 数据库
    - Mysql,索引优化
    - 关系型和NoSql的使用场景
    - Redis缓存

7. Python Web框架
    - 常用框架对比, RESTful
    - WSGI原理
    - Web安全问题

8. 系统设计
    - 设计原则
    - 后端系统常用组件(缓存,数据库,消息队列等)
    - 技术选型和实现(短网址服务, Feed流系统)

### Python初/中级工程师技能要求

1. 初级工程师
    - 扎实的计算机理论基础
    - 代码规范,风格良好
    - 能在指导下靠谱地完成业务需求

2. 中级工程师
    - 扎实的计算机理论基础和丰富的项目经验
    - 能独立设计和完成项目需求
    - 熟悉常用的web组件(缓存,消息队列等)
    - 具备一定的系统设计能力

### 简历

1. 简历内容
    - 基本信息(姓名,学校,学历,联系方式等)
    - 职业技能(编程语言,框架,数据库,开发工具等)
    - 关键项目经验(担任职责,用到哪些技术)

2. 简历自我评价
    - 可有可无
    - 有则真诚简洁

3. 简历加分项
    - 知名项目经验
    - 技术栈比较匹配
    - 开源项目(github/技术blog/Linux/UNIX geek)

4. 简历注意事项
    - 内容精简,突出重点,不超过两页
    - 注意格式,推荐PDF
    - 信息真实,技能和岗位匹配,无太多无关内容

5. 自我介绍
    - 个人信息
    - 掌握的技术,参与的项目
    - 应聘的岗位,看法和兴趣

6. 自我介绍模板
    您好,我叫xx,毕业于xx,所学专业是xx
    之前就职于xx公司,担任后端工程师,负责xx项目,对xx技术比较熟悉
    我的工作经验和目前这个岗位较为匹配,希望能够应聘到这个岗位

## Python技术栈知识点

### Python语言基础

1. Python语言特性
    - 动态强类型语言
    - 动静态指的是运行期还是编译期确定类型
    - 强类型指的是不会发生隐式类型转换

2. Python作为后端语言优缺点
    - 胶水语言,轮子多,应用广泛
    - 语言灵活,生产力高
    - 性能问题,代码维护问题,Python2/3兼容问题

3. 什么是鸭子类型
    > 当看到一只鸟走起来像鸭子,游泳起来像鸭子,叫起来也想鸭子,这只鸟就可以被称为鸭子
    - 关注点在对象的行为,而不是类型(duck typing)
    - 比如 file, String, socket对象都支持read/write方法(file like object)
    - 再比如定义了 __iter__ 魔术方法的对象可以用for迭代
    - 鸭子类型更关注接口而非类型

4. 什么是monkey patch
    什么是 monkey patch?那些地方用到了,自己如何实现?
    - 所谓的monkey patch 就是运行时替换
    - 比如gevent库需要修改内置的socket
    - from gevent import monkey; monkey.patch_socket()

5. 什么是自省
    - 运行时判断一个对象的类型的能力
    - Python一切皆对象,用type,id,isinstance获取对戏那个类型信息
    - Inspect模块提供了更多获取对象信息的函数

6. 什么是列表和字典推导
    - 比如[i for i in range(10) if i%2==0]
    - 一种快速生成list/dict/set的方式,用来代替map/filter等
    - (i for i in range(10) if i%2==0)返回生成器

### Python2/3差异

1. Python3改进
    - print成为函数
    - 编码问题,Python3不再有Unicode对象,默认str就是Unicode
    - 除法变化,Python3除号返回浮点数
    - 类型注解(type hint).帮助IDE实现类型检查
    - 优化的super()方便直接调用父类函数
    - 高级解包操作. a, b, *rest = range(10)
    - Keyword only arguments.限定关键字参数
    - Chained exceptions. Python3重新抛出异常不会丢失栈信息
    - 一切返回迭代器range, zip, map, dict.values, ect.are all iterators
    - yield from 链接子生成器
    - asyncio内置库,async/await原生协程支持异步编程
    - 新的内置库enum, mock, asyncio, ipaddress, concurrent.futures等
    - 生成的pyc文件统一放到__pycache__
    - 一些内置库的修改. urllib, selector等
    - 性能优化等

2. Python2/3工具
    熟悉一些兼容2/3的工具
    - six模块
    - 2to3等工具转换代码
    - \__future\__


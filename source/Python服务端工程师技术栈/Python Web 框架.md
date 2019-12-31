# Python Web 框架

## WSGI与web框架

### 什么是WSGI

    Python Web Server Gateway Interface(pep3333)
    解决Python Web Server乱象mod_python, CGI, FastCGI等
    描述了Web Server(Gunicorn/uWSGI)如何与web框架(Flask/Django)交互,web框架如何处理请求

### 常用的Python web框架对比

    Django:大而全,内置ORM, Admin等组件,第三方插件较多
    Flask:微框架,插件机制,比较灵活
    Tornado:异步支持的微框架和异步网络库

### 什么是MVC

    Model:负责业务对象和数据库的交互(ORM)
    view:负责与用户的交互展示
    Controller:接收请求参数调用模型和视图完成请求

### 什么是ORM

Object Relational Mapping, 对象关系映射

    用于实现业务对象与数据表中的字段映射
    优势:代码更加面向对象,代码量更少,灵活性高,提升开发效率

## Web安全

### 什么是SQL注入

    通过构造特殊的输入参数传入Web应用,导致后端执行了恶意SQL
    通常犹豫程序员未对输入进行过滤,直接动态拼接SQL产生
    可以使用开源工具sqlmap,SQLninja检测

### 如何防范SQL注入

web安全一大原则:永远不要相信用户的任何输入

    对输入参数做好检查(类型和范围);过滤和转义特殊字符
    不要直接拼接sql,使用ORM可以大大降低sql注入风险
    数据库层:做好权限管理配置;不要明文存储敏感信息

### 什么是XSS

XSS(Cross Site Scripting),跨站脚本攻击

    恶意用户将代码植入到提供给其他用户使用的页面中,未经转义的恶意代码输出到其他用户的浏览器被执行
    用户浏览页面的时候嵌入页面中的脚本(js)会被执行,攻击用户
    主要分为两类:反射性(非持久型),存储型(持久型)

## 前后端分离和RESTful

### 什么是前后端分离?有哪些优点

后端只负责提供数据接口,不再渲染模板,前端获取数据并呈现

    前后端解耦,接口复用(前端和客户端公用接口),减少开发量
    各司其职,前后端同步开发,提升工作效率.定义好接口规范
    更有利于调试(mock),测试和运维部署

### 什么是RESTful

Representational State Transfer

    表现层状态转移,有HTTP协议的主要设计者Roy Fielding提出
    资源(Resources),表现层(Representation),状态转化(State Transfer)
    是一种以资源为中心的web软件架构风格,可以用Ajax和RESTful web服务构建应用

### RESTful 解释

    资源(Resources):使用URI指向的一个实体
    表现层(Representation):资源的表现形式,比如图片,HTML文本等
    状态转化(State Transfer):GET, POST, PUT, DELETE HTTP动词来操作资源,实现资源状态的改变

### RESTful的准则

设计概念和准则

    所有事物抽象为资源(resource),资源对应唯一的标识(identifier)
    资源通过接口进行操作实现状态转移,操作本身是无状态的
    对资源的操作不会改变资源的标识

### 什么是RESTful API

    通过 HTTP GET/POST/PUT/DELETE 获取/新建/更新/删除 资源
    一般使用json格式返回数据
    一般web框架都有相应的插件支持RESTful API
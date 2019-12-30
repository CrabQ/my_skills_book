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

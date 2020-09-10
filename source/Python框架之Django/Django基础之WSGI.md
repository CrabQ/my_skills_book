# Django基础之WSGI

## WSGI

WSGI（Web Server Gateway Interface),一种规范. 定义了使用Python编写的web应用程序与web服务器程序之间的接口格式, 实现web应用程序与web服务器程序间的解耦

常用的WSGI服务器有uwsgi, Gunicorn. 而Python标准库提供的独立WSGI服务器叫wsgiref, Django开发环境使用wsgiref

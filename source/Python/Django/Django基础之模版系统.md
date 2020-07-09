# Django基础之模版系统

```python
# {{ 变量 }}  {% 逻辑 %}
```

## 过滤器

```python
# 获取数据长度
<p>{{ name_list|length }}</p>

# 默认值
<p>{{ xx|default:'啥也没有' }}</p>

# 将值格式化为一个人类可读的文件尺寸 ,例如 '13 KB', '4.1 MB'
<p>{{ movesize|filesizeformat }}</p>

#  切片
<p>{{ name|slice:':3' }}</p>

#  时间格式化显示
<p>{{ now|date:'Y-m-d' }}</p>

#  字符截断
<p>{{ words|truncatechars:'9' }}</p>

#  单词截断
<p>{{ words|truncatewords:'3' }}</p>

# 移除所有与给出的变量相同的字符串
<p>{{ words|cut:'i' }}</p>

# 使用字符串连接列表
<p>{{ name_list|join:'+' }}</p>

# 将字符串识别成标签
<p>{{ tag|safe }}</p>
```

标签

```python
# for循环
{% for key,value in d1.items %}
{{ forloop.counter }}
    <li>{{ key }} -- {{ value }}</li>
{% endfor %}

# forloop.counter      当前循环的索引值(从1开始)，forloop是循环器，通过点来使用功能
# forloop.counter0     当前循环的索引值（从0开始）
# forloop.revcounter   当前循环的倒序索引值（从1开始）
# forloop.revcounter0  当前循环的倒序索引值（从0开始）
# forloop.first        当前循环是不是第一次循环（布尔值）
# forloop.last         当前循环是不是最后一次循环（布尔值）
# forloop.parentloop   本层循环的外层循环的对象，再通过上面的几个属性来显示外层循环的计数等


# if
{% if num > 100 or num < 0 %}
    <p>无效</p>
{% elif num > 80 and num < 100 %}
    <p>优秀</p>
{% else %}
    <p>凑活吧</p>
{% endif %}

# with
{% with business.employees.count as total %}
    {{ total }}
{% endwith %}

# csrf_token
{% csrf_token %}
```

## 模板继承

```python
{% extends "base.html" %}

{% block title %}
    xxx
{% endblock %}
# block.super 显示模板内容
```

## 组件

```python
{% include 'navbar.html' %}
```

## 自定义过滤器

```python
# app应用内创建templatetags文件夹
# templatetags文件夹创建随意名字文件

# app1/templatetags/add_info.py
from django import template

register = template.Library()

@register.filter
# 最多两个参数
def add_underline(v1, v2):
    return v1+v2

# 模板使用,数据加上__
    {% load add_info %}
    <p>{{ data|add_underline:'__' }}</p>
```

## 自定义标签

```python
# app应用内创建templatetags文件夹
# templatetags文件夹创建随意名字文件

# app1/templatetags/add_info.py
from django import template

register = template.Library()

@register.simple_tag
# 任意参数
def add_word(v1, v2, v3):
    return v1+v2+v3

# 模板使用,数据加上
    {% load add_info %}
    <p>{% add_word data '__' '++' %}</p>
```

## inclusion_tag

```python
# app应用内创建templatetags文件夹
# templatetags文件夹创建随意名字文件

# app1/templatetags/add_info.py
@register.inclusion_tag(filename='inclusion.html')
def add_list(list):
    return {'alist': list}

# templates/inclusion.html
<ol>
    {% for i in alist %}
    <li>{{ i }}</li>
    {% endfor %}
</ol>

# 模板使用,html页面添加列表,test_list为views函数传递的列表
    {% load add_info %}
    {% add_list test_list %}
```

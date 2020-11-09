# Django基础之form组件

```python
# 1 生成页面HTML标签
# 2 校验用户提交的数据合法性
# 3 保留用户输入的数据
```

## 生成页面HTML标签

```python
from django import forms

def mobile_validate(value):
    mobile_re = re.compile(r'^13[0-9]{9}')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

class LoginForm(forms.Form):
     name = forms.CharField(
        required=True,  #默认等于True，内容不能为空
        min_length=6,
        label='用户名',
        initial='地铁', #初始值，默认值
        help_text='请输入用户名',
        error_messages={'required':'不能为空！','min_length':'太短！'},
        widget=forms.widgets.TextInput,
    )
    password = forms.CharField(
        min_length=8,
        max_length=10,  #最大长度不能超过10位
        label='密码',
        widget=forms.widgets.PasswordInput(), #密文输入
    )

# radio单选框
    sex = forms.ChoiceField(
        label='性别',
        initial=3,
        choices=((1, "男"), (2, "女"), (3, "保密")),
        widget=forms.widgets.RadioSelect(),
    )

# select下拉单选框
    city = forms.ChoiceField(
        label='性别',
        initial=3,
        choices=((1, "北京"), (2, "上海"), (3, "东莞")),
        widget=forms.widgets.Select(),
    )

# checkbox多选框
    hobby = forms.MultipleChoiceField(
        label='爱好',
        choices=((1, "抽烟"), (2, "喝酒"), (3, "烫头")),
        widget=forms.widgets.CheckboxSelectMultiple,
    )

# select下拉多选框
    girls = forms.MultipleChoiceField(
        label='爱好',
        choices=((1, "抽烟"), (2, "喝酒"), (3, "烫头")),
        widget=forms.widgets.SelectMultiple,
    )

# 单选checkbox
    status = forms.ChoiceField(
        label='remeber me!!',
        choices=(('True', "记住密码"), ('False', "不记住密码")),
        widget=forms.widgets.CheckboxInput,
    )

#给标签加属性
widget=forms.widgets.TextInput(attrs={'class':'form-control'}),
```

### 批量添加标签样式

```python
class LoginForm(forms.Form):
    # 批量添加标签样式
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})
```

## 校验用户提交的数据合法性

```python
def register(request):
    form_obj = LoginForm()
    if request.method == 'GET':
        return render(request,'register.html',{'form_obj':form_obj})
    else:
        form_obj = LoginForm(request.POST)
        #校验数据，全部通过校验，返回True
        if form_obj.is_valid():
            # model.save()
            return HttpResponse('注册成功')
        else:
            return render(request,'register.html',{'form_obj':form_obj})
```

html写法

```html
<form action="" method="post" novalidate>
  {% csrf_token %}
  <div>
    <label for="">{{ form_obj.name.label }}</label>
    {{ form_obj.name }}
    {{ form_obj.name.help_text }}
    <span style="color: red;font-size: 14px;">{{ form_obj.name.errors.0 }}</span>
  </div>
  <input type="submit">
</form>
```

### RegexValidator验证器

```python
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.validators import RegexValidator

class MyForm(Form):
    user = fields.CharField(
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
    )
```

#### 自定义验证函数

```python

import re
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError


# 自定义验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

class PublishForm(Form):

    # 使用自定义验证规则
    phone = fields.CharField(validators=[mobile_validate, ], )
```

### 局部钩子和全局钩子

```python
class LoginForm(forms.Form):
    ...

    # 局部钩子
    def clean_name(self):
        value = self.cleaned_data['name']
        if 'a' in value:
            raise ValidationError('含有敏感词汇')
        else:
            return value

    # 全局钩子
    def clean(self):
        if self.cleaned_data['password'] == self.cleaned_data['r_password']:
            return self.cleaned_data
        else:
            #给某个字段单独添加报错信息
            self.add_error('r_password','两次输入的密码不一致！')
            raise ValidationError('两次输入的密码不一致！')
```

## ModelForm

Django 提供一个辅助类来让我们可以从Django的模型创建Form, 这就是ModelForm

```python
# 通过model的属性自动翻译成form的属性，来进行form组件的工作

from django.core.exceptions import ValidationError

from . import models

class BookModelForm(forms.ModelForm):
    # 覆盖models里面写的字段验证, 添加更多的验证
    # title=forms.CharField(max_length=15,min_length=6)

    class Meta:
        model = models.Book
        # fields=['title','publishs',]
        fields='__all__'
        # 排除
        exclude = ['title','xx',]
        # 帮助提示信息
        # help_texts = None
        labels = {
            'title':'书名',
            'publishDate':'出版日期',
        }
        widgets = {
            'publishDate':forms.widgets.TextInput(attrs={'type':'date'}),
        }
        error_messages = {
            'title':{'required':'不能为空',},
            'publishDate':{'required':'不能为空',}
        }

    # 局部钩子
    def clean_title(self):
        value = self.cleaned_data.get('title')
        return value

    # 全局钩子
    # def clean(self):
    #     ...
```

### 使用ModelForm创建对象

```python
>>> from myapp.models import Book
>>> from myapp.forms import BookForm

# 根据POST数据创建一个新的form对象
>>> form_obj = BookForm(request.POST)

# 创建书籍对象
>>> new_ book = form_obj.save()
```

### 使用ModelForm更新数据

```python
>>> edit_obj = Book.objects.get(id=1)
# 基于一个书籍对象创建form对象, 使用POST提交的数据更新书籍对象
>>> form_obj = BookForm(request.POST, instance=edit_obj)
>>> form_obj.save()
```

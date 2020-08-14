# Django基础之Auth认证模块

Auth模块是Django自带的用户认证模块

## auth模块常用方法

authenticate()

```python
from django.contrib.auth import authenticate, login
# 用户认证功能, 即验证用户名以及密码是否正确
user = authenticate(username='usernamer',password='password')
```

login(HttpRequest, user)

```python
# 用户登录的功能, 本质上会在后端为该用户生成相关session数据
# 该函数接受一个HttpRequest对象，以及一个经过认证的User对象
user = authenticate(username='usernamer',password='password')
if user is not None:
    login(request, user)

```

logout(request)

```python
# 调用该函数当前请求的session信息会全部清除. 用户即使没有登录也不会报错
```

is_authenticated()

```python
# 用来判断当前请求是否通过了认证
def my_view(request):
  if not request.user.is_authenticated():
    return redirect('login')
```

login_required()

```python
# 装饰器工具, 用来快捷的给某个视图添加登录校验
# settings.py可配置登录成功后跳转路由, 默认跳转'/accounts/login/ '
# LOGIN_URL = '/login/'

from django.contrib.auth.decorators import login_required

@login_required
def myview():
    pass
```

create_user()

```python
# 创建新用户
from django.contrib.auth.models import User

user = User.objects.create_user(username='用户名',password='密码',email='邮箱',...)
```

create_superuser()

```python
创建新的超级用户
from django.contrib.auth.models import User

user = User.objects.create_superuser(username='用户名',password='密码',email='邮箱',...)
```

check_password(password)

```python
# 检查密码是否正确 True|False
ok = user.check_password('密码')
```

set_password(password)

```python
# 修改密码
user.set_password(password='')
user.save()
```

## 扩展默认的auth_user表

```python
from django.contrib.auth.models import AbstractUser
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11, null=True, unique=True)

    def __str__(self):
        return self.username

# 扩展默认的auth_user表需要在settings.py设置
# AUTH_USER_MODEL = "app名.UserInfo"
```

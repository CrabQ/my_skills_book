# Django第三方模块

## django-cors-headers解决跨域问题

安装模块

```shell
pip install django-cors-headers
```

使用

```python
# settings.py
# 1. 添加app
INSTALLED_APPS = [
    'corsheaders',
]

# 2. 添加中间件
# 在SessionMiddleware后面以及CommonMiddleware前面
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware'
    'django.middleware.common.CommonMiddleware',
]

# 3. 添加配置参数
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ('http://localhost:63342',)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    # 'XMLHttpRequest',
    # 'X_FILENAME',
    # 'accept-encoding',
    'authorization',
    'content-type',
    # 'dnt',
    # 'origin',
    # 'user-agent',
    # 'x-csrftoken',
    # 'x-requested-with',
    # 'Pragma',
)
```

## xadmin

安装

```shell
# 下载对应版本
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2
```

```python
# 注册app
# luffyapi/settings/dev.py
INSTALLED_APPS = [
    # xadmin主体模块
    'xadmin',
    # 渲染表格模块
    'crispy_forms',
    # 为模型通过版本控制，可以回滚数据
    'reversion',
]
```

```shell
# 数据迁移
python manage.py makemigrations
python manage.py migrate
```

替换掉admin

```python
# luffyapi/urls.py
# xadmin的依赖
import xadmin
xadmin.autodiscover()
# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
]
```

创建超级用户

```shell
python manage.py createsuperuser
```

xadmin全局配置

```python
# luffyapi/apps/home/xadmin.py
import xadmin
from xadmin import views


# xadmin全局配置
class GlobalSettings(object):
    site_title = "luffy"  # 设置站点标题
    site_footer = "luffy有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)

# 注册app
```

## django-redis

安装

```shell
pip install django-redis
```

配置

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "DECODE_RESPONSES": True,
            "PASSWORD": "",
        }
    }
}
```

使用

```python
# 1 通过缓存
from django.core.cache import cache

# 2 获取连接
from django_redis import get_redis_connection
conn=get_redis_connection('default')
```

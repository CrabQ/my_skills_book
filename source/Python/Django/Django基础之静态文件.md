# Django基础之静态文件

## 静态文件配置

```python
# 修改settings.py文件

# 别名,url地址里引用 模板使用{% load static %}
STATIC_URL = '/static/'

# 静态文件所在文件夹
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics')
]
```

## 用户上传文件配置

```python
# 修改settings.py文件

# 用户上传文件的根目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 暴露后端指定文件夹资源

```python
# 方法1
# settings.py
MEDIA_URL = '/media/'


# 设置开发环境中访问文件方法
from BBS import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 方法2
from django.views.static import serve
from django.urls import  re_path
from BBS import settings

urlpatterns = [
    re_path(r'^media/(?P<path>.*)', serve, {'document_root':settings.MEDIA_ROOT}),
]
```

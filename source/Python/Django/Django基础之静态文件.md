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

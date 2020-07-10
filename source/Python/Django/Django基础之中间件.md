# Django基础之中间件

## 中间件的五个方法

```python
# 按顺序执行
process_request(self,request)
process_view(self, request, view_func, view_args, view_kwargs)
process_template_response(self,request,response)
process_exception(self, request, exception)
process_response(self, request, response)
```

## 自定义中间件

```python
# 应用下创建一个文件夹，文件夹下面创建一个xx.py文件
from django.utils.deprecation import MiddlewareMixin

class MD1(MiddlewareMixin):
    def process_request(self,request):
        return None
    def process_response(self,request,response)
        return response
```

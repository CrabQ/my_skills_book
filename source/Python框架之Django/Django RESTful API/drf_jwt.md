# drf_jwt

## 安装

```shell
pip install djangorestframework-jwt
```

## 基本使用

相关配置

```python
# settings.py
REST_FRAMEWORK = {
    # 全局使用
    # 'DEFAULT_AUTHENTICATION_CLASSES': ["rest_framework_jwt.authentication.JSONWebTokenAuthentication"]
}

JWT_AUTH = {
    # 自定义登录认证返回结果, 默认只返回token字段
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'jwt_abstract_user.utils.jwt_rph',

    # 设置过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
}


# views.py
class BooksView(APIView):
    # 局部禁用
    # authentication_classes = []
    # 局部启用
    authentication_classes = [jwt_authentication]

    def get(self, request):
        print(request.user)
        return Response('ok')
```

自定义drf_jwt默认的登录认证返回结果

```python
# urls.py
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 1. 简单使用: 配置登录认证路由
    path('login/', obtain_jwt_token),
    path('books/', views.BooksView.as_view()),
]


# utils.py
# 自定义登录认证返回结果, 默认只返回token字段
def jwt_rph(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        "msg": "登录成功",
        "status": 100,
    }
```

## 自定义多种登录方式, 手动签发token

用户访问login链接, 返回token

路由配置

```python
# urls.py

from django.urls import path

from . import views

urlpatterns = [
    # 2. 自定义login,手动签发token: 1). 配置自定义login, 完成多方式登录路由
    path('login2/', views.LoginViewSet.as_view({'post':'login'})),
]
```

视图函数

```python
# views.py

# 2. 自定义login,手动签发token: 2).自定义login, 返回token
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .ser import LoginModelSerializer


class LoginViewSet(ViewSet):

    def login(self, request):
        # 序列化类写多方式登录逻辑, 传入数据生成序列化对象
        ser = LoginModelSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        token = ser.context.get("token")
        username = ser.context.get("username")

        return Response({'token': token, 'username': username, "msg": "登录成功", "status": 100, })
```

序列化类, 完成多方式登录, 手动签发token

```python
# utils.py

import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from jwt_abstract_user import models


# 2. 自定义login,手动签发token: 3).认证用户, 完成多方式登录, 手动签发token
class LoginModelSerializer(serializers.ModelSerializer):
    # 覆盖数据库中的字段,变成新的字段
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # 判断不同形式用户名
        if re.match(r"^1[3-9][0-9]{9}$", username):
            user = models.User.objects.filter(phone=username).first()
        elif re.match(r'.+@\w+\.\w+', username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()

        if not user:
            raise ValidationError("用户不存在")
        if not user.check_password(password):
            raise ValidationError("用户名或密码错误")

        # 传入user, 获取payload
        payload = jwt_payload_handler(user)
        # 传入payload, 获取token
        token = jwt_encode_handler(payload)

        # 返回token
        self.context['token'] = token
        self.context['username'] = user.username

        return attrs
```

## 自定制基于jwt的认证类

用户携带token访问某个url, token认证通过, 返回内容, 否则拒绝

路由配置

```python
# urls.py

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('books/', views.BooksView.as_view()),
]
```

自定制基于jwt的认证类

```python
# utils.py

# 自定制基于jwt的认证类
# 继承以下两个都行
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
# from rest_framework.authentication import BaseAuthentication

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.utils import jwt_decode_handler
import jwt

from .models import User

class jwt_authentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_value:
            raise AuthenticationFailed("没有携带认证信息!")
        try:
            # 验证token并取出payload
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("签名过期!")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("用户非法!")
        user = User.objects.filter(id=payload.get('user_id')).first()
        return user, jwt_value
```

视图函数中引用定制的认证类

```python
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import jwt_authentication


class BooksView(APIView):
    # 使用自定义认证类
    authentication_classes = [jwt_authentication]

    def get(self, request):
        print(request.user)
        return Response('ok')
```

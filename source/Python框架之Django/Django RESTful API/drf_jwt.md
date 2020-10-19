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
    # 用户登录,返回token
    path('login/', views.UserLoginViewSet.as_view(actions={'post': 'login', })),
    # 需要token认证的视图
    path('hi/', views.HiView.as_view()),
]
```

序列化类, 多方式登录, 手动签发token

```python
# ser.py
import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from jwt_abstract_user import models


# 认证用户, 完成多方式登录, 手动签发token
class UserLoginSerializer(serializers.ModelSerializer):
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

        return attrs
```

自定制基于jwt的认证类

用户携带token访问某个url, token认证通过, 返回内容, 否则拒绝

```python
# utils.py
# 继承以下两个都行
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.utils import jwt_decode_handler
import jwt

from .models import User


class CustomerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed('无认证信息!')
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('签名过期!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('用户非法!')
        user = User.objects.filter(pk=payload.get('user_id')).first()
        return user, token
```

视图

```python
# views.py
from .utils import CustomerAuthentication

# 登录视图,获取token
class UserLoginViewSet(ViewSet):
    def login(self, request, *args, **kwargs):
        login_ser = ser.UserLoginSerializer(data=request.data)
        login_ser.is_valid(raise_exception=True)
        token = login_ser.context.get('token')
        return Response(data={"token": token})


# token认证, 通过则返回信息
class HiView(GenericAPIView):
    authentication_classes = [CustomerAuthentication, ]

    def get(self, request, *args, **kwargs):
        return Response(data={'hi': request.user.username})
```

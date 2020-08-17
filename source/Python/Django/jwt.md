# jwt

```shell
传统token方式

用户登录成功后, 服务端生成一个随机token给用户, 并且在服务端(数据库或缓存)中保存一份token.
以后用户再来访问时需携带token, 服务端接收到token之后去数据库或缓存中进行校验token的是否超时,是否合法

jwt方式

用户登录成功后, 服务端通过jwt生成一个随机token给用户(服务端无需保留token)
以后用户再来访问时需携带token,服务端接收到token之后通过jwt对token进行校验
```

## jwt创建token

```shell
# 由 . 连接的三段字符串组成
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

第一段HEADER部分, 固定包含算法和token类型, 对此json进行base64url加密, 这就是token的第一段

```shell
{
  "alg": "HS256",
  "typ": "JWT"
}
```

第二段PAYLOAD部分, 包含一些数据, 对此json进行base64url加密, 这就是token的第二段

```shell
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
  ...
}
```

第三段SIGNATURE部分, 把前两段的base密文通过.拼接起来.
然后对其进行HS256加密, 再然后对hs256密文进行base64url加密, 最终得到token的第三段

```shell
base64url(
    HMACSHA256(
      base64UrlEncode(header) + "." + base64UrlEncode(payload),
      your-256-bit-secret (秘钥加盐)
    )
)
```

## python实现

```python
import datetime

import jwt
from jwt import exceptions


SALT = 'sdgl3uw406t823-kLfslh]34|95SDH4-09365--1831kyth'

def create_token():
    header = {
        'typ': 'jwt',
        'alg': 'HS256',
    }

    payload = {
        'user_id': 1,
        'user_name': 'xiaoming',
        'exp': datetime.datetime.now()+datetime.timedelta(seconds=7)
    }

    res = jwt.encode(headers=header, key=SALT, payload=payload, algorithm='HS256')

    return res.decode('utf-8')

def get_payload(token):
    try:
        res = jwt.decode(jwt=token, key=SALT, verify=True)
        return res
    except exceptions.ExpiredSignatureError:
        print('token已失效')
    except jwt.DecodeError:
        print('token认证失败')
    except jwt.InvalidTokenError:
        print('非法的token')


if __name__ == "__main__":
    res = create_token()
    print(get_payload(res))
```

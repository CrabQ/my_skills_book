# request

> [开源地址](https://github.com/kennethreitz/requests)
> [中文文档 API](http://docs.python-requests.org/zh_CN/latest/index.html)

## 安装

```shell
pip install requests
```

## GET请求

```python
import requests

kw = {'wd':'长城'}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

# params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
response = requests.get("http://www.baidu.com/s?", params=kw, headers=headers)

# 查看响应内容，response.text 返回的是Unicode格式的数据
print(response.text)

# 查看响应内容，response.content返回的字节流数据
print(respones.content)

# 查看完整url地址
print(response.url)
#'http://www.baidu.com/s?wd=%E9%95%BF%E5%9F%8E'

# 查看响应头部字符编码
print(response.encoding)
#'utf-8'

# 手动指定编码方式
response.encoding = 'utf-8'

# 查看响应码
print(response.status_code)
#200
```

## POST请求

```python
import requests

formdata = {
    "type":"AUTO",
    "i":"i love python",
    "doctype":"json",
    "xmlVersion":"1.8",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_ENTER",
    "typoResult":"true"
}

url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

response = requests.post(url, data = formdata, headers = headers)

print(response.text)
#{"type":"EN2ZH_CN","errorCode":0,"elapsedTime":2,"translateResult":[[{"src":"i love python","tgt":"我喜欢python"}]],"smartResult":{"type":1,"entries":["","肆文","高德纳"]}}

# 如果是json文件可以直接显示
print(response.json())
#{u'errorCode': 0, u'elapsedTime': 0, u'translateResult': [[{u'src': u'i love python', u'tgt': u'\u6211\u559c\u6b22python'}]], u'smartResult': {u'type': 1, u'entries': [u'', u'\u8086\u6587', u'\u9ad8\u5fb7\u7eb3']}, u'type': u'EN2ZH_CN'}
```

## 代理

```python
import requests

# 根据协议类型，选择不同的代理
proxies = {
  "http": "http://12.34.56.79:9527",
  "https": "http://12.34.56.79:9527",
}

response = requests.get("http://www.baidu.com", proxies = proxies)
print response.text

# 如果代理需要使用HTTP Basic Auth，可以使用下面这种格式：
proxy = { "http": "mr_mao_hacker:sffqry9r@61.158.163.130:16816" }

response = requests.get("http://www.baidu.com", proxies=proxy)

print(response.text)

#如果是Web客户端验证，需要添加 auth = (账户名, 密码)

import requests

auth=('test', '123456')

response = requests.get('http://192.168.199.107', auth=auth)
```

## Cookies与Session

### Cookies

```python
#import requests

reponse = requests.get("http://www.baidu.com/")

#返回CookieJar对象
cookiejar = reponse.cookies

#将CookieJar对象转化为字典
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)

print(cookiejar)
#<RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>

print(cookiedict)
#{'BDORZ': '27315'}

```

### Session

```python
# 实现人人网登录

import requests

# 1. 创建session对象，可以保存Cookie值
ssion = requests.session()

# 2. 处理headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

# 3. 需要登录的用户名和密码
data = {"email":"mr_mao_hacker@163.com", "password":"alarmchime"}

# 4. 发送附带用户名和密码的请求，并获取登录后的Cookie值，保存在ssion里
ssion.post("http://www.renren.com/PLogin.do", data = data)

# 5. ssion包含用户登录后的Cookie值，可以直接访问那些登录后才可以访问的页面
response = ssion.get("http://www.renren.com/410043129/profile")
```

### session.headers.update

session.headers.update(headers)无法对request.prepare()生效

自定义一个微信request,继承Request,使用session.send处理之后获取响应内容，然而发现headers没有更新，代码如下

```python
from requests import Request
from requests import Session

class WeixinRequest(Request):
    def __init__(self, url, method='GET', headers=None, timeout=5):
        super(WeixinRequest, self).__init__(method, url, headers)
        self.timeout = timeout

if __name__ == '__main__':
    session = Session()
    headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    url = 'https://www.baidu.com'
    weixin = WeixinRequest(url=url)
    print(session.headers)
    session.headers.update(headers)
    print(session.headers)
    response = session.send(weixin.prepare())
    print(response.request.headers)

# 未update前的Session()自带headers
{'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
# update后的headers
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
# session.send(weixin.prepare())获取的headers
{}
```

要用`Session.prepare_request()`取代 `Request.prepare()`

> 参考: [prepared-request](https://requests.readthedocs.io/en/master/user/advanced/#prepared-requests)

```python
# response = session.send(weixin.prepare())
response = session.send(session.prepare_request(weixin))

{'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
```

## SSL证书验证

Requests也可以为HTTPS请求验证SSL证书

```python
# 12306需要证书验证

import requests
response = requests.get("https://www.12306.cn/mormhweb/")
print(response.text)

#果然：
SSLError: ("bad handshake: Error([('SSL routines', 'ssl3_get_server_certificate', 'certificate verify failed')],)",)

#如果我们想跳过 12306 的证书验证，把 verify 设置为 False 就可以正常请求了。
r = requests.get("https://www.12306.cn/mormhweb/", verify = False)
```

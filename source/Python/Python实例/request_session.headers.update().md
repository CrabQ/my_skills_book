# request_session.headers.update()

## session.headers.update(headers)无法对request.prepare()生效

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

结果发现使用session.send(weixin.prepare())并不会使用update之后的session.headers，要用Session.prepare_request() 取代 Request.prepare()
参考[prepared-request](http://docs.python-requests.org/zh_CN/latest/user/advanced.html#prepared-request)
> 你立即准备和修改了 PreparedRequest 对象，然后把它和别的参数一起发送到 requests.* 或者 Session.*。
> 然而，上述代码会失去 Requests Session 对象的一些优势， 尤其 Session 级别的状态，例如 cookie 就不会被应用到你的请求上去。要获取一个带有状态的 PreparedRequest， 请用 Session.prepare_request() 取代 Request.prepare() 的调用

代码修改一下，就可以更新headers

```python
# response = session.send(weixin.prepare())
response = session.send(session.prepare_request(weixin))

{'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
```

# Django基础之Cookie和Session

## Django中操作Cookie

```python
# Cookie本身最大支持4096字节

# 设置Cookie
rep ＝ render(request, ...)
rep.set_cookie(key,value,...)
rep.set_signed_cookie(key,value,salt='加密盐', max_age='过期时间', ...)

# 获取Cookie
request.COOKIES['key']
request.get_signed_cookie(key, default=RAISE_ERROR, salt='', max_age=None)

# 删除Cookie
rep.delete_cookie("user")
```

## Django中操作Session

```python
# 获取、设置、删除Session中数据
request.session.get('k1',None)
request.session['k1'] = 123
request.session.setdefault('k1',123) # 存在则不设置
del request.session['k1']

# 会话session的key
request.session.session_key

# 将所有Session失效日期小于当前日期的数据删除
request.session.clear_expired()

# 检查会话session的key在数据库中是否存在
request.session.exists("session_key")

# 删除当前会话的所有Session数据
request.session.delete()
　　
# 删除当前的会话数据并删除会话的Cookie
request.session.flush()

# 设置会话Session和Cookie的超时时间
request.session.set_expiry(value)
    # 如果value是个整数, session会在些秒数后失效
    # 如果value是个datatime或timedelta, session就会在这个时间后失效
    # 如果value是0,用户关闭浏览器session就会失效
    # 如果value是None,session会依赖全局session失效策略
```

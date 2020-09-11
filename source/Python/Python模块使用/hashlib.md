# hashlib

## md5加密

```python
import hashlib

# 待加密信息
str = 'this is a md5 test.'

# 创建md5对象
m = hashlib.md5()

# 或者 b = bytes(str, encoding='utf-8'
b = str.encode(encoding='utf-8')

m.update(b)
str_md5 = m.hexdigest()

# 另一种写法：b''前缀代表的就是bytes
str_md5 = hashlib.md5(b'this is a md5 test.').hexdigest()
```

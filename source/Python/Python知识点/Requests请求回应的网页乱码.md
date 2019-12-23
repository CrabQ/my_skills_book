# Requests请求回应的网页乱码

```python
#查看编码方式
print(wb_data.headers['content-type'])
print(wb_data.encoding) # response的内容编码
print(wb_data.apparent_encoding) #response headers 里设置的编码
print(requests.utils.get_encodings_from_content(wb_data.text)) #response返回的html header标签里设置的编码
#text/html
#ISO-8859-1  # response的内容编码
#UTF-8-SIG   #response headers 里设置的编码
#['utf-8']   #response返回的html header标签里设置的编码
```

解决办法

1. 使用.encoding属性改变response的内容编码,在代码里加上下面一行代码

   ```python
   # apparent_encoding使用的是什么编码，就改为什么，不然即使是utf-8也会出现乱码
   wb_data = requests.get(articleUrl,headers=headers)
   wb_data.encoding = 'utf-8' #手动指定编码方式
   ```

2. 使用原始的Response.content
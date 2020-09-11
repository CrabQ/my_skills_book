# json

## json模块

```shell
1. json.loads() Json格式字符串解码转换成Python对象
2. json.dumps() python类型转化为json字符串，返回一个str对象
3. json.dump()  将Python内置类型序列化为json对象后写入文件
4. json.load()  读取文件中json形式的字符串转化成python类型
```

## 读取json文件

```python
import json

# 读取json文件
with open(r'./a.json', 'r') as f:
    context = json.load(f)

name = context.get('name')
children = context.get('children')
```

## 写入json数据

```python
import json

items = {'user':'xiao',
        'age':'17'
        }

with open("./test.json",'a', encoding = "utf-8") as f:
    # ensure_ascii=False, 不加会转化成ascii码写到文件中,中文字符都会变成 Unicode 字符
    f.write(json.dumps(items, ident=2, ensure_ascii = False) + "\n")
    #另一种方式：
    #json.dump(items, f, ensure_ascii=False )
```

## json序列化时间日期类型的数据

```python
import json
from datetime import datetime
from datetime import date

# 对含有日期格式数据的json数据进行转换
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field,date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,field)
```

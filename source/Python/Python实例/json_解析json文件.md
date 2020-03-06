# json_解析json文件

## json模块

json模块提供以下四个功能，用于字符串和python数据类型间进行转换

1. json.loads() 把Json格式==字符串==解码转换成Python对象
2. json.dumps() 实现python类型转化为json==字符串==，返回一个str对象 把一个Python对象编码转换成Json字符串
3. json.dump()  将Python内置类型序列化为json对象后==写入文件==
4. json.load()  读取==文件==中json形式的字符串元素 转化成python类型

## 读取json文件

```python
import json

infile = r'./br08402_gene.json'

# 读取json文件
with open(infile, 'r') as f:
    context = json.load(f)

name = context.get('name')
children = context.get('children')
```

## 写入json数据

python3 默认的是UTF-8格式

- 在dump的时候要加上ensure_ascii=False,不然会变成ascii码写到文件中,中文字符都会变成 Unicode 字符
- 另外python3在向txt文件写中文的时候也要注意在打开的时候加上```encoding='utf-8'```

```python
import json

items = {'user':'xiao',
        'age':'17'
        }

with open("./test.json",'a', encoding = "utf-8") as f:
    f.write(json.dumps(items, ident=2, ensure_ascii = False) + "\n")
    #另一种方式：
    #json.dump(items, f, ensure_ascii=False )
```

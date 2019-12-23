# csv_以逗号分隔字符串,但忽略双引号内的逗号

现有数据格式如下，需要以逗号分隔字符串,但忽略双引号内的逗号，即`"Anemia, Hemolytic"`内的逗号不进行分割

```python
a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,22425172'
```

需要的效果如下：

```python
['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '22425172']
```

目前想到两种方法

1. 使用正则re.split进行字符串分割
2. 使用csv模块的reader进行分割

## 使用正则re.split进行字符串分割

```python
import re

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,22425172'
b = re.split(r',\s*(?![^"]*\"\,)', a)
print(len(b))
print(b)

9
['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '22425172']
```

```python
r',\s*(?![^"]*\"\,)'

# \s表示匹配空白字符，*表示匹配前一个字符0次或者无数次,\s*即表示如果是,,会匹配为'',这样数据分割出来的列表长度一致，下标对应的字符串不会混乱
# (?![^"]*\"\,)表示匹配后面有"asg",的逗号，但是不匹配后面是asg",的逗号，重点是这个，分为两部分解释
# [^"]*\"\,在原始字符串模式下，表示匹配asdgdg",但是不匹配"asdgdg",
# 1(?!2)表示匹配13中的1,但是不匹配12中的1
```

组合在一起，在以逗号分割的时候，就可以忽略双引号中的逗号。
但是有一个问题，就是如果字符串尾部也有双引号的话，最后的双引号内的逗号会被分割，如下面字符串：

```python
import re

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,"22425172,test"'
b = re.split(r',\s*(?![^"]*\"\,)', a)
print(len(b))
print(b)

10
['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '"22425172', 'test"']
```

目前的解决办法是，在字符串后面加上`,`就可以让字符串尾部双引号内的逗号不被分割，但是这样分割出来的列表长度+1，列表最后一个元素为`''`

```python
import re

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,"22425172,test"'
a = a + ','
b = re.split(r',\s*(?![^"]*\"\,)', a)
print(len(b))
print(b)

10
['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '"22425172,test"', '']
```

## 使用csv模块的reader进行分割

```python
import csv

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,22425172'
b = [a]
reader = csv.reader(b, delimiter=',')
for row in reader:
    print(len(row))
    print(row)

9
['11-BETA-HSD3', '100174880', 'Anemia, Hemolytic', 'MESH:D000743', '', 'Water Pollutants, Chemical', '4.49', '', '22425172']
```

使用这个方法简单快速，其他的分隔符也可以使用

# csv

## 解析tsv文件

```shell
tsv和csv都是以纯文本文件存储的电子表格格式

TSV：用制表符分隔数据
CSV：用逗号分隔数据
```

## 读取tsv文件

```python
import csv

infile = r'./a.tsv'
with open(infile, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        # 返回一个列表的迭代，每一行都是一个列表
        for row in reader:
            print(row)
```

## 写入csv文件

```python
import csv

# 打开时加上newline='',防止写入数据每行都会增加一个空行
with open(r'a.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['mim_id', 'entrez_gene_id', 'name', 'ensembl_gene_id'])
```

## 以逗号分隔字符串,但忽略双引号内的逗号

以逗号分隔字符串,但忽略双引号内的逗号

```python
# Anemia, Hemolytic
a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,22425172'

# ['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '22425172']
```

### 使用正则re.split进行字符串分割

```python
import re

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,22425172'
b = re.split(r',\s*(?![^"]*\"\,)', a)
print(len(b))
print(b)

# 9
# ['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '22425172']
```

```python
r',\s*(?![^"]*\"\,)'

# \s表示匹配空白字符，*表示匹配前一个字符0次或者无数次,\s*即表示如果是,,会匹配为'',这样数据分割出来的列表长度一致，下标对应的字符串不会混乱
# (?![^"]*\"\,)表示匹配后面有"asg",的逗号，但是不匹配后面是asg",的逗号，重点是这个，分为两部分解释
# [^"]*\"\,在原始字符串模式下，表示匹配asdgdg",但是不匹配"asdgdg",
# 1(?!2)表示匹配13中的1,但是不匹配12中的1
```

如果字符串尾部也有双引号,最后的双引号内的逗号会被分割

```python
import re

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,"22425172,test"'
b = re.split(r',\s*(?![^"]*\"\,)', a)
print(len(b))
print(b)

# 10
# ['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '"22425172', 'test"']
```

```python
# 在字符串后面加上,可以让字符串尾部双引号内的逗号不被分割
# 但是这样分割出来的列表长度+1
import re

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,"22425172,test"'
a = a + ','
b = re.split(r',\s*(?![^"]*\"\,)', a)
print(len(b))
print(b)

# 10
# ['11-BETA-HSD3', '100174880', '"Anemia, Hemolytic"', 'MESH:D000743', '', '"Water Pollutants, Chemical"', '4.49', '', '"22425172,test"', '']
```

### 使用csv模块的reader进行分割

```python
import csv

a = '11-BETA-HSD3,100174880,"Anemia, Hemolytic",MESH:D000743,,"Water Pollutants, Chemical",4.49,,22425172'
b = [a]
reader = csv.reader(b, delimiter=',')
for row in reader:
    print(len(row))
    print(row)

# 9
# ['11-BETA-HSD3', '100174880', 'Anemia, Hemolytic', 'MESH:D000743', '', 'Water Pollutants, Chemical', '4.49', '', '22425172']
```

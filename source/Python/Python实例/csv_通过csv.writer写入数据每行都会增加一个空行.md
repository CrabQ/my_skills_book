# csv_通过csv.writer写入数据每行都会增加一个空行

```python
import csv
import sys

with open(sys.path[0] + '/1.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile,    fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '10001', 'name':'Mike', 'age': 20})


['id', 'name', 'age']
[]
['10001', 'Mike', '20']
[]
```

python关于CSV标准库的介绍中有写到:
> If csvfile is a file object, it should be opened with newline=''.

打开时加上`newline=''`即可：

```python
with open(sys.path[0] + '/1.csv' , 'w', newline='')
```

# csv_解析csv、tsv文件

## 解析tsv文件

tsv和csv都是以纯文本文件存储的电子表格格式

- TSV：tab separated values；即“制表符分隔值”，用制表符分隔数据
- CSV： comma separated values；即“逗号分隔值”，用逗号分隔数据

所以tsv文件可以用python的csv模块进行解析，只需指定分隔符即可。
> [csv](https://docs.python.org/3/library/csv.html#csv-fmt-params)

## 读取tsv文件

```python
import csv

infile = r'./all_gene_disease_pmid_associations.tsv'
with open(infile, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        # 返回一个列表的迭代，每一行都是一个列表
        for row in reader:
            print(row)
```

## 写入csv文件

```python
import csv

with open(r'C:/Users/CRAB/Desktop/ene.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['mim_id', 'entrez_gene_id', 'name', 'ensembl_gene_id'])
```

# openpyxl

新建,删除表

```python
import openpyxl
from openpyxl.styles import Alignment, PatternFill

# 新建Excel
book = openpyxl.Workbook()
# 新建表
sheet = self.book.create_sheet(sheet_name)
# 删除默认表
self.workbook.remove(self.workbook['Sheet'])
# 保存
self.book.save('a.xlsx')
```

设置单元格

```shell
# 值
sheet.['a1'].value = '123'
# 最新的一行写入
sheet.append([1,2,3,4])

# 设置单元格高,宽
sheet.['a1'].height = 30
sheet.['a1'].width = 20

# 居中
sheet.['a1'].alignment = Alignment(horizontal='center', vertical='center')

# 填充颜色
sheet.['a1'].fill = PatternFill("solid", fgColor="FFFF00")

# 合并单元格
sheet.merge_cells('a6:f6')

# 设置列宽
import string
s = workbook.create_sheet('a')
for i in string.ascii_lowercase:
    s.column_dimensions[i].width = 20
```

## 追加写入Excel

```python
import openpyxl

# 向excel中写入新的一条记录
def save_result_to_excel(data:dict, excel_name):
    # 不存在则创建excel
    if not os.path.exists(excel_name):
        wb = openpyxl.Workbook()
        sheet = wb[wb.sheetnames[0]]
        # 设置列宽
        sheet.column_dimensions['A'].width = 40.0
        sheet.column_dimensions['B'].width = 30.0
        sheet.column_dimensions['C'].width = 20.0

        cols = len(data.keys())
        for i in range(cols):
            sheet.cell(row=1, column=i+1).value = list(data.keys())[i]
            sheet.cell(row=2, column=i+1).value = list(data.values())[i][0]
    else:
        # 获取已存在的Excel
        wb = openpyxl.load_workbook(excel_name)
        sheet = wb[wb.sheetnames[0]]
        cols = len(data.keys())
        # 获取行数
        max_row = sheet.max_row
        for i in range(cols):
            sheet.cell(row=max_row+1, column=i+1).value = list(data.values())[i][0]
    # 最后保存
    wb.save(excel_name)
```

## 删除行

```python
import openpyxl
wb = openpyxl.load_workbook(filename='xxxxxx.xlsx')
ws = wb.active
# 通过迭代删除
for row in ws.iter_rows():
    if not row[0].value:
        continue
    if row[0].value % 5 == 0:
        ws.delete_rows(row[0].row)
wb.save(filename='yyyyyyy.xlsx')
wb.close()
```
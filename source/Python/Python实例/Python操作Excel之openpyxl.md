# Python操作Excel之openpyxl

新建,删除表

```python
import openpyxl
from openpyxl.styles import Alignment, PatternFill

# 新建Excel
book = openpyxl.Workbook()
# 新建表
sheet = self.book.create_sheet(sheet_name)
# 删除默认表
self.book.remove_sheet(self.book.get_sheet_by_name('Sheet'))
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
```

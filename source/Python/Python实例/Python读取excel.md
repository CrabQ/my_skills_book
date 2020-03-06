# Python读取excel

## xlrd读取excel

```python
import xlrd

def read_excel(infile):
    # 获取文件
    excel_file = xlrd.open_workbook(infile)
    # 获取sheet名
    print(excel_file.sheet_names())
    # ['array_list_new', 'Sheet1']

    # 获取sheet内容
    sheet = excel_file.sheet_by_index(0)
    # sheet = excel_file.sheet_by_name('array_list_new')
    print(sheet)
    # <xlrd.sheet.Sheet object at 0x0000029F479EAE10>

    # 获取sheet名称、行数、列数
    print(sheet.name, sheet.nrows, sheet.ncols)
    # array_list_new 514 13

    # 获取第三行和第二列的值
    rows = sheet.row_values(2)
    cols = sheet.col_values(1)
    # print(rows, cols)
```

## openpyxl追加写入Excel

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

## xlsxwriter写入xlsx文件

```python

import xlsxwriter
from xlsxwriter.exceptions import DuplicateWorksheetName

def write_excel(self, sheet, result):
    """
    向excel中写入数据
    :params sheet: 疾病名字，表名
    :params result: 数据列表
    """
    # excel文件路径
    infile = 'C:/Users/CRAB/Desktop/右边分类.xlsx'
    # 打开一个xlsx文件（如果打开的文件存在 ，则清空该文件，如果文件不存在，则新建）
    workbook = xlsxwriter.Workbook(infile)
    try:
        sheet = workbook.add_worksheet(sheet)
    # 避免重名
    except DuplicateWorksheetName:
        sheet = workbook.add_worksheet(sheet+'(1)')
    # 写入字段名
    field_name = ['id', 'disease_source', 'GeneSymbol', 'Disease', 'PubMed_ID', 'Sentence', 'judge', 'result']
    for i in range(len(field_name)):
        sheet.write(0, i, field_name[i])

    rows = len(result)
    cols = len(result[0])
    # print(rows, cols)
    for i in range(rows):
        for j in range(cols):
            # 第一行已写入字段名
            sheet.write(i+1, j, result[i][j])

    # 关闭excel文件
    workbook.close()
```

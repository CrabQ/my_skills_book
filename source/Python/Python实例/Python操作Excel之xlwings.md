# Python操作Excel之xlwings

```python
import xlwings as xw

if __name__ == '__main__':

    # 新建一个Excel
    wb = xw.Book()
    # 新建一个表,在最后插入
    sheet = self.book.sheets.add(sheet_name, after=self.book.sheets[-1])
    # 获取一个表
    sht = wb.sheets[0]
    # 修改表名
    sht.name = '新建表'

    # 设置整个表内所有表哥宽高
    sheet.cells.column_width = 15
    sheet.cells.row_height = 30
    # 居中
    sheet.cells.api.HorizontalAlignment = constants.HAlign.xlHAlignCenter

    # 写入数据
    # 如果写入二维数组,则二维数组内长度要一致
    # sht.range((1,1)).value = [1,2,3,4,5]
    sht.range((0,3)).value = [1,2,3,4,5]
    # 位置移动
    next_range = sheet.range('a2').offset(row_offset=1)

    # 删除默认表
    self.book.sheets['Sheet1'].delete()
    # 保存
    wb.save('./新建表.xlsx')
    # 关闭程序,一个应用程序对应一个Excel实例,所以要退出app,不然其他程序无法操作此excel表
    wb.app.quit()
```

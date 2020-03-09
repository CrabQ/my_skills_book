# Python操作Excel之xlwings

```python
import xlwings as xw

if __name__ == '__main__':

    # 新建一个Excel
    wb = xw.Book()
    # 新建一个表
    sht = wb.sheets[0]
    # 修改表名
    sht.name = '新建表'
    # 写入数据
    # sht.range((1,1)).value = [1,2,3,4,5]
    sht.range((0,3)).value = [1,2,3,4,5]
    # 保存
    wb.save('./新建表.xlsx')
    # 关闭程序,一个应用程序对应一个Excel实例,所以要退出app,不然其他程序无法操作此excel表
    wb.app.quit()
```

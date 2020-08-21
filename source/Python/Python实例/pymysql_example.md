# pymysql_example

插入数据

```python
import pymysql
db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()

data = {
    'id': '20120001',
    'name': 'Bob',
    'age': 21
}

table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
update = ','.join([" {key} = %s".format(key=key) for key in data])
sql += update
try:
    cursor.execute(sql, tuple(data.values())*2):
    db.commit()
    # 如下写法, 可能不会return, 使用发现正常插入数据, execute返回值会为0, 尚未找到答案
    # db.insert_id() 也是, 即使在db.commit()之前获取, 也可能是0, 尚未找到答案
    if cursor.execute(sql, tuple(data.values())*2):
        db.commit()
        return kw
except:
    print('Failed')
    db.rollback()
finally:
    cursor.close()
    db.close()
```

更新数据

```python
sql = 'UPDATE students SET age = %s WHERE name = %s'
try:
   cursor.execute(sql, (25, 'Bob'))
   db.commit()
except:
   db.rollback()
finally:
    db.close()
```

删除数据

```python
table = 'students'
condition = 'age > 20'

sql = 'DELETE FROM  {table} WHERE {condition}'.format(table=table, condition=condition)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
finally:
    db.close()
```

查询数据

```python
sql = 'SELECT * FROM students WHERE age >= 20'
try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    row = cursor.fetchone()
    while row:
        print('Row:', row)
        row = cursor.fetchone()
except:
    print('Error')
```

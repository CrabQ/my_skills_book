# pymongo实例

初始化

```python
import pymongo、

# 连接MongoDB
client = pymongo.MongoClient(host='localhost', port=27017)
# 指定数据库
db = client['test']

# 指定集合
collection = db['students']
```

插入数据

```python
# 单个插入
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
result = collection.insert_one(student)
print(result)
print(result.inserted_id)

# <pymongo.results.InsertOneResult object at 0x10d68b558>
# 5932ab0f15c2606f0c1cf6c5

# 多个插入
student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}

result = collection.insert_many([student1, student2])
print(result)
print(result.inserted_ids)

# <pymongo.results.InsertManyResult object at 0x101dea558>
# [ObjectId('5932abf415c2607083d3b2ac'), ObjectId('5932abf415c2607083d3b2ad')]
```

查询

```python
# 单个
result = collection.find_one({'name': 'Mike'})
print(type(result))
print(result)

# <class 'dict'>
# {'_id': ObjectId('5932a80115c2606a59e8a049'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}

# 多个
results = collection.find({'age': 20})
print(results)
for result in results:
    print(result)

# <pymongo.cursor.Cursor object at 0x1032d5128>
# {'_id': ObjectId('593278c115c2602667ec6bae'), 'id': '20170101', 'name': 'Jordan', 'age': 20, 'gender': 'male'}
# {'_id': ObjectId('593278c815c2602678bb2b8d'), 'id': '20170102', 'name': 'Kevin', 'age': 20, 'gender': 'male'}
# {'_id': ObjectId('593278d815c260269d7645a8'), 'id': '20170103', 'name': 'Harden', 'age': 20, 'gender': 'male'}


# 查询年龄大于 20 的数据
results = collection.find({'age': {'$gt': 20}})

# 查询名字以 M 开头的学生数据
results = collection.find({'name': {'$regex': '^M.*'}})
```

统计

```python
# 统计符合某个条件的数据
count = collection.find({'age': 20}).count()
```

排序

```python
#  pymongo.ASCENDING 指定升序，如果要降序排列可以传入 pymongo.DESCENDING。
results = collection.find().sort('name', pymongo.ASCENDING)
```

偏移

```python
# 忽略前 2 个元素，得到第三个及以后的元素
results = collection.find().sort('name', pymongo.ASCENDING).skip(2)
# 指定要取的结果个数
results = collection.find().sort('name', pymongo.ASCENDING).skip(2).limit(2)
```

更新

```python
# 将 name 为 Kevin 的数据的年龄进行更新，首先指定查询条件，然后将数据查询出来，修改年龄

# 单个
condition = {'name': 'Kevin'}
student = collection.find_one(condition)
student['age'] = 26
result = collection.update_one(condition, {'$set': student})
print(result)
print(result.matched_count, result.modified_count)

# <pymongo.results.UpdateResult object at 0x10d17b678>
# 1 0

# 多个
condition = {'age': {'$gt': 20}}
result = collection.update_many(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)

# <pymongo.results.UpdateResult object at 0x10c6384c8>
# 3 3
```

删除

```python
result = collection.delete_one({'name': 'Kevin'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$lt': 25}})
print(result.deleted_count)

<pymongo.results.DeleteResult object at 0x10e6ba4c8>
1
4
```

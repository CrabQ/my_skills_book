# MongoDB基础

## 增删查改

```sql
-- 切换数据库,如果数据库不存在，则指向数据库，但不创建，直到插入数据或创建集合时数据库才被创建
use old

-- 查看当前数据库名称
db

-- 查看所有数据库名称(列出所有在物理上存在的数据库)
show dbs

-- 删除当前指向的数据库
db.dropDatabase()

-- 集合创建
-- db.createCollection(name, options)
db.createCollection('test')
-- { "ok" : 1 }
-- 或者直接db.test

-- 查看当前数据库的集合
show collections

-- 删除集合
-- db.集合名称.drop()
db.test.drop()
```

插入

```sql
-- 插入一条数据
db.test.insertOne({'name':'xiaolv', 'age':53})

-- 插入多条数据
db.test.insertMany([{'name':'ming', 'age':43}, {'name':'hong', 'age':23}])
```

查询

```sql
-- 查询全部
db.test.find()

-- 查询某条数据
db.test.findOne({'name':'hong'})
```

更新

```sql
db.集合名称.update(
   <query>,
   <update>,
   {multi: <boolean>}
)
-- 参数query:查询条件，类似sql语句update中where部分
-- 参数update:更新操作符，类似sql语句update中set部分
-- 参数multi:可选，默认是false，表示只更新找到的第一条记录，值为true表示把满足条件的文档全部更新

db.test.updateOne({'name':'hong'}, {$set:{'age':10}})
-- 无对应属性会直接生成
db.test.updateMany({'age':10}, {$set:{'name':'huang'}})
```

保存

```sql
-- db.集合名称.save(document)
db.stu.save({_id:'20160102','name':'yk',gender:1})
```

删除

```sql
-- 参数query:可选，删除的文档的条件
-- 参数justOne:可选，如果设为true或1，则只删除一条，默认false，表示删除多条

db.test.remove(
    {'name':'xiaoan'},
    {justone:true}
)

-- 清空数据库
db.test.remove({})
```

## 运算符

```sql
-- 大于或者等于
db.test.find({'age':{$gte:43}})

-- 小于
db.test.find({'age':{$lt:30}})
```

## 修改器

```sql
-- $inc, age为10的第一条数据age-5
db.test.updateOne({'age':10},{$inc:{'age':-5}})

-- $set
db.test.updateOne({'name':'ming'}, {$set:{'sex':'male'}})

-- $unset 删除Key(field)
db.test.updateOne({'name':'ming'}, {$unset:{'sex':'male'}})

-- $push 在Array尾端加入一个新元素
-- db.test.updateMany({}, {$set:{'t_list':[1,2,4,5]}})
db.test.updateOne({'name':'ming'}, {$push:{'t_list':6}})

-- $pull 指定删除Array中的某一个元素,全删
db.test.updateOne({'name':'ming'}, {$pull:{'t_list':6}})

-- $pop 指定删除Array中的第一个或最后一个元素
-- 1表示最后一个, -1表示第一个
db.test.updateOne({'name':'ming'}, {$pop:{'t_list':1}})

-- $ 当做array下标
db.test.updateOne({'name':'huang', 't_list':4}, {$set:{'t_list.$':8}})
```

## 先排序再跳过最后选取

```sql
-- limit, 选取前2
db.test.find().limit(2)

-- skip, 跳过前2
db.test.find().skip(2)

-- 排序, 1 升序, -1 降序
db.test.find().sort({'age':1})

-- 一定是先排序再跳过最后选取
db.test.find().sort({'age':1}).limit(2).skip(1)
```

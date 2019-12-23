# Mongo实例

查看当前数据库名称

```sql
db
```

查看所有数据库名称(列出所有在物理上存在的数据库)

```sql
show dbs
```

切换数据库,如果数据库不存在，则指向数据库，但不创建，直到插入数据或创建集合时数据库才被创建

```sql
use images360
```

删除当前指向的数据库

```sql
db.dropDatabase()
```

集合创建

```sql
# db.createCollection(name, options)
db.createCollection('test')

{ "ok" : 1 }
```

查看当前数据库的集合

```sql
show collections

images360
test
```

删除集合

```sql
# db.集合名称.drop()
db.test.drop()

true
```

插入

```sql
# db.集合名称.insert(document)
db.test.insert({'name':'xiaolv'})

WriteResult({ "nInserted" : 1 })
```

简单查询
```sql
# db.集合名称.find()
db.test.find()

{ "_id" : ObjectId("5cb93ad6dd3b1a3c7a66ca42"), "name" : "xiaoming" }
```

全文档更新

```sql
db.集合名称.update(
   <query>,
   <update>,
   {multi: <boolean>}
)
# 参数query:查询条件，类似sql语句update中where部分
# 参数update:更新操作符，类似sql语句update中set部分
# 参数multi:可选，默认是false，表示只更新找到的第一条记录，值为true表示把满足条件的文档全部更新

db.test.update(
    {'name':'xiaowang'},
    {'name':'xiaohong'}
)
```

指定属性更新，通过操作符$set

```sql
db.test.update(
    {'name':'xiaowang'},
    {$set:{'name':'xiaoan'}}
)

WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```

修改多条匹配到的数据

```sql
db.stu.update({},{$set:{gender:0}},{multi:true})
```

保存

```sql
db.集合名称.save(document)
db.stu.save({_id:'20160102','name':'yk',gender:1})
```

删除

```sql
db.集合名称.remove(
   <query>,
   {
     justOne: <boolean>
   }
)

# 参数query:可选，删除的文档的条件
# 参数justOne:可选，如果设为true或1，则只删除一条，默认false，表示删除多条

db.test.remove(
    {'name':'xiaoan'},
    {justone:true}
)

WriteResult({ "nRemoved" : 1 })
```

全部删除

```sql
db.test.remove({})
```

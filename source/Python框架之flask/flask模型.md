# flask模型

## 安装

```shell
pip install pymysql flask-script flask-migrate flask-sqlalchemy
```

## 使用

```python
# 数据库配置
# settings.py
class Config:
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATADASE_URL = 'mysql_pymysql://root:root@127.0.0.1:3306/flask_db'
```

```shell
# 数据库迁移
python app.py db init
python app.py db migrate
python app.py db upgrade
```

## orm

```python
# 所有
User.query.all()

# 一个
User.query.get(pk)

# 过滤
User.query.filter

# 过滤之字符串
User.username.startswith('')
User.username.endswith('')
User.username.contains('')
User.username.like('')
User.username.in_('')
User.username == 'zzz

# 过滤之整型,日期类型
User.age.__lt__(18)
User.create_time.__ge__('2020-09-01')
User.age.between(1,18)

# 多个条件
from sqlarchemy import 
and_ or_ not_

# 排序
# 升序
order_by('id')
# 倒序
order_by(-User.id)

# 跳过两条获取两条
User.query.offset(2).limit(2).all()
```

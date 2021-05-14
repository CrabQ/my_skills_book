# flask模型

## 安装

```python
# 1. 项目启动脚本命令
# pip install flask-script
from flask_script import Manager

# app = Flask(__name__, template_folder='../template', static_folder='../static')
manager = Manager(app=app)

if __name__ == '__main__':
    manager.run()


# 2. ORM
# pip install pymysql flask-sqlalchemy
# 2.1 配置
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flask_study'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

# 2.2 关联
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# app = Flask(__name__, template_folder='../template', static_folder='../static')
db.init_app(app)

# 3. 数据库同步命令
# pip install flask-migrate
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(db=db, app=app)
manager.add_command('db', MigrateCommand)
```

## 使用

```shell
# 项目初始化(只需执行一次)
python app.py db init
# 迁移
python app.py db migrate
# 同步
python app.py db upgrade

# 每次修改model, 先迁移后同步
```

## orm

```python
# 所有
User.query.all()

# 一个
User.query.get(pk)

# 过滤
User.query.filter
# 模型类.query.filter(模型.字段 == 值)
# 模型类.query.filter_by(字段 = 值)

# 过滤之字符串
User.username.startswith('')
User.username.endswith('')
User.username.contains('')
User.username.like('')
User.username.in_(['', ''])
User.username == 'zzz

# 过滤之整型,日期类型
User.age.__lt__(18)
User.create_time.__ge__('2020-09-01')
User.age.between(1,18)

# 多个条件
from sqlarchemy import and_, or_, not_
# user_list = User.query.filter(or_(User.username.like('z%'), User.username.contains('i'))).all()

# 排序
# 升序
order_by('id')
# 倒序, 写法:-模型类.字段名
order_by(-User.id)

# 跳过两条获取两条
User.query.offset(2).limit(2).all()


# 增
User = User()
user.xx=xx
db.session.add(user)
db.session.commit()

# 删
user=User.query.get(id)
db.session.delete(user)
db.session.commit()

# 改
user=User.query.get(id)
user.xx=xx
db.session.commit()
```
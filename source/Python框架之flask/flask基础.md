# flask基础

## 基础

```python
from flask import Flask
from flask import redirect
from flask  import render_template
from flask import request

# 实例化Flask对象APP
app = Flask(__name__)

# app中的route装饰器
@app.route('/')
def index(): # 视图函数
    return 'hello world'

@app.route('/home')
def home():
    # 跳转
    return redirect('/')

@app.route('/hi', methods=['get', 'POST'])
def hi():
    # 请求方式
    print(request.method)
    # POST

    # 表单数据
    print(request.form)
    # ImmutableMultiDict([('user', 'a'), ('password', 'b')])

    print(request.form.get('user'))
    # a

    # url参数, http://127.0.0.1:5000/hi?id=1&user=lv
    print(request.args)
    # ImmutableMultiDict([('id', '1'), ('user', 'lv')])

    # to_dict之后获取form和url中的数据, key同名的话form中的会被覆盖
    print(request.values.to_dict())

    print(request.cookies)
    # ImmutableMultiDict([('csrftoken', 'NrHiFQTUGa0LTTHvEcIVqLCsnDYGOyxo7LiOiwt4wr6xPM3LVLNeEgPBMJfLjxNw')])

    print(request.headers)

    # 获取上传文件
    print(request.files)


    # 与django不同, 字典需要打散, **dict, flask参数依次传递
    return render_template('hi.html', name='rookie', sex='male')

if __name__ == '__main__':
    # 启动web服务
    app.run('0.0.0.0', 5000, debug=True)

```

## 模板语言Jinjia2以及render_template

### Markup封装HTML标签

```python
from flask import Markup

@app.route('/hi', methods=['get', 'POST'])
def hi():
    tag = "<input type='text' name='user' value='hi'>"
    tag = Markup(tag)
    return render_template('hi.html', tag=tag)
```

### 模板执行函数

```python
def sum(a, b):
    return a + b

@app.route('/hi', methods=['get', 'POST'])
def hi():
    # 前端用法: {{ tag(1,2) }}
    return render_template('hi.html', tag=sum)
```

### 全局函数,无需后端传递给前端

```python
@app.template_global()
def sum_two(a, b):
    return a + b

# 过滤器
@app.template_filter()
def sum_three(a, b, c):
    return a + b + c


@app.route('/hi', methods=['get', 'POST'])
def hi():
    # 前端用法: {{ sum_two(1,2) }}, {{ 1 | sum_three(2,3) }}
    return render_template('hi.html', )
```

### block与include

与Django用法一致

## session

不安全, 不建议使用

```python
from flask import Flask
from flask import redirect
from flask import render_template
from flask import session

app = Flask(__name__)
# 加密字符串
app.secret_key = 'sldjglsjgljsldjglsjl'

@app.route('/')
def index():
    session['hi'] = 'hello'
    return redirect('/hi')


@app.route('/hi')
def hi():
    if session.get('hi') == 'hello':
        return render_template('hi.html')
    else:
        return 'error'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
```

## 路由系统

```python
from flask import Flask
from flask import  request
from flask import redirect
from flask import render_template
from flask import url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

app.config['SERVER_NAME'] = 'a.com'
# defaults 视图函数的参数默认值
# endpoint 反向路由解析
# strict_slashes=True url结尾不能是/
# redirect_to 直接跳转不经过视图函数
# subdomain : 子域名前缀, hi.a.com
@app.route('/hi/<int:id>', endpoint='hello', defaults={'nid':1}, strict_slashes=True, redirect_to='/', subdomain='hi')
def hi(nid, id):
    print(url_for('hello', id=100))
    print(nid)
    print(id)
    return render_template('hi.html')


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

```

## Flask配置

```python
# 修改配置有两种方式

# 1. 直接修改
app.config["DEBUG"] = True

# 2. 使用类的方式导入
# settings.py
class FlaskSetting:
    DEBUG = True
    SECRET_KEY = "DragonFire"

# flask文件中导入
app.config.from_object("settings.FlaskSetting")
```

### 实例化配置

```python
app = Flask(__name__, static_folder='static', static_url_path=None, template_folder='templates')
# static_folder 静态文件目录的路径 默认当前项目中的static目录
# static_url_path  静态文件目录的url路径 默认不写是与static_folder同名,远程静态文件时复用
# template_folder  template模板目录, 默认当前项目中的 templates 目录
```

### 蓝图, BluePrint

相当于Django中的app,独立功能

```python
# 蓝图文件bp.py
from flask import Blueprint

bp = Blueprint('bp', __name__)

@bp.route('/bp')
def index():
    return 'hi, bp'

# flask启动文件
from flask import Flask
from bp import bp

app = Flask(__name__)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
```

## before_request与after_request

```python
from flask import Flask
from flask import request, session, redirect

app = Flask(__name__)

# @app.before_request 在请求(request)进入视图函数之前执行
# @app.before_first_request 只执行一次
# @app.after_request 在响应(response)返回客户端之前执行,结束视图函数之后
@app.before_request
def is_login():
    if request.path == '/login':
        return None
    if not session.get('user'):
        return redirect('/login')

@app.route('/login')
def login():
    return 'login'

@app.route('/home')
def home():
    return 'home'

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
```

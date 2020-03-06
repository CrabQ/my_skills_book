# virtualenv和virtualenvwrapper

## 安装virtualenv

```shell
pip3 install virtualenv
```

创建目录

```shell
mkdir myproject
cd myproject/
myproject $
```

创建一个独立的Python运行环境，命名为venv

```shell
myproject $ virtualenv virtualenv spider_env --no-site-packages venv
# Using base prefix '/usr/local/.../Python.framework/Versions/3.4'
# New python executable in venv/bin/python3.4
# Also creating executable in venv/bin/python
# Installing setuptools, pip, wheel...done.
```

命令virtualenv就可以创建一个独立的Python运行环境，我们还加上了参数--no-site-packages，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。

新建的Python环境被放到当前目录下的venv目录。有了venv这个Python环境，可以用source进入该环境：

```shell
myproject $ source venv/bin/activate
(venv)myproject $
# windows下
spider_env\Scripts\activate
```

注意到命令提示符变了，有个(venv)前缀，表示当前环境是一个名为venv的Python环境。

在venv环境下，用pip安装的包都被安装到venv这个环境下，系统Python环境不受任何影响。也就是说，venv环境是专门针对myproject这个应用创建的。

退出当前的venv环境，使用deactivate命令：

```shell
(venv)myproject $ deactivate
```

此时就回到了正常的环境，现在pip或python均是在系统Python环境下执行。

完全可以针对每个应用创建独立的Python运行环境，这样就可以对每个应用的Python环境进行隔离。

virtualenv是如何创建“独立”的Python运行环境的呢？原理很简单，就是把系统Python复制一份到virtualenv的环境，用命令source venv/bin/activate进入一个virtualenv环境时，virtualenv会修改相关环境变量，让命令python和pip均指向当前的virtualenv环境。

## 安装virtualenvwrapper

```shell
# 依赖 virtualenv
pip3 install virtualenvwrapper-win
```

win10中，添加系统环境变量 WORKON,指向 path/dir  (自己想要的虚拟环境目录位置)

```shell
# 变量名
WORKON_HOME
# 变量值
D:\program\program_code\python36_virtualenv_home
```

linux

```shell
# 把下面两行代码添加到 ~/.bashrc文件中

vim ~/.bashrc

export WORKON_HOME=~/envs
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
export VIRTUALENVWRAPPER_PYTHON=/usr/local/python/bin/python3.6
# 指定virtualenv的路径
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/python/bin/virtualenv
source /usr/local/python/bin/virtualenvwrapper.sh

读取文件，生效
source ~/.bashrc
```

使用

```shell
# 创建一个干净的虚拟环境
mkvirtualenv my_spider
# 查看环境
workon
# 进入/切换环境
workon my_spider
# 退出当前环境
deactivate
# 删除环境
rmvirtualenv my_spider
```

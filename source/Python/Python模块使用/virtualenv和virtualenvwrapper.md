# virtualenv和virtualenvwrapper

## 安装使用virtualenv

### 安装

```shell
pip3 install virtualenv
```

### 使用

```shell
# 创建目录
mkdir myproject
cd myproject/

# 创建一个独立的Python运行环境，命名为spider_env
myproject $ virtualenv spider_env --no-site-packages

# 切换环境
myproject $ source spider_env/bin/activate
(spider_env)myproject $

# windows下
spider_env\Scripts\activate

# 退出当前的venv环境
(spider_env)myproject $ deactivate
```

## 安装virtualenvwrapper

```shell
# 依赖 virtualenv
pip3 install virtualenvwrapper-win
```

### win

```shell
# 添加系统环境变量
WORKON_HOME  D:\program\program_code\python36_virtualenv_home
```

### linux

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

## virtualenvwrapper使用

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

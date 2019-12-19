# sphinx+Git+readthedocs环境搭建
## sphinx
安装sphinx
```python
pip install sphinx
```
新建路径,创建项目
```python
cd my_skills_book
sphinx-quickstart
```
安装主题
```python
pip install sphinx_rtd_theme
```
修改配置文件
```python
# source/conf.py

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
```
个人习惯使用markdown,添加markdown支持
> [recommonmark](https://github.com/readthedocs/recommonmark)
```python
pip install recommonmark
```
修改配置文件,添加扩展,文件关联
```python
# source/conf.py

extensions = [
    'recommonmark',
]

source_suffix = ['.rst', '.md']
```
修改索引,添加二级索引
```python
# source/index.rst

# 修改toctree,添加sphinx
.. toctree::
   :maxdepth: 2
   :glob:

   sphinx/index

```
创建二级索引
```python
# 创建文件 source/sphinx/index.rst
# 添加索引
sphinx
==========

.. toctree::
   :maxdepth: 2
   :glob:

   sphinx

```
创建sphinx文件,开始进行文档编写
```python
# source/sphinx/sphinx.md
```
## Git
初始化git仓库,添加文件`.gitignore`并推送到github
> [托管到github.md](../Git/托管到github.md)
```python
# .gitignore

_build/*
build/*
```

## readthedocs
注册帐号,关联github,直接import项目
```python
# 如果readthedocs build的过程报错: contents.rst not found
# source/conf.py,配置文件添加如下内容
master_doc = 'index'
```
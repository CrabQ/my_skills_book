# python文件打包

## 使用pyinstaller打包

输出配置文件.spec文件,进行自定义配置

```python
pyi-makespec-w server.py
# -w 不生成黑色控制台窗口
```

修改配置,添加资源

```python
# 修改Analysis的datas,添加当前路径下的models文件夹
# server.spec
a = Analysis(['server.py'],
             datas=[('./models', 'models')],
)
```

打包

```python
pyinstaller server.spec
```

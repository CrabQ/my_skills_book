# pyinstaller

```shell
-F 打包成一个exe文件
-D 创建目录，包含exe和依赖
-c 使用控制台
-w 使用窗口

pyinstaller -D -w start.py
```

## 使用pyinstaller打包

输出.spec文件,进行自定义配置

```shell
pyi-makespec -w server.py
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

```shell
pyinstaller server.spec
```

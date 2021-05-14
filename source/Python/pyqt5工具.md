# pyqt5工具

pycharm添加外部工具

```shell
# 1. settings 搜索 external tools

# 2. 添加一个新的
# name:Qt Designer_3.8
# program:D:\program\program_code\miniconda3\envs\qt5\Lib\site-packages\PySide2\designer.exe
# working directory:$ProjectFileDir$

# name:pyuic_3.8
# program:D:\program\program_code\miniconda3\envs\qt5\Scripts\pyuic5.exe
# arguments:$FileName$ -o $FileNameWithoutExtension$_ui.py -x
# working directory:$FileDir$

# name:pyrcc5_3.8
# program:D:\program\program_code\miniconda3\envs\qt5\Scripts\pyrcc5.exe
# arguments:$FileName$ -o $FileNameWithoutExtension$_rc.py
# working directory:$FileDir$
```

转换

```shell
# ui转换为py文件
pyuic5.exe test.ui -o test.py

# -x 添加main函数
pyuic5.exe test.ui -o test.py -x

# 转换资源文件
pyrcc5.exe test.qrc -o test_rc.py
```

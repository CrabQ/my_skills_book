# PYQT5

## 环境安装

```shell
# 新建环境
conda create -n qt5 python==3.8.3

# 安装pyqt5, PySide2
pip install PyQt5==5.15.1
pip install PySide2==5.15.1
```

测试是否安装成功

```python

from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("软件名称")
window.resize(600,500)

btn = QPushButton(window)
btn.setText("按钮")
btn.resize(120, 30)
btn.move(100, 100)
btn.setStyleSheet('background-color:green;font-size:16px;')

label =QLabel(window)
label.setText('标签')
label.setStyleSheet('background-color:green;font-size:16px;')
# label.show()
window.show()

sys.exit(app.exec_())


# 面对对象
from PyQt5.Qt import *
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()  # 调用父类QWidget中的init方法
        self.setWindowTitle("软件名称")
        self.resize(600, 500)
        self.func_list()

    def func_list(self):
        self.func()

    def func(self):
        btn = QPushButton(self)
        btn.setText("软件内容")
        btn.resize(120, 30)
        btn.move(100, 100)
        btn.setStyleSheet('background-color:green;font-size:20px;')


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个应用程序对象
    # sys.argv可以接收用户命令行启动时所输入的参数，根据参数执行不同程序
    # qApp 为全局对象
    print(sys.argv)
    print(app.arguments())
    print(qApp.arguments())
    # 以上三个输出结果是一样的
    window = Window()

    window.show()
    sys.exit(app.exec_())  # 0是正常退出
    # app.exec_()  进行循环
    # sys.exit()   检测退出原因
```

报错

```shell
# 报错no qt platform plugin could be initialized
# 添加环境变量
# QT_QPA_PLATFORM_PLUGIN_PATH
# D:\program\program_code\miniconda3\envs\qt5\Lib\site-packages\PyQt5\Qt\plugins\platforms
```

# 基础

```python
from PyQt5.Qt import *  # 主要包含了我们常用的一些类, 汇总到了一块
import sys


# 1. 创建一个应用程序对象
app = QApplication(sys.argv)
# print(app.arguments())
# print(qApp.arguments())


# 2. 控件的操作
# 创建控件,设置控件(大小,位置,样式...),事件,信号的处理
# 2.1 创建控件
# 当我们创建一个控件之后, 如果说,这个控件没有父控件, 则把它当做顶层控件(窗口)
# 系统会自动的给窗口添加一些装饰(标题栏), 窗口控件具备一些特性(设置标题,图标)
window = QWidget()

# 2.2 设置控件
# window.setText("hello")
window.setWindowTitle("hello")
window.resize(400, 400)

# 控件也可以作为一个容器(承载其他的控件)
label = QLabel(window)
label.setText("xxx")
label.setWindowTitle("xxxxxxx")
label.move(100, 50)
# label.show()

# 2.3 展示控件
# 刚创建好一个控件之后,(这个控件没有什么父控件), 默认情况下不会被展示,只有手动的调用show()才可以
# 如果说这个控件, 有父控件的,那么一般情况下, 父控件展示之后, 子控件会自动展示
window.show()


# 3. 应用程序的执行, 进入到消息循环
# 让整个程序开始执行,并且进入到消息循环(无限循环)
# 检测整个程序所接收到的用户的交互信息
sys.exit(app.exec_())
```

### QObject

```python
# QObject:所有的Qt对象的基类

from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject的学习")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        self.func()

    def func(self):
        obj = QObject()
        obj.setObjectName("notice")
        print(obj.objectName())

        obj.setProperty("notice_level", "error")
        obj.setProperty("notice_level2", "warning")

        print(obj.property("notice_level"))
        print(obj.dynamicPropertyNames())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
```

QObject-API

```python
obj = QObject()
# 给一个Qt对象设置一个名称,一般这个名称是唯一的，当做对象的ID来使用
obj.setObjectName("notice")
# 获取一个Qt对象的名称
print(obj.objectName())
# notice

# 给一个Qt对象动态的添加一个属性与值
obj.setProperty("notice_level", "error")
obj.setProperty("notice_level2", "warning")

print(obj.property("notice_level"))
# error

# 获取一个对象中所有通过setProperty()设置的属性名称
print(obj.dynamicPropertyNames())
# [PyQt5.QtCore.QByteArray(b'notice_level'), PyQt5.QtCore.QByteArray(b'notice_level2')]
```

父子对象

```python
obj0 = QObject()
obj1 = QObject()
obj2 = QObject()

# 设置父对象,只能一个
obj1.setParent(obj0)
obj2.setParent(obj0)
obj2.setObjectName("2")

# 获取父对象
print(obj1.parent())
# <PyQt5.QtCore.QObject object at 0x0000022264689670>

# 获取所有直接子对象
print(obj0.children())

# 获取某一个指定名称和类型的子对象, (QObject, 名称， 查找选项)
# 查找选项 Qt.FindChildrenRecursively：默认递归查找； Qt.FindDirectChildrenOnly：只查找直接子对象
print(obj0.findChild(QObject, "2", Qt.FindDirectChildrenOnly))

# 获取某多个指定名称和类型的子对象，参数同findChild
print(obj0.findChildren(QObject))
```

信号

```python
self.obj = QObject()
def destroy_cao(obj):
    print("对象被释放了", obj)

# widget.信号.connect(槽)，连接信号与槽
self.obj.destroyed.connect(destroy_cao)

del self.obj

# objectNameChanged

# obj.disconnect()  取消连接信号与槽
self.obj.objectNameChanged.disconnect()

# widget.blockSignals(bool) 临时（取消）阻止指定控件所有的信号与槽的连接
self.obj.blockSignals(True)

# widget.signalsBlocked()   信号是否被阻止
self.obj.signalsBlocked()

# widget.receivers(信号) 返回连接到信号的接收器数量
self.obj.receivers(self.obj.objectNameChanged)
```

类型判定

```python
# 是否是控件类型
obj.isWidgetType()

# 一个对象是否继承（直接或者间接）自某个类
obj.inherits("QWidget")
```

对象删除

```python
# obj.deleteLater()
# 删除一个对象时, 也会解除它与父对象之间的关系,deleteLater()并没有将对象立即销毁，而是向主消息循环发送了一个event，下一次主消息循环收到这个event之后才会销毁对象
```

定时器

```python
# startTimer(ms, Qt.TimerType) -> timer_id  开启一个定时器
# Qt.TimerType：
#   Qt.PreciseTimer:精确定时器：尽可能保持毫秒准确
#   Qt.CoarseTimer:粗定时器：5%的误差间隔
#   Qt.VeryCoarseTimer：很粗的定时器：只能到秒级
# timer_id：定时器的唯一标识

# 根据定时器ID，杀死定时器
# killTimer(timer_id)

# timerEvent()
# 定时器执行事件

from PyQt5.Qt import *
import sys

class MyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText("10")
        self.move(100, 100)
        self.setStyleSheet("font-size: 22px;")

    def setSec(self, sec):
        self.setText(str(sec))

    def startMyTimer(self, ms):
        self.timer_id = self.startTimer(ms)

    def timerEvent(self, *args, **kwargs):
        current_sec = int(self.text())
        current_sec -= 1
        self.setText(str(current_sec))

        if current_sec == 0:
            self.killTimer(self.timer_id)

app = QApplication(sys.argv)
window = QWidget()
window.resize(500, 500)

label = MyLabel(window)
label.setSec(5)
label.startMyTimer(500)

window.show()
sys.exit(app.exec_())
```

### QWidget

所有的可视控件的基类，是一个最简单的空白控件，没有父控件的控件, 称之为窗口

大小位置

```python
# 设置部分：
window = QWidget()

# 操控的是x, y；也就是pos，包括窗口框架
window.move(200, 100)

# 操控的是宽高，不包括窗口框架
window.resize(500, 500)

# 设置固定尺寸
window.setFixedSize(500, 500)

# 根据内容自适应大小
window.adjustSize(500, 500)

# 此处参照为用户区域
window.setGeometry(0, 0, 150, 150)

# 设置最小宽度
window.setMinimumWidth(500)
# 设置最大宽度
window.setMaximumWidth(800)
# 设置最小尺寸
window.setMinimumSize(200, 200)
# 设置最大尺寸
window.setMaximumSize(500, 500)



# 获取部分
# 相对于父控件的x位置，顶层控件（没有父控件）则相对于桌面的x位置
window.x()

# 相对于父控件的y位置，顶层控件（没有父控件）则相对于桌面的y位置
window.y()

# x和y的组合
window.pos()

# 控件的宽度，不包含任何窗口框架
window.width()

# 控件的高度，不包含任何窗口框架
window.height()

# width和height的组合
window.size()

# 用户区域相对于父控件的位置和尺寸组合
window.geometry()

# 0, 0, width, height的组合
window.rect()

# 框架大小
window.frameSize()

# 框架尺寸
window.frameGeometry()
```

内容边距

```python
label = QLabel(window)
label.resize(300, 300)
label.setStyleSheet("background-color: cyan;")

# 设置内容边距,setContentsMargins(左, 上, 右, 下)
label.setContentsMargins(100, 200, 0, 0)

# 获取内容边距
label.getContentsMargins()

# 获取内容区域
label.contentsRect()
```

鼠标相关

```python
# 设置鼠标形状
setCursor()

# 重置形状
unsetCursor()

# 鼠标跟踪,判定是否设置了鼠标跟踪
hasMouseTracking()

# 设置鼠标是否跟踪
setMouseTracking(bool)
# 不跟踪,鼠标移动时，必须处于按下状态，才会触发mouseMoveEvent事件
# 跟踪,鼠标移动时，不处于按下状态，也会触发mouseMoveEvent事件

# 自定义鼠标，QCursor对象
pixmap()
pos()
setPos(x, y)
```

事件消息

```shell
显示和关闭事件
  showEvent(QShowEvent)
    控件显示时调用

  closeEvent(QCloseEvent)
    控件关闭时调用

移动事件
  moveEvent(QMoveEvent)
    控件移动时调用

调整大小
  resizeEvent(QResizeEvent)
    控件调整大小时调用

鼠标事件
  进入和离开事件
    enterEvent(QEvent)
      鼠标进入时触发

    leaveEvent(QEvent)
      鼠标离开时触发

  mousePressEvent(QMouseEvent)
    鼠标按下时触发

  mouseReleaseEvent(QMouseEvent)
    鼠标释放时触发

  mouseDoubleClickEvent(QMouseEvent)
    鼠标双击时触发

  mouseMoveEvent(QMouseEvent)
    鼠标按下后移动时触发
    setMouseTracking(True)
      追踪设置后
      没有按下的移动也能触发

键盘事件
  keyPressEvent(QKeyEvent)
    键盘按下时调用

  keyReleaseEvent(QKeyEvent)
    键盘释放时调用

焦点事件
  focusInEvent(QFocusEvent)
    获取焦点时调用

  focusOutEvent(QFocusEvent)
    失去焦点时调用

拖拽事件
  dragEnterEvent(QDragEnterEvent)
    拖拽进入控件时调用

  dragLeaveEvent(QDragLeaveEvent)
    拖拽离开控件时调用

  dragMoveEvent(QDragMoveEvent)
    拖拽在控件内移动时调用

  dropEvent(QDropEvent)
    拖拽放下时调用

绘制事件
  paintEvent(QPaintEvent)
    显示控件, 更新控件时调用

改变事件
  changeEvent(QEvent)
    窗体改变, 字体改变时调用

右键菜单
  contextMenuEvent(QContextMenuEvent)
    访问右键菜单时调用

输入法
  inputMethodEvent(QInputMethodEvent)
    输入法调用
```

```python

from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("事件消息的学习")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        pass

    def showEvent(self, QShowEvent):
        print("窗口被展示了出来")

    def closeEvent(self, QCloseEvent):
        print("窗口被关闭了")

    def moveEvent(self, QMoveEvent):
        print("窗口被移动了")

    def resizeEvent(self, QResizeEvent):
        print("窗口改变了尺寸大小")

    def enterEvent(self, QEvent):
        print("鼠标进来了")
        self.setStyleSheet("background-color: yellow;")

    def leaveEvent(self, QEvent):
        print("鼠标移开了")
        self.setStyleSheet("background-color: green;")

    def mousePressEvent(self, QMouseEvent):
        print("鼠标被按下")

    def mouseReleaseEvent(self, QMouseEvent):
        print("鼠标被释放")

    def mouseDoubleClickEvent(self, QMouseEvent):
        print("鼠标双击")

    def mouseMoveEvent(self, QMouseEvent):
        print("鼠标移动了")

    def keyPressEvent(self, QKeyEvent):
        print("键盘上某一个按键被按下了")

    def keyReleaseEvent(self, QKeyEvent):
        print("键盘上某一个按键被释放了")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())

```

父子关系

```shell
API
  childAt(x, y)
    获取在指定坐标的控件

  parentWidget()
    获取指定控件的父控件

  childrenRect()
    所有子控件组成的边界矩形
```

层级控制

```shell
同级控件API
  lower()
    将控件降低到最底层

  raise_()
    将控件提升到最上层

  a.stackUnder(b)
    让a放在b下面
```

顶层窗口相关

```python
API
  图标
    setWindowIcon(QIcon("resource/header_icon.png"))
    windowIcon()

  标题
    setWindowTitle("xxxx")
    windowTitle()

  不透明度
    setWindowOpacity(float)
    windowOpacity()

  窗口状态
    setWindowState(state)
      Qt.WindowNoState
        无状态

      Qt.WindowMinimized
        最小化

      Qt.WindowMaximized
        最大化

      Qt.WindowFullScreen
        全屏

      Qt.WindowActive
        活动窗口

    windowState()

  最大化最小化
    控制
      showFullScreen()
        全屏显示
          不包含窗口框架

      showMaximized()
        最大化
          包括窗口框架

      showMinimized()
        最小化

      showNormal()
        正常

    判定
      isMinimized()
        是否是最小化窗口

      isMaximized()
        是否是最大化窗口

      isFullScreen()
        是否全屏

  窗口标志
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
      窗口样式
        Qt.Widget
          默认是一个窗口或控件
            有父控件, 就是一般控件
            没有父控件,则是窗口

        Qt.Window
          是一个窗口，有窗口边框和标题

        Qt.Dialog
          是一个对话框窗口

        Qt.Sheet
          是一个窗口或部件Macintosh表单

        Qt.Drawer
          是一个窗口或部件Macintosh抽屉

        Qt.Popup
          是一个弹出式顶层窗口

        Qt.Tool
          是一个工具窗口

        Qt.ToolTip
          是一个提示窗口，没有标题栏和窗口边框

        Qt.SplashScreen
          是一个欢迎窗口，是QSplashScreen构造函数的默认值

        Qt.SubWindow
          是一个子窗口

      顶层窗口外观标志
        Qt.MSWindowsFixedSizeDialogHint
          窗口无法调整大小

        Qt.FramelessWindowHint
          窗口无边框

        Qt.CustomizeWindowHint
          有边框但无标题栏和按钮，不能移动和拖动

        Qt.WindowTitleHint
          添加标题栏和一个关闭按钮

        Qt.WindowSystemMenuHint
          添加系统目录和一个关闭按钮

        Qt.WindowMaximizeButtonHint
          激活最大化和关闭按钮，禁止最小化按钮

        Qt.WindowMinimizeButtonHint
          激活最小化和关闭按钮，禁止最大化按钮

        Qt.WindowMinMaxButtonsHint
          激活最小化，最大化和关闭按钮

        Qt.WindowCloseButtonHint
          添加一个关闭按钮

        Qt.WindowContextHelpButtonHint
          添加问号和关闭按钮，同对话框

        Qt.WindowStaysOnTopHint
          窗口始终处于顶层位置

        Qt.WindowStaysOnBottomHint
          窗口始终处于底层位置

    windowFlags()
```

交互状态

```shell
API
  是否可用
    setEnabled(bool)
      设置控件是否禁用

    isEnabled()
      获取控件是否可用

  是否显示/隐藏
    setVisible(bool)
      设置控件是否可见
        传递的参数值为True也不一定可见

    isHidden()
      判定控件是否隐藏
        一般是基于父控件可见

    isVisible()
      获取控件最终状态是否可见

    isVisibleTo(widget)
      如果能随着widget控件的显示和隐藏, 而同步变化, 则返回True

  是否编辑
    设置窗口标题xxx[*]
    setWindowModified(bool)
      被编辑状态显示*
      没有被编辑不显示*

    isWindowModified()
      窗口是否是被编辑状态

  是否为活跃窗口
    isActiveWindow()

  关闭
    close()
    补充
      setAttribute(Qt.WA_DeleteOnClose, True)
```

信息提示

```python
API
  状态提示
    statusTip()
    setStatusTip(str)
    效果
      鼠标停在控件上时, 展示在状态栏

  工具提示
    toolTip()
    setToolTip(str)

    时长
      toolTipDuration()
      setToolTipDuration(msec)

    效果
      鼠标悬停在控件上一会后, 展示在旁边

  这是啥提示
    whatsThis()
    setWhatsThis(str)
```

焦点控制

```python
API
  单个控件角度
    setFocus()
      指定控件获取焦点

    setFocusPolicy(Policy)
      设置焦点获取策略

      Policy
        Qt.TabFocus
          通过Tab键获得焦点

        Qt.ClickFocus
          通过被单击获得焦点

        Qt.StrongFocus
          可通过上面两种方式获得焦点

        Qt.NoFocus
          不能通过上两种方式获得焦点(默认值),setFocus仍可使其获得焦点

    clearFocus()
      取消焦点

  父控件角度
    focusWidget()
      获取子控件中当前聚焦的控件

    focusNextChild()
      聚焦下一个子控件

    focusPreviousChild()
      聚焦上一个子控件

    focusNextPrevChild(bool)
      True: 下一个
      False: 上一个

    setTabOrder(pre_widget, next_widget)
      静态方法
      设置子控件获取焦点的先后顺序
```

#### 信号

```shell
windowTitleChanged(QString)
窗口标题改变信号

windowIconChanged(QIcon)
窗口图标改变信号

customContextMenuRequested(QPoint)
自定义上下文菜单请求信号
```

## 按钮

### QAbstractButton

所有按钮控件的基类，提供按钮的通用功能

提示文本

```python


API
  setText(str)
    设置按钮提示文本

  text()
    获取按钮提示文本
```

图标相关

```python

API
  setIcon(QIcon("resource/h1.png"))
    设置图标

  setIconSize(QSize(w, h))
    设置图标大小

  icon()
    获取图标

  iconSize()
    获取图标大小
```

设置快捷键

```python

作用
  通过指定的快捷键, 触发按钮的点击

方式1: 有提示文本的
  如果提示文本包含＆符号（'＆'）的, 则QAbstractButton会自动创建快捷键

方式2: 没有提示文本的
  setShortcut("Alt+G")
```

自动重复

```python
API
  setAutoRepeat(bool)
    设置自动重复

  setAutoRepeatInterval(毫秒)
    设置自动重复检测间隔

  setAutoRepeatDelay(毫秒)
    设置初次检测延迟

  autoRepeat()
    获取是否自动重复

  autoRepeatInterval()
    获取自动重复检测间隔

  autoRepeatDelay()
    获取初次检测延迟
```

状态

```python
API
  isDown()
    是否按下按钮
    setDown(bool)
      设置按钮, 是否被按下

  isChecked()
    是否选中了按钮
    isCheckable()
      按钮是否可以被选中
      setCheckable(bool)
        设置按钮, 是否可以被选中

    setChecked(bool)
      设置按钮, 是否被选中

    toggle()
      切换选中与非选中状态

  继承于QWidget中的能用状态
    isEnabled()
    setEnabled(bool)
```

排他性

```python
概念
  如果同时存在多个按钮, 而此时所有按钮又设置了排他性,
  则在同一时刻只能选中一个按钮

API
  autoExclusive()
    是否自动排他
    一般按钮都是False, 只有单选按钮是True

  setAutoExclusive(bool)
    设置自动排他
```

点击

```python
API
  click()
    普通点击

  animateClick(ms)
    动画点击
```

设置有效区域

```python
API
  重写hitButton(QPoint)
    有效返回True
    无效返回False
```

#### 信号

```python
# 鼠标按下信号
pressed()

# 鼠标释放
#   控件内松开鼠标
#   鼠标移出控件范围后
released()

# 控件内按下+控件内释放
clicked(checked = false)

# 切换信号(一般在单选框或者复选框中使用)
toggled(bool checked)
```

### QPushButton

用来给用户点击, 来完成某种动作的控件

创建按钮控件

```python
QPushButton()
  创建一个无父控件的按钮控件

QPushButton(parent)
  创建控件的同时, 设置父控件

QPushButton(text, parent)
  创建控件的同时, 设置提示文本和父控件

QPushButton(icon, text, parent)
  创建控件的同时, 设置图标, 提示文本和父控件
```

快捷键

```python
设置英文文本时, 使用&符号
QPushButton("&Sz", window)
setText("&Sz")
```

#### 菜单

```python
API
  setMenu(QMenu)
    设置菜单

  menu()
    获取菜单

  showMenu()
    展示菜单
```

菜单示例

```python
from PyQt5.Qt import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(600, 600)
    # 添加一个按钮
    btn = QPushButton(window)
    btn.setText("xxx")

    # 添加一个菜单
    menu = QMenu(window)

    # 子菜单 最近打开
    open_recent_menu = QMenu(menu)
    open_recent_menu.setTitle("最近打开")

    # 行为动作 新建  打开  分割线 退出
    # new_action = QAction()
    # new_action.setText("新建")
    # new_action.setIcon(QIcon("xxx.png"))
    new_action = QAction(QIcon("xxx.png"), "新建", menu)
    new_action.triggered.connect(lambda: print("新建文件"))

    open_action = QAction(QIcon("xxx.png"), "打开", menu)
    open_action.triggered.connect(lambda: print("打开文件"))

    exit_action = QAction("退出", menu)
    exit_action.triggered.connect(lambda: print("退出程序"))

    file_action = QAction("Python-GUI编程-PyQt5")

    # 绑定菜单
    menu.addAction(new_action)
    menu.addAction(open_action)
    open_recent_menu.addAction(file_action)
    menu.addMenu(open_recent_menu)
    # 添加分割线
    menu.addSeparator()
    menu.addAction(exit_action)

    # 绑定按钮
    btn.setMenu(menu)

    window.show()
    sys.exit(app.exec_())
```

右键菜单

```python
from PyQt5.Qt import *
import sys

class Window(QWidget):
    # 默认上下文菜单调用这个方法
    def contextMenuEvent(self, evt):
        menu = QMenu(self)

        # 子菜单 最近打开
        open_recent_menu = QMenu(menu)
        open_recent_menu.setTitle("最近打开")

        # 行为动作 新建  打开  分割线 退出
        # new_action = QAction()
        # new_action.setText("新建")
        # new_action.setIcon(QIcon("xxx.png"))
        new_action = QAction(QIcon("xxx.png"), "新建", menu)
        new_action.triggered.connect(lambda: print("新建文件"))

        open_action = QAction(QIcon("xxx.png"), "打开", menu)
        open_action.triggered.connect(lambda: print("打开文件"))

        exit_action = QAction("退出", menu)
        exit_action.triggered.connect(lambda: print("退出程序"))

        file_action = QAction("Python-GUI编程-PyQt5")

        menu.addAction(new_action)
        menu.addAction(open_action)
        open_recent_menu.addAction(file_action)
        menu.addMenu(open_recent_menu)
        menu.addSeparator()
        menu.addAction(exit_action)

        # point,菜单跟随点
        menu.exec_(evt.globalPos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    # 自定义菜单
    def show_menu():
      print('菜单')
    window.setContextMenuPolicy(Qt.CustomContextMenu)
    window.customContextMenuRequested.connect(show_menu)

    sys.exit(app.exec_())
```

#### 边框是否保持扁平

```python

API
  setFlat(bool)
    默认值为False
    设置了此属性，则除非按下按钮，否则大多数样式都不会绘制按钮背景

  isFlat()
    获取当前按钮边框是否扁平
```

#### 默认处理

```python

API
  setAutoDefault(bool)
    设置为自动默认按钮（需要点击之后）

  autoDefault()

  setDefault(bool)
   设置为自动默认按钮（不需要点击）

  isDefault()
```

```python
from PyQt5.Qt import *
import sys

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = QWidget()

    btn = QPushButton(window)
    btn2 = QPushButton(window)
    btn2.setText("btn2")
    btn2.move(200, 200)

    # 需要点击之后才默认
    btn2.setAutoDefault(True)

    print(btn.autoDefault())
    # False
    print(btn2.autoDefault())
    # True

    # 这样设置不用点击直接默认
    # btn2.setDefault(True)

    window.show()
    sys.exit(app.exec_())
```

### QCommandLinkButton

类似于单选按钮的用途，因为它用于在一组互斥选项之间进行选择

命令链接按钮不应单独使用，而应作为向导和对话框中单选按钮的替代选项

```python
继承自
  QPushButton

QCommandLinkBut​​ton(text, description ,parent)

API
  setDescription(str)
  description()
```

```python
from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QCommandLinkButton使用")
window.resize(500, 500)


btn = QCommandLinkButton("标题", "描述", window)
btn.setText("标题2")
btn.setDescription("xxx")
btn.setIcon(QIcon("xxx.png"))

print(btn.description())

window.show()
sys.exit(app.exec_())
```

### QToolButton

提供了一个快速访问按钮

通常是在工具栏内部使用，工具按钮通常不显示文本标签，而是显示图标

```python
API
  setText(str)
  setIcon(QIcon)
  setIconSize(QSize)
  setToolTip(str)

  如果文本和图标同时设置, 则默认只展示图标
```

示例

```python
from PyQt5.Qt import *
import sys


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QToolButton使用")
window.resize(500, 500)

tb = QToolButton(window)
tb.setText("工具")
tb.setIcon(QIcon("xxx.png"))
tb.setIconSize(QSize(60, 60))
tb.setToolTip("这是一个新建按钮")

window.show()
sys.exit(app.exec_())
```

#### 按钮样式风格

```python
API
  setToolButtonStyle(Qt.ToolButtonStyle)
    风格取值

      Qt.ToolButtonIconOnly
        仅显示图标

      Qt.ToolButtonTextOnly
        仅显示文字

      Qt.ToolButtonTextBesideIcon
        文本显示在图标旁边

      Qt.ToolButtonTextUnderIcon
        文本显示在图标下方

      Qt.ToolButtonFollowStyle
        遵循风格

  toolButtonStyle()

# tb.setToolButtonStyle(Qt.ToolButtonFollowStyle)
```

#### 设置箭头

```python

API
  setArrowType(Qt.ArrowType)
    Qt.ArrowType
      Qt.NoArrow
        无箭头

      Qt.UpArrow
        向上箭头

      Qt.DownArrow
        向下箭头

      Qt.LeftArrow
        向左箭头

      Qt.RightArrow
        向右箭头

  arrowType()

# tb.setArrowType(Qt.LeftArrow)
```

#### 自动提升

```python
API

  setAutoRaise(bool)
  autoRaise()

应用场景

  在自动提升模式下，该按钮仅在鼠标指向时才会绘制3D帧
  在工具栏(QToolBar)中, 默认就是自动提升
```

#### 菜单

```python
API
  setMenu(QMenu)
  menu()


菜单弹出模式API

  setPopupMode(QToolButton.ToolButtonPopupMode)

    QToolButton.ToolButtonPopupMode

      QToolButton.DelayedPopup
        鼠标按住一会才显示
        类似于浏览器后退按钮

      QToolButton.MenuButtonPopup
        有一个专门的指示箭头
        点击箭头才显示

      QToolButton.InstantPopup
        点了按钮就显示
        点击信号不会发射

  popupMode()
```

工具按钮菜单示例

```python
from PyQt5.Qt import *
import sys


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QToolButton使用")
window.resize(500, 500)

tb = QToolButton(window)
tb.setText("工具")
tb.setIcon(QIcon("xxx.jpg"))
tb.setIconSize(QSize(60, 60))
tb.setToolTip("这是一个新建按钮")

# 遵循风格
tb.setToolButtonStyle(Qt.ToolButtonFollowStyle)
tb.setAutoRaise(True)

menu = QMenu(tb)
menu.setTitle("菜单")

sub_menu = QMenu(menu)
sub_menu.setTitle("子菜单")
sub_menu.setIcon(QIcon("xxx.jpg"))
action1 = QAction(QIcon("xxx.jpg"), "行为1", menu)
action1.setData([1, 2, 3])
action2 = QAction("行为2", menu)
action2.setData({"name": "sz"})
action1.triggered.connect(lambda :print("点击了行为1菜单选项"))
menu.addMenu(sub_menu)
menu.addSeparator()
menu.addAction(action1)
menu.addAction(action2)

tb.clicked.connect(lambda :print("工具按钮被点击了"))

tb.setMenu(menu)

# 菜单弹出模式
tb.setPopupMode(QToolButton.MenuButtonPopup)

# 当点击某个action时触发, 并会将action传递出来
# QAction对象可以通过setData(Any)绑定数据, data()获取数据
def do_action(action):
    print("点击了行为", action.data())
tb.triggered.connect(do_action)

window.show()
sys.exit(app.exec_())
```

### QRadioButton

用于给用户提供若干选项中的单选操作

```python
from PyQt5.Qt import *
import sys


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QRadioButton-功能测试")
window.resize(500, 500)

rb_nan = QRadioButton("男", window)
rb_nan.setShortcut("Alt+M")
rb_nan.move(10, 10)
rb_nan.setChecked(True)

rb_nv = QRadioButton("女-&Female", window)
rb_nv.move(10, 50)
rb_nv.setIcon(QIcon("xxx.png"))
rb_nv.toggled.connect(lambda isChecked: print(isChecked))

# 是否排他
rb_nv.setAutoExclusive(False)

window.show()
sys.exit(app.exec_())
```

### QButtonGroup

提供一个抽象的按钮容器, 可以将多个按钮划分为一组

不具备可视化的效果，一般放的都是可以被检查的按钮

```python
创建按钮组
  QButtonGroup(parent)

添加按钮
    addButton(QAbstractButton, id = -1)
      如果id为-1，则将为该按钮分配一个id。自动分配的ID保证为负数，从-2开始。
      如果要分配自己的ID，请使用正值以避免冲突

查看按钮
    buttons()
      查看所有按钮组中的按钮

    button(ID)
      根据ID获取对应按钮, 没有则返回None

    checkedButton()
      获取选中的那个按钮

移除按钮
    removeButton(QAbstractButton)
    移除指定按钮
    注意，不是从界面上移除，是从抽象关系上移除

绑定和获取ID
    setId(QAbstractButton，int)
    id(QAbstractButton)
      指定按钮对应的ID，如果不存在此按钮，则返回-1

    checkedId()
      选中的ID
      如果没有选中按钮则返回-1

独占设置
    setExclusive(bool)
    exclusive()

信号

buttonClicked(int/QAbstractButton)
  当按钮组中的按钮被点击时, 发射此信号

buttonPressed(int/QAbstractButton)
  当按钮组中的按钮被按下时, 发射此信号

buttonReleased(int/QAbstractButton)
  当按钮组中的按钮被释放时, 发射此信号

buttonToggled(QAbstractButton/int, bool)
  当按钮组中的按钮被切换状态时, 发射此信号

重点注意
  如果一个对象向外界提供的信号名称一样, 但参数不一样
  外界在使用信号时, 可以使用如下格式进行选择
  signal_name[type]

    signal_name
      信号名称

    type
      参数类型
```

```python
from PyQt5.Qt import *
import sys


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("按钮组的使用")
window.resize(500, 500)

# 创建四个单选按钮
# 男女
r_male = QRadioButton("男", window)
r_female = QRadioButton("女", window)
r_male.move(100, 100)
r_female.move(100, 150)
r_male.setChecked(True)

sex_group = QButtonGroup(window)
sex_group.addButton(r_male, 1)
sex_group.addButton(r_female, 2)

# 是否
r_yes = QRadioButton("是", window)
r_no = QRadioButton("否", window)
r_yes.move(300, 100)
r_no.move(300, 150)
answer_group = QButtonGroup(window)
answer_group.addButton(r_yes)
answer_group.addButton(r_no)

# 设置ID
answer_group.setId(r_yes, 1)
answer_group.setId(r_no, 2)

# 设置选中
r_no.setChecked(True)

def test(val):
    # print(val)
    print(sex_group.id(val))
sex_group.buttonClicked.connect(test)

window.show()
sys.exit(app.exec_())
```

### QCheckBox

用于给用户提供若干选项中的多选操作

```python
创建复选框按钮
  QCheckBox(parent=None)
  QCheckBox(text, parent=None)

常用继承父类操作
  图标
    setIcon(QIcon)

  快捷键
    文本加&
    setShortcut()

设置是否三态
    setTristate(bool=True)
    isTristate()

设置复选框状态
    setCheckState(Qt.CheckState)
    checkState()
      Qt.Unchecked
        该项目未选中

      Qt.PartiallyChecked
        部分选中

      Qt.Checked
        真的被选中

信号
  stateChanged(int state)
    选中或清除选中时, 发射此信号
```

```python
from PyQt5.Qt import *
import sys


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QCheckBox 功能测试")
window.resize(500, 500)

cb = QCheckBox("&Python", window)
cb.setIcon(QIcon("xxx.png"))
cb.setIconSize(QSize(60, 60))
cb.setTristate(True)
cb.setCheckState(Qt.PartiallyChecked)
# cb.setCheckState(Qt.Checked)

# 三态都触发
cb.stateChanged.connect(lambda state: print(state))

# 三态的话，部分和全部都当成true，这两个间切换不会触发
# cb.toggled.connect(lambda isChecked: print(isChecked))

window.show()
sys.exit(app.exec_())
```

## 输入控件

### QLineEdit

是一个单行文本编辑器,允许用户输入和编辑单行纯文本

```python
控件的创建
      QLineEdit(parent: QWidget = None)
      QLineEdit(str, parent: QWidget = None)

文本的设置和获取
    setText(str)
      设置内容文本

    insert(newText)
      在光标处插入文本

    text()
      获取真实内容文本

    displayText()
      获取用户能看到的内容文本

输出模式
    setEchoMode(QLineEdit.EchoMode)
      QLineEdit.EchoMode
            NoEcho = 1
          不输出

            Normal = 0
          正常输出

            Password = 2
          密文形式

            PasswordEchoOnEdit = 3
          编辑时明文, 结束后密文

    echoMode() -> QLineEdit.EchoMode
      获取输出模式


占位提示字符串
    setPlaceholderText(notice_str)
    placeholderText()

清空按钮显示
    setClearButtonEnabled(bool)
    isClearButtonEnabled() -> bool

添加操作行为
    addAction(QAction, QLineEdit.ActionPosition)
        QLineEdit.ActionPosition
        QLineEdit.LeadingPosition
          搁前面

        QLineEdit.TrailingPosition
          搁后面

    addAction(QIcon, QLineEdit.ActionPosition) -> QAction

自动补全
    setCompleter(QCompleter)
      设置完成器

输入限制
    内容长度限制
      setMaxLength(int)
        设置限制输入的长度

      maxLength()
        获取输入长度

    只读限制
      setReadOnly(bool)
      isReadOnly()

    规则验证
      setValidator(QValidator)

        设置验证器
      setInputMask(mask_str)
        掩码验证

    判定输入文本是否通过验证
      hasAcceptableInput()
```

#### QValidator

验证器，用于验证用户输入数据的合法性

```python
如果一个输入框设置了验证器，到时用户在文本框中输入内容时，首先会将内容传递给验证器进行验证
    validate(self, input_text, pos)
      return (QValidator.Acceptable,  input_text, pos)
        验证通过

      return (QValidator.Intermediate,  input_text, pos)
        暂不作判定是否通过验证

      return (QValidator.Invalid,  input_text, pos)
        验证不通过

  如果输入框结束输入后, 上述的验证状态并非有效, 则会调用修复方法
    fixup(self, input_text)
      return 修正后文本

是一个抽象类, 使用前需要进行子类化操作
  系统提供子类
    QIntValidator(bottom, top, parent)
      限制整型数据范围

    QDoubleValidator
      浮点类型数据限制范围

    QRegExpValidator
      通过正则表达式限定

```

#### 编辑

```python
是否被编辑
    isModified()
    setModified(bool)

光标控制
    cursorBackward(bool mark，int steps = 1)
      向后(左)移动steps个字符
        mark: True
          带选中效果

        mark: False
          不带选中效果

    cursorForward(bool mark，int steps = 1)
      向前(右)移动steps个字符

    cursorWordBackward(bool mark)
      向后(左)移动一个单词长度

    cursorWordForward(bool mark)
      向前(右)移动一个单词长度

    home(bool)
      移动到行首

    end(bool)
      移动到行尾

    setCursorPosition(int)
      设置光标位置

    cursorPosition()
      获取光标位置

    cursorPositionAt(const QPoint＆ pos)
      获取指定坐标位置对应文本光标位置

文本边距设置
    getTextMargins()
    setTextMargins(int left，int top，int right，int bottom)

对齐方式
    setAlignment(Qt.Alignment)
      设置输入文本的对齐方式
      Qt.Alignment
        水平
          Qt.AlignLeft
          Qt.AlignRight
          Qt.AlignHCenter
          Qt.AlignJustify
            此处同左对齐

        垂直
          Qt.AlignTop
          Qt.AlignBottom
          Qt.AlignVCenter
          Qt.AlignBaseline

        Qt.AlignCenter
          等同于
            Qt.AlignHCenter | Qt.AlignVCenter
          垂直和水平都居中

    alignment() -> Qt.Alignment

常用编辑功能

    退格
      backspace()
        删除选中文本或删除光标左侧一个字符

    删除
      del_()

        删除选中文本或删除光标右侧的一个字符

    清空
      clear()
        删除所有文本框内容

    复制
      copy()

    剪切
      cut()

    粘贴
      paste()

    撤消
      isUndoAvailable()
      undo()

    重做
      isRedoAvailable()
      redo()

    拖放
      setDragEnabled(bool)
        设置选中文本后是否可以拖拽

    文本选中
      setSelection(start_pos, length)
        选中指定区间的文本

      selectAll()
        选中所有文本

      deselect()
        取消选中已选择文本

      hasSelectedText()
        是否有选中文本

      selectedText() -> str
        获取选中的文本

      selectionStart() -> int
        选中的开始位置

      selectionEnd() -> int
        选中的结束位置

      selectionLength() -> int
        选中的长度
```

####  信号

```python
textEdited( text)
  文本编辑时发射的信号

textChanged(text)
  文本框文本发生改变时发出的信号

returnPressed()
  按下回车键时发出的信号

editingFinished()
  结束编辑时发出的信号

cursorPositionChanged(int oldPos，int newPos)
  光标位置发生改变时发出的信号

selectionChanged()
  选中的文本发生改变时发出的信号
```

#### QTextEdit

是一个高级的WYSIWYG(What You See Is What You Get 所见即所得)查看器/编辑器，支持使用HTML样式标签的富文本格式。

它经过优化，可以处理大型文档并快速响应用户输入。

适用于段落和字符

##### 内容设置

```python
继承 QAbstractScrollArea

占位提示文本
  setPlaceholderText(str)
  placeholderText() -> str

内容设置

  普通文本
    setPlainText(str)
    insertPlainText(str)
    toPlainText() -> str

  HTML
    setHtml(str)
    insertHtml(str)
    toHtml() -> str

  设置文本(自动判定)
    setText(str)

  追加文本
    append(str)

  清空
  clear()

  文本光标
    通过文本光标, 可以操作编辑 文本文档 对象
      获取文本文档的方法
        te.document() -> QTextDocument
        补充
          QTextDocument
              保存带格式的文本文档
              为样式化文本和各种类型的文档元素提供支持
              是结构化富文本文档的容器

  textCursor() -> QTextCursor
          插入文本
            insertText(str)
              插入文本(普通文本)

            insertText(QString text, QTextCharFormat format)
              插入文本, 带格式
              QTextCharFormat
                针对于部分字符的格式描述

            insertHtml(html_str)
              插入HTML 字符串

          插入图片
            insertImage(QTextImageFormat)
              QTextImageFormat
                    tf.setName("xxx.png")
                    tf.setWidth(20)
                    tf.setHeight(20)

            insertImage(QTextImageFormat, QTextFrameFormat.Position)
            insertImage(name_str)
            insertImage(QImage, name_str=None)

          插入句子
            insertFragment(QTextDocumentFragment )
              QTextDocumentFragment
                构建对象
                  fromHtml(html_str)
                  fromPlainText(str)

          插入列表
            insertList(QTextListFormat) -> QTextList
              在当前位置插入一个新块，并使其成为具有给定格式的新创建列表的第一个列表项。返回创建的列表

            insertList(QTextListFormat.Style) -> QTextList
              在当前位置插入一个新块，并使其成为具有给定格式的新创建列表的第一个列表项。返回创建的列表

            createList(QTextListFormat ) -> QTextList
              创建并返回具有给定格式的新列表，并使当前段落的光标位于第一个列表项中

            createList(QTextListFormat.style ) -> QTextList
              创建并返回具有给定格式的新列表，并使当前段落的光标位于第一个列表项中

            补充
              QTextListFormat
                setIndent(int)
                setNumberPrefix(str)
                setNumberSuffix(str)
                setStyle(QTextListFormat_Style)

              QTextListFormat.Style
                QTextListFormat.ListDisc
                  一个圆圈

                QTextListFormat.ListCircle
                  一个空的圆圈

                QTextListFormat.ListSquare
                  一个方块

                QTextListFormat.ListDecimal
                  十进制值按升序排列

                QTextListFormat.ListLowerAlpha
                  小写拉丁字符按字母顺序排列

                QTextListFormat.ListUpperAlpha
                  大写拉丁字符按字母顺序排列

                QTextListFormat.ListLowerRoman
                  小写罗马数字（仅支持最多4999项）

                QTextListFormat.ListUpperRoman
                  大写罗马数字（仅支持最多4999项）

          插入表格

            insertTable(int rows, int columns) -> QTextTable
            insertTable(int rows, int columns, QTextTableFormat) -> QTextTable
            补充
              QTextTableFormat

                setAlignment(self, Union, Qt_Alignment=None, Qt_AlignmentFlag=None)
                  对齐方式

                setCellPadding(self, p_float)
                  内边距

                setCellSpacing(self, p_float)
                  外边距

                setColumnWidthConstraints(self, Iterable, QTextLength=None)
                  设置列宽

          插入文本块
            insertBlock()
              插入一个空的文本块

            insertBlock(QTextBlockFormat)
              插入文本块的同时, 设置文本块格式

            insertBlock(QTextBlockFormat, QTextCharFormat )
              插入文本块的同时, 设置文本块格式和文本字符格式

          插入框架
            insertFrame(QTextFrameFormat) -> QTextFrame

      设置和合并格式
          setBlockCharFormat(QTextCharFormat)
            设置要格式化的当前块（或选择中包含的所有块）的块char 格式

          setBlockFormat(QTextBlockFormat)
            设置当前块的块格式（或选择中包含的所有块）以进行格式化

          setCharFormat(QTextCharFormat)
            将光标的当前字符格式设置为给定格式。如果光标有选择，则给定格式应用于当前选择

          mergeBlockCharFormat(QTextCharFormat)
            合并当前块的char格式

          mergeBlockFormat(QTextBlockFormat)
            合并当前块的格式

          mergeCharFormat(QTextCharFormat)
            合并当前字符格式

      获取内容和格式相关
          block() -> QTextBlock
            获取光标所在的文本块

          blockFormat() -> QTextBlockFormat
            获取光标所在的文本块格式

          blockCharFormat() -> QTextCharFormat
            获取光标所在的文本块字符格式

          blockNumber() -> int
            获取光标所在的文本块编号

          charFormat() -> QTextCharFormat
            获取文本字符格式

          currentFrame() -> QTextFrame
            获取当前所在的框架

          currentList() -> QTextList
            获取当前所在的文本列表

          currentTable() -> QTextTable
            获取当前的表格

      文本选中和清空
          选中
            setPosition(int pos, QTextCursor.MoveMode=MoveAnchor)
              设置光标位置
              需要反向设置回去

            movePosition(QTextCursor.MoveOperation, QTextCursor.MoveMode=MoveAnchor, int n = 1)
              移动指定长度后, 参照移动选项和模式确定最终位置以及是否选中文本
              需要反向设置

            select(QTextCursor.SelectionType)
              需要反向设置

          选中内容获取
            selectedText() -> str
            selection() -> QTextDocumentFragment
            selectedTableCells() -> (int firstRow, int numRows, int firstColumn, int numColumns)

          选中的位置获取
            selectionStart() -> int
            selectionEnd() -> int

          清空和判定
            clearSelection()
              取消文本的选中
              需要反向设置

            hasSelection() -> bool
              是否有选中文本

          选中文本的移除
            removeSelectedText()
              移除选中的文本

          补充
            QTextCursor.MoveMode
              QTextCursor.MoveAnchor
                将锚点移动到与光标本身相同的位置。

              QTextCursor.KeepAnchor
                将锚固定在原处。

            QTextCursor.MoveOperation
              QTextCursor.NoMove
                将光标保持在原位

              QTextCursor.Start
                移至文档的开头。

              QTextCursor.StartOfLine
                移动到当前行的开头。

              QTextCursor.StartOfBlock
                移动到当前块的开头。

              QTextCursor.StartOfWord
                移动到当前单词的开头。

              QTextCursor.PreviousBlock
                移动到上一个块的开头。

              QTextCursor.PreviousCharacter
                移至上一个字符。

              QTextCursor.PreviousWord
                移到上一个单词的开头。

              QTextCursor.Up
                向上移动一行。

              QTextCursor.Left
                向左移动一个字符。

              QTextCursor.WordLeft
                向左移动一个单词。

              QTextCursor.End
                移到文档的末尾。

              QTextCursor.EndOfLine
                移动到当前行的末尾。

              QTextCursor.EndOfWord
                移到当前单词的末尾。

              QTextCursor.EndOfBlock
                移动到当前块的末尾。

              QTextCursor.NextBlock
                移动到下一个块的开头。

              QTextCursor.NextCharacter
                移动到下一个角色。

              QTextCursor.NextWord
                转到下一个单词。

              QTextCursor.Down
                向下移动一行。

              QTextCursor.Right
                向右移动一个角色。

              QTextCursor.WordRight
                向右移动一个单词。

              QTextCursor.NextCell
                移动到当前表中下一个表格单元格的开头。如果当前单元格是行中的最后一个单元格，则光标将移动到下一行中的第一个单元格。

              QTextCursor.PreviousCell
                移动到当前表内的上一个表格单元格的开头。如果当前单元格是行中的第一个单元格，则光标将移动到上一行中的最后一个单元格。

              QTextCursor.NextRow
                移动到当前表中下一行的第一个新单元格。

              QTextCursor.PreviousRow
                移动到当前表中上一行的最后一个单元格。

            QTextCursor.SelectionType
              QTextCursor.Document
                选择整个文档。

              QTextCursor.BlockUnderCursor
                选择光标下的文本块。

              QTextCursor.LineUnderCursor
                选择光标下的文本行。

              QTextCursor.WordUnderCursor
                选择光标下的单词。如果光标未定位在可选字符串中，则不选择任何文本。

      删除内容
          deleteChar()
            如果没有选中文本, 删除文本光标后一个字符
            如果有选中文本, 则删除选中文本

          deletePreviousChar()
            如果没有选中文本, 删除文本光标前一个字符
            如果有选中文本, 则删除选中文本

      位置相关
          atBlockEnd()
            是否在文本块末尾

          atBlockStart()
            是否在文本块开始

          atEnd()
            是否在文档末尾

          atStart()
            是否在文档开始

          columnNumber() -> int
            在第几列

          position()
            光标位置

          positionInBlock()
            在文本块中的位置

      开始和结束编辑标识
          beginEditBlock()
          endEditBlock()
```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```



```python

```


```python

```


# js与jQuery

## 原生js事件

变色

```html
<!DOCTYPE html>
<html lang="zh-CN">
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .c1 {
            width: 500px;
            height: 500px;
            border-radius: 40%;
        }

        .bg_green {
            background-color: green;
        }

        .bg_red {
            background-color: red;
        }
    </style>
</head>

<body>
    <div id="c1" class="c1 bg_green bg_red"></div>
    <button id="d1">变色</button>
    <script>
        var btnEle = document.getElementById('d1')
        var divEle = document.getElementById('c1')
        btnEle.onclick = function () {
            divEle.classList.toggle('bg_red')
        }
    </script>
</body>

</html>
```

input标签获取,失去焦点

```html
<!DOCTYPE html>
<html lang="zh-CN">
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
<input type="text" value="hi" id="d1">
<script>
    var iEle = document.getElementById('d1')
    iEle.onfocus=function () {
        iEle.value = ''
    }
    iEle.onblur=function (){
        iEle.value = 'hello'
    }
</script>
</body>

</html>
```

定时器

```html
<!DOCTYPE html>
<html lang="zh-CN">
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <input type="text" id="d1" style="display: block; width: 200px; height: 40px;">
    <button id="d2">开始</button><button id="d3">停止</button>
    <script>
        let iEle = document.getElementById("d1")
        let start = document.getElementById('d2')
        let end = document.getElementById('d3')
        let t = null
        function showTime() {
            let currentTime = new Date();
            iEle.value = currentTime.toLocaleString();
        }
        showTime()
        start.onclick = function () {
            if (!t) {
                t = setInterval(showTime, 1000);
            }
        }
        end.onclick = function () {
            clearInterval(t)
            t = null
        }
    </script>
</body>

</html>
```

## jQuery

### 基本选择器

```shell
# id选择器
$('#c1')

# class选择器
$('.d1')

# 标签选择器
$('span')

# jQuery对象变成标签对象
$('.d1')[0]

# 标签对象变成jQuery对象
$(document.getElementById('d1'))
```

### 组合选择器

```shell
# id是d1的div
$('div.d1')

# 获取多个
$('#c2, .d1, p')

# 后代span
$('div span')

# 儿子span
$('div>span')

# div同级第一个span
$('div+span')

# div同级所有span
$('div~span')
```

### 基本筛选器

```shell
# 第一个
$('ul li:first')

# 第二个
$('ul li:eq(2)')

# 最后一个
$('ul li:last')

# 索引为偶数的,包含0
$('ul li:even')

# 索引为奇数的
$('ul li:odd')

# 索引大于2的
$('ul li:gt(2)')

# 排除id为d1的li
$('ul li:not("#d1")')

# 内部含有P标签的div
$('div:has("p")')
```

### 属性选择器

```shell
# 有此属性的标签
$('[username="json"]')
```

### 表单选择器

```shell
# 仅适用表单
$(':password')
```

### 筛选器方法

```shell
# 同级别下一个
$('#d1').next()
# nextAll() 所有
# nextUntile('.c1') 直到
# prev() 上一个, 同上

# 父标签
$('#d1').parent()
# parents() 所有

# 儿子
$('#d1').children()

# 同级别上下所有
$('#d1').siblings()

# $('div p')
$('div').find('p')

# $('div span:first')
$('div span').first()

# $('ul li:not("#d1")')
$('ul li').not('#d1')
```

### 样式操作

```shell
# hasClass()
# removeClass()
# addClass()
# toggleClass()
```

### CSS操作

```shell
$('p').first().css('color',red)
```

### 位置操作

```shell
# 相对于浏览器窗口
offset()

# 相对于父标签
position()

# 页面滚动
scrollTop()
```

### 尺寸

```shell
# 文本
$('p').height()

# 文本+padding
$('p').innerHeight

# 文本+padding+border
$('p').outerHeigth
```

### 文本操作

```shell
$('div').text()

# 可以识别标签
$('div').html()
```

### 获取值操作

```shell
$('p').val()
```

### 属性操作

```shell
$('#d1').attr('name', 'h')

# 获取属性
$('#d1').attr()

# 判断checkbox, radio, option是否被选中
$('#d1').prop('checked', true)
```

### 文档处理

```shell
# 新建标签
let $pEle = $('<p>')

# 内部尾部追加, appendTo
$('#d1').append($pEle)
$pEle.appendTo($('#d1'))

# 内部头部追加
$('#d1').prepend($pEle)

# 放在某个标签后面, insertAfter
$('#d1').after($pEle)

# before, insertBefore

# 删除标签
$('#d1').remove()

# 清空标签内部所有内容
$('#d1').empty()
```

### 事件

```shell
# 默认只克隆html和css, 不可隆事件. 需要加clone(true)
clone()
```

三级菜单

```html
    <script>
        $('.title').click(function () {
            // 先给所有的子菜单items加hide
            $('.items').addClass('hide')
            // 然后将被点击标签内部的hide移除
            $(this).children().removeClass('hide')
        })
    </script>
```

回到顶部

```html
    <script>
        $(window).scroll(function () {
            if ($(window).scrollTop()>300) {
                $('#d1').removeClass('hide')
            }else{
                $('#d1').addClass('hide')
            }
            // 再添加点击回到顶部事件, $(window).scrollTop(0)
        })
    </script>
```

阻止后续事件执行与事件冒泡

```shell
return false
```

事件委托

```shell
# 在指定范围内, 将事件委托给某个标签, 可以是后面动态创建的标签
$('body').on('click', 'button', function(){
    alert(123)
})
```

等待页面加载完毕之后再执行代码

```html
$(function(){
    // js代码
})

// 直接写在body最下方
```

动态展示用户上传的头像

```js
<script>
    $('#myfile').change(function () {
        // 先生成一个文件阅读器对象
        let myFileReaderObj = new FileReader();
        // 获取用户上传的头像
        let fileObj = $(this)[0].files[0];
        // 文件阅读器对象读取文件
        myFileReaderObj.readAsDataURL(fileObj) // 异步IO操作
        // 等待文件阅读器对象加载完毕之后展示
        myFileReaderObj.onload = function () {
            $('#myimg').attr('src', myFileReaderObj.result)
        }
    })
</script>
```

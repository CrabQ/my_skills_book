# lxml_xpath获取标签内的包括所有下级标签的所有文字内容

现有html源码如下

```html
<div>
    <ul class="1">test
        <li>1</li>
        <li>12<a>bcd</a></li>
        <li>123</li>
        <li>1234</li>
    </ul>
    <ul class="2">
        <li>2</li>
        <li>22<a>efg</a></li>
        <li>223</li>
        <li>2234</li>
    </ul>
</div>
```

想要获取`ul class="1"`下所有的文字内容，即

```shell
test
1
12 bcd
123
1234
```

使用`text()`只能获取当前层级的内容，下一层级的并不能获取到

```python
from lxml import etree

a = """<div>
    <ul class="1">test
        <li>1</li>
        <li>12<a>bcd</a></li>
        <li>123</li>
        <li>1234</li>
    </ul>
    <ul class="2">
        <li>2</li>
        <li>22<a>bcd</a></li>
        <li>223</li>
        <li>2234</li>
    </ul>
</div>
    """
b = etree.HTML(a)
c = b.xpath('//ul/text()')
print(c)

['test\n        ', '\n        ', '\n        ', '\n        ', '\n    ', '\n        ', '\n        ', '\n        ', '\n        ', '\n    ']
```

可通过xpath的string()函数实现

```python
from lxml import etree

a = """<div>
    <ul class="1">test
        <li>1</li>
        <li>12<a>bcd</a></li>
        <li>123</li>
        <li>1234</li>
    </ul>
    <ul class="2">
        <li>2</li>
        <li>22<a>bcd</a></li>
        <li>223</li>
        <li>2234</li>
    </ul>
</div>
    """
b = etree.HTML(a)
c = b.xpath('string(//ul)')
print(c)

test
        1
        12bcd
        123
        1234
```

结果如上（没有去掉空白字符）,如果想要获取`ul class="2"`下所有的文字内容,可通过如下3种方式：

```python
from lxml import etree

a = """<div>
    <ul class="1">test
        <li>1</li>
        <li>12<a>bcd</a></li>
        <li>123</li>
        <li>1234</li>
    </ul>
    <ul class="2">
        <li>2</li>
        <li>22<a>bcd</a></li>
        <li>223</li>
        <li>2234</li>
    </ul>
</div>
    """
b = etree.HTML(a)
# c = b.xpath('string(//ul[2])')
# c = b.xpath('string(//ul[@class="2"])')
c = b.xpath('//ul')[1].xpath('string(.)')
print(c)

        2
        22bcd
        223
        2234

```

1. 直接选取`ul`的第二个`children`

   ```python
   c = b.xpath('string(//ul[2])')
   ```

2. 通过`class`属性定位

   ```python
   c = b.xpath('string(//ul[@class="2"])')
   ```

3. 先获取储存所有`ul`的列表，再从列表中获取第二个`ul`,`.`表示当前节点

   ```python
   b.xpath('//ul')[1].xpath('string(.)')
    ```

xpath中text()和string()以及data()的区别
> [XPath中的text()和string()区别](https://blog.csdn.net/weixin_39285616/article/details/78463091)

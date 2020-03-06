# lxml_解析内存中的xml

> To parse from a string, use the ``fromstring()`` function instead.
>Note that it is generally faster to parse from a file path or URL
>than from an open file object or file-like object.

```python
result = handle.read()

doc = etree.fromstring(result)
```
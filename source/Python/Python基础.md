# Python基础

## python的垃圾回收机制

```shell
# 1. 循环引用导致的内存泄露

l1 = [1]
l2 = [2]

l1.append(l2)
# l1 = [值1的内存地址, l2的内存地址]
print(id(l2))
print(id(l1[1]))

l2.append(l1)
# l2 = [值2的内存地址, l1的内存地址]
print(id(l1))
print(id(l2[1]))

del l1
del l2
# l1, l2循环引用,并没有被回收

# 2. 标记清除,解决循环引用
# 3. 隔代回收
```

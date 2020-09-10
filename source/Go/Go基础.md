# Go基础

## 基础数据类型

### 整型

```go
package main

import "fmt"

func main() {

	var a int = 10
	fmt.Printf("%d \n", a) // 10
	fmt.Printf("%b \n", a) // 1010

	var b int = 077        // 8进制, 以0开头
	fmt.Printf("%o \n", b) // 77

	var c int = 0xff    //16进制, 以 0x开头
	fmt.Printf("%x", c) // ff
	fmt.Printf("%X", c) // FF
}
```

### 浮点型

```go
// float32 的浮点数的最大范围约为 3.4e38, 可用常量定义: math.MaxFloat32
// float64 的浮点数的最大范围约为 1.8e308, 可用常量定义: math.MaxFloat64

package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Printf("%f \n", math.Pi)
	fmt.Printf("%.2f \n", math.Pi)
}
```

### 复数

```go
package main

import (
	"fmt"
)

func main() {
	var c1 complex64
	c1 = 1 + 2i
	var c2 complex128
	c2 = 2 + 3i
	fmt.Println(c1) // (1+2i)
	fmt.Println(c2) // (2+3i)
}
```

### 布尔值

```shell
布尔类型变量的默认值为false
Go 语言中不允许将整型强制转换为布尔型
布尔型无法参与数值运算, 也无法与其他类型进行转换
```

### byte和rune类型

```shell
Go 语言的字符有以下两种

uint8, 或者叫 byte 型, 代表了ASCII码的一个字符
rune, 代表一个 UTF-8字符, rune类型实际是一个int32
```

遍历字符串

```go
package main

import (
	"fmt"
)

func main() {
	s := "heool! 算了"
	for i := 0; i < len(s); i++ { // byte
		fmt.Printf("%v(%c)", s[i], s[i])
	}
	// 104(h)101(e)111(o)111(o)108(l)33(!)32( )231(ç)174(®)151()228(ä)186(º)134()
	fmt.Println("")

	for _, r := range s { // rune
		fmt.Printf("%v(%c)", r, r)
	}
	// 104(h)101(e)111(o)111(o)108(l)33(!)32( )31639(算)20102(了)
}
```

修改字符串

```go
package main

import (
	"fmt"
)

func main() {
	s := "hello"
	bytes1 := []byte(s)
	bytes1[0] = 'p'
	fmt.Println(string(bytes1))

	r := "红番薯"
	runer1 := []rune(r)
	runer1[0] = '紫'
	fmt.Println(string(runer1))
}
```

### Array(数组)

```shell
数组是同一种数据类型元素的集合
在Go语言中,数组从声明时就确定, 使用时可以修改数组成员但数组大小不可变
# var a [3]int
# var b [34]int
# a和b是不同的数据类型

# 数组是值类型, 赋值和传参会复制整个数组. 因此改变副本的值不会改变本身的值

数组支持 == != 操作符, 因为内存总是被初始化过的
[n]*T表示指针数组, *[n]T表示数组指针
```

### 切片

```shell
切片是一个拥有相同类型元素的可变长度的序列. 它是基于数组类型做的一层封装

切片是一个引用类型, 它的内部结构包含地址, 长度和容量

切片是引用类型, 不支持直接比较, 只能和nil比较

切片的本质就是对底层数组的封装, 它包含了三个信息: 底层数组的指针, 切片的长度(len)和切片的容量(cap)
```

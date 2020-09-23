# shell编程

```shell
#!/bin/bash

# 1. 变量和$符


# 反引号, $(cmd)执行命令
echo $((1+1)) # 2

echo $(whoami) # root

echo `whoami` # root

a=1000

# ${变量名}取值, {}可忽略
echo '$a的值'${a} # $a的值1000

# 执行脚本, ./a.sh  -n=3 -a=4

# $0 文件名
echo "$0" # ./a.sh

# $1-$n 参数值
echo '$1的值'$1 # $1的值-n=3

# $# 参数个数
echo '$#的值'$# # $#的值2

# $*, $@表示所有的参数
echo '$*的值'$* # $*的值-n=3 -a=4
echo '$@的值'$@ # $@的值-n=3 -a=4

# $?脚本执行结果, 0表示执行完成, 正常退出
echo '$?的值'$? # $?的值0


# 2. 环境变量

export x=yes

# 获取用户输入
# read -p '请输入你的年龄: ' age
# echo 'age: '$age


# 3. 条件判断语句

# if命令执行成功then, else
if ls /
then
    echo '命令执行成功'
else
    echo '命令执行失败'
fi

# 条件测试语句, [  ]两边空格
# 数字比较-gt, -eq, -ne, -ge
if [ 3 -gt 2 ]
then
    echo '3>2'
else
    echo '3<2'
fi

# 条件测试语句, 字符串 = < >
x=yes
y=no
if [ $x = $y ]
then
    echo 'yes'
else
    echo 'no'
fi

# 判断是否是文件夹 [ -d path ] -f 是否是文件

# 条件判断, case语句

b=3

case $b in
    1)
        echo 是1
        ;;
    2)
        echo 是2
        ;;
    *)
        echo 其他
        ;;
esac

# 4. 循环语句

# for((j=0;j<=10;j++))
for i in `seq 1 10`
do
    echo $i
done

# 5. 函数, function可以不写
function foo(){
    echo 'foo里的$0' $0
    echo 'foo里的$1' $1
    echo 'foo里的$2' $2
    echo 'foo里的$#' $#
}

foo 1 2 3

# 6. 数组
name=(hong ming 123)
# 默认打印第0个
echo $name
# 获取第3个
echo ${name[2]}
# 获取所有 *, @
echo ${name[*]}
echo ${name[@]}
# 获取长度
echo ${#name[@]}
# 遍历
for n in ${name[@]}
do
    echo $n
done
```

# shell编程

```shell
#!/bin/bash

# 变量和$符

# 反引号, $(cmd)执行命令
echo $((1+1)) # 2

echo $(whoami) # root

echo `whoami` # root

# ${变量名}取值, {}可忽略
echo '$a的值'${a} # $a的值1000

# 执行脚本, ./a.sh  -n=3 -a=4

# $0 脚本名称,全路径执行则为全路径名称
echo "$0" # ./a.sh
# 只获取脚本名称
# basename /tmp/test.sh

# $1-$n 参数值(9之后要加上{}, ${10})
echo '$1的值'$1 # $1的值-n=3

# $# 参数个数
echo '$#的值'$# # $#的值2

# $*, $@表示所有的参数
echo '$*的值'$* # $*的值-n=3 -a=4
echo '$@的值'$@ # $@的值-n=3 -a=4

# $?上一个命令执行结果, 0表示执行完成, 正常退出
echo '$?的值'$? # $?的值0

# 获取脚本pid
echo $$
# $! 获取上一个在后台运行的脚本PID

# 获取命令行最后一个参数
echo $_

# 字符的匹配替换
url=www.baidu.com.cn
# #从前往后
[root@crab tmp]# echo ${url#*.}
# baidu.com.cn
[root@crab tmp]# echo ${url#*.*.}
# com.cn
[root@crab tmp]# echo ${url##*.}
# cn

# %从后往前
[root@crab tmp]# echo ${url%.*}
# www.baidu.com
[root@crab tmp]# echo ${url%%.*}
# www

# 整数运算
echo $((1+1))
echo $[1+2]

# 环境变量
export x=yes

# 获取用户输入
# read -p '请输入你的年龄: ' age
# echo 'age: '$age
```

文件判断

```shell
[root@crab tmp]# [ -e /etc/hosts ]
[root@crab tmp]# echo $?
0

[root@crab tmp]# test -f /etc/
[root@crab tmp]# echo $?
1

# -e 是否存在
# -f 是否是文件
# -d 目录
# -x 可执行
# -r 可读
# -w 可写
```

数值比较

```shell
# 整数运算
expr 1 + 2

[ 1 -ge 2 ]

# 多个比较
# -a and
# -o or
[ 10 -eq 10 -a 10 -gt 100 ] && echo 1 || echo 0
# 0

[ 10 -eq 10 -o 10 -gt 100 ] && echo 1 || echo 0
# 1
```

字符串比较

```shell
# 字符串比较要加双引号
[ "$USER" == "root" ] && echo 1 || echo 0
# 1

# -z 字符串长度为0,真
# -n 长度不为0,真
[ -z "USER" ] && echo 1 || echo 0
# 0
[ -n "USER" ] && echo 1 || echo 0
# 1
```

正则比对

```shell
# 正则比对, 两个 [[]]

[[ $USER =~ ^r ]] && echo 1 || echo 0
# 1
[[ ! $USER =~ ^1 ]] && echo 1 || echo 0
# 1
```

条件判断

```shell
# if命令执行成功then, else
if ls /
then
    echo '命令执行成功'
else
    echo '命令执行失败'
fi

# 条件测试语句, [  ]两边空格
# 字符串 = < >
x=yes
y=no
if [ $x = $y ]
then
    echo 'yes'
else
    echo 'no'
fi

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
```

循环语句

```shell
let i++

# for((j=0;j<=10;j++))
for i in `seq 1 10`
do
    echo $i
done
```

函数

```shell
# 函数, function可以不写
function foo(){
    echo 'foo里的$0' $0
    echo 'foo里的$1' $1
    echo 'foo里的$2' $2
    echo 'foo里的$#' $#
}

foo 1 2 3

test() {
    echo 100
    return 1
}
result=`test`
echo $?
# 1
echo $result
# 100
```

函数与循环实例

```shell
#!/bin/bash
menu(){
cat<<EOF
                1. help帮助
                2. 显示内存使用
                3. 显示磁盘使用
                4. 显示系统负载
                5. 显示登录用户
                6. 查看IP地址
                7. 查看Linux-version
                0. 退出
EOF
}
menu
while true
do
read -p "请输入要查看的系统编号:" num
case $num in
    1)
        menu
        ;;
    2)
        free -h
        ;;
    3)
        df -h
        ;;
    4)
        uptime
        ;;
    5)
        w;;
    6)
        curl cip.cc
        ;;
    7)
        cat /etc/redhat-release | awk '{print $(NF-1)}'
        ;;
    0)
        exit
        ;;
    *)
        menu
        ;;
esac
done
```

数组

```shell
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
# 获取索引
echo ${!name[@]}
# 遍历
for n in ${name[@]}
do
    echo $n
done

# 取消
unset name

# 字符串作为索引
declare -A name
name=([a]=aa [b]=bb [c]=cc)
```

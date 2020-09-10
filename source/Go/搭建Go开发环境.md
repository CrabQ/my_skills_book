# 搭建Go开发环境

[安装go](https://golang.google.cn/dl/)

## GOPROXY

```shell
go env -w GOPROXY=https://goproxy.cn,direct
```

## 跨平台编译

windows下编译一个linux下可执行文件

```shell
SET CGO_ENABLED=0  // 禁用CGO
SET GOOS=linux  // 目标平台是linux
SET GOARCH=amd64  // 目标处理器架构是amd64

# go build
```

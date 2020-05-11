# Dockerfile定制镜像

## Dockerfile

### Dockerfile概念

> Dockerfile是一个文本文件,包含了一条条的指令,每一条指令构建一层,基于基础镜像,最终构建出一个新的镜像
> Dockerfile -> build -> Docker Images -> run -> Docker Container

#### 执行流程

```shell
# Docker 从基础镜像运行一个容器
# 执行一条指令并对容器作出修改
# 执行类似 docker commit 的操作提交一个新的镜像层
# Docker 再基于刚提交的镜像运行一个新容器
# 执行 Dockerfile 中的下一条指令直到完成
```

#### 保留字指令

```shell
# FROM  基础镜像, 当前新镜像是基于哪个镜像的
# MAINTAINER  镜像维护者
# RUN 容器构建时需要运行的命令
# EXPOSE  当前容器对外暴露的端口号
# WORKDIR 指定在创建容器后, 终端默认登录的工作目录
# ENV 用来构建镜像过程中设置环境变量
# ADD 将宿主机目录下的文件拷贝进镜像且 ADD 命令自动处理 url 和解压 tar 包
# COPY  类似 ADD, 拷贝文件和目录到镜像中
# VOLUME  容器数据化, 保存数据和数据持久化
# CMD 指定容器运行时要启动的命令,可以有多个 CMD 指令, 但只有最后一个生效, CMD 会被 docker run 后面的参数代替
# ENTRYPOINT  指定容器运行时要启动的命令,ENTRYPOINT 的目的和 CMD 一样, 都是指定容器启动程序以及参数
# ONBUILD 当构建一个被继承的 Dockerfile 时运行命令, 父镜像被继承后, 父镜像 onbuild 被触发
```

## 第一部分:基础镜像信息

```shell
FROM nginx:2.17
```

## 第二部分:维护者信息

```shell
MAINTAINER docker_user docker_user@email.com
```

## 第三部分:镜像操作指令

```shell
ENV VERSION=1.0 DEBUG=on NAME="Happy Feet"
# 指定一个环境变量,会被后续RUN指令使用,并在容器运行时保持

ARG USERNAME=vscode
# 设置环境变量,不同的是ARG所设置环境变量只在构建镜像时有效

WORKDIR /app
# 后续的RUN、CMD、ENTRYPOINT指令配置工作目录,后续各层目录会被指定

USER root
# 同上WORKDIR,指定运行容器时的用户名或UID

RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
# 每运行一条RUN指令,镜像添加新的一层并提交

COPY hom* /mydir/
# 复制本地主机的<src>(Dockerfile 所在目录的相对路径)到容器中的<dest>

ADD hom* /mydir/
# 复制指定的<src>到容器中的<dest>,其中<src>可以是一个URL,tar文件会自动解压
# 建议解压缩情况下才使用,复制就只用COPY

VOLUME /data
# 创建挂载点指定某些目录挂载为匿名卷
# 在运行时如果用户不指定挂载,其应用也可以正常运行,不会向容器存储层写入大量数据

EXPOSE 80
# 暴露80端口,仅声明,不做端口映射

HEALTHCHECK --interval=5s --timeout=3s CMD curl -fs http://localhost/ || exit 1
# 健康检查
# 每5秒检查一次,超过3秒没响应就视为失败,使用 curl -fs http://localhost/ || exit 1 作为健康检查命令

ONBUILD COPY . /app/
# 当所创建的镜像作为其它新创建镜像的基础镜像时,执行的操作指令
```

## 第四部分:容器启动时执行指令

```shell
CMD ["nginx", "-g", "daemon off;"]
# CMD 容器启动命令
# Dockerfile只能有一条CMD命令多条的话只有最后一条会被执行
# 启动容器时候指定了运行的命令则会覆盖掉CMD指定的命令

ENTRYPOINT [ "curl", "-s", "https://ip.cn" ]
# 入口点
# 指定容器启动程序及参数
# 同上只能有一条ENTRYPOINT命令
# 当指定了ENTRYPOINT后,CMD命令将作为参数传给ENTRYPOINT指令
# <ENTRYPOINT> "<CMD>"
# 运行容器docker run myip -i
# 结果为: curl -s https://ip.cn -i

```

## 构建镜像

```shell
# 构建镜像, Dockerfile所在目录,
docker build -t 名称:标签 .
# .表示上下文路径

docker build http://server/context.tar.gz
# Docker引擎会下载这个包并自动解压缩.以其作为上下文开始构建

```

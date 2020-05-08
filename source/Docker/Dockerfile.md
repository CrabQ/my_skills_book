# Dockerfile

```shell
# 第一部分:基础镜像信息
# FROM python:3.6-buster

# 第二部分:维护者信息
# MAINTAINER docker_user docker_user@email.com

# 第三部分:镜像操作指令

# RUN ln -sf /dev/stdout /var/log/nginx/access.log
# 每运行一条RUN指令,镜像添加新的一层并提交

# USER
# 指定运行容器时的用户名或UID,后续的RUN也会使用指定用户

# ENV DEBIAN_FRONTEND=noninteractive
# 指定一个环境变量,会被后续RUN指令使用,并在容器运行时保持

# ARG USERNAME=vscode
# 设置环境变量,不同的是ARG所设置环境变量只在构建镜像时有效

# WORKDIR
# 后续的RUN、CMD、ENTRYPOINT指令配置工作目录

# VOLUME
# 创建挂载点

# COPY <src> <dest>
# 复制本地主机的<src>(Dockerfile 所在目录的相对路径)到容器中的<dest>

# ADD <src> <dest>
# 复制指定的<src>到容器中的<dest>,其中<src>可以是一个URL,tar文件会自动解压

# EXPOSE 80
# 暴露80端口

# ONBUILD ADD . /app/src
# 当所创建的镜像作为其它新创建镜像的基础镜像时,执行的操作指令

# 第四部分:容器启动时执行指令

# CMD ["nginx", "-g", "daemon off;"]
# Dockerfile只能有一条CMD命令多条的话只有最后一条会被执行
# 启动容器时候指定了运行的命令则会覆盖掉CMD指定的命令

# ENTRYPOINT
# 容器启动后执行的命令,只能有一条ENTRYPOINT命令多条的话只有最后一条会被执行
```

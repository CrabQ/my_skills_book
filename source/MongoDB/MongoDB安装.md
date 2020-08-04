# 安装MongoDB

## win 10安装MongoDB

下载

> [mongodb](https://www.mongodb.com/download-center/community)

```shell
# 安装路径
D:\program\program_database\MongoDB\Server\4.0\
# 新建数据储存目录
D:\program\program_database\MongoDB\Server\4.0\data\db
```

以管理员进入bin目录，设置mongodb服务

```shell
mongod --bind_ip 0.0.0.0 --logpath  "D:\program\program_database\MongoDB\Server\4.0\log\mongodb.log" --logappend --dbpath   "D:\program\program_database\MongoDB\Server\4.0\data\db" --port 27017 --serviceName  "MongoDB" --serviceDisplayName "MongoDB" --install
# 绑定 IP 为 0.0.0.0，即任意 IP 均可访问，指定日志路径、数据库路径、端口，指定服务名称
```

添加环境变量

```shell
D:\program\program_database\MongoDB\Server\4.0\bin
```

安装pymongo

```shell
pip3 install pymongo
```

安装robomongo(navicat12也可以链接MongoDB)
> [robomongo](https://robomongo.org/download)

## docker安装

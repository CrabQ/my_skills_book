# Centos7安装Mongodb
1. 下载

   ```shell
   wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.2.1.tgz
   ```

2. 解压移动

   ```shell
   tar -zxvf mongodb-linux-x86_64-rhel70-4.2.1.tgz
   # 移动到/usr/local/下
   mv  mongodb-linux-x86_64-rhel70-4.2.1 /usr/local/mongodb

   # 配置环境变量
   # vim /etc/profile
   # mongodb
   export PATH=$PATH:/usr/local/mongodb/bin

   # 创建数据存放文件夹和日志记录文件夹
   mkdir data
   mkdir logs
   ```

3. 配置

   ```shell
   # /usr/local/mongodb/bin目录下
   # vim mongodb.conf
   dbpath = /usr/local/mongodb/data/
   logpath = /usr/local/mongodb/logs/mongodb.log
   port = 27017
   fork = true #已守护进程方式启用
   auth=true #安全认证
   bind_ip=0.0.0.0 #允许远程访问
   ```

4. 启动

   ```shell
   # /usr/local/mongodb/bin目录下
   ./mongod -f mongodb.conf
   # 关闭
   ./mongod  --shutdown
   ```
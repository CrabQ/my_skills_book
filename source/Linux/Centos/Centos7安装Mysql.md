# Centos7安装Mysql

## yum按照

1. 卸载默认安装的mariadb：

   ```shell
   yum remove mariadb.x86_64
   ```

2. 获取mysql官方yum源

   ```shell
   wget https://repo.mysql.com//mysql80-community-release-el7-3.noarch.rpm
   ```

3. 本地安装yum源

   ```shell
   yum localinstall mysql80-community-release-el7-3.noarch.rpm
   ```

4. 使用yum安装

   ```shell
   yum install mysql-community-server.x86_64
   ```

5. 启动mysql

   ```shell
   service mysqld start
   ```

6. 查找默认登录密码

   ```shell
   cat /var/log/mysqld.log | grep password
   ```

7. 登录修改默认密码

   ```shell
   mysql -u root -p

   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new password';
   ```

## 源码包安装

```shell
# 下载
wget https://cdn.mysql.com/archives/mysql-8.0/mysql-8.0.18-el7-x86_64.tar.gz

# 解压
tar -zxvf mysql-8.0.18-el7-x86_64.tar.gz

# 移动
mv mysql-8.0.18-el7-x86_64 /usr/local/mysql
```
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
wget http://mirrors.sohu.com/mysql/MySQL-8.0/mysql-8.0.18-el7-x86_64.tar.gz

# 解压
tar -zxvf mysql-8.0.18-el7-x86_64.tar.gz

# 移动
mv mysql-8.0.18-el7-x86_64 /usr/local/mysql

# 配置环境变量
echo 'export PATH=$PATH:/usr/local/mysql/bin' >> /etc/profile
source /etc/profile

# 建立mysql用户和组
useradd mysql

# 创建相关目录并修改权限
mkdir -p /root/mysql/3306/data
chown -R mysql.mysql /usr/local/mysql
chown -R mysql.mysql /root/mysql
chmod -R 755 /root/mysql/3306/data

# 初始化数据
/usr/local/mysql/bin/mysqld --initialize-insecure --user=root --basedir=/usr/local/mysql --datadir=/root/mysql/3306/data

# 添加mysql启动到本地服务
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql.server

# 使用systemd管理mysql
cat > /etc/systemd/system/mysqld_3306.service <<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql/bin/mysqld --defaults-file=/root/mysql/3306/my.cnf
LimitNOFILE = 5000
EOF

# 启动
systemctl start mysqld_3306.service

# 报错
# Starting MySQL.Logging to '/usr/local/mysql/data/izbp128jigdcjx00os4h3sz.err'.
# . ERROR! The server quit without updating PID file (/usr/local/mysql/data/izbp128jigdcjx00os4h3sz.pid).
```

## 安装mysql5.173

```shell
# 下载
wget http://dev.mysql.com/get/Downloads/MySQL-5.1/mysql-5.1.73.tar.gz
# 解压
tar -xvf mysql-5.1.73.tar.gz
cd mysql-5.1.73

# 安装相关依赖
yum install ncurses ncurses-devel
yum install -y gcc-c++*

# 编译到指定目录
./configure  '--prefix=/app/mysql5.1.73' '--without-debug' '--with-charset=utf8' '--with-extra-charsets=all' '--enable-assembler' '--with-pthread' '--enable-thread-safe-client' '--with-mysqld-ldflags=-all-static' '--with-client-ldflags=-all-static' '--with-big-tables' '--with-readline' '--with-ssl' '--with-embedded-server' '--enable-local-infile' '--with-plugins=innobase' CXXFLAGS="-Wno-narrowing -fpermissive"
# 安装
make
make install

# 复制配置文件 自启动文件 自启动
cp support-files/my-medium.cnf /app/mysql5.1.73_data/my.cnf
# cp -r support-files/mysql.server /etc/init.d/5.1.73_mysqld
# /sbin/chkconfig --del 5.1.73_mysqld
# /sbin/chkconfig --add 5.1.73_mysqld
# /sbin/chkconfig mysqld on

# 修改权限
chown -R mysql:mysql /app/mysql5.1.73 /app/mysql5.1.73_data
# 初始化mysql
/app/mysql5.1.73/bin/mysql_install_db --user=mysql --basedir=/app/mysql5.1.73 --datadir=/app/mysql5.1.73_data/data/

# 添加执行权限
# chmod a+wrx /etc/init.d/5.1.73_mysqld
# /etc/init.d/5.1.73_mysqld start

# 启动
/app/mysql5.1.73/bin/mysqld_safe --defaults-file=/app/mysql5.1.73_data/my.cnf &

# root添加密码
/app/mysql5.1.73/bin/mysqladmin -S /app/mysql5.1.73_data/mysql.sock -h localhost -u root password 'root'
# chmod a+wrx /etc/init.d/mysql
# service mysqld start

# 测试登录
/app/mysql5.1.73/bin/mysql -S /app/mysql5.1.73_data/mysql.sock -u root -p

# 使用systemd管理mysql
vim /etc/systemd/system/mysqld_5.1.173.service
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=mysql
Group=mysql
ExecStart=/app/mysql5.1.73/bin/mysqld_safe --defaults-file=/app/mysql5.1.73_data/my.cnf
LimitNOFILE = 10000

```

# Centos7安装apache+mod_wsgi并配置django

1. 安装apache

    ```shell
    yum install httpd-devel -y
    # 启动
    systemctl start httpd
    # 开机启动
    systemctl enable httpd
    ```

2. 编译安装mod_wsgi

    > [Quick Installation Guide](https://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html)

   ```shell
   # 下载
   wget https://codeload.github.com/GrahamDumpleton/mod_wsgi/tar.gz/4.6.5
   # 解压
   tar zxfv 4.6.5

   # 进入目录编译安装
   ./configure --with-apxs=/usr/bin/apxs \
     --with-python=/home/envs/my_blog/bin/python
   make
   make install
   ```

3. 配置apache

   ```shell
   # /etc/httpd/conf/httpd.conf
   # 文件最后加入
   LoadModule wsgi_module modules/mod_wsgi.so

   <VirtualHost *:80>
       WSGIDaemonProcess my_blog python-home=/home/envs/my_blog/ python-path=/home/my_blog
       WSGIProcessGroup my_blog
       WSGIScriptAlias / /home/my_blog/my_blog/wsgi.py

       <Directory /home/my_blog/my_blog> #设置项目目录访问权限
           <Files wsgi.py>
               Require all granted
           </Files>
       </Directory>

       #设置静态文件夹目录
       Alias /static/ /home/my_blog/static_collected/
       <Directory /home/my_blog/static_collected> #设置静态文件目录访问权限
           Require all granted
       </Directory>

       #设置媒体文件目录
       Alias /media/ /home/my_blog/media/
       <Directory /home/my_blog/media> #设置媒体文件访问权限
           Require all granted
       </Directory>

       Alias /favicon.ico /home/my_blog/favicon.ico
       <Directory /home/my_blog>
           <Files favicon.ico>
               Require all granted
           </Files>
       </Directory>

   </VirtualHost>
   ```

4. 重启apache

   ```shell
   systemctl restart httpd
   ```

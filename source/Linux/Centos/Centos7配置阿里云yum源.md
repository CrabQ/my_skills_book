# Centos7配置阿里云yum源

1. 进入centos的yum文件夹，用wget下载repo文件

   ```shell
   cd  /etc/yum.repos.d/
   wget  http://mirrors.aliyun.com/repo/Centos-7.repo
   ```

2. 备份系统原来的repo文件

   ```shell
   mv CentOS-Base.repo CentOS-Base.repo.bak
   ```

3. 替换系统原理的repo文件

   ```shell
   mv Centos-7.repo CentOs-Base.repo
   ```

4. yum源更新

   ```shell
   yum clean all
   yum makecache
   yum update
   ```

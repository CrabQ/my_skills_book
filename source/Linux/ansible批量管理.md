# ansible批量管理

```shell
# 基于sshd, 先要确保sshd秘钥分发完成
# 1. 安装
yum install -y ansible

# 2. 编写主机管理清单
# vim /etc/ansible/hosts
[rsync:children]
rsync_server
rsync_client

[rsync_server]
172.16.245.27

[rsync_client]
172.16.245.1
172.16.245.2

# 3. 测试
ansible all -a 'hostname'

# 模块的应用语法格式:
# ansible 主机名称/主机组名称/主机地址信息/all -m(指定应用的模块信息) 模块名称 -a(指定动作信息) '执行动作'

# 模块:
script  批量执行本地脚本
copy    批量分发传输数据信息
fetch   将远程主机数据进行拉去到本地管理主机
yum     安装卸载软件包
service 管理服务运行状态
user    批量创建用户并设置密码信息
mount   批量挂载操作
cron    批量部署定时任务信息
ping    远程管理测试模块
```

## 剧本

```shell
# 组成(paly部分: 定义主机信息和变量等信息, task部分: 定义需要完成的任务信息)
- host: all
  remoto_user: root
  vars:
    file_name:crab_file
  tasks:
    - name: touch new files
     shell: touch /tmp/{{file_name}}

# 执行步骤
# 1. 语法检查
ansible-palybook --syntax-check rsync.yaml
# 2. 模拟执行
ansible-palybook -C rsync.yaml
# 3. 执行
ansible-palybook rsync.yaml
```

主机清单

```shell
# /etc/ansible/hosts
[rsync:children]
rsync_server
rsync_client

[rsync_server]
172.16.245.27

[rsync_client]
172.16.245.1
172.16.245.2
```

剧本

```yaml
- hosts: rsync_server
  vars:
    backupdir: /backup01
    passfile: rsync.password
  tasks:
    - name: 01-install rsync
      yum: name=rsync state=installed
    - name: 02-push conf file
      copy: src=/etc/ansible/server_file/rsync_server/rsyncd.conf dest=/etc/
    - name: 03-create user
      user: name=rsync craate_home=no shell=/sbin/nologin
    - name: 04-create backup dir
      file: path={{backupdir}} state=directory owner=rsync group=rsync
    - name: 05-create password file
      copy: content=rsync_backup:crab123 dest=/etc/{{rsync.password}} mode=600
    - name: -6-start rsync server
      service: name=rsyncd state=started enabled=yes
```


# Docker开启远程访问

修改配置文件

```shell
# vi /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock
```

重新读取配置文件,重新启动docker服务

```shell
systemctl daemon-reload
systemctl restart docker
```

查看是否开启成功

```shell
curl http://127.0.0.1:2375/info
```

如果无法连接,很大可能是防火墙的问题,启动防火墙,并配置端口开放

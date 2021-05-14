# VS code配置

## 配置

> [vscode_settings](https://github.com/CrabQ/my_skills_book/blob/master/source/VS%20code/vscode_settings.json)

## 插件安装

remote-ssh

```shell
# 配置config
ssh-keygen -t rsa -C "your email"
# 获取生成的id_ras.pub上传到服务器
~/.ssh/authorized_keys
# 连接
```

## markdown定义图片缩放

```shell
# 扩展 Markdown Parser
运行 Markdown Preview Enhanced: Extend Parser 命令
然后 parser.js 文件
# 替换为

onWillParseMarkdown: function(markdown) {
    return new Promise((resolve, reject)=> {
      markdown = markdown.replace(/\!\[([1-9]?[1-9]?[0-9])\%\]\(([\w\W]+?)\)/gm, (c0, c1,c2) =>'\<img style\=\"width: '+c1+'\%\" src\=\"'+c2+'\"  alt=\"\" align\=center \/\>');
      return resolve(markdown)
    })
  },

# 图片写法
![80%](.assets/wait.png)
```

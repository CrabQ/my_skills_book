### git学习笔记
> [廖雪峰的Git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
#### 基础

```python
# 初始化git仓库
git init

git config --global user.name "oldestcrab"

git config --global user.email "oldestcrab@gmail.com"

# 查看远程库信息
git remote

# 删除远程库origin信息
git remote remove origin

# 已有的本地仓库与远程库关联
git remote add origin git@github.com:oldestcrab/mybooks.git

# 把当前分支master推送到远程master,-u参数,把本地的master分支和远程的master分支关联起来,后续可不用-u参数
git push -u origin master

# 拉取远程仓库到master分支
git pull origin master

# 从远程库拉取仓库到本地
git clone git@github.com:oldestcrab/by_scrapy.git

git status

git add

git commit -m 'first commit'

git log --graph

# 查看difference
git diff README.md

# 撤销还没有add进暂存区的文件改动
git checkout a.md

# 版本回退,HEAD表示当前版本,上一个版本就是HEAD^,上上一个版本就是HEAD^^
git reset --hard HEAD

# 通过commit id回退
git reset --hard 1094a

# 查看命令历史
git reflog

# 丢弃工作区的修改,即让这个文件回到最近一次git commit或git add时的状态
git checkout -- README.md

# 暂存区的修改撤销掉(unstage),重新放回工作区
git reset HEAD README.md

# 删除文件
git rm
git commit

# 恢复误删文件(只能恢复文件到最新版本,你会丢失最近一次提交后你修改的内容)
git checkout -- README.md

# 暂存当前工作
git stash

# 查看暂存的工作
git stash list

# 恢复暂存的工作(用git stash apply恢复,但是恢复后,stash内容并不删除,你需要用git stash drop来删除)
# 恢复的同时把stash内容也删了
git stash pop

# 恢复指定的暂存工作
git stash apply stash@{0}

```
#### 分支
> 合并dev分支，--no-ff参数，表示禁用Fast forward，简单地说就是 -no-ff 模式进行了一次新的 git commit 操作。合并分支时，加上--no-ff参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并。而fast forward合并就看不出来曾经做过合并，它是直接把 master 的指针直接指向了 dev 分支的最新提交。
```python
# 查看当前分支 
git branch

# 新建分支dev 
git branch dev

# 切换到dev分支 
git checkout dev

# 新建分支dev并切换当前分支为dev
git checkout -b dev

# 默认使用fast forward模式合并分支dev到主分支,注意当前分支应为主分支
git merge dev

# 使用普通模式合并dev分支
git merge --no-ff -m "merge with no-ff" dev

# 删除dev分支 
git branch -d dev

# 强制删除dev分支
git branch -D dev

# 推送分支dev
git push origin dev

# 本地已有分支设置关联并推送到远程分支(尚未创建的分支)
git push --set-upstream origin dev

# 基于远程分支创建本地分支,本地和远程分支的名称最好一致
git checkout -b dev origin/dev
  
# 建立本地分支和远程分支的关联
# git branch --set-upstream-to=origin/远程分支的名字 本地分支的名字
git branch --set-upstream-to=origin/dev dev
```

#### 标签
> 创建的标签都只存储在本地，不会自动推送到远程
```python
# 新建标签v1.0,默认为HEAD,也可以指定一个commit id
git tag v1.0

# 指定标签v1.0信息
git tag -a v1.0 -m "blablabla..."

# 查看所有标签信息
git tag

# 查看标签说明
git show v1.0

# 切换到tagv1.0
git checkout v1.0

# 推送一个本地标签v1.0
git push origin v1.0

# 推送全部未推送过的本地标签
git push origin --tags

# 删除一个本地标签v1.5
git tag -d v1.5

# 删除一个远程标签
git push origin :refs/tags/v1.5
```

#### 忽略文件
> 忽略某些文件时，在Git工作区的根目录下创建一个特殊的`.gitignore`文件，`.gitignore`文件本身要放到版本库里，并且可以对.gitignore做版本管理！

```python
# 忽略所有` .a `结尾的文件
*.a

# 但` lib.a `除外
!lib.a

# 仅仅忽略项目根目录下的 `TODO `文件,不包括 `subdir/TODO`
/TODO

#忽略 `build/ `目录下的所有文件
build/

#会忽略` doc/notes.txt `但不包括` doc/server/arch.txt`
doc/*.txt

```

.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。那么解决方法就是先把本地缓存删除（改变成未track状态），然后再提交：
``` git
git rm -r --cached test/

git commit -m 'update .gitignore 忽略已track的test'

git push origin master

```
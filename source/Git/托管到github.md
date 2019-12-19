# 托管到github
> [从0开始学习 GitHub 系列之「向GitHub 提交代码」](https://mp.weixin.qq.com/s?__biz=MzA4NTQwNDcyMA==&mid=2650661821&idx=1&sn=c6116ed82bff2d083bb152fbd8cbc38d&scene=21#wechat_redirect)
1. 生成SSH key,把`id_rsa.pub`的内容复制到github上
```python
ssh-keygen -t rsa
```
2. GitHub 上添加 SSH key
```python
# 测试
ssh -T git@github.com
```
3. 设置用户名与邮箱
```python
git config --global user.name "CrabQ"
git config --global user.email "18819425701@163.com"

```
4. 关联远程仓库
```python
# 克隆远程仓库
git clone git@github.com:CrabQ/my_skills_book.git

# 关联本地项目并推送到远程
git remote add origin https://github.com/CrabQ/my_skills_book.git
git push -u origin master
```

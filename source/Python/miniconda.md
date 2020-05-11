# miniconda

## conda基础命令

```shell
# 创建环境
conda create -n py36 python=3.6.8

# 查看环境列表
conda info -e
conda env list

# 激活环境
activate py36
# linux激活环境
source activate py36

# 退出环境
conda deactivate

# 删除环境
conda remove -n py36 --all
conda env remove -n py36

# 安装包
conda install requests

# 查看已安装包列表
conda list

# 更新包
conda update requests

# 删除包
conda remove requests

# 更新conda
conda update conda
# 更新conda应用
conda update miniconda
# 更新python到最新版
conda udpate python
```

## 修改镜像地址

```shell
# ~/.condarc
# 添加镜像源
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/

# 查看已安装镜像
conda config --show

# 删除镜像
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

# 恢复原镜像
conda config --remove-key channels
```

import os
import shutil
import re

def classify(root_dir):

    # 复制所有文件到根目录下

    count = 1
    for home, dirs, files in os.walk(root_dir):
        # 获取根目录下的所有文件
        for f in files:
            # 拼接原来的文件路径
            old_file_dir = os.path.join(home, f)
            # 获取文件类型
            file_type = f.split('.')[-1]
            # 拼接新的文件路径
            new_file_dir = root_dir + '/' + str(count) + '.' + file_type
            # 重命名并移动文件
            if not os.path.exists(new_file_dir):
                os.rename(old_file_dir, new_file_dir)
                count += 1


    # 删除根目录下的所有文件夹

    for f in os.listdir(root_dir):
        f_dir = os.path.join(root_dir, f)
        if os.path.isdir(f_dir):
            # 删除非空文件夹
            shutil.rmtree((f_dir))


    # 每30个文件放入一个文件夹

    new_file_list = os.listdir(root_dir)
    # 对文件进行排序
    # new_file_list = sorted(new_file_list, key = lambda i:int(re.match(r'(\d+)',i).group()))
    new_file_list.sort( key = lambda i:int(re.match(r'(\d+)',i).group()))
    new_count = 1
    for f in range(0, len(new_file_list), 30):
        # 新建子文件夹
        new_dir = os.path.join(root_dir, str(new_count))
        os.mkdir(new_dir)

        # 移动文件
        stop = min(len(new_file_list), f+30)
        for i in range(f, stop):
            file_name = os.path.join(root_dir, new_file_list[i])
            shutil.move(file_name, new_dir)

        new_count += 1

if __name__ == "__main__":
    root_dir = 'C:/Users/crab/Desktop/123'
    classify(root_dir)

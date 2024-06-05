import os

def rename_directories(root_path):
    # 遍历根目录
    for dir_name in os.listdir(root_path):
        # 构造完整的目录路径
        dir_path = os.path.join(root_path, dir_name)
        # 检查这个路径是否确实是一个目录
        if os.path.isdir(dir_path):
            # 用下划线替换空格
            new_dir_name = dir_name.replace(" ", "_")
            new_dir_path = os.path.join(root_path, new_dir_name)
            # 重命名目录
            os.rename(dir_path, new_dir_path)
            print(f"Renamed '{dir_name}' to '{new_dir_name}'")

# 使用示例
root_path = "val"  # 将此路径替换为你的目标目录路径
rename_directories(root_path)

import os
os.makedirs("text", exist_ok=True)
# 创建递归文件夹
# exist_ok=True：如果目标目录已存在，不抛 FileExistsError（默认 False 时会报错）
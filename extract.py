import os
import sys

# 检查输入文件是否存在
input_file = "data/word_out.txt"
output_file = "data/word_result.txt"

if not os.path.exists(input_file):
    print(f"输入文件 {input_file} 不存在.")
else:
    with open(input_file, "r", encoding="utf-8") as file:
        raw_data = file.readlines()

    # 获取从 main.py 传递过来的种子关键字参数
    seed_keywords = sys.argv[1:]

    # 创建一个字典来存储与每个关键字相关的搜索信息
    keyword_data = {keyword: [] for keyword in seed_keywords}

    # 遍历原始数据，查找包含种子关键字的信息
    for line in raw_data:
        for keyword in seed_keywords:
            if keyword in line:
                keyword_data[keyword].append(line.strip())

    with open(output_file, "w", encoding="utf-8") as f:
        for keyword, data in keyword_data.items():
            f.write(f"与关键字 '{keyword}' 相关的数据:\n")
            for item in data:
                f.write(item + "\n")
    print(f"数据已写入文件 {output_file}.")

import os

# 定义文件路径
input_file = "data/word_out.txt"
output_file = "data/word_result.txt"

# 检查输入文件是否存在
if not os.path.exists(input_file):
    print(f"输入文件 {input_file} 不存在.")
else:
    # 读取原始数据文件
    with open(input_file, "r", encoding="utf-8") as file:
        raw_data = file.readlines()

    # 定义种子关键字
    seed_keywords = ["柔和双沟", "女生", "中财网首页", "曹云金", "笑傲江湖电视剧"]

    # 创建一个字典来存储与每个关键字相关的搜索信息
    keyword_data = {keyword: [] for keyword in seed_keywords}

    # 遍历原始数据，查找包含种子关键字的信息
    for line in raw_data:
        for keyword in seed_keywords:
            if keyword in line:
                keyword_data[keyword].append(line.strip())

    # 将结果保存到文件，如果输出文件不存在，将自动创建它
    with open(output_file, "w", encoding="utf-8") as f:
        for keyword, data in keyword_data.items():
            f.write(f"与关键字 '{keyword}' 相关的数据:\n")
            for item in data:
                f.write(item + "\n")
    print(f"数据已写入文件 {output_file}.")

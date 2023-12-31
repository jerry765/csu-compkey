import os
import sys
import jieba
from pypinyin import lazy_pinyin

# 检查输入文件是否存在
input_file = "data/word_out.txt"

if not os.path.exists(input_file):
    print(f"输入文件 {input_file} 不存在.")
else:
    with open(input_file, "r", encoding="utf-8") as file:
        raw_data = file.readlines()

    # 获取从 main.py 传递过来的种子关键词参数
    seed_keywords = sys.argv[1:]

    # 创建一个字典，用于存储与每个关键字相关的搜索信息
    keyword_data = {keyword: [] for keyword in seed_keywords}

    # 遍历原始数据，查找包含种子关键词的信息
    for line in raw_data:
        for keyword in seed_keywords:
            if keyword in line:
                # 使用jieba分词器对匹配的行进行分词
                segments = jieba.lcut(line.strip())
                keyword_data[keyword].append(segments)

    # 根据关键词生成文件名（使用拼音）
    for keyword, data in keyword_data.items():
        # 使用拼音作为文件名
        pinyin_name = ''.join(lazy_pinyin(keyword))
        output_file = f"word_output/word_result_{pinyin_name}.txt"
        print(f"正在生成文件：{output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            for item in data:
                # 将分词后的内容写入文件
                f.write(" ".join(item) + "\n")
        print(f"数据与关键字 '{keyword}' 相关的数据已写入文件 {output_file}.")


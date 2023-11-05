import os
import sys
from pypinyin import lazy_pinyin
import concurrent.futures
import re
import jieba

# 检查输入文件是否存在
input_file = "data/word_out.txt"

if not os.path.exists(input_file):
    print(f"输入文件 {input_file} 不存在.")
    sys.exit(1)

# 获取从 main.py 传递过来的种子关键词参数
seed_keywords = sys.argv[1:]

# 创建一部字典，用于存储与每个关键字相关的搜索信息
keyword_data = {keyword: [] for keyword in seed_keywords}

# 使用正则表达式合并所有关键词为一个模式
keywords_pattern = re.compile("|".join(map(re.escape, seed_keywords)))


# 并发处理每一行
def process_lines(lines):
    for line in lines:
        # 使用jieba分词器对匹配的行进行分词
        keyword_segments = jieba.lcut(line.strip())
        for keyword in seed_keywords:
            if keyword in line:
                keyword_data[keyword].append(keyword_segments)


with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

chunk_size = len(lines) // 10  # 调整块的大小
chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]

# 使用线程池并行处理每个块
with concurrent.futures.ThreadPoolExecutor() as executor:
    for chunk in chunks:
        executor.submit(process_lines, chunk)

# 根据关键词生成文件名（使用拼音）
def write_keyword_data(keyword, data):
    pinyin_name = ''.join(lazy_pinyin(keyword))
    output_file = f"word_output/word_result_{pinyin_name}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for keyword_segments in data:
            # 将分词后的关键词写入文件
            f.write(" ".join(keyword_segments) + "\n")
    print(f"数据与关键字 '{keyword}' 相关的数据已写入文件 {output_file}.")

# 并发写入数据
with concurrent.futures.ThreadPoolExecutor() as executor:
    for keyword, data in keyword_data.items():
        executor.submit(write_keyword_data, keyword, data)

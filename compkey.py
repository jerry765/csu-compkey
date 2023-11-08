import os
import sys

from pypinyin import lazy_pinyin


def calculate_competitive_keywords(tfidf_scores):
    # 根据TF-IDF分数排序关键词
    sorted_keywords = sorted(tfidf_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_keywords


def read_tfidf_scores(output_dir, keyword):
    # 将关键词转换为拼音
    keyword_pinyin = ''.join(lazy_pinyin(keyword))
    # 根据新的目录和文件命名规则构建文件路径
    output_file_path = os.path.join(output_dir, f'tfidf_{keyword_pinyin}.txt')

    tfidf_scores = {}
    with open(output_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                word, score = parts
                tfidf_scores[word] = float(score)

    return tfidf_scores


def write_competitive_keywords(output_dir, keyword, competitive_keywords):
    # 将关键词转换为拼音
    keyword_pinyin = ''.join(lazy_pinyin(keyword))
    output_file_path = os.path.join(output_dir, f'compete_{keyword_pinyin}.txt')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for word, weight in competitive_keywords:
            file.write(f"{word}: {weight}\n")


# 设置文件夹路径
tfidf_output_dir = 'tfidf_output'  # 修改为正确的输入目录

# 确保compete_output目录存在
compete_output_dir = 'compete_output'
if not os.path.exists(compete_output_dir):
    os.makedirs(compete_output_dir)

# 关键词列表
keywords = sys.argv[1:]

# 对于列表中的每个关键词读取TF-IDF权重并计算竞争性关键词
for keyword in keywords:
    tfidf_scores = read_tfidf_scores(tfidf_output_dir, keyword)
    competitive_keywords = calculate_competitive_keywords(tfidf_scores)
    write_competitive_keywords(compete_output_dir, keyword, competitive_keywords)

    # 打印结果的路径
    print(f"关键词 '{keyword}' 的竞争性关键词及权重已写入: {compete_output_dir}/compete_{''.join(lazy_pinyin(keyword))}.txt")

import os
import sys
from pypinyin import lazy_pinyin
import mysql.connector

def calculate_competitive_keywords(tfidf_scores):
    sorted_keywords = sorted(tfidf_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_keywords

def read_tfidf_scores(output_dir, keyword):
    keyword_pinyin = ''.join(lazy_pinyin(keyword))
    output_file_path = os.path.join(output_dir, f'tfidf_{keyword_pinyin}.txt')

    tfidf_scores = {}
    with open(output_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                word, score = parts
                tfidf_scores[word] = float(score)
    return tfidf_scores

def get_db_config(filename):
    config = {}
    with open(filename, 'r', encoding="utf-8") as file:
        for line in file:
            if line.startswith('#') or '=' not in line:
                continue
            key, value = line.strip().split('=', 1)
            config[key.strip()] = value.strip()
    return config

def write_competitive_keywords_to_db(db_config, keyword, competitive_keywords):
    conn = mysql.connector.connect(
        host=db_config['db_host'],
        user=db_config['db_user'],
        password=db_config['db_password'],
        database=db_config['db_name']
    )
    cursor = conn.cursor()

    cursor.execute("INSERT INTO SeedKeyword (Keyword) VALUES (%s)", (keyword,))
    seed_keyword_id = cursor.lastrowid

    for word, weight in competitive_keywords:
        cursor.execute("INSERT INTO CompetitiveKeyword (SeedKeywordID, Keyword, CompetitiveScore) VALUES (%s, %s, %s)",
                       (seed_keyword_id, word, weight))

    conn.commit()
    cursor.close()
    conn.close()

# 设置文件夹路径
tfidf_output_dir = 'tfidf_output'  # 修改为正确的输入目录

# 读取数据库配置
db_config = get_db_config('config.ini')

# 关键词列表
keywords = sys.argv[1:]

# 主要逻辑
for keyword in keywords:
    tfidf_scores = read_tfidf_scores(tfidf_output_dir, keyword)
    competitive_keywords = calculate_competitive_keywords(tfidf_scores)
    write_competitive_keywords_to_db(db_config, keyword, competitive_keywords)
    print(f"关键词 '{keyword}' 的竞争性关键词及权重已写入数据库")

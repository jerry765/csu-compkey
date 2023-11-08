import os
import sys

import jieba
from pypinyin import lazy_pinyin
from sklearn.feature_extraction.text import TfidfVectorizer

input_dir = 'word_output'
output_dir = 'tfidf_output'
stop_words_file = 'data/stop_words.txt'
keywords = sys.argv[1:]


# 定义加载停用词的函数
def load_stop_words(stop_words_file):
    with open(stop_words_file, 'r', encoding='utf-8') as f:
        stop_words = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
    return stop_words


# 加载停用词
stop_words = load_stop_words(stop_words_file)

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# 定义从文件中读取文档的函数，并去除关键词
def read_and_preprocess_documents(input_dir, keyword_pinyin):
    input_file_path = os.path.join(input_dir, f'word_result_{keyword_pinyin}.txt')
    documents = []
    if os.path.exists(input_file_path):
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 使用jieba进行分词，并去除停用词和关键词
                clean_line = ' '.join([word for word in jieba.cut(line.strip()) if word not in stop_words])
                if clean_line:
                    documents.append(clean_line)
    else:
        print(f"文件 {input_file_path} 不存在.")
    return documents


# 定义计算TF-IDF的函数
def calculate_tfidf(documents):
    tfidf_vectorizer = TfidfVectorizer(min_df=0.01, max_df=0.95, binary=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    return tfidf_matrix, tfidf_vectorizer.get_feature_names_out()


# 定义将TF-IDF结果写入文件的函数
def write_tfidf_to_file(output_dir, keyword_pinyin, tfidf_matrix, feature_names):
    output_file_path = os.path.join(output_dir, f'tfidf_{keyword_pinyin}.txt')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for doc_index in range(tfidf_matrix.shape[0]):
            for word_idx in tfidf_matrix[doc_index].indices:
                word = feature_names[word_idx]
                score = tfidf_matrix[doc_index, word_idx]
                if score < 1.0:  # 只写入小于1.0的分数
                    file.write(f"{word}: {score}\n")


# 对每个关键词处理
for keyword in keywords:
    keyword_pinyin = ''.join(lazy_pinyin(keyword))
    documents = read_and_preprocess_documents(input_dir, keyword_pinyin)
    if documents:
        tfidf_matrix, feature_names = calculate_tfidf(documents)
        write_tfidf_to_file(output_dir, keyword_pinyin, tfidf_matrix, feature_names)
        print(f"完成关键词 '{keyword}' 的TF-IDF计算并已保存到文件。")


# 主程序入口
# if __name__ == "__main__":
#     input_dir = 'word_output'
#     output_dir = 'tfidf_output'
#     stop_words_file = 'data/stop_words.txt'
#     keywords = ['郭德纲', '女']
#
#     # 加载停用词
#     stop_words = load_stop_words(stop_words_file)
#
#     # 确保输出目录存在
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     # 对每个关键词处理
#     for keyword in keywords:
#         keyword_pinyin = ''.join(lazy_pinyin(keyword))
#         documents = read_and_preprocess_documents(input_dir, keyword_pinyin)
#         if documents:
#             tfidf_matrix, feature_names = calculate_tfidf(documents)
#             write_tfidf_to_file(output_dir, keyword_pinyin, tfidf_matrix, feature_names)
#             print(f"完成关键词 '{keyword}' 的TF-IDF计算并已保存到文件。")

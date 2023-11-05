import math
import os
import jieba
import re


def load_data(data_folder):
    data = {}

    for filename in os.listdir(data_folder):
        keyword = re.match(r'word_result_(.*?)\.txt', filename)
        if keyword:
            keyword = keyword.group(1)
        else:
            continue

        try:
            with open(os.path.join(data_folder, filename), "r", encoding="utf-8") as file:
                lines = file.readlines()
            data[keyword] = [line.strip() for line in lines]
        except UnicodeDecodeError:
            print(f"Skipping file {filename} due to encoding issue.")
            continue

    return data


def calculate_mutual_information(data, seed_keywords, intermediate_keyword):
    seed_count = 0
    intermediate_count = 0
    common_count = 0

    # 计算seed关键词的总出现次数
    for keyword in seed_keywords:
        seed_count += sum(1 for line in data[keyword] if keyword in line)

    # 计算intermediate关键词的出现次数
    intermediate_count = sum(1 for line in data[intermediate_keyword] if intermediate_keyword in line)

    # 计算seed和intermediate关键词共同出现的次数
    common_count = sum(
        1 for keyword in seed_keywords if keyword in line and intermediate_keyword in line for line in
        data[keyword])

    # 添加拉普拉斯平滑
    smoothing_factor = 0.5
    p_x_y = (common_count + smoothing_factor) / (len(data[seed_keywords[0]]) + smoothing_factor * len(seed_keywords))
    p_x = (seed_count + smoothing_factor) / (len(data[seed_keywords[0]]) + smoothing_factor * len(seed_keywords))
    p_y = (intermediate_count + smoothing_factor) / (len(data[intermediate_keyword]) + smoothing_factor)

    mutual_information = p_x_y * math.log2(p_x_y / (p_x * p_y))

    return mutual_information


def get_intermediate_keywords(data, seed_keywords, n):
    # 创建一个字典，用于存储中介关键词及其互信息分数
    mi_scores = {}

    for intermediate_keyword in data:
        if intermediate_keyword not in seed_keywords:  # 排除中介关键词中的种子关键词
            mi_score = calculate_mutual_information(data, seed_keywords, intermediate_keyword)
            mi_scores[intermediate_keyword] = mi_score

    # 按互信息分数降序排序中介关键词
    sorted_intermediate_keywords = sorted(mi_scores, key=lambda x: -mi_scores[x])

    # 选择前n个中介关键词
    top_intermediate_keywords = sorted_intermediate_keywords[:n]

    print("Top Intermediate Keywords:", top_intermediate_keywords)
    return top_intermediate_keywords


def calculate_competitiveness(data, seed_keyword, intermediate_keyword):
    seed_lines = data[seed_keyword]
    intermediate_lines = data[intermediate_keyword]

    seed_count = sum(1 for line in seed_lines if seed_keyword in line)
    intermediate_count = sum(1 for line in intermediate_lines if intermediate_keyword in line)
    common_count = sum(1 for line in seed_lines if seed_keyword in line and intermediate_keyword in line)

    if seed_count == 0:
        competitiveness = 0
    else:
        competitiveness = common_count / seed_count

    return competitiveness


def compkey(seed_keywords, n):
    data_folder = "word_output"  # 存放每个关键字数据文件的文件夹
    output_folder = "intermediate_output"  # 存放中介关键字文件的文件夹

    data = load_data(data_folder)
    intermediate_keywords = get_intermediate_keywords(data, seed_keywords, n)

    competitiveness_data = []

    for seed_keyword in seed_keywords:
        for intermediate_keyword in intermediate_keywords:
            competitiveness = calculate_competitiveness(data, seed_keyword, intermediate_keyword)
            competitiveness_data.append((seed_keyword, intermediate_keyword, competitiveness))

    # 排序竞争性关键词
    competitiveness_data.sort(key=lambda x: -x[2])

    # 输出结果
    for seed_keyword, intermediate_keyword, competitiveness in competitiveness_data:
        print(f"(种子) {seed_keyword}  (中介) {intermediate_keyword}  (竞争度) {competitiveness:.2f}")


if __name__ == '__main__':
    seed_keywords = ["guodegang", "nv"]  # 用实际种子关键字替换
    n = 10  # 需要获取的竞争关键词的数量
    compkey(seed_keywords, n)

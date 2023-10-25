import os

word_in_file = "data/user_tag_query.10W.TRAIN"
word_out_file = "data/word_out.txt"

# 检查输入文件是否存在
if not os.path.exists(word_in_file):
    print(f"请导入文件: 数据文件 {word_in_file} 不存在.")
else:
    with open(word_in_file, 'r', encoding='gbk', errors='ignore') as in_file:
        with open(word_out_file, 'w', encoding='utf-8') as out_file:
            for line in in_file:
                try:
                    line = line.strip()
                    chars = list(line)
                    for i in range(39, len(chars)):
                        out_file.write(chars[i])
                        if chars[i] == '\t':
                            out_file.write('\n')
                except UnicodeDecodeError:
                    continue  # 忽略无效字符并继续处理下一行

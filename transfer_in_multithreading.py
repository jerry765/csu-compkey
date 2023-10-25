import os
import concurrent.futures
from itertools import islice
from multiprocessing import Manager

def process_chunk(chunk, result_list):
    result = []
    for line in chunk:
        try:
            line = line.strip()
            chars = list(line)
            for i in range(39, len(chars)):
                result.append(chars[i])
                if chars[i] == '\t':
                    result.append('\n')
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError occurred for line: {line}")
    result_list.append("".join(result))

if __name__ == '__main__':
    word_in_file = "data/user_tag_query.10W.TRAIN"
    word_out_file = "data/word_out.txt"

    if not os.path.exists(word_in_file):
        print(f"请导入文件: 数据文件 {word_in_file} 不存在.")
    else:
        with open(word_in_file, 'r', encoding='gbk', errors='ignore') as in_file:
            with open(word_out_file, 'w', encoding='utf-8') as out_file:
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    manager = Manager()
                    result_list = manager.list()
                    chunk_size = 1000  # 调整块的大小
                    futures = []

                    # 读取 data 并分块处理
                    while True:
                        chunk = list(islice(in_file, chunk_size))
                        if not chunk:
                            break
                        futures.append(executor.submit(process_chunk, chunk, result_list))

                    # 等待所有进程完成
                    for future in concurrent.futures.as_completed(futures):
                        future.result()

                    # 写入结果
                    for result in result_list:
                        out_file.write(result)

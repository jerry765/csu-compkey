import subprocess
import time

# 提示用户输入种子关键字
seed_keywords_input = input("请输入种子关键字，用空格分隔：")
seed_keywords = seed_keywords_input.split()  # 使用split()将输入的字符串分割成关键字列表

# # 先使用普通处理
# print("---开始处理原始数据---")
# transfer_process = subprocess.Popen(["python", "transfer.py"])
# transfer_process.wait()  # 等待transfer.py完成
# print("---原始数据处理完成---")
#
# # 记录transfer.py的结束时间
# transfer_end_time = time.time()

# 记录开始时间
start_time = time.time()

# 再使用多线程处理
print("---开始多线程处理原始数据---")
transfer_in_multithreading_process = subprocess.Popen(["python", "transfer.py"])
transfer_in_multithreading_process.wait()  # 等待transfer_in_multithreading.py完成
print("---多线程处理原始数据完成---")

# 记录transfer_in_multithreading.py的结束时间
transfer_in_multithreading_end_time = time.time()

# 运行extract.py，传递种子关键字作为参数
print("---开始查找种子关键词相关信息---")
extract_process = subprocess.Popen(["python", "extract.py"] + seed_keywords)
extract_process.wait()  # 等待extract.py完成
print("---种子关键词相关信息写入完成---")

# 记录extract.py的结束时间
extract_end_time = time.time()

# # 再使用多线程处理，传递种子关键字作为参数
# print("---开始多线程查找种子关键词相关信息---")
# extract_process = subprocess.Popen(["python", "extract_in_multithreading.py"] + seed_keywords)
# extract_process.wait()  # 等待extract.py完成
# print("---种子关键词相关信息多线程写入完成---")

# # 记录extract.py的结束时间
# extract_in_multithreading_end_time = time.time()

# 开始处理中介关键词
print("---开始寻找中介关键词并计算权重---")
intermediate_process = subprocess.Popen(["python", "intermediate.py"] + seed_keywords)
intermediate_process.wait()
print("---中介关键词寻找完成---")

# 记录intermediate.py的结束时间
intermediate_end_time = time.time()

# 开始运行compkey算法
print("---开始compkey算法---")
compkey_process = subprocess.Popen(["python", "compkey.py"] + seed_keywords)
compkey_process.wait()
print("---compkey算法运行玩成---")

compkey_end_time = time.time()

# 计算各个进程的耗时
# transfer_duration = transfer_end_time - start_time
transfer_in_multithreading_duration = transfer_in_multithreading_end_time - start_time
extract_duration = extract_end_time - transfer_in_multithreading_end_time
# transfer_in_multithreading_duration = transfer_in_multithreading_end_time - transfer_end_time
# extract_in_multithreading_duration = extract_in_multithreading_end_time - extract_end_time
intermediate_duration = intermediate_end_time - extract_end_time
compkey_duration = compkey_end_time - intermediate_end_time

# 输出耗时信息
# print(f"普通处理耗时: {transfer_duration:.2f} 秒")
print(f"多线程处理耗时: {transfer_in_multithreading_duration:.2f} 秒")
print(f"关键词查找耗时: {extract_duration:.2f} 秒")
print(f"查找中介关键词耗时:{intermediate_duration:2f} 秒")
print(f"compkey算法耗时:{compkey_duration:2f} 秒")
# print(f"多线程关键词查找耗时: {extract_in_multithreading_duration:.2f} 秒")

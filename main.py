import subprocess
import time

# 记录开始时间
start_time = time.time()

# 运行transfer.py
print("---开始分析原始数据---")
transfer_process = subprocess.Popen(["python", "transfer.py"])
transfer_process.wait()  # 等待transfer.py完成
print("---原始数据分析完成---")

# 记录transfer.py的结束时间
transfer_end_time = time.time()

# 运行extract.py
print("---开始查找种子关键词相关信息---")
extract_process = subprocess.Popen(["python", "extract.py"])
extract_process.wait()  # 等待extract.py完成
print("---种子关键词相关信息写入完成---")

# 记录extract.py的结束时间
extract_end_time = time.time()

# 计算各个进程的耗时
transfer_duration = transfer_end_time - start_time
extract_duration = extract_end_time - transfer_end_time

# 输出耗时信息
print(f"transfer.py 耗时: {transfer_duration:.2f} 秒")
print(f"extract.py 耗时: {extract_duration:.2f} 秒")

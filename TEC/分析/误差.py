import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import chardet

# 文件夹路径
folder_path = r'C:/Users/hll/Desktop/CO/EX/GP/TEC/hll(1)'

# 获取文件夹中的所有文件
all_files = os.listdir(folder_path)

# 筛选出所有的TXT文件
txt_files = [file for file in all_files if file.endswith('.txt')]

# 定义标准值
standard_values = [25, 33]

# 初始化数据存储列表
file_names = []
average_temps = []
relative_errors = []
std_devs = []

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

# 读取每个TXT文件的数据并计算误差
for file_name in txt_files:
    file_path = os.path.join(folder_path, file_name)
    
    # 检测文件编码
    encoding = detect_encoding(file_path)
    
    # 读取文件数据
    data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['时间', '温度'], encoding=encoding)
    
    # 计算温度数据的平均值
    average_temp = data['温度'].mean()
    
    # 找到距离平均值最近的标准值
    closest_standard = min(standard_values, key=lambda x: abs(x - average_temp))
    
    # 计算相对误差
    relative_error = abs((average_temp - closest_standard) / closest_standard)
    
    # 计算标准差
    std_dev = data['温度'].std()
    
    # 存储数据
    file_names.append(file_name)
    average_temps.append(average_temp)
    relative_errors.append(relative_error)
    std_devs.append(std_dev)

# 创建数据框架
df = pd.DataFrame({
    'File Name': file_names,
    'Average Temperature': average_temps,
    'Relative Error': relative_errors,
    'Standard Deviation': std_devs
})

# 打印误差分析报告
print(df)

# 生成相对误差和标准差汇总图
fig, ax = plt.subplots(figsize=(16, 8))

# 绘制条形图（相对误差）
bars1 = ax.bar(np.arange(len(file_names)) - 0.2, relative_errors, width=0.4, color='skyblue', label='Relative Error')

# 绘制条形图（标准差）
bars2 = ax.bar(np.arange(len(file_names)) + 0.2, std_devs, width=0.4, color='orange', label='Standard Deviation')

# 在每个条形顶端标注对应的数据（相对误差）
for bar, value in zip(bars1, relative_errors):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=12)

# 在每个条形顶端标注对应的数据（标准差）
for bar, value in zip(bars2, std_devs):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=12)

# 设置标签和标题
ax.set_xlabel('File Name', fontsize=20)
ax.set_ylabel('Value', fontsize=20)
ax.set_title('Relative Error and Standard Deviation Analysis of Temperature Data', fontsize=24)
ax.tick_params(axis='x', rotation=45, labelsize=14)
ax.tick_params(axis='y', labelsize=18)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(fontsize=16)

# 设置x轴刻度
ax.set_xticks(np.arange(len(file_names)))
ax.set_xticklabels(file_names)

# 调整布局
plt.tight_layout()

# 展示图像
plt.show()

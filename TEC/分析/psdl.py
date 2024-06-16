import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch
import numpy as np

# 文件夹路径
folder_path = r'C:/Users/hll/Desktop/CO/EX/GP/TEC/hll(1)'

# 获取文件夹中的所有文件
all_files = os.listdir(folder_path)

# 筛选出所有的TXT文件
txt_files = [file for file in all_files if file.endswith('.txt')]

# 读取每个TXT文件的数据并生成图像
for file_name in txt_files:
    file_path = os.path.join(folder_path, file_name)
    data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['时间', '温度'])
    
    time = data['时间']
    temperature = data['温度']
    
    # 计算采样频率
    dt = np.mean(np.diff(time))
    fs = 1 / dt
    
    # 计算PSD
    frequencies, psd = welch(temperature, fs=fs)
    
    # 创建一个子图
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # 绘制PSD图（对数坐标）
    ax.loglog(frequencies, psd, label='PSD')
    ax.set_xlabel('Frequency (Hz)', fontsize=20)
    ax.set_ylabel('PSD ($K^2/Hz$)', fontsize=20)
    ax.set_title(f'Power Spectral Density - {file_name}', fontsize=20)
    ax.legend(fontsize=20)
    ax.grid(True, which='both', linestyle='--')
    ax.tick_params(axis='both', which='major', labelsize=18)
    
    # 调整布局以防止标题和标签重叠
    plt.tight_layout(pad=3.0)
    
    # 展示图像
    plt.show()

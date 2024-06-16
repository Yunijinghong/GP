import os
import pandas as pd
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# 设置工作目录
os.chdir(r"C:\Users\hll\Desktop\CO\EX\GP\GP7")

# 读取Excel文件，从第二行开始，读取第2到第80行的数据
filename = '实验数据.xlsx'  # 替换为你的Excel文件名
data = pd.read_excel(filename, skiprows=1, nrows=79, usecols=[0, 1, 2, 3])

# 提取x轴和y轴数据
x = data.iloc[:, 0].values
y1 = data.iloc[:, 1].values
y2 = data.iloc[:, 2].values
y3 = data.iloc[:, 3].values

# 使用三次样条插值进行平滑
x_fine = np.linspace(min(x), max(x), 1000)
cs1 = CubicSpline(x, y1)
cs2 = CubicSpline(x, y2)
cs3 = CubicSpline(x, y3)

# 找到峰和谷
peaks_y1 = signal.find_peaks(cs1(x_fine))[0]
valleys_y1 = signal.find_peaks(-cs1(x_fine))[0]

peaks_y2 = signal.find_peaks(cs2(x_fine))[0]
valleys_y2 = signal.find_peaks(-cs2(x_fine))[0]

peaks_y3 = signal.find_peaks(cs3(x_fine))[0]
valleys_y3 = signal.find_peaks(-cs3(x_fine))[0]

# 创建一个空 DataFrame
results = pd.DataFrame()

# 确保所有列长度一致，分别填充峰和谷
max_len = max(len(peaks_y1), len(valleys_y1), len(peaks_y2), len(valleys_y3), len(peaks_y3), len(valleys_y3))

# 填充缺失的部分为空值（NaN）
results['y1_peaks'] = np.nan * np.ones(max_len)
results['y1_valleys'] = np.nan * np.ones(max_len)
results['y2_peaks'] = np.nan * np.ones(max_len)
results['y2_valleys'] = np.nan * np.ones(max_len)
results['y3_peaks'] = np.nan * np.ones(max_len)
results['y3_valleys'] = np.nan * np.ones(max_len)

# 赋值给 DataFrame
results.loc[:len(peaks_y1)-1, 'y1_peaks'] = x_fine[peaks_y1]
results.loc[:len(valleys_y1)-1, 'y1_valleys'] = x_fine[valleys_y1]
results.loc[:len(peaks_y2)-1, 'y2_peaks'] = x_fine[peaks_y2]
results.loc[:len(valleys_y2)-1, 'y2_valleys'] = x_fine[valleys_y2]
results.loc[:len(peaks_y3)-1, 'y3_peaks'] = x_fine[peaks_y3]
results.loc[:len(valleys_y3)-1, 'y3_valleys'] = x_fine[valleys_y3]

print("Peaks and Valleys Table:")
print(results)

# 绘制散点图和平滑曲线，并标注峰和谷
plt.figure(figsize=(12, 8))

# 绘制 y1 数据
plt.scatter(x, y1, label='2.0V', color='blue')  # 2.0V
plt.plot(x_fine, cs1(x_fine), label='2.0V ', color='cyan')

# 标注 y1 的峰和谷
if not pd.isna(results['y1_peaks']).all():
    plt.scatter(results['y1_peaks'], cs1(results['y1_peaks']), color='red', label='2.0V peaks')
if not pd.isna(results['y1_valleys']).all():
    plt.scatter(results['y1_valleys'], cs1(results['y1_valleys']), color='green', label='2.0V valleys')

# 绘制 y2 数据
plt.scatter(x, y2, label='1.8V', color='orange')  # 1.8V
plt.plot(x_fine, cs2(x_fine), label='1.8V ', color='yellow')

# 标注 y2 的峰和谷
if not pd.isna(results['y2_peaks']).all():
    plt.scatter(results['y2_peaks'], cs2(results['y2_peaks']), color='red', label='1.8V peaks')
if not pd.isna(results['y2_valleys']).all():
    plt.scatter(results['y2_valleys'], cs2(results['y2_valleys']), color='green', label='1.8V valleys')

# 绘制 y3 数据
plt.scatter(x, y3, label='2.2V', color='purple')  # 2.2V
plt.plot(x_fine, cs3(x_fine), label='2.2V ', color='magenta')

# 标注 y3 的峰和谷
if not pd.isna(results['y3_peaks']).all():
    plt.scatter(results['y3_peaks'], cs3(results['y3_peaks']), color='red', label='2.2V peaks')
if not pd.isna(results['y3_valleys']).all():
    plt.scatter(results['y3_valleys'], cs3(results['y3_valleys']), color='green', label='2.2V valleys')

plt.xlabel('VG2K')
plt.ylabel('IP')
plt.title('Data with Smoothed Curves, Peaks, and Valleys')
plt.legend()
plt.show()

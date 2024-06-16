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

# 找到谷
valleys_y1 = signal.find_peaks(-cs1(x_fine))[0]
valleys_y2 = signal.find_peaks(-cs2(x_fine))[0]
valleys_y3 = signal.find_peaks(-cs3(x_fine))[0]

# 确定最大长度
max_len = max(len(valleys_y1), len(valleys_y2), len(valleys_y3))

# 创建一个长度一致的 DataFrame
valleys_info = pd.DataFrame(np.nan, index=range(max_len), columns=['y1_x', 'y1_y', 'y2_x', 'y2_y', 'y3_x', 'y3_y'])

# 填充谷点的横坐标和纵坐标
valleys_info.loc[:len(valleys_y1)-1, 'y1_x'] = x_fine[valleys_y1]
valleys_info.loc[:len(valleys_y1)-1, 'y1_y'] = cs1(x_fine[valleys_y1])

valleys_info.loc[:len(valleys_y2)-1, 'y2_x'] = x_fine[valleys_y2]
valleys_info.loc[:len(valleys_y2)-1, 'y2_y'] = cs2(x_fine[valleys_y2])

valleys_info.loc[:len(valleys_y3)-1, 'y3_x'] = x_fine[valleys_y3]
valleys_info.loc[:len(valleys_y3)-1, 'y3_y'] = cs3(x_fine[valleys_y3])

print("Valleys Information:")
print(valleys_info)

# 绘制散点图和平滑曲线，并标注谷点
plt.figure(figsize=(12, 8))

# 绘制 y1 数据及谷点
plt.scatter(x, y1, label='2.0V', color='blue')  # 2.0V
plt.plot(x_fine, cs1(x_fine), color='cyan')
plt.scatter(valleys_info['y1_x'], valleys_info['y1_y'], color='green', label='2.0V valleys')

# 绘制 y2 数据及谷点
plt.scatter(x, y2, label='1.8V', color='orange')  # 1.8V
plt.plot(x_fine, cs2(x_fine), color='yellow')
plt.scatter(valleys_info['y2_x'], valleys_info['y2_y'], color='green', label='1.8V valleys')

# 绘制 y3 数据及谷点
plt.scatter(x, y3, label='2.2V', color='purple')  # 2.2V
plt.plot(x_fine, cs3(x_fine), color='magenta')
plt.scatter(valleys_info['y3_x'], valleys_info['y3_y'], color='green', label='2.2V valleys')

plt.xlabel('VG2K')
plt.ylabel('IP')
plt.title('Data with Smoothed Curves and Valleys')
plt.legend()
plt.show()

import os
import pandas as pd
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 设置工作目录
os.chdir(r"C:\Users\hll\Desktop\CO\EX\GP\GP7")

# 读取Excel文件，跳过第一行，读取第2到第80行的数据
filename = '实验数据.xlsx'  # 替换为你的Excel文件名
data = (pd.read_excel(filename, skiprows=1, nrows=79, usecols=[0, 1]))

# 提取x轴和y轴数据
x = data.iloc[:, 0].values
y1 = data.iloc[:, 1].values  # 只读取第二列数据

# 使用三次样条插值进行平滑
x_fine = np.linspace(min(x), max(x), 1000)
cs1 = CubicSpline(x, y1)

# 找到峰和谷
peaks_y1 = signal.find_peaks(cs1(x_fine))[0]
valleys_y1 = signal.find_peaks(-cs1(x_fine))[0]

# 提取后六个峰和谷的数值
last_peaks_x = x_fine[peaks_y1][-6:]  # 最后六个峰的x坐标
last_peaks_y = cs1(x_fine[peaks_y1])[-6:]  # 最后六个峰的y坐标

last_valleys_x = x_fine[valleys_y1][-6:]  # 最后六个谷的x坐标
last_valleys_y = cs1(x_fine[valleys_y1])[-6:]  # 最后六个谷的y坐标

# 使用线性回归来拟合峰和谷
peak_model = LinearRegression()
valley_model = LinearRegression()

# 拟合峰
peak_model.fit(last_peaks_x.reshape(-1, 1), last_peaks_y)

# 拟合谷
valley_model.fit(last_valleys_x.reshape(-1, 1), last_valleys_y)

# 获取峰和谷的拟合直线斜率
peak_slope = peak_model.coef_[0]  # 峰的斜率
valley_slope = valley_model.coef_[0]  # 谷的斜率

# 计算相关系数
peak_r2 = r2_score(last_peaks_y, peak_model.predict(last_peaks_x.reshape(-1, 1)))
valley_r2 = r2_score(last_valleys_y, valley_model.predict(last_valleys_x.reshape(-1, 1)))

# 输出斜率和相关系数
print(f"Peak Slope: {peak_slope}, Peak R^2: {peak_r2}")
print(f"Valley Slope: {valley_slope}, Valley R^2: {valley_r2}")

# 获取拟合曲线
x_fit = np.linspace(min(x), max(x), 100)  # 拟合的x坐标范围
y_peaks_fit = peak_model.predict(x_fit.reshape(-1, 1))
y_valleys_fit = valley_model.predict(x_fit.reshape(-1, 1))

# 绘制曲线
plt.figure(figsize=(12, 8))

# 绘制 y1 数据
plt.scatter(x, y1, label='Data', color='blue')  # 原始数据
plt.plot(x_fine, cs1(x_fine), label='Smoothed Curve', color='cyan')  # 平滑曲线

# 标注最后六个峰
plt.scatter(last_peaks_x, last_peaks_y, color='red', label='Last 6 Peaks')
plt.plot(x_fit, y_peaks_fit, color='orange', linestyle='--', label='Peak Line Fit')  # 峰的拟合曲线

# 标注最后六个谷
plt.scatter(last_valleys_x, last_valleys_y, color='green', label='Last 6 Valleys')
plt.plot(x_fit, y_valleys_fit, color='purple', linestyle='--', label='Valley Line Fit')  # 谷的拟合曲线

plt.xlabel('VG2K')
plt.ylabel('IP')
plt.title('Peaks and Valleys with Fitted Curves')
plt.legend()
plt.show()

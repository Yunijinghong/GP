import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

# 给定的数据
data = np.array([
    [22.471471, 4.640862],
    [33.948949, -0.147486],
    [46.207207, 6.788575],
    [58.621622, 30.274436]
])

# 获取 x 和 y 的数据
x = data[:, 0]
y = data[:, 1]

# 计算皮尔逊相关系数
correlation, p_value = pearsonr(x, y)

print("Pearson correlation coefficient:", correlation)
print("P-value:", p_value)

# 尝试线性拟合
linear_fit = np.polyfit(x, y, 1)
linear_model = np.poly1d(linear_fit)

# 尝试二次多项式拟合
quadratic_fit = np.polyfit(x, y, 2)
quadratic_model = np.poly1d(quadratic_fit)

# 生成拟合曲线
x_fit = np.linspace(min(x), max(x), 100)
y_linear = linear_model(x_fit)
y_quadratic = quadratic_model(x_fit)

# 绘制数据点和拟合曲线
plt.scatter(x, y, color='red', label='Data points')
plt.plot(x_fit, y_linear, color='blue', label='Linear fit')
plt.plot(x_fit, y_quadratic, color='green', label='Quadratic fit')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear and Quadratic Fit with Pearson Correlation')
plt.legend()
plt.show()

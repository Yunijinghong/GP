import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

# 生成一些模拟数据
np.random.seed(42)
x = np.linspace(-5, 5, 100)  # 输入数据
y = 3 * np.sin(x) + np.random.normal(0, 0.5, x.shape)  # 目标数据，加入了一些随机噪声

# 拆分训练集和验证集
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)

# 神经网络需要输入为二维，因此调整x的形状
x_train = x_train.reshape(-1, 1)
x_val = x_val.reshape(-1, 1)

# 定义神经网络模型
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(1,)),  # 输入层
    layers.Dense(64, activation='relu'),  # 第一个隐藏层
    layers.Dense(1)  # 输出层
])

# 编译模型
model.compile(optimizer='adam', loss='mse')

# 训练模型
history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=100, verbose=1)

# 预测
x_test = np.linspace(-6, 6, 100).reshape(-1, 1)  # 测试数据，用于可视化
predictions = model.predict(x_test)

# 可视化结果
plt.scatter(x, y, label='Data')  # 原始数据
plt.plot(x_test, predictions, color='red', label='Fitted Curve')  # 拟合曲线
plt.xlabel('x')
plt.ylabel('y')
plt.title('Function Fitting with Neural Network')
plt.legend()
plt.show()

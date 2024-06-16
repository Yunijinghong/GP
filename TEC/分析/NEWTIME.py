import pandas as pd
import matplotlib.pyplot as plt
import glob

# 文件夹路径
folder_path = 'C:/Users/hll/Desktop/CO/EX/GP/TEC/hll(1)'

# 获取文件夹中所有txt文件的路径
txt_files = glob.glob(f'{folder_path}/*.txt')

# 遍历每个txt文件，读取数据并绘制时序图
for file_path in txt_files:
    # 读取txt文件
    df = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['Time', 'Temperature'])

    # 提取时间和温度数据
    time = df['Time']
    temperature = df['Temperature']

    # 从文件路径中提取文件名作为图表标题的一部分
    file_name = file_path.split('\\')[-1]  # 注意在Windows中使用反斜杠

    # 绘制时序图
    plt.figure()
    plt.plot(time, temperature, marker='o', linestyle='-', label=file_name)
    plt.title(f'Time vs Temperature - {file_name}')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()
    plt.grid(True)
    plt.show()

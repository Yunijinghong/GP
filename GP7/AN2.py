import pandas as pd

# 定义初始数据
data = {
    '2.0V_peaks': [8.885886, 17.318318, 28.093093, 39.960961, 52.531532],
    '2.0V_valleys': [9.822823, 22.471471, 33.948949, 46.207207, 58.621622],
    '1.8V_peaks': [28.015015, 38.711712, 52.375375, 65.570571, 78.375375],
    '1.8V_valleys': [22.627628, 34.183183, 46.129129, 58.075075, 71.192192],
    '2.2V_peaks': [16.537538, 27.936937, 39.804805, 52.297297, 65.336336],
    '2.2V_valleys': [22.549550, 34.105105, 46.285285, 58.699700, 71.426426]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 计算峰与峰、谷与谷的间距
df['2.0V_peak_spacing'] = df['2.0V_peaks'].diff().fillna(0)
df['2.0V_valley_spacing'] = df['2.0V_valleys'].diff().fillna(0)

df['1.8V_peak_spacing'] = df['1.8V_peaks'].diff().fillna(0)
df['1.8V_valley_spacing'] = df['1.8V_valleys'].diff().fillna(0)

df['2.2V_peak_spacing'] = df['2.2V_peaks'].diff().fillna(0)
df['2.2V_valley_spacing'] = df['2.2V_valleys'].diff().fillna(0)

# 转换为LaTex表格格式
latex_table = df.to_latex(index=False, float_format="%.6f", caption="Peaks and Valleys with Spacing", label="tab:spacing_table")

print(latex_table)

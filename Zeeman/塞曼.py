import cv2
import numpy as np
import matplotlib.pyplot as plt

# 图像文件路径
image_path = 'C:\\Users\\hll\\Desktop\\CO\\EX\\GP\\Zeeman\\dm.png'

# 使用 OpenCV 加载图像
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 检查图像是否成功加载
if img is None:
    print(f"错误：无法从 {image_path} 加载图像")
    exit()

# 高斯模糊以减少噪声
blurred_img = cv2.GaussianBlur(img, (9, 9), 2)

# 使用 HoughCircles 检测圆环
circles = cv2.HoughCircles(blurred_img, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                           param1=50, param2=30, minRadius=20, maxRadius=200)

# 如果检测到圆环，绘制它们
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        # 绘制圆环和中心点
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)
        cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # 多选取几个点进行分析
        for k in range(-3, 4):
            for l in range(-3, 4):
                if k == 0 and l == 0:
                    continue  # 跳过圆心点自身
                px = x + k
                py = y + l
                if px >= 0 and px < img.shape[1] and py >= 0 and py < img.shape[0]:
                    cv2.rectangle(img, (px - 2, py - 2), (px + 2, py + 2), (255, 0, 0), -1)  # 绘制额外的点

# 显示带有检测到的圆环和额外点的图像
plt.figure(figsize=(10, 10))
plt.imshow(img, cmap='gray')
plt.title('检测到的圆环和额外点')
plt.axis('off')
plt.show()

# 打印检测到的圆环信息
print("检测到的圆环：")
if circles is not None:
    for (x, y, r) in circles:
        print(f"圆心坐标：({x}, {y})，半径：{r}")

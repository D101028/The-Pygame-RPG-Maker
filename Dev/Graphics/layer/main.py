import cv2
import numpy as np

# 創建一個960x720的純黑色背景圖像
height, width = 720, 960
background = np.zeros((height, width, 4), dtype=np.uint8)

# 設置中心點和半徑
center_x, center_y = width // 2, height // 2
radius = 192
# radius = min(center_x, center_y)  # 半徑設為寬和高的一半

# 填充背景為黑色
background[:, :, 0:3] = 0  # 黑色
background[:, :, 3] = 255  # alpha通道設置為完全不透明

# 創建一個漸變透明的圓形
for y in range(height):
    for x in range(width):
        # 計算到中心點的距離
        distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        if distance < radius:
            # 計算透明度，距離越遠透明度越低
            alpha = 255 * (distance / radius)
            background[y, x, 3] = int(alpha)

# 保存最終圖像
cv2.imwrite('dark_cover_192.png', background)

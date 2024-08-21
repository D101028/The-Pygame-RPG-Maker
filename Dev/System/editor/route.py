import pygame
import time
import json

from settings import FPS

# 初始化 Pygame
pygame.init()

# 設定視窗大小
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("滑鼠座標紀錄")

# 設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 初始化變數
running = True
recording = False
positions = []
start_time = 0
interval = 1/FPS  # 設定時間間隔 (秒)

# 主循環
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not recording:
                # 開始紀錄
                recording = True
                positions = []
                start_time = time.time()
                print("開始紀錄")
            else:
                # 停止紀錄並將座標存入檔案
                recording = False
                with open('coordinates.json', 'w') as file:
                    json.dump(positions, file)
                print("紀錄結束，座標已存入 coordinates.json")

    if recording:
        current_time = time.time()
        if current_time - start_time >= interval:
            x, y = pygame.mouse.get_pos()
            positions.append((x, y))
            start_time = current_time
            print(f"記錄座標: {(x, y)}")

    # 填充背景色
    screen.fill(WHITE)

    # 畫出所有紀錄的座標點
    for pos in positions:
        pygame.draw.circle(screen, BLACK, pos, 3)

    # 畫更新
    pygame.display.flip()

# 結束 Pygame
pygame.quit()

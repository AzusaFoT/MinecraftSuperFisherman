import pyautogui
import time
import gc

# 設定掃描的範圍（左上角和右下角的座標）
x_start, y_start = 1790, 1050
x_end, y_end = 1810, 1080



# 目標色碼（RGB格式）
target_color = (255, 255, 255) 

# 掃描間隔距離（像素）
step = 10

# for 迴圈控制掃描次數
for i in range(36000):  # 掃100次
    if i % 10 == 0:
        gc.collect()  # 每10輪手動清理記憶體
    print("開始第",i,"次")
    for x in range(x_start, x_end, step):
        for y in range(y_start, y_end, step):
            # 截圖並取得像素色碼
            screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
            pixel_color = screenshot.getpixel((0, 0))
            
            # 比對色碼
            if pixel_color == target_color:
                # 符合就移動滑鼠並點擊右鍵
                pyautogui.moveTo(x, y)
                pyautogui.click(button='right')
                print(f"右鍵點擊：{x}, {y}")
                time.sleep(0.5)
                
    print("結束第",i,"次")
    time.sleep(1)  # 每次掃完等待一點時間
    
import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui

class FishingApp:
    def __init__(self, root):
        self.root = root
        root.title("喵牌釣魚大師")
        root.geometry("350x220")
        root.resizable(False, False)

        self.font_name = ("俐方體11號", 12)

        # 標題
        self.label_title = tk.Label(root, text="🐟 自動釣魚工具", font=(self.font_name[0], 16), fg="#FF6600")
        self.label_title.pack(pady=(10, 5))

        # 時間輸入框區域
        frame_time = tk.Frame(root)
        frame_time.pack(pady=5)

        self.entry_hours = tk.Spinbox(frame_time, from_=0, to=99, width=3, font=self.font_name)
        self.entry_hours.grid(row=0, column=0, padx=(0, 5))
        self.entry_hours.delete(0, "end")
        self.entry_hours.insert(0, "10")

        label_hours = tk.Label(frame_time, text="小時", font=self.font_name)
        label_hours.grid(row=0, column=1, padx=(0, 15))

        self.entry_minutes = tk.Spinbox(frame_time, from_=0, to=59, width=3, font=self.font_name)
        self.entry_minutes.grid(row=0, column=2, padx=(0, 5))
        self.entry_minutes.delete(0, "end")
        self.entry_minutes.insert(0, "00")

        label_minutes = tk.Label(frame_time, text="分鐘", font=self.font_name)
        label_minutes.grid(row=0, column=3)

        # 剩餘時間標籤
        self.label_timer = tk.Label(root, text="", font=self.font_name, fg="#333333")
        self.label_timer.pack(pady=(20, 0))

        # 按鈕區域（放在最底下）
        frame_btn = tk.Frame(root)
        frame_btn.pack(side=tk.BOTTOM, pady=(5, 15))

        self.btn_start = tk.Button(
            frame_btn, text="開始釣魚", font=self.font_name,
            bg="#FF6600", fg="white", width=12,
            command=self.start_fishing
        )
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_stop = tk.Button(
            frame_btn, text="停止釣魚", font=self.font_name,
            bg="#A9A9A9", fg="#696969", width=12,
            command=self.stop_fishing,
            state=tk.DISABLED
        )
        self.btn_stop.grid(row=0, column=1, padx=10)

        self.running = False
        self.thread = None
        self.remaining_seconds = 0

    def fishing_loop(self, total_seconds):
        x_start, y_start = 1790, 1050
        x_end, y_end = 1810, 1080
        target_color = (255, 255, 255)
        step = 10
        end_time = time.time() + total_seconds

        while self.running and time.time() < end_time:
            for x in range(x_start, x_end, step):
                for y in range(y_start, y_end, step):
                    if not self.running:
                        break
                    screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
                    pixel_color = screenshot.getpixel((0, 0))
                    if pixel_color == target_color:
                        pyautogui.moveTo(x, y)
                        pyautogui.click(button='right')
                        print(f"右鍵點擊：{x}, {y}")
                        time.sleep(0.5)
            time.sleep(1)
        self.stop_fishing()

    def update_timer(self):
        if self.running and self.remaining_seconds > 0:
            total_minutes = self.remaining_seconds // 60
            hrs = total_minutes // 60
            mins = total_minutes % 60
            self.label_timer.config(text=f"剩餘時間: {hrs:02d} 小時 {mins:02d} 分鐘")
            self.remaining_seconds -= 60
            self.root.after(60000, self.update_timer)
        else:
            self.label_timer.config(text="")

    def start_fishing(self):
        try:
            hours = int(self.entry_hours.get())
            minutes = int(self.entry_minutes.get())
            total_seconds = hours * 3600 + minutes * 60
            if total_seconds <= 0:
                messagebox.showwarning("錯誤", "請輸入有效的時間")
                return
        except ValueError:
            messagebox.showwarning("錯誤", "時間輸入格式錯誤")
            return

        if self.running:
            return

        self.running = True
        self.remaining_seconds = total_seconds

        self.entry_hours.config(state='disabled')
        self.entry_minutes.config(state='disabled')

        self.btn_start.config(state=tk.DISABLED, bg="#A9A9A9", fg="#696969")
        self.btn_stop.config(state=tk.NORMAL, bg="#D50000", fg="black")

        self.thread = threading.Thread(target=self.fishing_loop, args=(total_seconds,), daemon=True)
        self.thread.start()
        self.update_timer()

    def stop_fishing(self):
        if not self.running:
            return
        self.running = False
        self.label_timer.config(text="")

        self.entry_hours.config(state='normal')
        self.entry_minutes.config(state='normal')

        self.btn_start.config(state=tk.NORMAL, bg="#FF6600", fg="white")
        self.btn_stop.config(state=tk.DISABLED, bg="#A9A9A9", fg="#696969")

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingApp(root)
    root.mainloop()

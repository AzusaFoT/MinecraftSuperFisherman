import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui
from PIL import Image, ImageTk
import os

class FishingApp:
    def __init__(self, root):
        self.root = root
        root.title("喵牌釣魚大師")
        root.geometry("350x200")
        root.resizable(False, False)

        self.font_name = ("俐方體11號", 12)

        self.is_showing_help = False

        # 主畫面 Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 標題
        self.label_title = tk.Label(self.main_frame, text="🐟 自動釣魚工具", font=(self.font_name[0], 16), fg="#FF6600")
        self.label_title.pack(pady=(10, 5))

        # 時間輸入框區域
        frame_time = tk.Frame(self.main_frame)
        frame_time.pack(pady=5)

        self.entry_hours = tk.Spinbox(frame_time, from_=0, to=99, width=3, font=self.font_name)
        self.entry_hours.grid(row=0, column=0, padx=(0, 0))
        self.entry_hours.delete(0, "end")
        self.entry_hours.insert(0, "10")

        label_hours = tk.Label(frame_time, text="小時", font=self.font_name)
        label_hours.grid(row=0, column=1, padx=(0, 0))

        self.entry_minutes = tk.Spinbox(frame_time, from_=0, to=59, width=3, font=self.font_name)
        self.entry_minutes.grid(row=0, column=2, padx=(0, 0))
        self.entry_minutes.delete(0, "end")
        self.entry_minutes.insert(0, "00")

        label_minutes = tk.Label(frame_time, text="分鐘", font=self.font_name)
        label_minutes.grid(row=0, column=3)

        # 剩餘時間標籤
        self.label_timer = tk.Label(self.main_frame, text="", font=self.font_name, fg="#333333")
        self.label_timer.pack(pady=(5, 0))

        # 圖片（左上角）
        self.frame_topleft = tk.Frame(self.root)
        self.frame_topleft.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)
        try:
            img = Image.open(os.path.join(os.path.dirname(__file__), "azusa.png"))
            img = img.resize((32, 32), Image.Resampling.LANCZOS)
            self.azusa_img = ImageTk.PhotoImage(img)
            self.label_img = tk.Label(self.frame_topleft, image=self.azusa_img, cursor="hand2")
            self.label_img.pack()
            self.label_img.bind("<Button-1>", self.toggle_help)
        except Exception as e:
            print("圖片載入失敗:", e)

        # 按鈕區域（放在最底下）
        frame_btn = tk.Frame(self.main_frame)
        frame_btn.pack(side=tk.BOTTOM, pady=(0, 20))

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

        # 說明畫面
        self.help_frame = tk.Frame(root)
        # 在 help_frame 中加一個中介 Frame
        self.help_inner_frame = tk.Frame(self.help_frame)
        self.help_inner_frame.pack(expand=True)

        # 說明文字放進 inner_frame 並用 padding 適度控制
        self.label_help = tk.Label(
            self.help_inner_frame,
            text="   AzusaFoT超級釣魚大師\n- 請確保您的釣竿有附魔\n- 請確保您是2K螢幕\n- 本工具只支援自動出竿\n   收竿要靠岩漿燒\n【按作者圖示返回主畫面】",
            font=self.font_name,
            justify="left"
        )
        self.label_help.pack(padx=10, pady=10)


        self.running = False
        self.thread = None
        self.remaining_seconds = 0

    def toggle_help(self, event):
        if self.running:
            return
        if not self.is_showing_help:
            self.main_frame.pack_forget()
            self.help_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.help_frame.pack_forget()
            self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.frame_topleft.lift()  # 確保圖示永遠在最上層

        self.is_showing_help = not self.is_showing_help

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
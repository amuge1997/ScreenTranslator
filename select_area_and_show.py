import tkinter as tk
import ocr_and_translate
import threading
import time



class SelectArea:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.config(bg="gray")
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # 捕捉鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # 记录开始坐标
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # 创建矩形
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        # 更新矩形框
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # 获取矩形框的坐标
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        # 确保起点坐标和终点坐标正确
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        # 退出全屏窗口
        # self.root.quit()
        # return x1, y1, x2, y2
        left = int(x1)
        right = int(x2)
        top = int(y1)
        bottom = int(y2)
        print(left, right, top, bottom)
        self.canvas.destroy()
        self.callback(left, right, top, bottom)


class Translate:
    def __init__(self, root) -> None:
        self.root = root
        self.width, self.height = 400, 100
        self.alpha = 0.7
        self.label = tk.Label(root, text="None", fg="white", bg="black", font=("Arial", 14), wraplength=self.width)

    def make_window_transparent(self, window, alpha):
        # 设置窗口背景透明
        window.attributes("-alpha", alpha)

    def start_move(self, event):
        # 记录鼠标按下时的初始位置
        global x_offset, y_offset
        x_offset = event.x
        y_offset = event.y

    def move_window(self, event):
        # 移动窗口
        x = event.x_root - x_offset
        y = event.y_root - y_offset
        self.root.geometry(f"+{x}+{y}")

    def create_transparent_window(self):
        root = self.root
        root.attributes("-fullscreen", False)
        # 设置窗口为顶层窗口，始终显示在最上层
        root.attributes("-topmost", True)
        
        # 去除窗口标题栏，使其更像一个浮动窗口
        root.overrideredirect(True)

        # 设置窗口大小
        root.geometry(f"{self.width}x{self.height}")
        
        # 设置窗口背景颜色和透明度，仅在初始化时执行一次
        root.configure(bg='black')
        self.make_window_transparent(root, self.alpha)

        # 创建标签以显示文字，设置文字颜色和字体
        self.label.pack(expand=True)

        # 绑定鼠标事件
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.move_window)

        # 运行窗口主循环
        root.mainloop()











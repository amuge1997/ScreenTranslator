import tkinter as tk
import ocr_and_translate
import threading
import time


def task():
    while True:
        time.sleep(0.1)
        left, right, top, bottom = select_area.get_xy()
        text = ocr_and_translate.run(left, right, top, bottom)
        # print(text)
        if text is not None:
            translate.label['text'] = text
        else:
            translate.label['text'] = ""
    pass

def start_task():
    task_thread = threading.Thread(target=task)
    task_thread.start()


class SelectArea:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-alpha", 0.2)
        self.root.config(bg="black")
        root.geometry(f"{400}x{100}")
        root.attributes("-topmost", True)
        root.title("Screen Translator")
        root.update()
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.draw_red_border()
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        # root.overrideredirect(True)
        
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_window)

        root.bind("<Configure>", self.on_resize)

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
    
    def on_resize(self, event):
        self.draw_red_border()
    
    def draw_red_border(self):
        # 获取窗口的宽度和高度

        root = self.root
        canvas = self.canvas
        width = root.winfo_width()
        height = root.winfo_height()
        # print(width, height)

        # 清除之前的内容（如果有）
        canvas.delete("border")

        # 绘制四条红线，分别位于窗口的上下左右四个边框
        line_width = 3
        canvas.create_line(0, 0, width, 0, fill="red", width=line_width, tags="border")    # 顶部边框
        canvas.create_line(0, 0, 0, height, fill="red", width=line_width, tags="border")   # 左侧边框
        canvas.create_line(0, height, width, height, fill="red", width=line_width, tags="border")  # 底部边框
        canvas.create_line(width, 0, width, height, fill="red", width=line_width, tags="border")   # 右侧边框

    
    def get_xy(self):
        x = root.winfo_rootx()
        y = root.winfo_rooty()

        # 获取窗口的宽度和高度
        width = root.winfo_width()
        height = root.winfo_height()
        # print(x,y,width,height)

        left, right, top, bottom = x, x+width, y, y+height

        return int(left), int(right), int(top), int(bottom)


class Translate:
    def __init__(self, root) -> None:
        self.root = root
        self.width, self.height = 400, 100
        self.alpha = 0.7
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

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        root.update()
        self.draw_red_border()
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.label = tk.Label(self.canvas, text="None", fg="white", bg="black", font=("Arial", 14), wraplength=self.width)

        # 创建标签以显示文字，设置文字颜色和字体
        self.label.pack(expand=True)
        # label_window = self.canvas.create_window(0, 0, anchor="nw", window=self.label, width=self.canvas.winfo_width(), height=self.canvas.winfo_height())

        # 绑定鼠标事件
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.move_window)

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
    
    def draw_red_border(self):
        # 获取 Canvas 的宽度和高度
        root = self.root
        canvas = self.canvas
        width = root.winfo_width()
        height = root.winfo_height()
        # print(width, height)

        # 清除之前的内容（如果有）
        canvas.delete("border")

        # 绘制四条红线，分别位于窗口的上下左右四个边框
        line_width = 1
        canvas.create_line(0, 0, width, 0, fill="red", width=line_width, tags="border")    # 顶部边框
        canvas.create_line(0, 0, 0, height, fill="red", width=line_width, tags="border")   # 左侧边框
        canvas.create_line(0, height-1, width, height-1, fill="red", width=line_width, tags="border")  # 底部边框
        canvas.create_line(width-1, 0, width-1, height, fill="red", width=line_width, tags="border")   # 右侧边框



if __name__ == '__main__':
    root = tk.Tk()
    second_root = tk.Toplevel()
    select_area = SelectArea(root)
    translate = Translate(second_root)
    start_task()
    root.mainloop()






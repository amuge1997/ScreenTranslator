import tkinter as tk
import ocr_and_translate
import threading
import time
from select_area_and_show import SelectArea, Translate




def task(left, right, top, bottom):
    while True:
        time.sleep(0.1)
        text = ocr_and_translate.run(left, right, top, bottom)
        # print(text)
        if text is not None:
            translate.label['text'] = text
        else:
            translate.label['text'] = ""

def start_task(left, right, top, bottom):
    task_thread = threading.Thread(target=task, args=(left, right, top, bottom,))
    task_thread.start()

def callback(left, right, top, bottom):
    start_task(left, right, top, bottom)
    translate.create_transparent_window()


if __name__ == '__main__':
    root = tk.Tk()  
    select_area = SelectArea(root, callback)
    translate = Translate(root)
    root.mainloop()










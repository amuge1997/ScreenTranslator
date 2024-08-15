
import pyautogui
import cv2 as cv
import cv2
from googletrans import Translator
import numpy as np
import pytesseract

file_path = 'result.txt'

# 创建翻译器对象
translator = Translator()

def cut_scrren():
    # 截图整个屏幕
    screenshot = pyautogui.screenshot()
    # 保存截图
    screenshot_np = np.array(screenshot)
    return screenshot_np


def cut_target_area(image, left, right, top, bottom):
    return image[top:bottom, left:right, :]


def show(image):
    cv2.imshow('Processed Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def cut_scale(image, scale_percent):

    # 获取原图像的尺寸
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)

    # 设置缩放后的尺寸
    dim = (width, height)

    # 缩小图像
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized_image

def ocr(resize_image):
    gray = cv2.cvtColor(resize_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(binary_image)
    return text

def text_process(text):
    text = text.replace("\n", ' ')
    return text

def save_text(text):
    with open(file_path, "w", encoding='utf8') as file:
        file.write(text)


def run(left, right, top, bottom):
    try:
        image = cut_scrren()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cut_image = cut_target_area(image, left, right, top, bottom)
        resize_image = cut_scale(cut_image, 0.5)
        text = ocr(resize_image)
        text = text_process(text)
        translated = translator.translate(text, src='en', dest='zh-cn')
        result = str(translated.text)
        # save_text(result)
        # print(text)
        # print(result)
        return result
    except:
        return None


if __name__ == '__main__':
    run()

















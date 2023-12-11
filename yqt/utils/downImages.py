# -*- coding: UTF-8 -*-

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from PIL import Image


import time


def get_position(driver):
    """
    获取验证码位置
    :return: 验证码位置元组
    """
    img = WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
    time.sleep(0.5)
    location = img.location
    size = img.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
        'width']
    return top, bottom, left, right


# 获取网页截图
def get_screenshot(driver):
    """
    获取网页截图
    :return: 截图对象
    """
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


# 获取验证码图片
def get_geetest_image(driver, name=None):
    """
    获取验证码图片
    :return: 图片对象
    """
    top, bottom, left, right = get_position(driver)
    screenshot = get_screenshot(driver)
    captcha = screenshot.crop((left, top, right, bottom))
    captcha.save(name)
    return name
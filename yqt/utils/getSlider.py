# -*- coding: UTF-8 -*-


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 获取初始验证按钮
def get_geetest_button(driver):
    """
    获取初始验证按钮
    :return:
    """
    button = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
    return button


# 获取滑块对象
def get_slider(driver):
    """
    获取滑块
    :return: 滑块对象
    """
    try:
        slider = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
    except Exception:
        return
    return slider



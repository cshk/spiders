# -*- coding: UTF-8 -*-


from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.downImages import get_geetest_image
from utils.initBrowser import init_chrome_driver
from utils.jsExecute import img1JS, img2JS, restoreJS
from utils.getGap import get_gap_offset
from utils.getSlider import get_geetest_button, get_slider
from utils.getTracks import get_tracks


import time
import os


USERNAME = '11111'
PASSWORD = '12311456'
tryNum = 4
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH = os.path.join(BASE_DIR, 'imgs')
IMG1_PATH = os.path.join(IMG_PATH, 'imgs1')
IMG2_PATH = os.path.join(IMG_PATH, 'imgs2')



# 打开页面,输入账号与密码
def open(driver, url):
    """
    打开网页输入用户名密码
    :return: None
    """
    driver.get(url)
    # time.sleep(15)
    # checkSucc = driver.find_element(By.CLASS_NAME, 'geetest_success_radar_tip_content')
    # retry = driver.find_element(By.CLASS_NAME, "geetest_radar_tip_content")
    # if retry.text == "点击按钮进行验证":pass
    # print(checkSucc.text)
    return reTry(driver)


def getDistance(driver):
    # 获取验证码图片
    driver.execute_script(img1JS)
    slideIMAGE = get_geetest_image(driver, name=os.path.join(IMG1_PATH, str(int(time.time())) + '.png'))
    driver.execute_script(img2JS)
    bgIMAGE = get_geetest_image(driver, name=os.path.join(IMG2_PATH, str(int(time.time())) + '.png'))
    return get_gap_offset(bgIMAGE, slideIMAGE)


def crack(driver, xMax):
    # 输入用户名密码
    # 点击验证按钮
    time.sleep(2)
    driver.execute_script(restoreJS)
    slider = get_slider(driver)
    ActionChains(driver).click_and_hold(on_element=slider).perform()
    # 往右边移动258个位置
    for i in get_tracks(xMax-3, 2):
        ActionChains(driver).move_to_element_with_offset(slider, i, 0).perform()
    # 松开鼠标
    ActionChains(driver).pause(0.5).release().perform()

# def reTry(driver, tryNum):
#     i = 1
#     xMax = None
#     while i < tryNum:
#         # 第一次点击滑块
#         if i == 1:
#             button = get_geetest_button(driver)
#             button.click()
#             time.sleep(2)
#             xMax = getDistance(driver)-2
#             crack(driver, xMax)
#             i += 1
#         # 成功直接退出
#         elif driver.find_element(By.CLASS_NAME, 'geetest_success_radar_tip_content').text == "验证成功":
#             return "验证成功,退出"
#         # 滑块距离异常导致重试直接退出
#         elif driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').text == "请完成验证":
#             print("重试中...")
#             # crack(driver, xMax)
#             # i += 1
#             break
#         # 轨迹异常导致提示网络不给力直接退出
#         elif driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').text == "网络不给力":
#             print("网络不给力, 重新点击")
#             # button = get_geetest_button(driver)
#             # button.click()
#             # time.sleep(2)
#             # crack(driver, getDistance(driver))
#             # i += 1
#             break
#         else:
#             break
#         # 获取滑块状态
#         WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip_content')))
#         time.sleep(5)
#     return "异常"

def reTry(driver):
    i = 1
    xMax = None
    while i < tryNum:
        # 第一次点击滑块
        if i == 1:
            button = get_geetest_button(driver)
            button.click()
            time.sleep(2)
            xMax = getDistance(driver)-2
            crack(driver, xMax)
            i += 1
        # 成功直接退出
        elif driver.find_element(By.CLASS_NAME, 'geetest_success_radar_tip_content').text == "验证成功":
            return "验证成功,退出"
        # 滑块距离异常导致重试直接退出
        # elif driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').text == "请完成验证":
        #     print("重试中...")
        #     # crack(driver, xMax)
        #     # i += 1
        # # 轨迹异常导致提示网络不给力直接退出
        # elif driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').text == "网络不给力":
        #     print("网络不给力, 重新点击")
        #     # button = get_geetest_button(driver)
        #     # button.click()
        #     # time.sleep(2)
        #     # crack(driver, getDistance(driver))
        #     # i += 1
        else:
            break
        # 获取滑块状态
        WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip_content')))
    return "异常"




if __name__ == '__main__':
    url = "https://yqt.midu.com/staticweb/#/login"
    driver = init_chrome_driver()
    succCount = 0
    for _ in range(1, 11):
        print(f"第{_}次执行, 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        res = open(driver, url)
        if "成功" in res:
            succCount+=1
            print(f"成功, 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
            print("-------------------------------------------------------------------------")
            continue
        else:
            time.sleep(2)
    print("成功次数: ", succCount)

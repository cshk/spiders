# -*- coding: UTF-8 -*-


from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.downImages import get_geetest_image
from utils.initBrowser import init_chrome_driver
from utils.jsExecute import img1JS, img2JS, restoreJS
from utils.getGap import get_gap_offset, get_gap_offset2
from utils.getSlider import get_geetest_button, get_slider
from utils.getTracks import get_tracks
from utils.captcha import returnCaptcha


import time
import os


USERNAME = '11111'
PASSWORD = '12311456'
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH = os.path.join(BASE_DIR, 'imgs')
IMG1_PATH = os.path.join(IMG_PATH, 'imgs1')
IMG2_PATH = os.path.join(IMG_PATH, 'imgs2')
CAPTCHA_PATH = os.path.join(IMG_PATH, 'captcha')
CAPTCHA_NAME = os.path.join(CAPTCHA_PATH, str(int(time.time())) + '.png')

# 打开页面
def open(driver, url):
    """
    打开网页输入用户名密码
    :return: 返回结果
    """
    driver.get(url)
    return main(driver)

# 获取距离
def getDistance(driver):
    # 获取验证码图片
    driver.execute_script(img1JS)
    slideIMAGE = get_geetest_image(driver, name=os.path.join(IMG1_PATH, str(int(time.time())) + '.png'))
    driver.execute_script(img2JS)
    bgIMAGE = get_geetest_image(driver, name=os.path.join(IMG2_PATH, str(int(time.time())) + '.png'))
    distance = get_gap_offset2(bgIMAGE, slideIMAGE)
    if distance:
        return distance-2
    else:
        print("滑块距离获取失败")
        return 0

# 移动滑块
def Move(driver, xMax):
    time.sleep(2)
    driver.execute_script(restoreJS)
    slider = get_slider(driver)
    ActionChains(driver).click_and_hold(on_element=slider).perform()
    # 往右边移动258个位置
    for i in get_tracks(xMax-3, 2):
        ActionChains(driver).move_to_element_with_offset(slider, i, 0).perform()
    # 松开鼠标
    ActionChains(driver).pause(0.5).release().perform()

# 获取验证码
def captcha(driver):
    time.sleep(0.5)
    # 输入用户名密码
    username = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.ant-input.ng-untouched.ng-pristine.ng-invalid.ng-star-inserted')))
    username.send_keys(12345)
    password = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.ant-input.ng-untouched.ng-pristine.ng-invalid.ng-star-inserted')))
    password.send_keys(12345)
    time.sleep(1)
    WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.XPATH, '//img[@class="ng-star-inserted"]')))
    imgObj = driver.find_element(By.XPATH, '//img[@class="ng-star-inserted"]')
    imgObj.screenshot(CAPTCHA_NAME)
    res = returnCaptcha(CAPTCHA_NAME)
    captcha = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.ant-input.ng-untouched.ng-pristine.ng-invalid.ng-star-inserted')))
    captcha.send_keys(res)
    submit = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.login-form-button.ant-btn.ant-btn-primary')))
    time.sleep(1)
    submit.click()
    WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.errorText.ng-star-inserted')))
    loginStatusInfo = driver.find_element(By.CSS_SELECTOR, '.errorText.ng-star-inserted').text
    if "账号或密码" in loginStatusInfo:
        return "验证码验证成功, 返回密码错误信息"
    else:
        return "验证码校验失败"

# 启动入口
def main(driver):
    # 点击验证按钮
    WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
    button = get_geetest_button(driver)
    button.click()
    time.sleep(1)
    # 获取滑块距离
    xMax = getDistance(driver)
    # 移动滑块
    Move(driver, xMax)
    # 等待状态信息刷新
    time.sleep(2)
    # 滑块轨迹异常可以直接输入账户密码然后使用ocr识别简单验证码进行登录
    if driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').text == "网络不给力":
        print("网络不给力,直接登录,处理简单验证码")
        data = captcha(driver)
        if "验证成功" in data:
            return data
        else:
            return data
    # 成功直接退出
    elif driver.find_element(By.CLASS_NAME, 'geetest_success_radar_tip_content').text == "验证成功":
        return "验证成功,退出"
    else:
        return "滑动距离异常, 退出"


if __name__ == '__main__':
    url = "https://yqt.midu.com/staticweb/#/login"
    # 初始化chrome
    driver = init_chrome_driver()
    print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}-------------------------------------------")
    # 运行
    res = open(driver, url)
    if "成功" in res:
        print(f"成功, 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    else:
        print(res)

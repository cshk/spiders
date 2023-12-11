# -*- coding: UTF-8 -*-


from selenium import webdriver


def init_chrome_driver():
    """
    初始化一个 chrome Driver
    :return: chrome Driver
    """
    option = webdriver.EdgeOptions()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

    # 实例化驱动
    driver = webdriver.Edge(options=option)
    return driver



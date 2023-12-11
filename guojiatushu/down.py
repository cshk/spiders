# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import requests
import time
import os


def img2pdf(chapterName, picPath):
    pngFiles = []
    tmp = []
    files = os.listdir(picPath)
    files.sort(key=lambda x: int(x[4:-4]), reverse=True)
    for file in files:
        filePath = picPath + '/' + file
        pngFiles.append(filePath)
    output = Image.open(pngFiles[0]).convert("RGB")
    pngFiles.pop(0)
    for png in pngFiles:
        pic = Image.open(png).convert('RGB')
        tmp.append(pic)
    output.save(f'{pdfPath}/{chapterName}.pdf', 'pdf', save_all=True, append_images=tmp)
    tmp.clear()
    print(f"{name} 图片转pdf完成")


def cut_img(data, path):
    img = Image.open(BytesIO(data))
    cropper = img.crop((620, 175, 1310, 970))
    cropper.save(path)


def getSingle(url, name):
    options = Options()
    options.add_argument('window-size=1920x1080')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.switch_to.frame("myframe")
    time.sleep(10)
    num = driver.find_element(By.XPATH, "//div[@class='fv__ui-toolbar-gotopage']").text.strip('/')
    next = driver.find_element(By.CSS_SELECTOR, ".fv__icon-toolbar-next-page")
    for i in range(int(num)):
        time.sleep(1)
        imgData = driver.get_screenshot_as_png()
        path = f'{chaptersPath}/{name}/page-{i+1}.png'
        cut_img(imgData, path)
        print(f"{name} page-{i+1}.png下载完成.")
        next.click()
        time.sleep(2)
    picPath = chaptersPath + "/" + name
    print(f"{name} 开始转换pdf.")
    img2pdf(name, picPath)


def getList(url):

    r = requests.get(url, headers=headers)
    data = r.content.decode('utf-8')
    html = BeautifulSoup(data, 'lxml')
    ul = html.find('ul', {'class': 'ul2 Z_clearfix'})
    lis = ul.select('li')
    for idx, li in enumerate(lis, start=1):
        content = li.select('a')
        name = content[0].string
        url = "http://read.nlc.cn" + content[1].get('href', '')
        data = name + " " + url
        with open('download.txt', 'a+', encoding='utf-8') as fp:
            fp.write(data+"\n")



if __name__ == '__main__':
    # url = "http://read.nlc.cn/allSearch/searchDetail?searchType=all&showType=1&indexName=data_892&fid=412000001748"
    # url = "http://read.nlc.cn/allSearch/searchDetail?searchType=all&showType=1&indexName=data_892&fid=412000001747"
    headers = {
        'Host': "read.nlc.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    # getList(url)
    dirName = "赫克尔-元哲学"
    base = os.getcwd() + "/" + dirName
    chaptersPath = base + "/" + "chapters"
    pdfPath = base + "/" + "pdfs"
    if not os.path.exists(base):
        os.mkdir(base)
        os.mkdir(chaptersPath)
        os.mkdir(pdfPath)
    with open('download.txt', encoding='utf-8') as fp:
        for line in fp.readlines():
            content = line.split(' ')
            name = content[0]
            url = content[1]
            if not os.path.exists(chaptersPath + "/" + name):
                os.mkdir(chaptersPath + "/" + name)
            getSingle(url, name)
            import random
            time.sleep(random.randint(10, 30))
    os.system('taskkill /im chromedriver.exe /F')
    os.system('taskkill /im chrome.exe /F')
    exit()



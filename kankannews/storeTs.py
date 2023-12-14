# -*-  coding: utf-8 -*-
"""
@author zz
@date 2023年12月13日 19:00:00
@packageName kankannews
@className 看看新闻直播第一财经ts文件采集
@version 1.0.0
@describe
"""
import time

import requests
import os
import re
from datetime import datetime


def ifExit():
    # 获取当前时间的时和分,当在指定小时过五分钟后退出
    curr = str(datetime.now().replace(microsecond=0).time()).split(':')
    if int(curr[0]) == 16 and int(curr[1]) >=5:
        print("当前时间为16:05,满足条件并退出")
        return False
    elif int(curr[0]) == 22 and int(curr[1]) >=5:
        print("当前时间为22:05,满足条件并退出")
        return False
    else:
        print("死循环中...")
        return True


def getTsName(url):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"{datetime.now().replace(microsecond=0)}\tM3u8文件请求异常")
            exit(-1)
        if int(r.headers.get('Content-Length', 0)) < 400:
            print(f"{datetime.now().replace(microsecond=0)}\tM3u8文件长度获取异常")
            exit(-1)
        m3u8File = r.content.decode('utf-8')
        tsUrlEnd = re.findall('dycj-.*?txspiseq=\d+.*', m3u8File)
        if tsUrlEnd:
            try:
                tsTime = tsUrlEnd[0].split('.')[0].split('-')[-1]
                tsKey = tsUrlEnd[0].split('=')[-1]
                tsUrl = "https://tencent-stream.kksmg.com/live/dycj-" + tsTime + '.ts?txspiseq=' + tsKey
                return tsTime, tsKey, tsUrl
            except Exception as e:
                print(f"{datetime.now().replace(microsecond=0)}\t{e}\tM3u8文件解析异常")
                exit(-1)
    except Exception as e:
        print(f"{datetime.now().replace(microsecond=0)}\t{e}\tM3u8文件下载异常")
        exit(-1)


def downloadTs(url, fileName):
    fileName = str(fileName) + ".ts"
    filePath = f"C:\\Users\\zz\\Videos\\ts\\{fileName}"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"{datetime.now().replace(microsecond=0)}\tts文件请求异常")
            exit(-1)
        if int(r.headers.get('Content-Length', 0)) < 100000:
            print(f"{datetime.now().replace(microsecond=0)}\tts文件长度获取异常")
            exit(-1)
        write2File(filePath, r.content)
    except Exception as e:
        print(f"{datetime.now().replace(microsecond=0)}\t{e}\tts文件下载异常")


def write2File(filePath, tsData):
    with open(filePath, 'wb') as fp:
        fp.write(tsData)
        print(f"{datetime.now().replace(microsecond=0)}\t{filePath} 文件下载完成")


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Host": "tencent-stream.kksmg.com",
        "Origin": "https://live.kankanews.com",
        "Platform": "pc",
        "Referer": "https://live.kankanews.com/"
    }
    f = open('./shcj.txt', 'r')
    url = f.read()
    f.close()
    tsTime, tsKey, tsUrl = getTsName(url)
    tsUrlPre = "https://tencent-stream.kksmg.com/live/"
    while 1:
        downloadTs(tsUrl, tsTime)
        tsTime = int(tsTime) + 1
        tsUrl = tsUrlPre + "dycj-" + str(tsTime) + '.ts?txspiseq=' + tsKey
        if not ifExit():
            print(f"{datetime.now().replace(microsecond=0)}\t采集任务结束")
            exit(1)
        time.sleep(7)





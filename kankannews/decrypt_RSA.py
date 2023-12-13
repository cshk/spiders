# -*-  coding: utf-8 -*-
"""
@author zz
@date 2023年12月13日 19:00:00
@packageName kankannews
@className 看看新闻直播m3u8采集
@version 1.0.0
@describe TODO 待更新不同时间段调用不同节目采集、自动同步到master采集机器
"""



"""
    站点:
        https://live.kankanews.com/huikan/
        东方卫视id: 648479
        第一财经id：648625
        上海新闻id：648560
        上海新闻(全天)
        07:00	09:30
        11:00	12:00	
        12:00	13:00
        17:00	18:30
        18:30	23:00
        第一财经(周一至周五)
        07:00	16:00
        21:00   22:00
        东方卫视(全天)
        07:00	09:00
        12:00	12:30
        17:00	19:00

https://volc-stream.kksmg.com/live/dfws/index.m3u8?volcSecret=590a28309783c0be49054c3875f6c232&volcTime=1702547711
https://tencent-stream.kksmg.com/live/dycj.m3u8?txSecret=17c6de392a8d6db4cdd85eecd2054c82&txTime=657ad100
https://volc-stream.kksmg.com/live/xwzh/index.m3u8?volcSecret=1455ec856f6852ff810b5b7878010527&volcTime=1702547712
"""

import random
import string
import time
import requests
import hashlib
import os
import re
import logging.config


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.conf'))
logger = logging.getLogger('applog')


def md5Encode(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()

def randomString(length=8):
    # 生成一个指定长度的随机字符串
    letters_and_digits = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_str

def getSign(nonce, timestamp, id):
    data = {
        "Api-Version": "v1",
        "channel_program_id": id,
        "nonce": nonce,
        "platform": "pc",
        "timestamp": timestamp,
        "version": "v2.0.0"
    }
    s = ""
    key = "28c8edde3d61a0411511d3b1866f0636"
    for k, v in data.items():
        s += k + "=" + v + "&"
    s += key
    encryptData = md5Encode(s)
    # print("第一次md5值: " ,encryptData)
    encryptData2 = md5Encode(encryptData)
    # print(encryptData2)
    return encryptData2


def replaceM3u8(srsPath, *args):
    dfws, dycj, xwzh = args
    with open(srsPath, 'r') as fp:
        content = fp.read()
    s1 = re.sub(r'url https://.*?/live/dfws/index.m3u8.*?;', dfws, content)
    s2 = re.sub(r'url https://.*?/live/dycj.m3u8.*?;', dycj, s1)
    s3 = re.sub(r'url https://.*?/live/xwzh/index.m3u8.*?;', xwzh, s2)
    with open(srsPath, 'w') as fp2:
        fp2.write(s3)


if __name__ == '__main__':
    showsId = {
        '东方卫视': '648479',
        '第一财经': '648625',
        '上海新闻': '648560',
    }
    srsPath = './srs.conf'
    newM3u8 = []
    if not os.path.exists('logs'):
        os.mkdir('logs')

    for k, v in showsId.items():
        nonce = randomString()
        timestamp = str(int(time.time()))
        sign = getSign(nonce, timestamp, v)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Nonce": nonce,
            "Origin": "https://live.kankanews.com",
            "Platform": "pc",
            "Referer": "https://live.kankanews.com/",
            "Sign": sign,
            "Timestamp": timestamp,
            "Version": "v2.0.0"

        }
        url = f"https://kapi.kankanews.com/content/pc/tv/program/detail?channel_program_id={v}"
        try:
            r = requests.get(url, headers=headers).json()
            encryptUrl = r['result']['channel_info']['live_address']
            decodeUrl = os.popen(r"node decrypt_RSA.js {}".format(encryptUrl))
            decodeUrl = decodeUrl.read().strip()
            decodeUrl = "url " + decodeUrl + ";"
            logger.info(f"{k} m3u8地址: {decodeUrl}")
            newM3u8.append(decodeUrl)
            exit()
        except Exception as e:
            logger.error(f"{k}m3u8地址: 请求异常.")
    replaceM3u8(srsPath, *newM3u8)


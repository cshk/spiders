# -*-  coding: utf-8 -*-

import random
import string
import time
import requests
import hashlib
import os


def md5Encode(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()

def randomString(length=8):
    # 生成一个指定长度的随机字符串
    letters_and_digits = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_str

def getSign(nonce, timestamp):
    data = {
        "Api-Version": "v1",
        "channel_program_id": '643384',
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



if __name__ == '__main__':
    nonce = randomString()
    timestamp = str(int(time.time()))
    sign = getSign(nonce, timestamp)
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
    url = "https://kapi.kankanews.com/content/pc/tv/program/detail?channel_program_id=643384"
    try:
        r = requests.get(url, headers=headers).json()
        encryptUrl = r['result']['channel_info']['live_address']
        decodeUrl = os.popen(r"node C:\Users\zz\Desktop\jsCodes\1.js {}".format(encryptUrl))
        print(decodeUrl.read().strip())
    except Exception as e:
        print("请求异常.")


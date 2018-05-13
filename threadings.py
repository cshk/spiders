import aiohttp
import asyncio
import os
from concurrent import futures
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.64'}
base_url = 'http://flupy.org/data/flags'
list = ('cn in us id br pk ng bd ru jp').split()


def download_flag(cc):
    url = '{}/{name}/{name}.gif'.format(base_url, name=cc)
    r = requests.get(url, headers=headers).content
    return r

# 保存图片


def save_imgs(image, filename):

    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    with open('imgs/' + filename, 'wb') as f:
        f.write(image)


def show_imgs(cc):
    print(cc)
# 获取单个图片


def get_one(cc):
    image = download_flag(cc)
    show_imgs(cc)
    save_imgs(image, cc + '.gif')
# 获取所有图片


def get_all(list):
    with futures.ThreadPoolExecutor(30) as tp:
        res = tp.map(get_one, sorted(list))


def main():
    get_all(list)


main()

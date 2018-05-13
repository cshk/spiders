"""
    百度音乐
    asyncio + aiohttp + 多进程 异步并发
"""
import requests
import json
import re
import os
import asyncio
import aiohttp
import multiprocessing


# 取mp3 name 和 url
# sid = '589660737'
# api = 'http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17206922749868485099_1525541803631&songid={}&_=1525541807548'.format(
#     sid)
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}


async def get_sid(api):
    async with aiohttp.ClientSession() as session:
        async with session.get(api, headers=headers) as r:
            sid = re.findall(r'.*?sid&quot;:(\d+)', await r.text())
            for id in sid:
                await get_music_info(id)


async def get_music_info(id):

    api = 'http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17206922749868485099_1525541803631&songid={}&_=1525541807548'.format(
        id)
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as r:
            dic = re.findall(r'\((.*)\)', await r.text())[0]
            data = json.loads(dic)
            try:
                title = data['songinfo']['title']
                lrc = data['songinfo']['lrclink']
                url = data['bitrate']['file_link']
                await download_music(url, title)
            except AttributeError as e:
                print(e)


async def download_music(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            # 写入本地
            if not os.path.exists('music'):
                os.mkdir('music')
            with open('music/' + filename + '.mp3', 'wb') as f:
                f.write(await r.read())
                print(filename + '.mp3 downloaded')


def main(url):
    loop = asyncio.get_event_loop()
    tasks = [get_sid(url)]  # 构建任务
    loop.run_until_complete(asyncio.wait(tasks))  # 等待任务完成
    loop.close()  # 关闭


if __name__ == '__main__':
    stars = ['张国荣', '刘德华', '周华健']
    query_lst = []
    for i in range(len(stars)):
        query_lst.append(
            'http://music.baidu.com/search?key={}'.format(stars[i]))
    p = multiprocessing.Pool()
    for url in query_lst:
        p.apply_async(main, args=(url,))

    p.close()
    p.join()

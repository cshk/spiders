"""
    一点资讯新闻抓取
    多进程+异步asyncio
"""

import asyncio
import aiohttp
import multiprocessing
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import motor.motor_asyncio
from bs4 import BeautifulSoup
import html

# 头条的URLs
base_urls = [
    'http://www.yidianzixun.com/channel/hot',
    # 'https://www.toutiao.com/ch/news_hot/',
    # 'https://www.toutiao.com/ch/news_tech/',
    # 'https://www.toutiao.com/ch/news_finance/',
    # 'https://www.toutiao.com/ch/news_world/',
    # 'https://www.toutiao.com/ch/news_military/',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}


# 连接数据库
def Connect_Mongodb():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        db = client['yidianzixun']
        collection = db['yidianzixun_spider']
    except ConnectionError as e:
        print('connect error :{}', format(e))
    else:
        return collection


# 配置浏览器
def config_driver():
    opts = Options()
    # 设置不加载图片
    prefs = {"profile.managed_default_content_settings.images": 2}
    opts.add_experimental_option("prefs", prefs)
    # 添加headless 模式
    opts.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=opts)
    return driver


async def get_page_source(url):
    """
    pull_down 下拉次数
    pixel 下拉像素
    entry 条目
    """
    pull_down = 3
    pixel = 2000
    driver = config_driver()
    driver.get(url)
    time.sleep(.5)
    entry = await get_info(0, driver.page_source)
    for i in range(pull_down):
        driver.execute_script('window.scrollTo(0, {})'.format(pixel))
        pixel += 200
        entry = await get_info(entry, driver.page_source)
        time.sleep(.5)


async def get_info(entry, response):
    # entry 跳过的条目
    all_info = BeautifulSoup(response, 'lxml').find('div', class_='channel-news-0').find_all('a', {'class': 'item'})
    for item in all_info[entry:]:
        try:
            title = item.find('div', class_='doc-title').get_text()
            url = 'https://www.yidianzixun.com' + item['href']
            source = item.find('span', class_='source').get_text()
            craw_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            pub_time = item.find('span', class_='date').get_text()
            if '刚刚' in pub_time:
                pub_time = craw_time
            detail = await get_detail(url)
            if '一点资讯' not in detail:
                continue
            soup = BeautifulSoup(detail, 'lxml')
            content = soup.find('div', class_='content-bd').get_text()
        except AttributeError:
            continue
        except IndexError:
            pass
        else:
            print('1')
            document = {
                'url': url,
                'title': title,
                'source': source,
                'crawl_time': craw_time,
                'content': content,
                'publish_time': pub_time,
            }
            print(document)
            # await do_insert(document)
    return len(all_info)


async def get_detail(url):
    async  with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            return await res.text()


# 插入数据
async def do_insert(document):
    try:
        # filename = document['title']
        # if not os.path.exists('news'):
        #     os.mkdir('news')
        # with open('news/{}.json'.format(filename), 'w') as f:
        #     f.write(json.dumps(document, ensure_ascii=False, indent=4))
        #     print('downloading {}'.format(document['title']))
        collection = Connect_Mongodb()
        res = await collection.insert_one(document)
    except BaseException as e:
        print('error {}'.format(e))
    else:
        print('res: {}'.format(repr(res.inserted_id)))


def main(url):
    loop = asyncio.get_event_loop()
    tasks = [get_page_source(url) for url in base_urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main(base_urls)
    #启用进程池
    p = multiprocessing.Pool()
    for url in base_urls:
        p.apply_async(main, args=(url,))
    p.close()
    p.join()
    config_driver().quit()
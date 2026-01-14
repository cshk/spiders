#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/8/28 22:13
# @Author : hk
# @File : single_async.py
from pathlib import Path

import aiofiles
import asyncio
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)

from config import URL, FILENAME, ITER_CHUNK_SIZE, HEADERS,CHUNK_COUNT
import niquests


async def get_file_size(url):
    async with niquests.AsyncSession() as session:
        resp = await session.head(url, headers=HEADERS)
        return int(resp.headers.get('Content-Length', 0))


async def download_chunk(session, url, start, end, chunk_id):
    headers = {"Range": f"bytes={start}-{end}"}
    print(f"开始分块下载: {chunk_id}")
    resp = await session.get(url, headers=headers)
    async with resp:
        chunk = await resp.content.read()
        return chunk, chunk_id


async def parallel_download(url, path, chunk_size = 1024*1024):
    file_size = await get_file_size(url)
    if file_size == 0:
        print("文件大小为0, 下载失败")
        return
    print(f"文件大小: {file_size} bytes")
    tasks = []
    async with niquests.AsyncSession() as session:
        for i in range(0, file_size, chunk_size):
            start = i
            end = min(i + chunk_size - 1, file_size - 1)
            task = download_chunk(session, url, start, end, i // chunk_size)
            tasks.append(task)

    res = await asyncio.gather(*tasks)
    res.sort(key=lambda x: x[1])
    with open(path, 'wb') as f:
        for chunk, _ in res:
            f.write(chunk)
    print(f"文件下载完成, 保存路径: {path}")

async def main() -> None:
    file_url = "https://dldir1.qq.com/qqfile/qq/PCQQ9.7.17/QQ9.7.17.29225.exe"
    path = Path.cwd() / "11"
    await parallel_download(file_url, path)

if __name__ == '__main__':
    asyncio.run(main())









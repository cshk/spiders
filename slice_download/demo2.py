#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/8/30 09:31
# @Author : hk
# @File : demo2.py



import niquests
from pathlib import Path
import rich
from config import HEADERS, ITER_CHUNK_SIZE, URL, FILENAME, CHUNK_COUNT
from utils import slice_by_count
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn, DownloadColumn, TransferSpeedColumn


def download_slice(idx, start, end, session, p, main_task):
    headers = HEADERS|{'Range': f'bytes={start}-{end}'}
    task = p.add_task(
        f"Downloading slice {idx}",
        total=end - start + 1,
        start=False
    )
    resp = session.get(URL, headers=headers, stream=True)
    with open(FILENAME, 'rb+') as fp:
        fp.seek(start)
        p.start_task(task)
        for chunk in resp.iter_content(chunk_size=ITER_CHUNK_SIZE):
            fp.write(chunk)
            p.update(task, advance=len(chunk))
            p.update(main_task, advance=len(chunk))


def main():
    Path(FILENAME).touch(exist_ok=True)
    max_workers = CHUNK_COUNT
    with (
        Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn("{task.percentage:>5.1f}%"),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(compact=True, elapsed_when_finished=True)
        ) as p,
        niquests.Session() as session,
        ThreadPoolExecutor(max_workers=max_workers) as pool,
    ):
        resp = session.head(URL, headers=HEADERS)
        content_length = int(resp.headers.get('content-length',0))
        rich.print(f"[color(100)]开始下载:")
        main_task = p.add_task(f"[color(204)]{FILENAME}", total=content_length)
        for idx, start, end in slice_by_count(content_length, CHUNK_COUNT):
            pool.submit(download_slice, idx, start, end, session, p, main_task)


if __name__ == '__main__':
    main()
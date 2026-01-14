#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/20 15:35
# @Author   : zz
# @File     : sync_multithreading_download.py
# @Annotate :
# ----------------------------
from asyncio import Event

from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from config import URL, FILENAME, CHUNK_COUNT, ITER_CHUNK_SIZE
from concurrent.futures import ThreadPoolExecutor
from utils import slice_by_count
from pathlib import Path


import time
import signal
import niquests


def download_slice(idx, start, end):
    headers = {"Range": f"bytes={start}-{end}"}
    task = p.add_task(f"Downloading slice {idx}", total=end - start + 1, start=False)
    resp = session.get(URL, headers=headers, stream=True)
    with open(file, "rb+") as fp:
        fp.seek(start)
        p.start_task(task)
        for chunk in resp.iter_content(chunk_size=ITER_CHUNK_SIZE):
            fp.write(chunk)
            p.update(task, advance=len(chunk))
            p.update(main_task, advance=len(chunk))
            if keyboard_interrupt_event.is_set():
                return


def single_handler(signal, frame):
    # ctrl + c 信号处理函数
    keyboard_interrupt_event.set()
    raise KeyboardInterrupt()



if __name__ == '__main__':
    keyboard_interrupt_event = Event()
    signal.signal(signal.SIGINT, single_handler)

    file = "TEST2-" + FILENAME
    Path(file).touch(exist_ok=True)
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
        resp = session.head(URL)
        content_length = int(resp.headers.get('content-length'))
        main_task = p.add_task(f"[color(204)]{file}", total=content_length)
        for idx, start, end in slice_by_count(content_length, CHUNK_COUNT):
            pool.submit(download_slice, idx, start, end)
        while not p.finished:
            time.sleep(1)
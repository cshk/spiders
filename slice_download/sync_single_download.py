#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/20 14:36
# @Author   : zz
# @File     : sync_single_download.py
# @Annotate : 单线程同步下载文件测试
# ----------------------------


from pathlib import Path
from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from config import URL, FILENAME, ITER_CHUNK_SIZE


import niquests

file = "TEST1-" + FILENAME
Path(file).touch(exist_ok=True)


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
    open(file, "wb") as fp
):
    resp = session.get(URL, stream=True)
    content_length = int(resp.headers.get('content-length'))
    main_task = p.add_task(f"[color(204)]{file}", total=content_length)
    for chunk in resp.iter_content(chunk_size=ITER_CHUNK_SIZE):
        fp.write(chunk)
        p.update(main_task, advance=len(chunk))


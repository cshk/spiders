#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/24 16:58
# @Author   : zz
# @File     : merge.py
# @Annotate :
# ----------------------------

from pathlib import Path
from m3u8 import M3U8
from typing import List
from itertools import accumulate

import asyncio
import aiofiles
from tqdm.asyncio import tqdm_asyncio


async def merge_files(files_list: List[Path], output_file: Path) -> None:
    async def fn1(file_path:Path, file_point:int):
        async with sem:
            async with aiofiles.open(file_path, 'rb') as f2:
                data = await f2.read()
                f1.seek(file_point)
                f1.write(data)

    sem = asyncio.Semaphore(256)
    file_sizes = [f.stat().st_size for f in files_list]
    file_points = accumulate(file_sizes[:-1], initial=0)
    with open(output_file, 'wb') as f1:
        tasks =[fn1(file_path, file_point) for file_path, file_point in zip(files_list, file_points)]
        await tqdm_asyncio.gather(*tasks)

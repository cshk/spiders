#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/24 15:15
# @Author   : zz
# @File     : run.py
# @Annotate :
# ----------------------------

from pathlib import Path
from tqdm.asyncio import tqdm_asyncio
# from Cryptodome.Cipher import AES
# from Cryptodome.Util.Padding import unpad
# from codes.logging_configs import logger
from typing import List,  Awaitable
from utils.merge import merge_files
from config import *

import m3u8
import certifi
import asyncio
import aiofiles
import niquests
import subprocess


class M3u8Downloader:
    def __init__(self):
        self.session: niquests.AsyncSession = niquests.AsyncSession(pool_maxsize=100)
        self.session.verify = certifi.where()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def load_m3u8(self, m3u8_url: str) -> m3u8.M3U8:
        print(f"正在读取m3u8链接: {m3u8_url}")
        resp: niquests.Response = await self.session.get(m3u8_url)
        return m3u8.M3U8(resp.text, base_uri=m3u8_url.rsplit("/", 1)[0])

    async def download(self, m3u8_url: str) -> None:
        playlist: m3u8.M3U8 = await self.load_m3u8(m3u8_url)
        print(f"m3u8文件解析成功, 共有{len(playlist.segments)}个分段")
        await self.download_ts(playlist)
        # key: m3u8.Key = playlist.keys[0]
        # if key:
        #     aes_key: bytes = await self.get_key(key.uri)
        #     iv: bytes = bytes.fromhex(key.iv[2:])
        #     await self.decrypt_ts(aes_key, iv)
        await self.merge_ts()
        self.ts2mp4()
        # self.clean_up()

    # async def get_key(self, key_url: str) -> bytes:
    #     resp: niquests.Response = await self.session.get(key_url)
    #     return resp.content

    # async def decrypt_ts(self, aes_key: bytes, iv: bytes) -> None:
    #     async def fn(enc_ts_file: Path) -> None:
    #         async with sem:
    #             aes: AES = AES.new(aes_key, AES.MODE_CBC, iv)
    #             dec_ts_file: Path = DEC_TS_DIR / enc_ts_file.name
    #             async with aiofiles.open(dec_ts_file, "rb") as enc_f:
    #                 data: bytes = await enc_f.read()
    #                 decrypted_data : bytes = unpad(aes.decrypt(data), AES.block_size)
    #                 with open(dec_ts_file, "wb") as dec_f:
    #                     dec_f.write(decrypted_data)
    #     sem: asyncio.Semaphore = asyncio.Semaphore(FILES_CONCURRENCY)
    #     tasks: list[Awaitable[None]] = [fn(enc_ts_file) for enc_ts_file in ENC_TS_DIR.iterdir()]
    #     await tqdm_asyncio.gather(*tasks)

    async def download_ts(self, playlist: m3u8.M3U8) -> None:
        async def fn(segment: m3u8.Segment, index: int) -> None:
            async with sem:
                ts_file: Path = TS_DIR / f"{index}.ts"
                resp: niquests.AsyncResponse = await self.session.get(segment.absolute_uri, stream=True)
                with open(ts_file, "wb") as f:
                    async for chunk in await resp.iter_content():
                        f.write(chunk)
        TS_DIR.mkdir(exist_ok=True)
        sem: asyncio.Semaphore = asyncio.Semaphore(FETCH_CONCURRENCY)
        tasks: list[Awaitable[None]] = [fn(segment, index) for index, segment in enumerate(playlist.segments)]
        print(f"开始下载ts文件")
        await tqdm_asyncio.gather(*tasks)

    @staticmethod
    async def merge_ts() -> None:
        ts_files: List[Path] = sorted(TS_DIR.iterdir(), key=lambda x: int(x.stem))
        print(f"开始合并ts文件")
        await merge_files(ts_files, OUTPUT_TS)

    @staticmethod
    def ts2mp4() -> None:
        ret: subprocess.CompletedProcess = subprocess.run([
            f"{FFMPEG_PATH}",
            "-i",
            f"{OUTPUT_TS}",
            "-c",
            "copy",
            "-y",
            f"{OUTPUT_MP4}",
        ], capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"ffmpeg命令执行失败: {ret.stderr}")
        else:
            print(f"ts文件合并成功, 输出文件: {OUTPUT_MP4}")

    # @staticmethod
    # def clean_up() -> None:
    #     for enc_ts_file in ENC_TS_DIR.iterdir(): enc_ts_file.unlink()
    #     for dec_ts_file in DEC_TS_DIR.iterdir(): dec_ts_file.unlink()
    #     ENC_TS_DIR.rmdir()
    #     DEC_TS_DIR.rmdir()
    #     OUTPUT_TS.unlink()

    @staticmethod
    async def main() -> None:
        url = "https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8"
        async with M3u8Downloader() as downloader:
            await downloader.download(url)


if __name__ == '__main__':
    asyncio.run(M3u8Downloader.main())
    # download = M3u8Downloader()
    # res = download.load_m3u8("https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8")
    # print(res)
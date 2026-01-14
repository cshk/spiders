#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/24 17:00
# @Author   : zz
# @File     : config.py
# @Annotate :
# ----------------------------


from pathlib import Path


OUTPUT_TS: Path = Path("merged.ts")
OUTPUT_MP4: Path = Path("output.mp4")
TS_DIR: Path = Path.cwd() / Path("ts-files")
# ENC_TS_DIR: Path = Path("enc-ts-files")
# DEC_TS_DIR: Path = Path("dec-ts-files")
FETCH_CONCURRENCY: int = 32
FILES_CONCURRENCY: int = 256
FFMPEG_PATH: str = r"D:\tools\ffmpeg\bin\ffmpeg.exe"
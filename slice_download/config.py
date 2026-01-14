#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/20 15:05
# @Author   : zz
# @File     : config.py
# @Annotate :
# ----------------------------


CHUNK_COUNT = 6
CHUNK_SIZE = 1024 * 1024 * 32  # 32MB
ITER_CHUNK_SIZE = 1024 * 64  # 64KB
# URL = 'https://mirrors.ustc.edu.cn/ubuntu-cdimage/releases/25.10/snapshot-3/ubuntu-25.10-snapshot3-desktop-amd64.iso'
URL = 'https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.22/releases/x86_64/alpine-virt-3.22.0_rc4-x86_64.iso'
FILENAME = URL.split('/')[-1]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/8/29 22:27
# @Author : hk
# @File : demo.py



import threading
import niquests
from tqdm import tqdm
from pathlib import Path

class MultiThreadDownload:

    def __init__(self, url, output, thread_count=4):
        self.url = url
        self.output = output
        self.thread_count = thread_count
        self.file_size = 0
        self.threads = []
        self.tmp_dir = "tmp_cache"
        self.lock = threading.Lock()


    def get_file_size(self):
        """
        获取文件大小
        :return:
        """
        with niquests.get(self.url, stream=True) as rep:
            self.file_size = int(rep.headers.get('Content-Length',0))
            return self.file_size

    def download_chunk(self, start, end, thread_id):
        """
        下载分块
        :param start:
        :param end:
        :param thread_id:
        :return:
        """
        headers = {'Range': f"bytes={start}-{end}"}
        tmp_file = Path.cwd() / self.tmp_dir / f"chunk_{thread_id}.tmp"

        with niquests.get(self.url, headers=headers, stream=True) as resp:
            with open(tmp_file, 'wb') as fp:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        fp.write(chunk)

    def merge_chunks(self):
        """
        合并分块
        :return:
        """
        with open(self.output, 'wb') as fp1:
            for i in range(self.thread_count):
                tmp_file = Path.cwd() / self.tmp_dir / f"chunk_{i}.tmp"
                with open(tmp_file, 'rb') as fp2:
                    fp1.write(fp2.read())
                Path.unlink(tmp_file)

    def cleanup(self):
        import shutil
        """
        清理临时文件
        :return:
        """
        if Path(self.tmp_dir).exists():
            shutil.rmtree(self.tmp_dir)

    def download(self):
        file_size = self.get_file_size()
        if file_size == 0:
            print("文件大小为0, 下载失败")
            return
        chunk_size = file_size // self.thread_count
        Path.mkdir(Path.cwd() / self.tmp_dir, exist_ok=True)

        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"正在下载 {self.url}") as pbar:
            threads = []
            for i in range(self.thread_count):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < self.thread_count - 1 else file_size - 1
                thead = threading.Thread(target=self.download_with_progress, args=(start, end, i, pbar))
                threads.append(thead)
                thead.start()
            for thead in threads:
                thead.join()
        self.merge_chunks()
        self.cleanup()


    def download_with_progress(self, start, end, i, pbar):
        self.download_chunk(start, end, thread_id=i)
        pbar.update(end - start + 1)


if __name__ == '__main__':
    url = "https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.22/releases/x86_64/alpine-virt-3.22.0_rc4-x86_64.iso"
    output = Path.cwd() / "alpine-virt-3.22.0_rc4-x86_64.iso"
    downloader = MultiThreadDownload(url,output, thread_count=8)
    downloader.download()
    print(f"文件下载完成, 保存路径: {output}")
























#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------
# @Time     : 2025/6/20 15:42
# @Author   : zz
# @File     : utils.py
# @Annotate :
# ----------------------------


from math import ceil


"""

    示例:
    总大小  1230000
    切分数量 11
    每个分片 111819
    第0次 start = 0           end=(0+111819,1230000)=111819                  yield 0//111810=0           0        111818
    第1次 start = 111819      end=(111819+111819=223638,1230000)=223638      yield 223638//111810=1      111819   223637
    ...
    第9次 start = 1006371     end= (1006371+111819=1118190, 1230000)=1118190 yield 1006371//111810=9    1006371  1118189
    第10次 start = 1118190    end = min(1118190 + 111819=1230009, 1230000)   yield 1118190//111810=10   1118190  1229999


    chunk_size = ceil(1230000 / 11) 向上取整函数; 返回大于或等于给定数字的最小整数,防止结果带小数
    end = min(start + chunk_size, content_length) min避免超出文件长度,最后一个小于前面的等分数量
    每次yield结果回去 end - 1 因为下一次的start指针等于end,如果不-1,每一次指针的结尾都会包含下一次的指针开始,就会多出来一位重复的
    最后将结束指针赋值给start进行位置更新
"""
def slice_by_size(content_length, chunk_size):
    """
    按照文件字节大小进行切片
    :param content_length: 文件总字节数
    :param chunk_size: 每个分片的字节数
    :return:
        返回一个三元组(分片数量, 开始字节, 结束字节)
        (0, 0, 104857599) (1, 104857600, 209715199)
        ...
        (54, 5662310400, 5665497087) 最后一个分片小于总大小
        总大小: 5665497088
    """
    start = 0
    # 确保切片起始位置不超过文件总大小
    while start < content_length:
        # 动态计算切片大小结束位置
        end = min(start + chunk_size, content_length)
        yield start // chunk_size, start, end - 1
        # 将下一个切片位置设置为当前分片结束位置,实现连续切片
        start = end


def slice_by_count(content_length, chunk_count):
    """
    按照切片数量进行切片, 然后多线程下载每个线程负责的切片数量
    :param content_length: 文件总字节数
    :param chunk_count: 目标切片数量
    :return: yield 序号 指针开始位置 指针结束位置
    """
    start = 0
    # 将文件总字节数除以目标切片数量, 得到每个切片的大小
    chunk_size = ceil(content_length / chunk_count)
    while start < content_length:
        end = min(start + chunk_size, content_length)
        yield start // chunk_size, start, end - 1
        start = end


if __name__ == '__main__':
    content_length = 5665497088 # 长度
    chunk_size = 1024 * 1024 * 100 # 100M
    chunk_count = 4
    print(*slice_by_size(content_length, chunk_size))
    print(*slice_by_count(content_length, chunk_count))
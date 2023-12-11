# -*- coding: UTF-8 -*-


import numpy as np


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def get_tracks(distance, seconds):
    """
    根据轨迹离散分布生成的数学生成
    成功率很高
    :param distance: 缺口位置
    :param seconds:  时间
    :param ease_func: 生成函数
    :return: 轨迹数组
    """
    distance += 20
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        offset = round(ease_out_quart(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    tracks.extend([-3, -2, -3, -2, -2, -2, -2, -1, -0, -1, -1, -1])
    return tracks
# -*- coding: UTF-8 -*-


from PIL import Image



def is_pixel_equal(img1, img2, x, y):
    """
    判断两张图片的同一像素点的RGB值是否相等
    """
    pixel1, pixel2 = img1.load()[x, y], img2.load()[x, y]
    # print(pixel1,pixel2)
    # 设定一个比较基准
    sub_index = 60

    # 比较
    if abs(pixel1[0] - pixel2[0]) < sub_index and abs(pixel1[1] - pixel2[1]) < sub_index and abs(
            pixel1[2] - pixel2[2]) < sub_index:
        return True
    else:
        return False


def get_gap_offset(img1, img2):
    """
        获取缺口的偏移量
    """
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    x = int(img1.size[0] / 4.2)
    for i in range(x, img1.size[0]):
        for j in range(img1.size[1]):
            # 两张图片对比,(i,j)像素点的RGB差距，过大则该x为偏移值
            if not is_pixel_equal(img1, img2, i, j):
                x = i
                return x
    return x


import ddddocr


def get_gap_offset2(bgIMAGE, slideIMAGE):
    slide = ddddocr.DdddOcr(det=False, ocr=False)

    with open(slideIMAGE, 'rb') as f:
        target_bytes = f.read()

    with open(bgIMAGE, 'rb') as f:
        background_bytes = f.read()
    try:
        res = slide.slide_comparison(target_bytes, background_bytes)
        return res['target'][0]
    except Exception as e:
        return 0

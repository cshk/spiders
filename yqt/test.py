# -*- coding: UTF-8 -*-


import time
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, 'imgs')
IMG1_PATH = os.path.join(IMG_PATH, 'imgs1')
IMG2_PATH = os.path.join(IMG_PATH, 'imgs2')

import ddddocr
import cv2

slide = ddddocr.DdddOcr(det=False, ocr=False)

with open(os.path.join(IMG1_PATH, '1694692054.png'), 'rb') as f:
    target_bytes = f.read()

with open(os.path.join(IMG2_PATH, '1694692055.png'), 'rb') as f:
    background_bytes = f.read()

res = slide.slide_comparison(target_bytes, background_bytes)

print(res['target'][0])

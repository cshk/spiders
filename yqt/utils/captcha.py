# -*- coding: UTF-8 -*-


import ddddocr


def returnCaptcha(CAPTCHA_NAME):
    ocr = ddddocr.DdddOcr()

    with open(CAPTCHA_NAME, 'rb') as f:
        image = f.read()
    return ocr.classification(image)

# -*- coding:utf-8 -*-


import os

from PIL import Image



def img2pdf(pngFiles, chapterName):
    tmp = []
    output = Image.open(pngFiles[0]).convert("RGB")
    pngFiles.pop(0)
    for file in pngFiles:
        pic = Image.open(file).convert('RGB')
        tmp.append(pic)
    output.save(f'{pdfPath}/{chapterName}.pdf', 'pdf', save_all=True, append_images=tmp)
    output.close()


if __name__ == '__main__':
    base = os.getcwd()
    pdfPath = base + '/太平广记29/pdfs'
    dirPath = base + '/太平广记29/chapters'
    dir_ = os.listdir(dirPath)
    for files in dir_:
        pngFiles = []
        chapterPath = dirPath+'/'+files
        chapterName = chapterPath.split('/')[-1]
        files = os.listdir(chapterPath)
        files.sort(key=lambda x:int(x[4:-4]), reverse=True)
        for file in files:
            print(file)
            filePath = chapterPath + '/' + file
            pngFiles.append(filePath)
        img2pdf(pngFiles, chapterName)
        print(f"{chapterName}.pdf 转换完成.")


























# -*- coding:utf-8 -*-



from PIL import Image
from PyPDF2 import PdfMerger, PdfReader
import os


def img2pdf(pngFiles, chapterName):
    """
    pngFiles.pop(0) Image对象为第一张，所以要pop出去
    tmp.append(pic) 这里的tmp列表需要释放内存
    :param pngFiles: 所有图片绝对地址
    :param chapterName: 目录名 对应文件名
    :return:
    """
    tmp = []
    output = Image.open(pngFiles[0]).convert("RGB")
    pngFiles.pop(0)
    for file in pngFiles:
        pic = Image.open(file).convert('RGB')
        tmp.append(pic)
    output.save(f'{pdfPath}/{chapterName}.pdf', 'pdf', save_all=True, append_images=tmp)
    # 内存释放
    tmp.clear()
    return 1


def getPdfs():
    """
        chaptersDir 章节目录
        chaptersDir.sort 对目录排序
    :return:
    """
    chaptersDir = os.listdir(dirPath)
    chaptersDir.sort(key=lambda x:int(x[1:-1]))
    for dir_ in chaptersDir:
        chapterPath = dirPath + '/' + dir_
        chapterName = chapterPath.split('/')[-1]
        files = os.listdir(chapterPath)
        files.sort(key=lambda x:int(x[4:-4]), reverse=True)
        for file in files:
            filePath = chapterPath + '/' + file
            pngFiles.append(filePath)
        img2pdf(pngFiles, chapterName)
        print(f"{chapterName}.pdf 转换完成.")
    return 1


def pdfMerge(pdfPath):
    """
        pageNum 定位页码进行pdf合并
        fileMerge.add_outline_item(title, pageNum)  指定当前pdf文件的书签名和页码
    :param pdfPath:
    :return:
    """
    pageNum = 0
    pdfs = os.listdir(pdfPath)
    pdfLst = [f for f in pdfs if f.endswith('.pdf')]
    pdfLst.sort(key=lambda x:int(x[1:-5]))
    pdfLst = [os.path.join(pdfPath, filename) for filename in pdfLst]
    fileMerge = PdfMerger()
    for pdf in pdfLst:
        pdfR = PdfReader(pdf)
        title = pdf.split('\\')[-1][:-4]
        fileMerge.append(pdf)
        fileMerge.add_outline_item(title, pageNum)
        pageNum += len(pdfR.pages) - 1
    fileMerge.write(savePath+"/o.pdf")
    fileMerge.close()


if __name__ == '__main__':
    base = os.getcwd()
    bookName = "太平广记29"
    pngFiles = []
    pdfPath = base + f'/{bookName}/pdfs'
    dirPath = base + f'/{bookName}/chapters'
    savePath = base + f'/{bookName}'
    getPdfs()
    # pdfMerge(pdfPath)
































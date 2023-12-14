# -*-  coding: utf-8 -*-
"""
@author zz
@date 2023-12-14 22:24
@packageName mergeTs.py
@describe  TS合并程序
@version 1.0.0
"""

"""
合并程序
43个文件为一组
6分钟检查一次,读取列表文件，如果list有43个
进行合并;文件名以启动时间为准，06:59开始,那么文件名就是 
"tv-shanghaicj-shanghaicj-{datetime.now().strftime('%Y%m%d-%H%M%S.%f')[:-3]}.mp4"
tv-shanghaicj-shanghaicj-20231214-065900.xxx.mp4
"""
import os
from datetime import datetime


BASEDIR = r"C:\Users\zz\Videos\ts"
STOREDIR = os.path.join(BASEDIR, "mp4")
TSLENGTH = 43
FLAGFILE = os.path.join(BASEDIR, "mergeflag")
TSLIST = os.path.join(BASEDIR, "tslist")
TSNAME = []


def getFlag():
    with open(FLAGFILE, 'r') as fp:
        flag = fp.read().strip()
        return flag


def write2flag(ts, fileName):
    with open(FLAGFILE, 'w', encoding='utf-8') as fp:
        fp.write(ts)
        print(f"{fileName} 文件已写入, 当前ts标志位为: ", ts)


def updateName(timestamp):
    obj = datetime.fromtimestamp(int(timestamp))
    obj = obj.strftime("%Y%m%d-%H%M%S.%f")[:-3]
    fileName = os.path.join(STOREDIR, "tv-shanghaicj-shanghaicj-" + obj + ".mp4")
    return fileName


def mergeFiles(TSNAME, flag):
    if not flag:
        command = ""
        timestamp = TSNAME[0].split('.')[0]
        fileName = updateName(timestamp)
        for _ in TSNAME[:38]:
            command += os.path.join(BASEDIR, _ + "|")
        os.popen(f'ffmpeg -y -i concat:"{command[:-1]}" -c copy {fileName}')
        write2flag(TSNAME[37], fileName)
    else:
        command = ""
        seek = TSNAME.index(flag)+1
        if len(TSNAME[seek:seek + 38]) == 38:
            timestamp = TSNAME[TSNAME.index(flag) + 1].split('.')[0]
            fileName = updateName(timestamp)
            for _ in TSNAME[seek:seek + 38]:
                command += os.path.join(BASEDIR, _ + "|")
            os.popen(f'ffmpeg -y -i concat:"{command[:-1]}" -c copy {fileName}')
            write2flag(TSNAME[seek + 38], fileName)
        else:
            try:
                timestamp = TSNAME[TSNAME.index(flag) + 1].split('.')[0]
                fileName = updateName(timestamp)
                for _ in TSNAME[seek:]:
                    command += os.path.join(BASEDIR, _ + "|")
                os.popen(f'ffmpeg -y -i concat:"{command[:-1]}" -c copy {fileName}')
                write2flag(TSNAME[-1], fileName)
            except IndexError:
                print("ts文件全部合并完成")
                exit()


def main():
    if not os.path.exists(STOREDIR):
        os.mkdir(STOREDIR)
    with open(TSLIST, 'r') as fp:
        for line in fp.readlines():
            TSNAME.append(line.strip())
    return TSNAME

if __name__ == "__main__":
    TSNAME = main()
    flag = getFlag()
    mergeFiles(TSNAME, flag)

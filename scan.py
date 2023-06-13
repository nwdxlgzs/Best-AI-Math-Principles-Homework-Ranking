'''
读取文件：namelist.txt
一行一个学生姓名，如果姓名后方有数字，那么是学号，否则学号为0(违规行为，但是为了程序运行支持)
'''
import sys
import re
import shutil
import os
student_list = []
with open('namelist.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip()
        if line:
            line = line.strip()
            # 判断有没有学号
            if line[-1].isdigit():
                # 找到学号的初始位置
                numfstIdx = len(line) - 1
                # 找到学号的位置
                numendIdx = numfstIdx
                while line[numfstIdx].isdigit():
                    numfstIdx -= 1
                numfstIdx += 1
                # 学号
                num = line[numfstIdx:numendIdx + 1]
                # 姓名
                name = line[:numfstIdx]
                student_list.append((name, num))
            else:
                student_list.append((line, '0'))
HomeWorkNum = 4  # 一共有几次作业(创建目录时用到)

# 中文数字
ZhNumDict = {
    # 简体必备
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
    '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
    '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
    '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30,
    '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35,
    '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39, '四十': 40,
    # 繁体支持
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
    '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10,
    '拾壹': 11, '拾贰': 12, '拾叁': 13, '拾肆': 14, '拾伍': 15,
    '拾陆': 16, '拾柒': 17, '拾捌': 18, '拾玖': 19, '贰拾': 20,
    '贰拾壹': 21, '贰拾贰': 22, '贰拾叁': 23, '贰拾肆': 24, '贰拾伍': 25,
    '贰拾陆': 26, '贰拾柒': 27, '贰拾捌': 28, '贰拾玖': 29, '叁拾': 30,
    '叁拾壹': 31, '叁拾贰': 32, '叁拾叁': 33, '叁拾肆': 34, '叁拾伍': 35,
    '叁拾陆': 36, '叁拾柒': 37, '叁拾捌': 38, '叁拾玖': 39, '肆拾': 40,
}


def TransNumStrAsInt(str):
    if str.isdigit():
        return int(str)
    else:
        return ZhNumDict[str]


'''
如果没有src/就创建文件夹：src
遍历src/下的文件
由：学号，姓名，第N次作业，后缀组成，可能存在空格、+、-、_等间隔符号，而且学号，姓名，第N次作业顺序不定，N是数字或者汉字都行
创建文件夹：dst，创建N个文件夹，每个文件夹里
保存格式：dst/{N}/学号+姓名+第N次作业.后缀
学号是一个至少大于3位的数字
'''

# 作业文件夹
HomeWorkDir = 'src'
# 重命名后的文件夹
RenameDir = 'dst'

# 如果没有src/就创建文件夹：src
if not os.path.exists(HomeWorkDir):
    os.mkdir(HomeWorkDir)

# 如果没有dst/就创建文件夹：dst
if not os.path.exists(RenameDir):
    os.mkdir(RenameDir)

# dst/下的子文件夹
for i in range(1, HomeWorkNum + 1):
    # 如果没有dst/{i}/就创建文件夹：dst/{i}/
    if not os.path.exists(os.path.join(RenameDir, str(i))):
        os.mkdir(os.path.join(RenameDir, str(i)))

# 作业文件夹下的文件
HomeWorkFileList = os.listdir(HomeWorkDir)

FailedList = []
# 遍历src/下的文件
for Raw_HomeWorkFile in HomeWorkFileList:
    HomeWorkFile = Raw_HomeWorkFile.strip()
    # 由：学号，姓名，第N次(作业)，后缀组成，可能存在空格、+、-、_等间隔符号，而且学号，姓名，第N次作业顺序不定，N是数字或者汉字都行
    # 例如：2017010101-张三_第一次作业.pdf
    # 例如：第2次作业 张三+154154.docx
    Sname = ''
    Sid = ''
    SHidx = 0
    # 文件拓展名
    Fext = HomeWorkFile.split('.')[-1]
    HomeWorkFile = HomeWorkFile[:-len(Fext) - 1].strip()
    # 学号至少3位以上，作为区分第N次作业的标志
    getidlen = 0
    for i in range(len(HomeWorkFile)):
        # 找到学号的初始位置
        if HomeWorkFile[i].isdigit():
            getidlen += 1
            if getidlen >= 3:  # 学号至少3位以上，作为区分第N次作业的标志
                endSidIdx = i
                # 继续找，直到不是数字
                while endSidIdx < len(HomeWorkFile) and HomeWorkFile[endSidIdx].isdigit():
                    endSidIdx += 1
                # 找到学号
                Sid = HomeWorkFile[i-2:endSidIdx]
                # 删除学号内容
                HomeWorkFile = HomeWorkFile[:i-2] + HomeWorkFile[endSidIdx:]
                break
        else:
            getidlen = 0
    HomeWorkFile = HomeWorkFile.strip()
    # 找到学号后，找到姓名，直接查student_list
    for student in student_list:
        if HomeWorkFile.find(student[0]) != -1 and (Sid == student[1] or 0 == student[1]):
            # 找到姓名
            Sname = student[0]
            # 删除姓名内容
            HomeWorkFile = HomeWorkFile.replace(student[0], '')
    HomeWorkFile = HomeWorkFile.strip()
    # 这时候过滤掉：第，次，作，业等
    rmap = {
        '第': '', '次': '', '人': '', '工': '', '智': '', '能': '',
        '数': '', '学': '', '原': '', '理': '', '作': '', '业': '',
        '大': '', '小': '', '测': '', '验': '', '考': '', '试': '',
        '报': '', '告': '', '课': '', '堂': '', '练': '', '习': '',
        '实': '', '验': '', ' ': '', '+': '', '-': '', '_': '',
        '\t': '', '*': '', '副': '', '本': '',
    }
    for k, v in rmap.items():
        HomeWorkFile = HomeWorkFile.replace(k, v)
    HomeWorkFile = HomeWorkFile.strip()
    # 剩下就是N了
    SHidx = TransNumStrAsInt(HomeWorkFile)
    # 保存格式：dst/{N}/学号+姓名+第N次作业.后缀
    # 先检查合法性
    if SHidx == None or SHidx <= 0 or SHidx > HomeWorkNum or Sname == '' or Sid == '':
        FailedList.append(Raw_HomeWorkFile)
        continue
    # 保存
    shutil.copy(os.path.join(HomeWorkDir, Raw_HomeWorkFile), os.path.join(
        RenameDir, str(SHidx), Sid + '-' + Sname + '-第' + str(SHidx) + '次作业.' + Fext))

# 输出失败的文件
if len(FailedList) > 0:
    print('以下文件重命名失败：')
    for f in FailedList:
        print(f)
    print('====================')

# 查询一下学生是否都交齐了
fnbak =[]# 备份文件信息防止反复读取
for i in range(1, HomeWorkNum + 1):
    fs = os.listdir(os.path.join(RenameDir, str(i)))
    for f in fs:
        # 删掉后缀
        f = f.split('.')[0]
        fnbak.append(f)
NotUploadList = {}#(学号，姓名，N)
findNU = False
for i in range(1, HomeWorkNum + 1):
    NotUploadList[i]=[]
    for student in student_list:
        FullMatchStr = student[1] + '-' + student[0] + '-第' + str(i) + '次作业'
        if fnbak.count(FullMatchStr) == 0:
            findNU = True
            NotUploadList[i].append((student[1], student[0]))
if findNU:
    print('以下同学没有交齐作业：')
    for i in range(1, HomeWorkNum + 1):
        if len(NotUploadList[i]) > 0:
            print('第' + str(i) + '次作业：', NotUploadList[i])
    print('====================')
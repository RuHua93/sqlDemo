# coding=utf-8
# 通用功能函数
import datetime
import string
import traceback
import sys

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

# 补齐字符串前导0
def addZero(str, slen):
    len_t = len(str)
    for i in range(slen-len_t):
        str = "0" + str
    return str

# 把原日期字符串转换成datetime类型的日期
# 此函数对韩饭网及大连生活网有效
def transTime(str):
    date = datetime.datetime.now()
    ye, mo, da, ho, mi, se = \
        date.year, date.month, date.day, date.hour, date.minute, date.second
    try:
        cur = ""
        cnt = 0
        for i in range(len(str)):
            if (str[i].isdigit()):
                cur = cur + str[i]
                if ((i == len(str)-1) or not str[i+1].isdigit()):
                    if (cnt == 0):
                        ye = int(cur)
                    elif (cnt == 1):
                        mo = int(cur)
                    elif (cnt == 2):
                        da = int(cur)
                    elif (cnt == 3):
                        ho = int(cur)
                    elif (cnt == 4):
                        mi = int(cur)
                    elif (cnt == 5):
                        se = int(cur)
                    cur = ""
                    cnt = cnt + 1
                    if (cnt == 6):
                        break
            continue
        date = datetime.datetime(ye, mo, da, ho, mi, se)
    except Exception, e:
        print e
        traceback.print_exc()
        date = datetime.datetime.now()
    return date

# 将datetime类型的日期改为SQLite的标准格式datetime字符串
def formatTime(time_d):
    return time_d.strftime("%Y-%m-%d %X")
# coding=utf-8
# 通用功能函数
import datetime
import traceback
import sys

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

# 获取当前系统时间,返回字典
def dateNow():
    date_t = datetime.datetime.now()
    date = {'year': str(date_t.year), 'month': str(date_t.month), 'day': str(date_t.day),
            'hour': str(date_t.hour), 'minute': str(date_t.minute), 'second': str(date_t.second),}
    return date

# 补齐字符串前导0
def addZero(str, slen):
    len_t = len(str)
    for i in range(slen-len_t):
        str = "0" + str
    return str

# 把中文日期转成字典类型的日期,此函数仅对韩饭网有效
def transTime(str):
    date = dateNow()
    try:
        cur = ""
        cnt = 0
        for i in range(len(str)):
            if (str[i].isdigit()):
                cur = cur + str[i]
                if ((i == len(str)-1) or not str[i+1].isdigit()):
                    if (cnt == 0):
                        date['year'] = addZero(cur, 4)
                    elif (cnt == 1):
                        date['month'] = addZero(cur, 2)
                    elif (cnt == 2):
                        date['day'] = addZero(cur, 2)
                    elif (cnt == 3):
                        date['hour'] = addZero(cur, 2)
                    elif (cnt == 4):
                        date['minute'] = addZero(cur, 2)
                    elif (cnt == 5):
                        date['second'] = addZero(cur, 2)
                    cur = ""
                    cnt = cnt + 1
                    if (cnt == 6):
                        break
            continue
    except Exception, e:
        print e
        traceback.print_exc()
        date = dateNow()
    return date

# 将字典类型的日期改为SQLite的标准格式datetime字符串
def formatTime(time_d):
    return str(time_d['year'])+"-"+str(time_d['month'])+"-"+str(time_d['day'])+\
           " "+str(time_d['hour'])+":"+str(time_d['minute'])+":"+str(time_d['second'])
# coding=utf-8
# 通用功能函数

import datetime, time
import traceback
import sys
from os import path
import sqlite3
import requests, json
from sqlDemo.items import SqlDemoItem
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import email.mime.multipart
import email.mime.text

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

def getLastScraped(keyword):
    filename = "/tmpdb/newdb.db"
    last_scraped = datetime.datetime.min
    if path.exists(filename):
        conn = sqlite3.connect(filename)
        csr = conn.cursor()
        csr.execute("select max(time) from sqlDemo where src = '"+keyword+"'")
        res = csr.fetchall()
        for re in res:
            if re[0] is None:
                continue
            time_s = re[0]
            last_s = time.strptime(time_s, "%Y-%m-%d %X")
            ye, mo, da, ho, mi, se = last_s[0:6]
            last_scraped = datetime.datetime(ye, mo, da, ho, mi, se)
    return last_scraped

# def sendEmail(item, email):
#
#
#     url="http://sendcloud.sohu.com/webapi/mail.send.json"
#
#     # 不同于登录SendCloud站点的帐号，您需要登录后台创建发信子帐号，使用子帐号和密码才可以进行邮件的发送。
#     params = {"api_user": "123456qsr_test_ZPwNvo", \
#     "api_key" : "LSzocAnSj7utE5ON",\
#     "from" : "service@sendcloud.im", \
#     "fromname" : "SendCloud测试邮件", \
#     "to" : "1377849411@qq.com", \
#     "subject" : "您订阅的"+str(item["title"])+"更新了,请前往\"我的订阅\"查看(邮件内容为代发服务提供,请忽略)", \
#     "html": "(请忽略以下内容)你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！", \
#     "resp_email_id": "true"
#     }
#
#     r = requests.post(url, files={}, data=params)
#     print r.text
#
#     return

def sendEmail(item, myemail):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    msg=email.mime.multipart.MIMEMultipart()
    msg['from']='13284252997@sina.cn'
    msg['to']= myemail
    msg['subject']=u'您订阅的'+item["title"].encode("utf-8")+u'更新了,请点击链接查看'
    content=str(item["link"])
    print content
    txt=email.mime.text.MIMEText(content.encode("utf-8"))
    msg.attach(txt)
    print myemail

    smtp=smtplib.SMTP()
    smtp.connect('smtp.sina.cn')
    smtp.login('13284252997@sina.cn','123456qsrtt')
    smtp.sendmail('13284252997@sina.cn',myemail,str(msg))
    smtp.quit()
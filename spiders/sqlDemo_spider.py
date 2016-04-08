# coding=utf-8
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sqlDemo.items import SqlDemoItem
import datetime
import traceback
import sys

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

# 检查title是否含"中字"
def checkTitle(str):
    if "中字" in str:
        return True
    return False

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

# 把中文时间转成datetime,此函数仅对韩饭网有效
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


# 将日字典类型的期改为SQLite的标准格式字符串
def formatTime(time_d):
    return str(time_d['year'])+"-"+str(time_d['month'])+"-"+str(time_d['day'])+\
           " "+str(time_d['hour'])+":"+str(time_d['minute'])+":"+str(time_d['second'])

class SqlDemoSpider(BaseSpider):
    name = "sqlDemo"
    allowed_domains = ["www.hanfan.cc"]
    start_urls = [
        "http://www.hanfan.cc/hanju/"
    ]

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        arts = hxs.select('//article')
        for art in arts:
            # print "######################"
            # print art.extract()
            # print "######################"
            times = art.select('p/time')
            # print "######################"
            # print times.extract()
            # print "######################"
            sites = art.select('header/h2/a')
            item = SqlDemoItem()
            item['time'] = dateNow()
            item['ctime'] = dateNow()
            item['src'] = "韩饭网".decode("utf8")
            item['rate'] = 0.0
            item['rnum'] = 0.0
            for time in times:
                if not time.extract():
                    continue
                s_time = time.select('text()').extract()[0]
                # 处理时间格式
                item['ctime'] = transTime(s_time)
            # print "######################"
            # print sites.extract()
            # print "######################"
            for site in sites:
                if not site.select('@title').extract() or not site.select('@href').extract():
                    continue
                s_title = site.select('@title').extract()[0]
                s_link = site.select('@href').extract()[0]
                # 检查是否包含"中字"
                # if not checkTitle(s_title):
                #     continue
                item['title'] = s_title
                item['link'] = s_link
                break
            # print "######################"
            # print "title"+item['title']
            # print "link"+item['link']
            # print "time"+item['time']
            # print "######################"
            item['ctime'] = formatTime(item['ctime'])
            item['time'] = formatTime(item['time'])
            if (not item.has_key('title')) or (not item.has_key('link')) or (not item.has_key('time')):
                continue
            yield item
        # if next_page is not None:
        #     yield Request(url=next_page, callback=self.parse_item)

        lis = hxs.select('//li')
        next_page = None
        for li in lis:
            if li.select('@class').extract() and li.select('@class').extract()[0] == "next-page":
                print "########"
                print li.select('a/@href').extract()
                print "########"
                next_page = li.select('a/@href').extract()[0]
        if next_page is not None:
            yield Request(url=next_page, callback=self.parse)
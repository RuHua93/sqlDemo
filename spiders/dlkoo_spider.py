# coding=utf-8
import string
import sys
from os import path
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import sqlite3

import datetime, time

from sqlDemo.funcs import transTime, formatTime
from sqlDemo.items import SqlDemoItem

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

class DlkooSpider(BaseSpider):
    name = "dlkoo"
    allowed_domains = ["www.dlkoo.com"]
    main_domain = "http://www.dlkoo.com"
    # 前十页基本包含了全部近期资源
    # 故只爬前十页
    start_urls = [
        "http://dlkoo.com/down/5"
    ]
    for i in range(2,10):
        start_urls.append("http://dlkoo.com/down/5/index_"+str(i)+".htm")
    still = True

    # 获取大连生活网当前已爬网页的最新更新时间
    # 如果当前数据库没有记录则设置为min
    filename = "/tmpdb/test.db"
    last_scraped = datetime.datetime.min
    if path.exists(filename):
        conn = sqlite3.connect(filename)
        csr = conn.cursor()
        csr.execute("select max(time) from sqlDemo")
        res = csr.fetchall()
        for re in res:
            last_s = time.strptime(re[0], "%Y-%m-%d %X")
            ye, mo, da, ho, mi, se = last_s[0:6]
            last_scraped = datetime.datetime(ye, mo, da, ho, mi, se)

    def parse(self, response):
        if not self.still:
            return
        hxs = HtmlXPathSelector(response)
        atags = hxs.select('//span[@class="movTi3"]/a')
        for atag in atags:
            hrf = atag.select('@href').extract()[0]
            txt = atag.select('text()').extract()[0]
            if u"韩剧" in txt:
                item_url = self.main_domain + hrf
                yield Request(url=item_url, callback=self.parse_item)
        cur_url = response.url
        cur_pn = cur_url[22]
        nxt_pn = string.atoi(cur_pn) + 1
        np_url = ("http://dlkoo.com/down/5/index_"+str(nxt_pn)+".htm")
        yield  Request(url=np_url, callback=self.parse)

    def parse_item(self, response):
        item = SqlDemoItem()
        hxs = HtmlXPathSelector(response)
        titles = hxs.select('//title/text()')
        item['link'] = response.url
        for title in titles:
            if title:
                item['title'] = title.extract()
        item['src'] = "大连生活网".decode("utf8")
        item['rate'] = 0.0
        item['rnum'] = 0.0
        rtimes = hxs.select('//span[@class="time"]/text()')
        if rtimes:
            rtime = rtimes[0]
            upd_time = rtime.extract()
            # datetime 类型的time
            dt_time = transTime(upd_time)
            std_time = formatTime(dt_time)
            item['time'] = item['ctime'] = std_time
            if dt_time <= self.last_scraped:
                self.still = False
        if item['time'] and item['title']:
            return item
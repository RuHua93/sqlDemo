# coding=utf-8
import sys
import sqlite3
import datetime, time
import string
from os import path
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sqlDemo.items import SqlDemoItem

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

class RbwSpider(BaseSpider):
    name = "rbw"
    main_domain = "http://www.y3600.com/"
    start_urls = [
        "http://www.y3600.com/hanju/"
    ]
    # 是否继续爬取
    still = True

    # 获取热播网生活网当前已爬网页的最新更新时间
    # 只爬取在这之后的网页
    # 如果当前数据库没有记录则设置为 datetime.datetime.min
    filename = "/tmpdb/test1.db"
    last_scraped = datetime.datetime.min
    if path.exists(filename):
        conn = sqlite3.connect(filename)
        csr = conn.cursor()
        csr.execute("select max(time) from sqlDemo where src = '热播网'")
        res = csr.fetchall()
        for re in res:
            if re[0] is None:
                continue
            last_s = time.strptime(re[0], "%Y-%m-%d %X")
            ye, mo, da, ho, mi, se = last_s[0:6]
            last_scraped = datetime.datetime(ye, mo, da, ho, mi, se)
    print "##############"
    print last_scraped

    def parse(self, response):
        # print "#############"
        # print self.still
        if not self.still:
            return
        hxs = HtmlXPathSelector(response)
        lis = hxs.select('//li')
        print lis
        for li in lis:
            select_str = 'div[@class="lionhover"]/div[@class="right_info"]/span[@class="date"]/text()'
            time_s = None
            if li.select(select_str).extract():
                time_s = li.select(select_str).extract()[0]
            if time_s:
                print "##################"
                print time_s
                item = SqlDemoItem()
                item['src'] = "热播网".decode("utf8")
                item['rate'] = item['rnum'] = 0.0
                item['time'] = item['ctime'] = time_s
                atag = li.select('a[@class="img playico"]')
                item['link'] = self.main_domain + atag.select('@href').extract()[0]
                item['title'] = atag.select('@title').extract()[0]
                if (not item.has_key('title')) or (not item.has_key('link')) or (not item.has_key('time')):
                    continue
                print "##################"
                print item
                yield item
        cur_url = response.url
        # 计算下一页
        print "############"
        print cur_url, len(cur_url)
        if len(cur_url) < 33:
            cur_pn = "1"
        else:
            cur_pn = cur_url[33]
        nxt_pn = string.atoi(cur_pn) + 1
        if nxt_pn <= 10:
            np_url = ("http://www.y3600.com/hanju/index_"+str(nxt_pn)+".html")
            # print "##############"
            # print np_url
            yield  Request(url=np_url, callback=self.parse)
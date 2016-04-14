# coding=utf-8
import sys
import datetime
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sqlDemo.funcs import transTime, formatTime
from sqlDemo.items import SqlDemoItem

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

class SqlDemoSpider(BaseSpider):
    name = "sqlDemo"
    start_urls = [
        "http://www.hanfan.cc/hanju/"
    ]

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        arts = hxs.select('//article')
        for art in arts:
            times = art.select('p/time')
            sites = art.select('header/h2/a')
            # 抓取单条信息
            item = SqlDemoItem()
            item['time'] = formatTime(datetime.datetime.now())
            item['ctime'] = formatTime(datetime.datetime.now())
            item['src'] = "韩饭网".decode("utf8")
            item['rate'] = 0.0
            item['rnum'] = 0.0
            for time in times:
                if not time.extract():
                    continue
                s_time = time.select('text()').extract()[0]
                # 处理时间格式
                item['ctime'] = formatTime(transTime(s_time))
                break
            for site in sites:
                if not site.select('@title').extract() or not site.select('@href').extract():
                    continue
                s_title = site.select('@title').extract()[0]
                s_link = site.select('@href').extract()[0]
                item['title'] = s_title
                item['link'] = s_link
                break
            if (not item.has_key('title')) or (not item.has_key('link')) or (not item.has_key('time')):
                continue
            yield item
        # 构造Request爬取下一页
        hrfs = hxs.select('//li[@class="next-page"]/a/@href')
        next_page = None
        for hrf in hrfs:
            next_page = hrf.extract()
        if next_page is not None:
            yield Request(url=next_page, callback=self.parse)
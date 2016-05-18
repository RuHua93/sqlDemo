# coding=utf-8
import sys
import datetime
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sqlDemo.items import SqlDemoItem
from sqlDemo.funcs import formatTime

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

class Hanj8Spider(BaseSpider):
    name = "hanj8"
    main_domain = "http://hanj8.com"
    start_urls = [
        "http://www.hanj8.com/hanju/"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        divs = hxs.select('//div[@class="contain_con"]')
        for div in divs:
            if not div.select('div[@class="box_tt"]/h2/text()').extract():
                continue
            year_t = div.select('div[@class="box_tt"]/h2/text()').extract()[0]
            # 只爬取2010-2016年的资源基本可以满足需求
            # 2010年以前的剧都完结了
            if "韩剧" in year_t and "201" in year_t:
                atags = div.select('ul[@class="list"]/a')
                for atag in atags:
                    item_url = self.main_domain + atag.select('@href').extract()[0]
                    yield Request(url=item_url, callback=self.parseItem)

    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        title_s = hxs.select('//title/text()').extract()[0]
        item = SqlDemoItem()
        item['title'] = title_s
        item['link'] = response.url
        item['src'] = "韩剧吧".decode("utf8")
        item['rate'] = 0.0
        item['rnum'] = 0.0
        paras = hxs.select('//div[@class="jianjie_right"]/p/text()').extract()
        for para in paras:
            if "更新时间" in para:
                time_s = self.getTime(para)
                item['time'] = item['ctime'] = time_s
                break
        if (not item.has_key('title')) or (not item.has_key('link')) or (not item.has_key('time')):
            return
        return item

    # 从原始字符串提取出更新时间
    def getTime(self, para):
        ret = None
        for i in range(len(para)):
            if i+19 < len(para) and para[i:i+3] == "201":
                ret = para[i:i+19]
        if ret is None:
            ret = formatTime(datetime.datetime.now())
        return ret
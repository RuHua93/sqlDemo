import sys
# coding=utf-8
import sys
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
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

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        atags = hxs.select('//span[@class="movTi3"]/a')
        for atag in atags:
            hrf = atag.select('@href').extract()[0]
            txt = atag.select('text()').extract()[0]
            if u"韩剧" in txt:
                item_url = self.main_domain + hrf
                yield Request(url=item_url, callback=self.parse_item)

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
        ska = hxs.select('//a[@class="skeya"]/text()').extract()
        if rtimes:
            rtime = rtimes[0]
            upd_time = rtime.extract()
            std_time = formatTime(transTime(upd_time))
            item['time'] = std_time
            item['ctime'] = std_time
        if item['time'] and item['title']:
            return item
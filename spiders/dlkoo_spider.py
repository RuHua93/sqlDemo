# coding=utf-8
import sys
import string
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sqlDemo.funcs import transTime, formatTime, getLastScraped
from sqlDemo.items import SqlDemoItem

# 编码改成utf8
reload(sys)
sys.setdefaultencoding("utf-8")

class DlkooSpider(BaseSpider):
    name = "dlkoo"
    main_domain = "http://dlkoo.com"
    # 前十页基本包含了全部近期资源
    # 故只爬前十页
    start_urls = [
        "http://dlkoo.com/down/5/"
    ]
    # 是否继续爬取
    still = True

    # 获取大连生活网当前已爬网页的最新更新时间
    # 只爬取在这之后的网页
    # 如果当前数据库没有记录则设置为 datetime.datetime.min
    last_scraped = getLastScraped('大连生活网')

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
        # 计算下一页地址
        cur_url = response.url
        if len(cur_url) < 30:
            cur_pn = "1"
        else:
            cur_pn = cur_url[30]
        nxt_pn = string.atoi(cur_pn) + 1
        if nxt_pn <= 10:
            np_url = ("http://dlkoo.com/down/5/index_"+str(nxt_pn)+".htm")
            yield Request(url=np_url, callback=self.parse)

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
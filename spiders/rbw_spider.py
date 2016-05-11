# coding=utf-8
import sys
import string
import datetime
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sqlDemo.items import SqlDemoItem
from sqlDemo.funcs import getLastScraped

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

    # 获取热播网当前已爬网页的最新更新时间
    # 只爬取在这之后的网页
    # 如果当前数据库没有记录则设置为 datetime.datetime.min
    last_scraped = getLastScraped('热播网')

    def parse(self, response):
        if not self.still:
            return
        hxs = HtmlXPathSelector(response)
        atags = hxs.select('//li[@class="tit"]/a')

        for atag in atags:
            item = SqlDemoItem()
            time_s = datetime.datetime.now().strftime("%Y-%m-%d %X")
            if atag.select('@href').extract():
                item['link'] = self.main_domain + atag.select('@href').extract()[0]
            else:
                continue

            if atag.select("@title").extract():
                item['title'] = atag.select('@title').extract()[0]
            else:
                continue
            item['src'] = "热播网".decode("utf8")
            item['rate'] = item['rnum'] = 0.0
            item['time'] = item['ctime'] = time_s
            if (not item.has_key('title')) or (not item.has_key('link')) or (not item.has_key('time')):
                continue
            dt_time = datetime.datetime.strptime(time_s, "%Y-%m-%d %X")
            if dt_time <= self.last_scraped:
                self.still = False
            yield item
        # 计算下一页地址
        cur_url = response.url
        if len(cur_url) < 33:
            cur_pn = "1"
        else:
            cur_pn = cur_url[33]
        nxt_pn = string.atoi(cur_pn) + 1
        if nxt_pn <= 10:
            np_url = ("http://www.y3600.com/hanju/index_"+str(nxt_pn)+".html")
            yield Request(url=np_url, callback=self.parse)

    # def parse(self, response):
    #     if not self.still:
    #         return
    #     hxs = HtmlXPathSelector(response)
    #     lis = hxs.select('//li')
    #
    #     for li in lis:
    #         select_str = 'div[@class="lionhover"]/div[@class="right_info"]/span[@class="date"]/text()'
    #         time_s = None
    #         # 热播网的更新日期没有秒钟这一项
    #         if li.select(select_str).extract():
    #             time_s = li.select(select_str).extract()[0] + ":01"
    #         else:
    #             time_s = datetime.datetime.now().strftime("%Y-%m-%d %X")
    #         # 热播网改了前端代码,看不到更新日期,所以只能加上面一行了
    #         if time_s:
    #             item = SqlDemoItem()
    #             item['src'] = "热播网".decode("utf8")
    #             item['rate'] = item['rnum'] = 0.0
    #             item['time'] = item['ctime'] = time_s
    #             atag = li.select('a[@class="img playico"]')
    #             item['link'] = self.main_domain + atag.select('@href').extract()[0]
    #             item['title'] = atag.select('@title').extract()[0]
    #             if (not item.has_key('title')) or (not item.has_key('link')) or (not item.has_key('time')):
    #                 continue
    #             dt_time = datetime.datetime.strptime(time_s, "%Y-%m-%d %X")
    #             if dt_time <= self.last_scraped:
    #                 self.still = False
    #             yield item
    #     # 计算下一页地址
    #     cur_url = response.url
    #     if len(cur_url) < 33:
    #         cur_pn = "1"
    #     else:
    #         cur_pn = cur_url[33]
    #     nxt_pn = string.atoi(cur_pn) + 1
    #     if nxt_pn <= 10:
    #         np_url = ("http://www.y3600.com/hanju/index_"+str(nxt_pn)+".html")
    #         yield Request(url=np_url, callback=self.parse)
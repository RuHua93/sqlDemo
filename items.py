# coding=utf-8
from scrapy.item import Item, Field

# 定义剧集信息Item
class SqlDemoItem(Item):
    tid = Field()
    title = Field()
    link = Field()
    src = Field()
    img = Field()
    time = Field()
    ctime = Field()
    rate = Field()
    rnum = Field()

# coding=utf-8
BOT_NAME = 'sqlDemo'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['sqlDemo.spiders']
NEWSPIDER_MODULE = 'sqlDemo.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES=['sqlDemo.pipelines.SqlDemoPipeline']

# 设置延迟防止被封IP
DOWNLOAD_DELAY = 0.25
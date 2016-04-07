# Scrapy settings for sqlDemo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'sqlDemo'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['sqlDemo.spiders']
NEWSPIDER_MODULE = 'sqlDemo.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES=['sqlDemo.pipelines.SqlDemoPipeline']

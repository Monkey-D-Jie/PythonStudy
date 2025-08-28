# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 设置需要爬取的对象
class DangdangSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    price = scrapy.Field()
    comment_num = scrapy.Field()
    link = scrapy.Field()
    pass

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGoodsDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义图书单项信息
    # 大类-文学馆
    cat_big = scrapy.Field()
    # 中类-小说
    cat_middle = scrapy.Field()
    # 小类-悬疑
    cat_small = scrapy.Field()
    # 书名
    book_name = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    price = scrapy.Field()
    comment_num = scrapy.Field()
    # 卖家名称
    seller = scrapy.Field()
    pass

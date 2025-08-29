# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidunewsDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classify = scrapy.Field()
    title = scrapy.Field()
    m_text = scrapy.Field()
    link = scrapy.Field()
    content =  scrapy.Field()
    pass

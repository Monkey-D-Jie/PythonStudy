# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidunewsDemoItem(scrapy.Item):
    # define the fields for your item here like:
    classify = scrapy.Field()
    classify_name = scrapy.Field()
    title = scrapy.Field()
    m_text = scrapy.Field()
    link = scrapy.Field()
    content =  scrapy.Field()
    img_url = scrapy.Field()
    pass

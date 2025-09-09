import scrapy
import urllib.request
import re
import random
from lxml import etree
from scrapy.http import Request
from jd_goods_demo.items import JdGoodsDemoItem

class GoodsSpider(scrapy.Spider):
    name = "goods"
    allowed_domains = ["jd.com"]
    start_urls = ["https://jd.com"]



    def parse(self, response):
        pass

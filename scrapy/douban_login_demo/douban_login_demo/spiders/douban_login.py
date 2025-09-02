import scrapy


class DoubanLoginSpider(scrapy.Spider):
    name = "douban_login"
    allowed_domains = ["douban.com"]
    start_urls = ["https://douban.com"]

    def parse(self, response):
        pass

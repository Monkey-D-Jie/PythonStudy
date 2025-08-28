import scrapy
from scrapy.http import Request
from lxml.etree import XPath

from dangdang_demo.items import DangdangSpiderItem

class DdSpider(scrapy.Spider):
    name = "dd"
    allowed_domains = ["dangdang.com"]
    # 按“好评率”倒序排序
    start_urls = ["https://category.dangdang.com/pg1-cid4003844-srsort_score_desc.html"]
    # title关键词：div/ul/li/a/title/text()
    # price关键词：div/ul/li/p/span[@class='price_n']
    # comment_num关键词：div/ul/li/p/a[@dd_name="单品评论"]
    # link关键：div/ul/li/a/[@href]
    # 请求url返回的内容将会被存放到response中
    def parse(self, response):
        if response:
            item = DangdangSpiderItem()
            # 使用xpath找到title标签中的内容
            item["title"] = response.xpath("//a[@dd_name='单品标题']/text()").extract()
            # //div/ul/li/p/span[@class='price_n']/text()
            item["price"] = response.xpath("//span[@class='price_n']/text()").extract()
            item["link"] = response.xpath("//a[@dd_name='单品图片']/@href").extract()
            # ①：通过这种方法，可以将没有评论的商品也一并补齐
            comment_nums = response.xpath("//a[@dd_name='单品评论']/text()").extract()
            max_length = max(len(item["title"]), len(item["price"]), len(item["link"]))
            # 遍历comment_nums本身的长度，如果为空则赋值0，在此基础上，再加上max_length与comment_nums的数量差值，即可得到max_length长度的数据
            # 其中不足的部分，将通过“0”来补齐
            padded_comment_nums = [x if x else '0' for x in comment_nums] + ['0'] * (max_length - len(comment_nums))
            item["comment_num"] = padded_comment_nums
            # ②：采用该方法，前提是访问页面中的每一个都有对应的评论。但实测下来发现，还是存在没有评论的商品。
            # item["comment_num"] = response.xpath("//a[@dd_name='单品评论']/text()").extract()
            # 返回数据，有点像java中的某个方法里的return
            yield item
            for i in  range (2,31):
                url = "https://category.dangdang.com/pg"+str(i)+"-cid4003844-srsort_score_desc.html"
                yield Request(url,callback=self.parse)

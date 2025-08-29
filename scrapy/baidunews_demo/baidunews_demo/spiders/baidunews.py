import json

import scrapy
import re
from scrapy.http import Request
from baidunews_demo.items import BaidunewsDemoItem


class BaidunewsSpider(scrapy.Spider):
    name = "baidunews"
    allowed_domains = ["news.baidu.com"]
    start_urls = ["https://news.baidu.com/widget?id=LocalNews&ajax=json"]
    '''
    [
        'LocalNews',
        'civilnews',
        'InternationalNews',
        'FinanceNews',
        'SportNews',
        'AutoNews',
        'HouseNews',
        'InternetNews',
        'InternetPlusNews',
        'TechNews',
        'EduNews',
        'GameNews',
        'DiscoveryNews',
        'HealthNews',
        'LadyNews',
        'SocialNews'
    ]
    '''
    all_news_id = [
        'LocalNews',
        'civilnews',
        'InternationalNews',
        'FinanceNews',
        'SportNews',
        'AutoNews',
        'HouseNews',
        'InternetNews',
        'InternetPlusNews',
        'TechNews',
        'EduNews',
        'GameNews',
        'DiscoveryNews',
        'HealthNews',
        'LadyNews',
        'SocialNews'
    ]

    def parse(self, response, req_url=None, classify=None):
        if req_url:
            # 如果指定了 req_url，则只处理这个 URL
            # classify = self.get_classify_from_url(req_url)
            data = response.body.decode("utf-8", "ignore")
            # print("进入到了指定了req_url的方法中。。。。。。。。")
            yield from self.parse_data_by_json(data, classify)
        else:
            for i in range(0,len(self.all_news_id)):
                cur_new_url = "https://news.baidu.com/widget?id=" + self.all_news_id[i] + "&ajax=json"
                # print("第"+str(i)+"个栏目，所属分类:"+str(self.all_news_id[i]))
                data = response.body.decode("utf-8","ignore")
                # 1.使用json来解析
                yield from self.parse_data_by_json(data,self.all_news_id[i])
                # 2.使用正则表达式来解析
                # self.parse_data_by_pat(data)
                yield Request(cur_new_url,callback=self.parse, cb_kwargs={"req_url": cur_new_url,"classify": self.all_news_id[i]})

    def parse_data_by_pat(self,data):
        classify_pat = '"name":"(.*?)"'
        m_title_pat = '"m_title":"(.*?)"'
        m_url_pat = '"url":"(.*?)"'
        m_text_pat = '"m_text":"(.*?)"'
        classify_var = re.compile(classify_pat, re.S).findall(data)
        m_title_var = re.compile(m_title_pat, re.S).findall(data)
        m_url_var = re.compile(m_url_pat, re.S).findall(data)
        m_text_var = re.compile(m_text_pat, re.S).findall(data)
        for j in range(0, len(m_url_var)):
            clean_url = re.sub(r'\\', '', m_url_var[j])
            print("---------->>>>>>", clean_url)


    def parse_data_by_json(self,data,classify):
        try:
            if classify:
                json_data = json.loads(data)
                # 获取数据，如果为空，则按空数组值获取，以避免可能得空指针异常出现
                first_news_rows = json_data.get("data", {}).get(classify, {}).get("data", {}).get("rows", {}).get("first")
                if first_news_rows:
                    row_classify_name = json_data.get("data", {}).get(classify, {}).get("data", {}).get("name")
                    print(classify+"========++++++++" + row_classify_name + "++++++++========"+classify)
                    for news in first_news_rows:
                        rows_item = BaidunewsDemoItem()
                        # print("Title:", news.get("title"))
                        # print("URL:", news.get("url"))
                        # print("Img URL:", news.get("imgUrl"))
                        # 赋值对象
                        rows_item["classify"] = row_classify_name
                        rows_item["classify_name"] = row_classify_name
                        rows_item["title"] = news.get("title")
                        rows_item["m_text"] = news.get("title")
                        rows_item["link"] = news.get("url")
                        rows_item["img_url"] = news.get("imgUrl")
                        # yield rows_item
                        # 提取新闻详情页内容
                        yield Request(
                            url=rows_item["link"],
                            callback=self.parse_news_content,
                            # 传递 item 到下一级解析函数
                            meta={"item": rows_item},
                            dont_filter=True
                        )
                else:
                    first_news_focus = json_data.get("data", {}).get(classify, {}).get("focusNews")
                    if first_news_focus:
                        focus_classify_name = json_data.get("data", {}).get(classify, {}).get("title")
                        print(classify+"========++++++++"+focus_classify_name+"++++++++========"+classify)
                        for news in first_news_focus:
                            focus_item = BaidunewsDemoItem()
                            # print("Title:", news.get("m_title"))
                            # print("URL:", news.get("m_url"))
                            # print("Img URL:", news.get("m_image_url"))
                            # 赋值对象
                            focus_item["classify"] = classify
                            focus_item["classify_name"] = focus_classify_name
                            focus_item["title"] = news.get("m_title")
                            focus_item["m_text"] = news.get("m_text")
                            focus_item["link"] = news.get("m_url")
                            focus_item["img_url"] = news.get("m_image_url")
                            # yield focus_item
                            # 提取新闻详情页内容
                            yield Request(
                                url=focus_item["link"],
                                callback=self.parse_news_content,
                                meta={"item": focus_item},
                                dont_filter=True
                            )
                    # else:
                    #     print(f"Warning: No valid 'first' or 'focusNews' found for classify '{classify}'")
            else:
                print("classify is empty, skipping parsing...")
        except Exception as e:
            print("解析 JSON 失败:", str(e))

    def parse_news_content(self, response):
        """
        解析新闻详情页，提取正文内容并写入 items
        :param response: Scrapy 响应对象
        """
        item = response.meta["item"]  # 获取上一级传来的 item 对象

        # 示例：使用 XPath 提取正文内容
        # print("获取到的response.body内容=======================",response.body.decode("utf-8","ignore"))
        content = response.xpath('//div[@class="dpu8C _2kCxD  "]//text()').getall()
        content = " ".join(content).strip()

        # 如果你的目标网站结构不同，请根据实际情况调整 XPath 表达式
        # 例如百度百家号可能用的是：
        # content = response.xpath("//div[@id='articleBody']//text()").getall()
        # print("=======>>>>>当前获取到的content内容",content)
        item["content"] = content  # 将正文内容存入 content 字段
        yield item  # 返回完整的 item 给 Pipeline 处理
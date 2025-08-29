import json

import scrapy
import re
from scrapy.http import Request


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
            self.parse_data_by_json(data, classify)
        else:
            for i in range(0,len(self.all_news_id)):
                cur_new_url = "https://news.baidu.com/widget?id=" + self.all_news_id[i] + "&ajax=json"
                # print("第"+str(i)+"个栏目，所属分类:"+str(self.all_news_id[i]))
                data = response.body.decode("utf-8","ignore")
                # 1.使用json来解析
                self.parse_data_by_json(data,self.all_news_id[i])
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
                first_news_rows = json_data.get("data", {}).get(classify, {}).get("data", {}).get("rows", {}).get("first")
                if first_news_rows:
                    print(classify+"========++++++++" + json_data.get("data", {}).get(classify, {}).get("data",{}).get("name") + "++++++++========"+classify)
                    for news in first_news_rows:
                        print("Title:", news.get("title"))
                        print("URL:", news.get("url"))
                        print("Img URL:", news.get("imgUrl"))
                else:
                    first_news_focus = json_data.get("data", {}).get(classify, {}).get("focusNews")
                    if first_news_focus:
                        print(classify+"========++++++++"+json_data.get("data", {}).get(classify, {}).get("title")+"++++++++========"+classify)
                        for news in first_news_focus:
                            print("Title:", news.get("m_title"))
                            print("URL:", news.get("m_url"))
                            print("Img URL:", news.get("m_image_url"))
                    # else:
                    #     print(f"Warning: No valid 'first' or 'focusNews' found for classify '{classify}'")
            else:
                print("classify is empty, skipping parsing...")
        except Exception as e:
            print("解析 JSON 失败:", str(e))
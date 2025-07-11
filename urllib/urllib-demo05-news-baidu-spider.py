import urllib.request
import  re
import requests
from bs4 import BeautifulSoup
'''
demo功能简介说明
从百度新闻首页扒取新闻，
并存放至本地
https://news.baidu.com/
'''
news_url="https://news.baidu.com/"
news_data=urllib.request.urlopen(news_url).read().decode("utf-8")
# pat ='<a href=\s?(.*?)\s.*?target="_blank"\s.*?>'
pat = '<a\s+href\s*=\s*["\'](.*?)["\'].*?target\s*=\s*"_blank"'
find_news_url=re.findall(pat,news_data)
print(find_news_url[0])
print(len(news_data))
soup = BeautifulSoup(news_data, 'html.parser', from_encoding="utf-8")
links = [a['href'] for a in soup.find_all('a', target="_blank")]
news_links = list(set(links))
with open("baidu_news_dynamic_links.txt", "w", encoding="utf-8") as f:
    for link in news_links:
        f.write(link + "\n")

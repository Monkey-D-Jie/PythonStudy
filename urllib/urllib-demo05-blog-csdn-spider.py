import urllib.request
import  re

import requests
from bs4 import BeautifulSoup
'''
demo功能简介说明
从CSDN扒取博文，
并存放至本地
'''
news_url="https://blog.csdn.net"
news_header = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")

opener = urllib.request.build_opener()
opener.addheaders=[news_header]
#全局安装opener
urllib.request.install_opener(opener)
blog_url_data=urllib.request.urlopen(news_url).read().decode("utf-8","ignore")

# test_data='<a data-report-query="spm=3001.7377&amp;utm_medium=distribute.pc_feed_blog.none-task-blog-personrec_tag-5-149221523-null-null.nonecase&amp;depth_1-utm_source=distribute.pc_feed_blog.none-task-blog-personrec_tag-5-149221523-null-null.nonecase" data-report-click="{&quot;mod&quot;:&quot;&quot;,&quot;extra&quot;:{&quot;index&quot;:4,&quot;navType&quot;:&quot;&quot;},&quot;dist_request_id&quot;:&quot;1752219293760_92461&quot;,&quot;ab_strategy&quot;:&quot;default&quot;,&quot;index&quot;:&quot;5&quot;,&quot;style&quot;:&quot;PIC_V2_11&quot;,&quot;strategy&quot;:&quot;personrec_tag&quot;,&quot;dest&quot;:&quot;https://blog.csdn.net/nmsoftklb/article/details/149221523&quot;,&quot;spm&quot;:&quot;3001.7377&quot;}" data-report-view="{&quot;mod&quot;:&quot;&quot;,&quot;extra&quot;:{&quot;index&quot;:4,&quot;navType&quot;:&quot;&quot;},&quot;dist_request_id&quot;:&quot;1752219293760_92461&quot;,&quot;ab_strategy&quot;:&quot;default&quot;,&quot;index&quot;:&quot;5&quot;,&quot;style&quot;:&quot;PIC_V2_11&quot;,&quot;strategy&quot;:&quot;personrec_tag&quot;,&quot;dest&quot;:&quot;https://blog.csdn.net/nmsoftklb/article/details/149221523&quot;,&quot;spm&quot;:&quot;3001.7377&quot;}" target="_blank" href="https://blog.csdn.net/nmsoftklb/article/details/149221523" class="article-title word-1" data-v-36c9265b>Spring IoC 如何注入一些简单的值（比如配置文件里的字符串、数字）？</a>'
# class="article-title word-1"
pat = 'target="_blank" href="(.*?)" class="article-title word-1" data-v-36c9265b>'
# pat = r'<a\b[^>]*?\s+href\s*=\s*["\'](.*?)["\'][^>]*?\s+class\s*=\s*["\']article-title word-1["\'][^>]*?>'
find_blog_url= re.compile(pat).findall(blog_url_data)
# print(blog_url_data)

# soup = BeautifulSoup(blog_url_data, "html.parser")
# links = [a['href'] for a in soup.find_all('a', class_="article-title word-1")]
# print(links)
# news_links = list(set(links))
# for i in range(0,len(news_links)):
#     save_path = "H:\\myIdeaWorkSpace\\PythonStudy\\testFile\\csdn-blog\\blog-"+str(i)+".html"
#     urllib.request.urlretrieve(news_links[i],filename=save_path)
#     print("第"+str(i)+"篇博文爬取并保存完毕！")
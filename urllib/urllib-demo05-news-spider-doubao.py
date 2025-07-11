'''
demo功能简介说明
从腾讯新闻首页扒取新闻，
并存放至本地
https://news.qq.com/rain/a/20250708A01XUP00
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 初始化浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://news.qq.com/")
time.sleep(3)  # 等待页面加载完成

# 可选：模拟滚动加载更多内容（根据页面逻辑调整）
# for _ in range(3):  # 滚动3次
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# 提取新闻链接（需根据实际页面的HTML结构调整选择器）
news_links = []
a_tags = driver.find_elements(By.TAG_NAME, "a")
for a in a_tags:
    href = a.get_attribute("href")
    if href and "news.qq.com/a/" in href:
        news_links.append(href)

# 去重并保存
news_links = list(set(news_links))
with open("tencent_news_dynamic_links.txt", "w", encoding="utf-8") as f:
    for link in news_links:
        f.write(link + "\n")

print(f"动态加载提取到{len(news_links)}条新闻链接")
driver.quit()
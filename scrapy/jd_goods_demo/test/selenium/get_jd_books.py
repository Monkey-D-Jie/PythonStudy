# 来自豆包
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_jd_books():
    # 1. 初始化 Chrome 浏览器（带反爬配置）
    options = webdriver.ChromeOptions()
    # 关键：隐藏 Selenium 特征（避免京东检测到自动化工具）
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # 模拟真实浏览器的 User-Agent（可替换为自己的）
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.155 Safari/537.36"
    )
    # 禁止加载图片（可选，加快页面加载）
    # options.add_argument("--blink-settings=imagesEnabled=false")

    # 2. 启动浏览器（webdriver-manager 自动管理驱动版本）
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),  # 自动下载匹配的 Chromedriver
        options=options
    )
    # 隐藏 webdriver 标识（进一步规避检测）
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    try:
        # 3. 访问京东图书列表页面
        target_url = "https://list.jd.com/list.html?cat=1713%2C3258&pvid=7efa6cc4a78241d393f3e83f16c3c936"
        driver.get(target_url)
        # 最大化窗口（模拟真实用户操作，部分网站会根据窗口大小调整渲染）
        driver.maximize_window()

        # 4. 等待页面加载（关键：等待骨架屏消失，真实商品出现）
        wait = WebDriverWait(driver, 20)  # 最长等待 20 秒
        # 等待第一个商品标题加载完成（替换骨架屏的空占位）
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="gl-i-wrap"]//em[contains(@class, "gl-name")]')
            )
        )

        # 5. 可选：滚动页面加载更多商品（京东列表是“滚动加载”，默认只加载前 30 个）
        # 滚动到页面底部，触发后续商品加载（可循环滚动多次，根据需求调整）
        for _ in range(2):  # 滚动 2 次，加载更多商品
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # 等待加载（根据网络速度调整）

        # 6. 提取商品信息（定位所有商品项，解析标题、价格、SKU 等）
        goods_list = driver.find_elements(By.XPATH, '//div[@class="gl-i-wrap"]')
        print(f"共找到 {len(goods_list)} 个商品\n")

        for idx, goods in enumerate(goods_list, 1):
            try:
                # 商品标题（去除空格和换行）
                title = goods.find_element(By.XPATH, './/em[contains(@class, "gl-name")]').text.strip()
                # 商品价格（注意：部分价格可能是“活动价”，需调整 XPath）
                price = goods.find_element(By.XPATH, './/strong[@class="J_price"]').text.strip()
                # 商品 SKU（从 href 中提取，如 https://item.jd.com/123456.html → SKU=123456）
                sku_href = goods.find_element(By.XPATH, './/a[@class="J_ClickStat"]').get_attribute("href")
                sku = sku_href.split("/")[-1].replace(".html", "") if sku_href else "未知"

                print(f"商品 {idx}")
                print(f"SKU: {sku}")
                print(f"标题: {title}")
                print(f"价格: {price} 元\n")
            except Exception as e:
                print(f"商品 {idx} 解析失败：{str(e)}")
                continue

    except Exception as e:
        print(f"整体流程失败：{str(e)}")
    finally:
        # 7. 关闭浏览器（或等待用户输入后关闭）
        input("按 Enter 键关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    get_jd_books()
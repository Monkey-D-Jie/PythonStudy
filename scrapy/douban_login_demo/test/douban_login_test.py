'''
参考链接
https://www.cnblogs.com/chenlove/p/14038543.html
https://blog.csdn.net/qq_44628911/article/details/121567024
'''
# encoding: utf-8
import os

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random
from webdriver_manager.chrome import ChromeDriverManager



def get_tracks(distance, rate=0.6, t=0.2, v=0):
    """
    将distance分割成小段的距离
    :param distance: 总距离
    :param rate: 加速减速的临界比例
    :param a1: 加速度
    :param a2: 减速度
    :param t: 单位时间
    :param t: 初始速度
    :return: 小段的距离集合
    """
    tracks = []
    # 加速减速的临界值
    mid = rate * distance
    # 当前位移
    s = 0
    # 循环
    while s < distance:
        # 初始速度
        v0 = v
        if s < mid:
            a = 20
        else:
            a = -3
        # 计算当前t时间段走的距离
        s0 = v0 * t + 0.5 * a * t * t
        # 计算当前速度
        v = v0 + a * t
        # 四舍五入距离，因为像素没有小数
        tracks.append(round(s0))
        # 计算当前距离
        s += s0


    return tracks


def slide2(driver):
    """滑动验证码"""
    try_num = 0
    while True:
        try:
            # 每次操作前重新切换iframe并获取元素
            driver.switch_to.default_content()  # 先回到默认内容
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="tcaptcha_iframe_dy"]'))

            # 重新获取滑块和刷新元素
            block = driver.find_element(By.XPATH, '//*[@id="tcOperation"]/div[7]')
            reload = driver.find_element(By.XPATH, '//*[@id="reload"]')

            time.sleep(2)  # 确保元素完全加载

            # 执行滑块操作
            # ActionChains(driver).click_and_hold(block).perform()
            # ActionChains(driver).move_by_offset(130, 0).perform()

            # 生成随机偏移量 (130±10到30)
            base_offset = 100
            variation = random.randint(30, 50)
            random_offset = base_offset + random.choice([0, 1]) * variation
            ActionChains(driver).click_and_hold(block).perform()
            ActionChains(driver).move_by_offset(random_offset, 0).perform()


            tracks = get_tracks(30)
            for track in tracks:
                ActionChains(driver).move_by_offset(track, 0).perform()

            ActionChains(driver).release().perform()
            time.sleep(2)

            # content_tip = driver.find_element(By.XPATH, '//*[@id="account"]/div[2]/div[2]/div/div[3]/div[1]/div[1]/text()',{})

            if driver.title == "登录豆瓣":
                print(f"失败...再来一次...第{try_num+1}次")
                reload.click()
                try_num +=1
                time.sleep(3)
            # if content_tip == "你的账号存在":
            #     break
            else:
                break
            if try_num == 10:
                # 尝试10次，还不行的就退出
                break
        except Exception as e:
            print(f"操作失败，重试中... 错误: {e}")
            time.sleep(2)
            continue




def slide(driver):
    """滑动验证码"""
    # 切换iframe
    # 如果定位节点在标签iframe内，那么则必须使用switch_to进行iframe的切换
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="tcaptcha_iframe_dy"]'))
    # driver.switch_to.frame(1)
    #找到滑块
    block = driver.find_element(By.XPATH,'//*[@id="tcOperation"]/div[7]')
    #找到刷新
    reload = driver.find_element(By.XPATH, '//*[@id="reload"]')
    time.sleep(5)
    try_count = 0
    while True:
        # 摁下滑块
        ActionChains(driver).click_and_hold(block).perform()
        # 移动
        ActionChains(driver).move_by_offset(160, 0).perform()
        #获取位移
        tracks = get_tracks(30)
        #循环
        for track in tracks:
            #移动
            ActionChains(driver).move_by_offset(track, 0).perform()
        # 释放
        ActionChains(driver).release().perform()
        #停一下
        time.sleep(2)
        #判断
        if driver.title == "登录豆瓣":
            print("失败...再来一次...")
            #单击刷新按钮刷新
            reload.click()
            # 停一下
            time.sleep(3)
        else:
            break
        if 10 == try_count:
            break
        else:
            try_count += 1


def main():
    """主程序"""
    url = "https://accounts.douban.com/passport/login"
    # service = Service(executable_path="./chromedriver.exe")  # 使用当前目录下的 chromedriver.exe
    # driver = webdriver.Chrome(service=service)
    service = Service(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    driver.find_element(By.XPATH, '//div[@class="account-body-tabs"]/ul/li[@class="account-tab-account"]').click()#切换到用户名+密码登录
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys("小号@qq.com")
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("名字@电话后6位")
    time.sleep(5)
    driver.find_element(By.XPATH, '//div[@class="account-form-field-submit "]/a[@class="btn btn-account btn-active"]').click()#点击登录
    # 停一下，等待出现
    time.sleep(5)
    #滑动验证码
    slide2(driver)


    print("成功")
    driver.quit()




if __name__ == '__main__':
    # 检查文件是否存在
    if not os.path.exists("./chromedriver.exe"):
        print("错误：在当前目录下找不到 chromedriver.exe")
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from selenium import webdriver

#############找到要下载的链接#############
browser = webdriver.Firefox()
#如果不想看到浏览器，可以用无痕浏览器phantomJS
# browser = webdriver.PhantomJS(executable_path="/Users/Hao/anaconda/bin/PhantomJS")
# 这边我们取B站鬼畜区排名页面，得到网页源代码
rank_url = "http://www.bilibili.com/ranking#!/origin/119/0/30/"

# 用Selnium的好处还在于返回的页面是js执行之后的页面。
browser.get(rank_url)
content = browser.page_source
browser.quit()

# 找到排名前100的视频页面
pattern = re.compile('<div class="rank-item"><div class="num">(.*?)'
                     '</div>.*?href="(.*?)"><div class="preview">.*?div class="title">(.*?)</div>', re.S)
item = re.findall(pattern, content)

base_url = "http://www.bilibili.com"

#####################视频嗅探及下载#####################
# 导入嗅探包BrowserMob
import time
import requests
from browsermobproxy import Server

for i in range(len(item)):
    # 设置网路监控代理
    server = Server()
    server.start()
    proxy = server.create_proxy()

    # 设置浏览器
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile)

    ##得到监控
    proxy.new_har("bilibili")
    # 得到网页源代码
    driver.get(base_url + item[i][1])

    # 打开视频
    # driver.find_element_by_name("pause_button").click()
    time.sleep(1)
    # 得到网络监控数据，json数据
    content = proxy.har  # returns a HAR JSON blob
    server.stop()
    driver.quit()

    # 视频链接分析
    video_box = []
    data = content['log']['entries']
    for j in range(len(data)):
        url = data[j]['request']['url']
        if url.find("mp4") != -1:
            print(url)
            video_box.append(url)


    # 视频下载，存储到data文件夹
    if len(video_box) >= 2:
        hd_video_url = video_box[1]
        #video = requests.get(hd_video_url, timeout=10)
        #string = "../data/" + item[i][0] + item[i][2] + '.mp4'
        #fp = open(string, 'wb')
        #fp.write(video.content)
    else:
        print("视频下载出现问题，视频页面不存在")

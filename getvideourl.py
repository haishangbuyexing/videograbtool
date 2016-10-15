#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# 导入嗅探包BrowserMob
import time
import requests
from browsermobproxy import Server

server = Server("/bin/browsermob-proxy-2.0-beta-6/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

# 设置浏览器
profile = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
driver = webdriver.Firefox(firefox_profile=profile)
driver.get("http://www.tongzhuo100.com/login/v/?url=http://www.tongzhuo100.com/")

# 输入账号密码
stu_id = driver.find_element_by_name("usr").send_keys("18500951888")
stu_pwd = driver.find_element_by_name("pwd")
stu_pwd.send_keys("tz4006345699")

# 登录
stu_pwd.send_keys(Keys.RETURN)
time.sleep(10)

##得到监控
proxy.new_har("baidu")
# 得到网页源代码
driver.get("http://g15.tongzhuo100.com/v/2015-03/30685.html")
time.sleep(10)
# 得到网络监控数据，json数据
while True:
    content = proxy.har  # returns a HAR JSON blob
    video_box = []
    data = content['log']['entries']
    getMp4 = False
    for j in range(len(data)):
        url = data[j]['request']['url']
        if url.find("mp4") != -1:
            print(url)
	    getMp4 = True
            video_box.append(url)
    if getMp4:
        break
    else:
        time.sleep(5)
server.stop()
driver.quit()



# -*- coding: utf-8 -*-
# 导入Selenium的webdriver
from selenium import webdriver
# 用来使用键盘、快捷键
from selenium.webdriver.common.keys import Keys


# 导入numpy 和pandas模块
# 将爬取的数据转化成DataFrame并存成excel文件
import pandas as pd
import numpy as np

#导入time模块，代码中多次用到。
import time

# 导入邮件模块
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
# 使用Chromedriver
driver = webdriver.Firefox()
# 打开portal登录页
driver.get("http://www.tongzhuo100.com/login/v/?url=http://www.tongzhuo100.com/")

# 输入账号密码
stu_id = driver.find_element_by_name("usr").send_keys("18500951888")
stu_pwd = driver.find_element_by_name("pwd")
stu_pwd.send_keys("tz4006345699")

# 登录
stu_pwd.send_keys(Keys.RETURN)
with open("firstsourcepage.txt", "wa+") as f:
    f.write(driver.page_source.encode('utf-8'))
versions = driver.find_elements_by_class_name('version')
for version in versions:
    print '---------------------------------------------'
    hrefs = version.find_elements_by_tag_name("a")
    for href in hrefs: 
        print href.get_attribute("href"), href.text
time.sleep(2)
## 进入研究生院
#driver.find_element_by_id("button-1027-btnWrap").click()
#time.sleep(2)
#driver.find_element_by_id("menuitem-1051-iconEl").click()
## 打开新的tab，载入成绩单页面。
#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'n')
#driver.get(
#    "https://portal.pku.edu.cn/portal2013/bizcenter/sgims/redirectToSGIMSO.do?urlRoot=yjxjTeaching&modId=yjxjcjcxYJS")
#time.sleep(2)
## 得到js加载完的网页代码
#html = driver.page_source
#print(html)
## .execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#
## 用简单的正则得到成绩数据
#import re
#pattern_head = re.compile("</a>(.*?)<img")
#item_head = re.findall(pattern_head, html)
#
#pattern_body = re.compile("\"on\">(.*?)</div>")
#item_content = re.findall(pattern_body, html)
#
## 将得到的结果输出excel
#
#n_col = int(len(item_head))  # 每门课多少数据
#n_row = int(len(item_content) / len(item_head))  # 多少门课
#grade_excel = pd.DataFrame(data=np.zeros([n_row, n_col]), columns=item_head)
#for i in range(n_row):
#    grade_excel.ix[i] = item_content[i * 21:(i + 1) * 21]
#
#
#    # 计算已经出分的门数
#num_existed_grades = sum(grade_excel['成绩'] != '\xa0')
driver.close()

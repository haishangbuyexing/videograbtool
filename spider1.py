#-*- coding: utf-8 -*-
import urllib2
import re
import sys
import sqlite3
import xlrd
import os,sys,datetime

# 导入Selenium的webdriver
from selenium import webdriver
# 用来使用键盘、快捷键
from selenium.webdriver.common.keys import Keys


# 导入numpy 和pandas模块
# 将爬取的数据转化成DataFrame并存成excel文件
import pandas as pd
import numpy as np

import requests
from browsermobproxy import Server
#导入time模块，代码中多次用到。
import time

reload(sys)
sys.setdefaultencoding("utf-8")
def getVideoUrl():
    getVideoMp4Url(u'鲁教版');
def getVideoMp4Url(version):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select id,url,mp4url from video where version=\'%s\';" % version
    cursor.execute(sql)
    result = cursor.fetchall()
    server = Server("/bin/browsermob-proxy-2.0-beta-6/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()
#    
#    # 设置浏览器
    profile = webdriver.FirefoxProfile()
    profile.set_preference("javascript.enabled", False)
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
    # 得到网页源代码
    for index in range(len(result)):
        if result[index][2]:
	    print "aready update %s" % result[index][1]
	else:
            proxy.new_har("tongzhuo")
	    driver.get(result[index][1])
            while True:
                content = proxy.har  # returns a HAR JSON blob
                data = content['log']['entries']
                getMp4 = False
                for j in range(len(data)):
                    url = data[j]['request']['url']
                    if url.find("mp4") != -1:
            	        getMp4 = True
	    	        sql = "update video set mp4url=\'%s\' where id=\'%s\';" % (url, result[index][0])
	    	        print sql
	    	        cursor.execute(sql)
                        conn.commit()
	    	        break;
                if getMp4:
                    break
                else:
                    time.sleep(3)
    conn.commit()
    conn.close()
    server.stop()
    driver.quit()

#def getVideoMp4Url(cursor, version):
#    sql = "select id,url from video where version=\'%s\';" % version
#    cursor.execute(sql)
#    result = cursor.fetchall()
#
#    server = Server("/bin/browsermob-proxy-2.0-beta-6/bin/browsermob-proxy")
#    proxy = server.create_proxy()
#    
#    # 设置浏览器
#    profile = webdriver.FirefoxProfile()
#    profile.set_preference("javascript.enabled", False)
#    profile.set_proxy(proxy.selenium_proxy())
#    driver = webdriver.Firefox(firefox_profile=profile)
#    driver.get("http://www.tongzhuo100.com/login/v/?url=http://www.tongzhuo100.com/")
#    
#    # 输入账号密码
#    stu_id = driver.find_element_by_name("usr").send_keys("18500951888")
#    stu_pwd = driver.find_element_by_name("pwd")
#    stu_pwd.send_keys("tz4006345699")
#    
#    # 登录
#    stu_pwd.send_keys(Keys.RETURN)
#    time.sleep(10)
#    
#    ##得到监控
#    proxy.new_har("tongzhuo")
#    # 得到网页源代码
#    for index in range(len(result)):
#        server.start()
#        driver.get(result[index][1])
#        # 得到网络监控数据，json数据
#        while True:
#	    print '-------------------------------'
#            content = proxy.har  # returns a HAR JSON blob
#            data = content['log']['entries']
#            getMp4 = False
#            for j in range(len(data)):
#                url = data[j]['request']['url']
#                if url.find("mp4") != -1:
#        	    getMp4 = True
#		    sql = "update video set mp4url=\'%s\' where id=\'%s\'" % (url, result[index][0])
#		    print sql
#		    cursor.execute(sql)
#		    break;
#            if getMp4:
#                server.stop()
#                driver.back()
#                break
#            else:
#                time.sleep(5)
#    server.stop()
#    driver.quit()

def getUrl():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select name from sqlite_master where type='table' and name='urls';"
    cursor.execute(sql)
    if cursor.fetchall():
        sql = "delete  from urls;"
    else:    
        sql = \
                       "create table if not exists urls " \
                       "(id interger primary key, " \
                       "url nvarchar not null, " \
                       "version nvarchar not null, " \
                       "grade nvarchar not null, " \
                       "gradeurl nvarchar not null, " \
                       "subject nvarchar not null);";

    cursor.execute(sql)
    driver = webdriver.Firefox()
    # 打开portal登录页
    driver.get("http://www.tongzhuo100.com/login/v/?url=http://www.tongzhuo100.com/")
    
    # 输入账号密码
    stu_id = driver.find_element_by_name("usr").send_keys("18500951888")
    stu_pwd = driver.find_element_by_name("pwd")
    stu_pwd.send_keys("tz4006345699")
    
    # 登录
    stu_pwd.send_keys(Keys.RETURN)
    time.sleep(15)
    versionslength = len(driver.find_elements_by_class_name('version'))
    versioncount = 0
    for versionindex in range(versionslength):
        length = len(driver.find_elements_by_class_name('version')[versionindex].find_elements_by_tag_name("a"))
	detailversion = "" 
	gradecount = 0
        for count in range(length): 
            hrefs = driver.find_elements_by_class_name('version')[versionindex].find_elements_by_tag_name("a")
	    if count == 0:
	        detailversion = hrefs[count].text.encode('utf-8')
		continue
	    else:
                grade = hrefs[count].text.encode('utf-8')
		url = hrefs[count].get_attribute("href").encode('utf-8')
		hrefs[count].click()
		time.sleep(1)
		subject = driver.find_element_by_class_name('subjectCon')
		subjectcount = 1
		for elementindex in range(len(subject.find_elements_by_tag_name('a'))):
		    subref = subject.find_elements_by_tag_name('a')[elementindex].get_attribute("href").encode('utf-8')
		    detailsubject = subject.find_elements_by_tag_name('a')[elementindex].find_element_by_tag_name("p").text.encode('utf-8')
                    sql = "insert into urls (id, url, version, grade, gradeurl, subject) "\
                          "values (\'%s\',\'%s\', \'%s\',\'%s\', \'%s\',\'%s\');" % (versioncount*1000 + gradecount*10 + subjectcount, subref, detailversion, grade, url, detailsubject)
                    cursor.execute(sql)
                    conn.commit()
		    subjectcount += 1
		driver.back()

            gradecount += 1
	versioncount += 1
    time.sleep(2)
    conn.commit()
    conn.close()
    driver.close()
  
def setVersionId():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select name from sqlite_master where type='table' and name='version';"
    cursor.execute(sql)
    if cursor.fetchall():
        sql = "delete from version;"
    else:
        sql = \
                   "create table if not exists version " \
                   "(versionid nvarchar primary key, " \
                   "value integer not null);";

    cursor.execute(sql)
    selectFromUrls = "select distinct version from urls order by id asc;" 
    cursor.execute(selectFromUrls)
    versions = cursor.fetchall()
    for count in range(len(versions)):
        sql = "insert into version (versionid, value) "\
                  "values (\'%s\', \'%s\');" % (versions[count][0].encode('utf-8'), count + 1)
        cursor.execute(sql)

    conn.commit()
    conn.close()

def setGradeId():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select name from sqlite_master where type='table' and name='grade';"
    cursor.execute(sql)
    if cursor.fetchall():
        sql = "delete  from grade;"
    else:
        sql = \
                   "create table if not exists grade " \
                   "(gradeid nvarchar primary key, " \
                   "value integer not null);";

    cursor.execute(sql)
    selectFromUrls = "SELECT DISTINCT grade from urls ORDER BY id ASC" 
    cursor.execute(selectFromUrls)
    grades = cursor.fetchall()
    for count in range(len(grades)):
        sql = "insert into grade (gradeid, value) "\
                  "values (\'%s\', \'%s\');" % (grades[count][0].encode('utf-8'), count + 1)
        cursor.execute(sql)
    #sql = "select value from grade where gradeid='七年级'"
    #value = int(cursor.execute(sql).fetchone()[0])
    sql = "insert into grade (gradeid, value) "\
              "values (\'%s\', \'%s\');" % (u"初一", count + 2 )
    cursor.execute(sql)

    sql = "insert into grade (gradeid, value) "\
              "values (\'%s\', \'%s\');" % (u"初二", count + 3)
    cursor.execute(sql)

    sql = "insert into grade (gradeid, value) "\
              "values (\'%s\', \'%s\');" % (u"初三", count + 4)
    cursor.execute(sql)

    sql = "insert into grade (gradeid, value) "\
              "values (\'%s\', \'%s\');" % (u"初四", count + 5)
    cursor.execute(sql)

    conn.commit()
    conn.close()
    
def setSubjectId():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select name from sqlite_master where type='table' and name='subject';"
    cursor.execute(sql)
    if cursor.fetchall():
        sql = "delete  from subject;"
    else:
        sql = \
                   "create table if not exists subject " \
                   "(subjectid nvarchar primary key, " \
                   "value integer not null);";

    cursor.execute(sql)
    selectFromUrls = "SELECT DISTINCT subject from urls ORDER BY id ASC" 
    cursor.execute(selectFromUrls)
    subjects = cursor.fetchall()
    for count in range(len(subjects)):
        sql = "insert into subject (subjectid, value) "\
                  "values (\'%s\', \'%s\');" % (subjects[count][0].encode('utf-8'), count + 1)
        cursor.execute(sql)
    conn.commit()
    conn.close()

def grabCourse(cursor, version, subject, gradeurl, subjecturl):
    req = urllib2.Request(subjecturl)
    response = urllib2.urlopen(req)
    prog = re.compile(r'<a href="(.*?)".*title="(.*?)">')
    result = prog.findall(response.read())
    getversionsql = "select value from version where versionid = \'%s\';" % version
    cursor.execute(getversionsql)
    fetchobj = cursor.fetchone()
    if not fetchobj:
        return
    versionIndex = int(fetchobj[0])
    getgradesql = "select gradeid,value from grade;" 
    gradeDict = dict(cursor.execute(getgradesql).fetchall())
    getsubject = "select value from subject where subjectid = \'%s\';" % subject
    subjectId = int(cursor.execute(getsubject).fetchone()[0])

    count = 1
    for url,line in result:
        line = unicode(line.lstrip().replace("'", "''"), "utf-8")
        if line[0] == u"高":
            gradeSize = 2
        elif line[0] == u"初":
            gradeSize = 2
        else:
            gradeSize = 3
            if line.find("年级") < 0:
                gradeSize = 2
        grade = line[0:gradeSize]
        gradeIndex = 0
        for key in gradeDict.keys():
            if key.find(grade) >= 0:
                gradeIndex = int(gradeDict[key])
        	break;
        subjectstr = line[gradeSize:gradeSize+2].encode('utf-8')
	if line.find("上册")>=0 or line.find("下册")>=0:
            semester = line[gradeSize+2:gradeSize+4].encode('utf-8')
            nameIndex = line.find("《")
            lession = line[gradeSize+4:nameIndex].encode('utf-8')
            name = line[nameIndex:].encode('utf-8')
	else:
            semester = "" 
            nameIndex = line.find("《")
            lession = line[gradeSize+2:nameIndex].encode('utf-8')
            name = line[nameIndex:].encode('utf-8')

        videoid = versionIndex*1000000 + subjectId*5000 + 300*gradeIndex + count
        sql = "insert into video (id, version, subject,subjecturl, grade, gradeurl, semester, lesson, section, name, url, mp4url) "\
                  "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\', \'%s\',\'%s\',\'%s\',\'%s\', \'%s\');" % ( videoid, version, subject, subjecturl, grade, gradeurl, semester, lession, '',name , url.encode('utf-8'), '')
        print videoid , gradeIndex, sql
        count = count + 1
        cursor.execute(sql)

def getVideoAttribute():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select name from sqlite_master where type='table' and name='video';"
    cursor.execute(sql)
    if cursor.fetchall():
        sql = "delete  from video;"
    else:
        sql = \
                   "create table if not exists video " \
                   "(id integer primary key, " \
                   "version nvarchar not null, " \
                   "subject nvarchar not null, " \
                   "subjecturl nvarchar, " \
                   "grade nvarchar not null, " \
                   "gradeurl nvarchar not null, " \
                   "semester  nvarchar not null, " \
                   "lesson nvarchar, " \
                   "section nvarchar, " \
                   "name nvarchar, " \
                   "url nvarchar, " \
                   "mp4url nvarchar);";
    cursor.execute(sql)
    selectFromUrls = "select * from urls order by id asc;" 
    cursor.execute(selectFromUrls)
    urls = cursor.fetchall()
    for url in urls:
        grabCourse(cursor, url[2].encode('utf-8'), url[5].encode('utf-8'), url[4].encode('utf-8'), url[1].encode('utf-8'))
        conn.commit()
    conn.commit()
    conn.close()


#getUrl()
#setVersionId()
#setGradeId()
#setSubjectId()
#getVideoAttribute()
getVideoUrl();
#print "四年英语下册".find("年级")

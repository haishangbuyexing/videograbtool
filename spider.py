#-*- coding: utf-8 -*-
import urllib2

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

top_level_url = "http://www.tongzhuo100.com/primary/v7/1/1/index.html"

password_mgr.add_password(None, top_level_url, "18500951888", "tz4006345699")

handler = urllib2.HTTPBasicAuthHandler(password_mgr)

opener = urllib2.build_opener(handler)

a_url = "http://www.baidu.com/"

opener.open(a_url)

urllib2.install_opener(opener)

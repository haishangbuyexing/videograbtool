#-*- coding: utf-8 -*-
import urllib2
import re
import sys
import sqlite3
reload(sys)
sys.setdefaultencoding("utf-8")
URL="http://www.tongzhuo100.com/primary/v7/1/1/index.html"

def grabCourse(version, url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    prog = re.compile(r'<p class="b1">(.*?)</p>')
    result = prog.findall(response.read())
    conn = sqlite3.connect('sqlite.db')
    createVideoTable = \
                   "create table if not exists video " \
                   "(id integer primary key, " \
                   "version nvarchar not null, " \
                   "subject nvarchar not null, " \
                   "grade nvarchar not null, " \
                   "semester  nvarchar not null, " \
                   "lesson nvarchar, " \
                   "section nvarchar, " \
                   "name nvarchar, " \
                   "url nvarchar);";
    conn.execute(createVideoTable)
    count = 0
    for line in result:
        line = unicode(line, "utf-8")
        grade = line[0:3].encode('utf-8')
        subject = line[3:3+2].encode('utf-8')
	semester = line[5:5+2].encode('utf-8')
	lession = line[7:7+4].encode('utf-8')
	name = line[11:].encode('utf-8')
        sql = "insert into video (id, version, subject, grade, semester, lesson, section, name, url) "\
                  "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\', \'%s\');" % (count, version, subject, grade, semester, lession, '',name , '')
        count = count + 1
        conn.execute(sql)

    conn.commit()
    conn.close()
grabCourse(u'鲁教版',URL)


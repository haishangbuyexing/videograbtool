#-*- coding: utf-8 -*-
import os,sys,datetime
#import MySQLdb as mysqldb
import xlrd
import xlwt
from xlwt import *
import constant
import sqlite3

#def create_db():
#    try:
#        conn = mysqldb.connect(host='localhost', user='root')
#        conn.autocommit(True)
#        cur = conn.cursor()
#        cur.execute(constant.SQL_VIDEO_DATABASE)
#        cur.execute(constant.SQL_VIDEO_USER)
#        cur.close()
#        conn.close()
#    except mysqldb.Error, e:
#        logger.error("Database Error %d: %s" % (e.args[0], e.args[1]))
#        return
#
#def importExcelToDb(excelfile, sheetname):
#    if not os.path.exists(excelfile):
#        logger.error("Excel File Error, The File %s Does Not Exist", excelfile)
#	return
#    book = xlrd.open_workbook(excelfile)
#    print( book.sheet_names() )
#    for sheet_name in book.sheet_names():
#        sheet = book.sheet_by_name(sheetname)
#        database = mysqldb.connect(host="localhost",
#                                   user = "root",
#        			   passwd = "",
#        			   db = "video")
#        cursor = database.cursor()
#        
#        query = """INSERT INTO videos (id, version, subject, grade, semester, lesson, section,  videourl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
#        for r in range(1, sheet.nrows):
#            version = sheet.cell(r,).value.decode("gbk").encode("utf-8")
#            subject = sheet.cell(r, 1).value.decode("gbk").encode("utf-8")
#            grade = sheet.cell(r, 2).value.decode("gbk").encode("utf-8")
#            semester = sheet.cell(r, 3).value.decode("gbk").encode("utf-8")
#            lesson = sheet.cell(r, 4).value.decode("gbk").encode("utf-8")
#            section = sheet.cell(r, 5).value.decode("gbk").encode("utf-8")
#            videourl = sheet.cell(r, 6).value
#            values = (videoid, version, subject, grade, semester, lesson, section, videourl)
#            cursor.execute(query, values)
#        cursor.close()
#        database.commit()
#        database.close()
# 
def exportDbToExcel(version, subject):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = "select id,grade,semester,lesson,name,mp4url from video where version=\'%s\' and subject=\'%s\';" % (version,subject)
    cursor.execute(sql)
    results = cursor.fetchall()
    w = Workbook(encoding='utf-8')
    ws = w.add_sheet(subject)
    for index in range(len(results)): 
        ws.write(index, 0, results[index][1])
        ws.write(index, 1, results[index][2])
        ws.write(index, 2, results[index][3])
        ws.write(index, 3, results[index][4])
        ws.write(index, 4, results[index][5])
    w.save("%s-%s.xlsx" % (version, subject))

exportDbToExcel(r'鲁教版', r'语文')
 

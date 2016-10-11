#-*- coding: utf-8 -*-
import os,sys,datetime
import MySQLdb as mysqldb
import xlrd
import constant

def create_db():
    try:
        conn = mysqldb.connect(host='localhost', user='root')
        conn.autocommit(True)
        cur = conn.cursor()
        cur.execute(constant.SQL_VIDEO_DATABASE)
        cur.execute(constant.SQL_VIDEO_USER)
        cur.close()
        conn.close()
    except mysqldb.Error, e:
        logger.error("Database Error %d: %s" % (e.args[0], e.args[1]))
        return

def importExcelToDb(excelfile, sheetname):
    if !os.path.exists(excelfile):
        logger.error("Excel File Error, The File %s Does Not Exist", excelfile)
	return
    book = xlrd.open_workbook(excelfile)
    print( book.sheet_names() )
    for sheet_name in book.sheet_names():

    sheet = book.sheet_by_name(sheetname)
    database = mysqldb.connect(host="localhost",
                               user = "root",
    			   passwd = "",
    			   db = "video")
    cursor = database.cursor()
    
    query = """INSERT INTO videos (id, version, subject, grade, semester, lesson, section,  videourl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    for r in range(1, sheet.nrows):
        version = sheet.cell(r,).value.decode("gbk").encode("utf-8")
        subject = sheet.cell(r, 1).value.decode("gbk").encode("utf-8")
        grade = sheet.cell(r, 2).value.decode("gbk").encode("utf-8")
        semester = sheet.cell(r, 3).value.decode("gbk").encode("utf-8")
        lesson = sheet.cell(r, 4).value.decode("gbk").encode("utf-8")
        section = sheet.cell(r, 5).value.decode("gbk").encode("utf-8")
        videourl = sheet.cell(r, 6).value
        values = (videoid, version, subject, grade, semester, lesson, section, videourl)
        cursor.execute(query, values)
    cursor.close()
    database.commit()
    database.close()
 
 create_db()
 importExcelToDb("")

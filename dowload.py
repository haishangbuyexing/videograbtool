# -*- coding: utf-8 -*-
import time
import requests
import sqlite3
import os,sys,datetime,errno
#from queue import Queue
#from threading import Thread
import logging
LOGFILE="downlog.txt"
logger = logging.getLogger("tongzhuo")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
file_handler = logging.FileHandler(LOGFILE)  
file_handler.setFormatter(formatter)  
logger.addHandler(file_handler)  

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
def down(down_dir,link, referer):
    """
    Download the images from the given link and store it to the designated directory
    Args:
        down_dir:the images storage folder
        link:the download link
    Raises:
        HTTPError:An error occured accessing the website
        URLError:An error occured when os no connection
        socket.error:An error occured during TCP/IP connection
    """
    directory = os.path.join(down_dir, os.path.basename(link))
    headers={'User-Agent': user_agent, 
             'Referer': referer
	    }#构造头部
    try:
        conn = requests.get(link, headers=headers, timeout=5)
    except:
        logger.error("download %s failed" % (link,)) 
        return False
    else:
        if conn:
            f = open(directory, 'wb')
            f.write(conn.content)
            f.close()
            return True
        else:
            return False
def download():
    DOWNLOAD_BASE_DIR="/root/Videos/tongzhuo"
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    sql = \
                           "create table if not exists dowloadedmp4 " \
                           "(downurl nvarchar primary key, " \
                            "downpath nvarchar not null, " \
                            "downdir nvarchar not null, " \
                           "finished interger not null);";
    cursor.execute(sql)
    sql = "select id, version, subject, grade, semester, lesson, name, mp4url, subjecturl from video where mp4url != '';"
    cursor.execute(sql)
    results =  cursor.fetchall()
    MAXCOUNT=20
    for index in range(len(results)):
        if results[index][6] == "":
            break
        strlist = results[index][7].split('_')
        if len(strlist) < 2:
           logger.error("the url is not valid %s %s %s %s %s %s %s %s" % (results[index][0], results[index][1],results[index][2],results[index][3],results[index][4],results[index][5],results[index][6],results[index][7])) 
           break
        for count in range(MAXCOUNT):      
           downloadurl = strlist[0] + '_' + "%s"%(count+1,)+".mp4"
           sql = "select * from dowloadedmp4 where downurl=\'%s\';" % downloadurl
           cursor.execute(sql)
           re = cursor.fetchone()
           if re :
               continue
           else:
               dirpath = "%s/%s/%s/%s/%s/%s/%s/" % (DOWNLOAD_BASE_DIR, results[index][1], results[index][2], results[index][3],results[index][4],results[index][5],results[index][6])
    	   try:
    	       os.makedirs(dirpath)
           except OSError as exc:
    	       if exc.errno == errno.EEXIST and os.path.isdir(dirpath):
    	           pass
    	       else:
                   logger.error("mkdir %s failed" % (dirpath,))
    		   continue
           if down(dirpath, downloadurl, results[index][7]):
               downpath = os.path.join(dirpath, os.path.basename(downloadurl))
               sql = "insert into dowloadedmp4 (downurl, downpath, downdir, finished) "\
                  "values (\'%s\',\'%s\',\'%s\', \'%s\');" % (downloadurl,  downpath, dirpath, 1)
	       print sql
               cursor.execute(sql)
      	       conn.commit()
    conn.commit()
    conn.close()
	            
download()

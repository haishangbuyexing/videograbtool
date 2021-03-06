# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:25:34 2015

@author: Gryps
"""

from queue import Queue
from threading import Thread
from time  import ctime,time,sleep
from urllib.request import HTTPError,URLError
import urllib.request,sys,math,os,socket
import logger
import json
json_str = ''
def app_init():
    """
    data init
    """
    if os.path.exists('data.json'):
        return
    data = {
        'threadnum' : 10,
	'videonum'  : 20,
    }
    with open('data.json', 'w') as f:
        json.dump(data, f)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
def down(down_dir,link):
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
    print(link)
    print(directory)
    req = urllib.request.Request(link)
    req.add_header("User-Agent", user_agent)
    req.add_header("Referer", link)
    conn = urllib.request.urlopen(req)
    f = open(directory, 'wb')
    f.write(conn.read())
    f.close()

def setup_dir():
    """
    Set the download directory of images downloaded
    Return:
        download_dir:the setting directory of images to be stored
    """
    download_dir = os.path.abspath("/home/dowload/")
    return download_dir

def get_link(origion, start,stop):
    """
    Acquire all downloading links and set to links array
    Args:
        start:the image initialed index value
        stop:the image terminated index value
    Return:
        links:the all link array for downloading
    """
    strlist = origion.split("_") 
    if len(strlist) != 2:
       logger.error("the url is not valid %s", origion) 
       return
    origion = strlist[0] + "_"
    links = []
    for x in range(start, stop):
        url = origion + str(x) + '.mp4'
        links.append(url)
    return links

class DownloadWorker(Thread):
    """
    The class of image downloading thread
    Function:
        __init__():initialization of threading
        run:the running of threading
    """
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            down_dir, link = self.queue.get()
            print( os.path.basename(link)+"\n" )
            try:
                down(down_dir,link)
            except HTTPError as e:
                print( os.path.basename(link)+': '+e.reason )
            except URLError as e:
                print( e.__weakref__ )
            except socket.error as e:
                print( e.__weakref__ )
            self.queue.task_done()

def main():
    app_init()
    with open('data.json', 'r') as f:
        json_data = json.load(f)
    print(json_data['videonum'])
    ts = time()
    start = 1 
    stop = int(json_data['videonum'])
    # set the number of threads
    threads = int(json_data['threadnum'])
    k = stop-start
    # acquire the download links
    links = [l for l in get_link(origion, start,stop)]
    # set the download storage directory
    down_dir = setup_dir()
    queue = Queue()
    # judge download numbers if greater than threads or not
    # if K< = threads ,set the k for threads,else set the threads for the number of thread
    if k <= threads:
        for x in range(k-1):
            print( queue.qsize() )
            worker = DownloadWorker(queue)
            worker.setDaemon(True)
            worker.start()
    else:
        for x in range(threads):
            worker = DownloadWorker(queue)
            worker.setDaemon(True)
            worker.start()
    # traverse the links and put the link to queue
    for link in links:
        queue.put((down_dir,link))
    # the new queue joining
    queue.join()
    print( 'Took {}'.format(time()-ts) )
    print( "The finished time:" + ctime() )

if __name__ == '__main__':
    #main()
    down("/root/Video/tongzhuo/", "http://v15.tongzhuo100.com/files/junior/eight/1DMGCG0K44_1.mp4")

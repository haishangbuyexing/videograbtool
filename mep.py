#-*- coding: utf-8 -*-
import sqlite3
import os, sys, datetime
import glob
import json
import subprocess
from subprocess import CalledProcessError 
import smbcommands
import commands
import logging
<<<<<<< HEAD
import Queue
from threading import Thread
=======
from collections import OrderedDict
>>>>>>> 0cd54ebd6e1705d2bb8a2be25dabdcd038f6d1bc
LOGFILE="downlog.txt"
logger = logging.getLogger("tongzhuo")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
file_handler = logging.FileHandler(LOGFILE)  
file_handler.setFormatter(formatter)  
logger.addHandler(file_handler)  
reload(sys)
sys.setdefaultencoding("utf-8")
#conn = sqlite3.connect('sqlite.db')
#cursor = conn.cursor()
#sql = "select name from sqlite_master where type='table' and name='mepfinisheddir';"
#cursor.execute(sql)
#if cursor.fetchall():
#    sql = "delete  from urls;"
#else:    
#    sql = \
#                   "create table if not exists mepfinisheddir" \
#                   "(mepdir nvarchar primary key, " \
#                   "mepfilepath nvarchar not null);";
#
#cursor.execute(sql)
def getLength(filename): 
    result, out = smbcommands.getstatusoutput('''ffprobe -i %s -show_entries format=duration -v quiet -of csv="%s" ''' %(filename.replace('\\', '\\\\').encode('gbk'), "p=0"))
    if result != 0:  
        logger.error("ffprobe %s error"%filename) 
        return -1
    return out
def convert(fileabpath ):
    fileduration =  float(getLength(fileabpath))
    if fileduration >= 480:
        basename = os.path.basename(fileabpath)
        if basename.find('atemp') > 0:
            os.remove(fileabpath)
	    return
        basedir = os.path.dirname(fileabpath)
        tempmp4 = os.path.join(basedir, "atemp-%s"%(basename,))
        try:
            cmd = '''ffmpeg -i  %s -vcodec libx264 %s''' %(fileabpath.replace('\\', '\\\\').encode('gbk'), tempmp4.replace('\\', '\\\\').encode('gbk'),)
            print cmd
            result = subprocess.check_output(cmd, shell='True')
        except CalledProcessError as e:
            logger.error("ffmpeg %s error"%fileabpath )
            if os.path.exists(tempmp4):
                os.remove(tempmp4)
	    return
        else:
            os.remove(fileabpath)
            os.rename(tempmp4,fileabpath)
class Converter(Thread): 
    def __init__(self, queue):
        Thread.__init__(self)
	self.queue = queue
    def run(self):
        while True:
	    convertfilepath = self.queue.get()
	    convert(convertfilepath)
	    self.queue.task_done()
	        
def mp4Convert(basedir):
    mepDict = {}
    threadMaxNum = 6
    queue = Queue.Queue()
    for x in range(threadMaxNum):
        worker = Converter(queue)
	worker.setDaemon(True)
	worker.start()
    for root, dirs, files in os.walk(basedir):
        for file in files:
	    if file.endswith('.mp4'):
<<<<<<< HEAD
                absolutefilepath = os.path.join(root, file).decode('utf-8')
		queue.put(absolutefilepath)
    queue.join()
 #def mp4Convert(basedir):
 #   mepDict = {}
 #   threadMaxNum = 6
 #   for root, dirs, files in os.walk(basedir):
 #       for file in files:
 #           if file.endswith('.mp4'):
 #               if not mepDict.get(root.decode('utf-8')):
 #                   mepDict[root.decode('utf-8')] = []
 #       	mepDict[root.decode('utf-8')].append(os.path.join(root, file).decode('utf-8'))
 #   for key in mepDict.keys():
 #       movielist = mepDict[key]
 #       if len(movielist) <= 0:
 #           break
 #       for index in range(len(movielist)):
 #           fileduration =  float(getLength(movielist[index]))
 #           if fileduration >= 480:
 #               fileabpath = movielist[index]
 #               basename = os.path.basename(fileabpath)
 #       	if basename.find('atemp') > 0:
 #                   os.remove(fileabpath)
 #       	    continue
 #               basedir = os.path.dirname(fileabpath)
 #       	tempmp4 = os.path.join(basedir, "atemp-%s"%(basename,))
 #       	try:
 #                   cmd = '''ffmpeg -i  %s -vcodec libx264 %s''' %(fileabpath.replace('\\', '\\\\').encode('gbk'), tempmp4.replace('\\', '\\\\').encode('gbk'),)
 #       	    print cmd
 #                   result = subprocess.check_output(cmd, shell='True')
 #               except CalledProcessError as e:
 #                   logger.error("ffmpeg %s error"%fileabpath )
 #       	    if os.path.exists(tempmp4):
 #                       os.remove(tempmp4)
 #       	    continue
 #               else:
 #                   os.remove(fileabpath)
 #                   os.rename(tempmp4,fileabpath)
 # 
 
#def createMep(basedir):
#    mepDict = {}
#    for root, dirs, files in os.walk(basedir):
#        for file in files:
#	    if file.endswith('.mp4'):
#	        if not mepDict.get(root.decode('utf-8')):
#	            mepDict[root.decode('utf-8')] = []
#		mepDict[root.decode('utf-8')].append(os.path.join(root, file).decode('utf-8'))
#    for key in mepDict.keys():
#        movielist = mepDict[key]
#	if len(movielist) <= 0:
#	    break
#        movie = movielist[0]
#	slist = movie.split('_')
#	if len(slist) < 2:
#	    break
#	movieConfigList = []
#	singleMovieDict = {
#                "BeginTime" : 0,
#	    	"EndTime" : 80000000,
#                "IsAudioFadeInOut":False,
#                "IsEnableAudio":False,
#                "IsEnableVideo":True,
#                "IsSilence":False,
#	    	"KeepFrameAtMediaTime":0,
#	    	"KeepFrameTimeLen":0,
#	    	"MediaClipEndTime":80000000,
#	    	"MediaClipStartTime":0,
#	    	"MediaPath":"%s"% movie,
#	    	"PlaySpeed":1,
#	    	"TransEffPreferTimeLen":0,
#	    	"Transform":[1,0,0,0,1,0,0,0,1],
#	    	"UseAudioTrackIndex":-1,
#	    	"Volume":1,
#	    	"ZOrder":0
#	}
#	movieConfigList.append(singleMovieDict)
#        startTime = 80000000
#	movieSumDuration = 0
#	for i in range(len(movielist)):
#	    file = slist[0] + "_%s.mp4"%(i+1)
#	    fileduration =  round(float(getLength(file))*10000000)
#	    if fileduration < 0:
#	        break
#	    movieSumDuration += fileduration
#	    if i == 0:
#	        fileduration = fileduration - 80000000
#	    endTime = startTime + fileduration
#	    singleMovieDict = {
#                        "BeginTime" : startTime,
#			"EndTime" : endTime,
#                        "IsAudioFadeInOut":False,
#                        "IsEnableAudio":False,
#                        "IsEnableVideo":True,
#                        "IsSilence":False,
#			"KeepFrameAtMediaTime":startTime,
#			"KeepFrameTimeLen":0,
#			"MediaClipEndTime":endTime,
#			"MediaClipStartTime":0,
#			"MediaPath":"%s"% file,
#			"PlaySpeed":1,
#			"TransEffPreferTimeLen":0,
#			"Transform":[1,0,0,0,1,0,0,0,1],
#			"UseAudioTrackIndex":-1,
#			"Volume":1,
#			"ZOrder":0
#	    }
#	    movieConfigList.append(singleMovieDict)
#	    startTime = endTime
#        watermarklist = []	
#	topWaterMarkNum = (int(movieSumDuration - 80000000)/10000000)/600 + 1
#        for i in range(topWaterMarkNum):
#	    beginTime = 80000000 + i*10*60*10000000
#	    endTime = 80000000 + (i + 1)*10*60*10000000
#	    if i == topWaterMarkNum:
#	        endTime = movieSumDuration
#	    if i/2 == 0:
#                areatransform = [0.96923035383224487,0,0,0,0.30460301041603088,0,503.6168212890625,7.7591605186462402,1]
#	    else:
#                areatransform = [1.0358484983444214,0,0,0,0.3046029806137085,0,116.80840301513672,5.8534984588623047,1]	        
#	    singleWaterMark= {
#                 "Alpha":255,
#	         "AreaHeight":100,
#	         "AreaLeft":0,
#	         "AreaTop":0,
#                 "AreaTransform": areatransform,
#                 "AreaType":0,
#	         "AreaWidth":100,
#	         "BeginTime":beginTime,
#	         "EndTime":endTime,
#	         "IsAreaSmooth":False,
#	         "IsFade":False,
#	         "Name":"AreaGuassBlur",
#	         "Radius":6,
#	         "Ver":1,
#	         "ZOrder":1
#	    }
#            watermarklist.append(singleWaterMark)	
#	downWaterMark= {
#                 "Alpha":255,
#	         "AreaHeight":100,
#	         "AreaLeft":0,
#	         "AreaTop":0,
#                 "AreaTransform": [4.1944594383239746,0,0,0,1.0099996328353882,0,146.68092346191406,278.67919921875,1],
#                 "AreaType":0,
#	         "AreaWidth":100,
#	         "BeginTime":movieSumDuration - 60000000,
#	         "EndTime":movieSumDuration,
#	         "IsAreaSmooth":False,
#	         "IsFade":False,
#	         "Name":"AreaGuassBlur",
#	         "Radius":6,
#	         "Ver":1,
#	         "ZOrder":1
#	    }
#        watermarklist.append(downWaterMark)	
#
#        mepId = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#	configList = {
#                     "AudioBits":16,
#		     "AudioChannels":2,
#		     "AudioList":None,
#		     "AudioSampleRate":44100,
#		     "Author":"jun.wang",
#		     "FrameList":None,
#		     "FrameTime":400000,
#		     "ID": mepId,
#		     "ImageEffectList":None,
#		     "ImageList":None,
#		     "MEPVer":65541,
#                     "MovieList": movieConfigList,
#		     "Name":"1",
#		     "OutputFileTypeName":r"MP4格式",
#		     "OutputVideoSizeName":"720*404(480P 16:9)",
#		     "RandTransEffs":None,
#                     "RemoveWatermarkEffectList": watermarklist,
#		     "SceneHeight":404,
#		     "SceneWidth":720,
#		     "TextList":None,
#		     "TmpDir": os.path.join(basedir, "mep%s"%mepId),
#		     "VideoOutputDisplayAspectRatio":-1,
#		     "VideoOutputFrameTime":400000,
#		     "VideoOutputHeight":404,
#		     "VideoOutputWidth":720
#	}
#	pathList = key.split(os.path.sep)
#        length = len(pathList)
#	if length < 6:
#	    continue
#	conn = sqlite3.connect('sqlite.db')
#        cursor = conn.cursor()
#        sql = '''select id from video where version=\'%s\' and subject=\'%s\' and grade=\'%s\' and semester=\'%s\' and lesson=\'%s\' and name=\"%s\";'''% (pathList[length - 6], pathList[length - 5],pathList[length - 4], pathList[length - 3], pathList[length - 2], pathList[length - 1])
#        cursor.execute(sql)
#        result = cursor.fetchone()
#        if len(result):
#            with open(os.path.join(basedir, "%s.mep"%result[0]), 'w') as f:
#                json.dump(configList, f, ensure_ascii=False, indent=2, sort_keys=True)
#
=======
	        if not mepDict.get(root.decode('utf-8')):
	            mepDict[root.decode('utf-8')] = []
		mepDict[root.decode('utf-8')].append(os.path.join(root, file).decode('utf-8'))
    for key in mepDict.keys():
        movielist = mepDict[key]
	if len(movielist) <= 0:
	    break
        movie = movielist[0]
	slist = movie.split('_')
	if len(slist) < 2:
	    break
	movieConfigList = []
	singleMovieDict = {
                "BeginTime" : 0,
	    	"EndTime" : 80000000,
                "IsAudioFadeInOut":"false",
                "IsSilence":"false",
	    	"KeepFrameAtMediaTime":0,
	    	"KeepFrameTimeLen":0,
	    	"MediaClipEndTime":80000000,
	    	"MediaClipStartTime":0,
	    	"MediaPath":"%s"% movie,
	    	"PlaySpeed":1,
	    	"TransEffPreferTimeLen":0,
	    	"Transform":[1,0,0,0,1,0,0,0,1],
	    	"UseAudioTrackIndex":-1,
	    	"Volume":1,
	    	"ZOrder":0
	}
	movieConfigList.append(singleMovieDict)
        startTime = 80000000
	movieSumDuration = 0
	for i in range(len(movielist)):
	    file = slist[0] + "_%s.mp4"%(i+1)
	    fileduration =  round(float(getLength(file))*10000000)
	    movieSumDuration += fileduration
	    if i == 0:
	        fileduration = fileduration - 80000000
	    endTime = startTime + fileduration
	    singleMovieDict = {
                        "BeginTime" : startTime,
			"EndTime" : endTime,
                        "IsAudioFadeInOut":"false",
                        "IsSilence":"false",
			"KeepFrameAtMediaTime":startTime,
			"KeepFrameTimeLen":0,
			"MediaClipEndTime":endTime,
			"MediaClipStartTime":0,
			"MediaPath":"%s"% file,
			"PlaySpeed":1,
			"TransEffPreferTimeLen":0,
			"Transform":[1,0,0,0,1,0,0,0,1],
			"UseAudioTrackIndex":-1,
			"Volume":1,
			"ZOrder":0
	    }
	    movieConfigList.append(singleMovieDict)
	    startTime = endTime
        watermarklist = []	
	topWaterMarkNum = (int(movieSumDuration - 80000000)/10000000)/600 + 1
        for i in range(topWaterMarkNum):
	    beginTime = 80000000 + i*10*60*10000000
	    endTime = 80000000 + (i + 1)*10*60*10000000
	    if i == topWaterMarkNum:
	        endTime = movieSumDuration
	    if i/2 == 0:
                areatransform = [0.96923035383224487,0,0,0,0.30460301041603088,0,503.6168212890625,7.7591605186462402,1]
	    else:
                areatransform = [1.0358484983444214,0,0,0,0.3046029806137085,0,116.80840301513672,5.8534984588623047,1]	        
	    singleWaterMark= {
                 "Alpha":255,
	         "AreaHeight":100,
	         "AreaLeft":0,
	         "AreaTop":0,
                 "AreaTransform": areatransform,
                 "AreaType":0,
	         "AreaWidth":100,
	         "BeginTime":beginTime,
	         "EndTime":endTime,
	         "IsAreaSmooth":"false",
	         "IsFade":"false",
	         "Name":"AreaGuassBlur",
	         "Radius":6,
	         "Ver":1,
	         "ZOrder":1
	    }
            watermarklist.append(singleWaterMark)	
	downWaterMark= {
                 "Alpha":255,
	         "AreaHeight":100,
	         "AreaLeft":0,
	         "AreaTop":0,
                 "AreaTransform": [4.1944594383239746,0,0,0,1.0099996328353882,0,146.68092346191406,278.67919921875,1],
                 "AreaType":0,
	         "AreaWidth":100,
	         "BeginTime":movieSumDuration - 60000000,
	         "EndTime":movieSumDuration,
	         "IsAreaSmooth":"false",
	         "IsFade":"false",
	         "Name":"AreaGuassBlur",
	         "Radius":6,
	         "Ver":1,
	         "ZOrder":1
	    }
        watermarklist.append(downWaterMark)	

        mepId = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	configList = {
                     "AudioBits":16,
		     "AudioChannels":2,
		     "AudioList":"null",
		     "AudioSampleRate":44100,
		     "Author":"jun.wang",
		     "FrameList":"null",
		     "FrameTime":400000,
		     "ID": mepId,
		     "ImageEffectList":"null",
		     "ImageList":"null",
		     "MEPVer":65541,
                     "MovieList": movieConfigList,
		     "Name":"1",
		     "OutputFileTypeName":r"MP4格式",
		     "OutputVideoSizeName":"720*404(480P 16:9)",
		     "RandTransEffs":"null",
                     "RemoveWatermarkEffectList": watermarklist,
		     "SceneHeight":404,
		     "SceneWidth":720,
		     "TextList":"null",
		     "TmpDir": os.path.join(basedir, "mep%s"%mepId),
		     "VideoOutputDisplayAspectRatio":-1,
		     "VideoOutputFrameTime":400000,
		     "VideoOutputHeight":404,
		     "VideoOutputWidth":720
	}
	pathList = key.split(os.path.sep)
        length = len(pathList)
	if length < 6:
	    continue
	conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()
        sql = '''select id from video where version=\'%s\' and subject=\'%s\' and grade=\'%s\' and semester=\'%s\' and lesson=\'%s\' and name=\"%s\";'''% (pathList[length - 6], pathList[length - 5],pathList[length - 4], pathList[length - 3], pathList[length - 2], pathList[length - 1])
	print sql
        cursor.execute(sql)
        result = cursor.fetchone()
        if len(result):
            with open(os.path.join(basedir, "%s.mep"%result[0]), 'w') as f:
                json.dump(configList, f, ensure_ascii=False, indent=2, sort_keys=True)

>>>>>>> 0cd54ebd6e1705d2bb8a2be25dabdcd038f6d1bc


             
#createMep(unicode("i:\\tongzhuo\\鲁教版", 'utf-8'))
mp4Convert(unicode("j:\\tongzhuo\\鲁教版\\语文", 'utf-8'))



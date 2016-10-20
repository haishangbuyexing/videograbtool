#-*- coding: utf-8 -*-
import subprocess
import commands
import os
def getstatusoutput(cmd):
    p = subprocess.Popen(cmd,shell=True, stdout = subprocess.PIPE,stderr= subprocess.PIPE)
    result = subprocess.Popen.wait(p) 
    lines = p.stdout.readlines()
    lines += p.stderr.readlines()
    p.communicate() 

    out = ""
    for i in range(0,len(lines)):
        if i == len(lines) - 1:
            out += lines[i].rstrip()
        else:
            out += lines[i]

    return result,out
    
if __name__=="__main__":

    cmd = '''ffmpeg -i %s -vcodec libx264 %s''' %("D:\\1DMG14110M_1.mp4 ", "D:\\temp.mp4")
    subprocess.check_call(cmd,  shell='True')

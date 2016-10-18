#-*- coding: utf-8 -*-
import subprocess

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
    rc,out = getstatusoutput("ffprobe %s -show_format 2>&1 | sed -n 's/duration=//p' " % ("/root/Videos/tongzhuo/鲁教版/地理/七年级/上册/第二章第1节/《地势和地形（3）》/1DMGCG0M1G_3.mp4".decode('utf-8'),))
    print rc
    print out

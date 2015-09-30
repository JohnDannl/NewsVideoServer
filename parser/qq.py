#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-1

@author: JohnDannl
'''

import sys
sys.path.append(r'..')
sys.path.append(r'../database')
from common import getHtml,r1
from database import table
from database import dbconfig
import logging

import xml.etree.ElementTree as ET

ctable=dbconfig.tableName[6]
suffix=[r'.m3u8',r'.mp3',r'mp4',r'.flv',r'.f4v']

def getVideoByUrl(url):
#     tDir=r'e:\tmp'
#     fileName=r'v1.html'
#     filePath=os.path.join(tDir,fileName)  
# url is like : http://v.qq.com/news/?tag=hot&vid=a00153364t6
    vid=r1(r'.*?vid=(.*)',url)
    videoUrl=getVideoByVid(vid)          
    return videoUrl

def getVideoByVid(vid):
    url = 'http://vv.video.qq.com/geturl?otype=xml&platform=1&vid=%s&format=2' % vid
    content=getHtml(url)
    videoUrl=None
    if content:
        videoUrl=r1(r'<url>(.*?)</url>',content)    
    return videoUrl

def main():
    rows=table.getTopUrls(ctable, 10)
    count=0
    for item in rows:
        count+=1
        print item[0],item[1]
        print count,'.',getVideoByUrl(item[0])       
        
if __name__=='__main__':  
#     main()
    print getVideoByVid(r'u00150m98m7');
    
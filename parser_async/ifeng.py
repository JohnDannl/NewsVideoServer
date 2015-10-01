#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-1

@author: JohnDannl
'''

import sys
sys.path.append(r'../')
sys.path.append(r'../database')
sys.path.append(r'../common')
from common.common import getHtml,r1
from database import table
from database import dbconfig
import logging

import xml.etree.ElementTree as ET

ctable=dbconfig.tableName['ifeng']

def getVideoByUrl(url):
#     tDir=r'e:\tmp'
#     fileName=r'v1.html'
#     filePath=os.path.join(tDir,fileName)  
#     url is like:http://v.ifeng.com/news/world/201408/015041f2-2979-9982-9fb1-950a9390ac64.shtml  
#     vInfo_url_prefix=r'http://v.ifeng.com/video_info_new/4/48/01de5902-0b5a-00f1-5154-47d50dda0448.xml'  
    vInfo_url_prefix=r'http://v.ifeng.com/video_info_new/'#4/48/01de5902-0b5a-00f1-5154-47d50dda0448.xml' 
    d1=r1(r'.*/(.*?)\.',url)
#     print d1,d1[len(d1)-2],d1[len(d1)-2:len(d1)]
    vInfo_url=vInfo_url_prefix+d1[len(d1)-2]+r'/'+d1[len(d1)-2:len(d1)]+r'/'+d1+r'.xml'
#     print vInfo_url
    content=getHtml(vInfo_url)
    
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)

    videoUrl=None
    if content:
        root = ET.fromstring(content)
        videoUrl=root[0].attrib.get('VideoPlayUrl')
    return videoUrl

def getUrlByVid(vid):
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        return url
    
def getVInfoUrl(url):
    if url:
        vInfo_url_prefix=r'http://v.ifeng.com/video_info_new/'
        d1=r1(r'.*/(.*?)\.',url)
        vInfo_url=vInfo_url_prefix+d1[len(d1)-2]+r'/'+d1[len(d1)-2:len(d1)]+r'/'+d1+r'.xml'
        return vInfo_url
        
def getVideoUrlByContent(content):
    if content:
        root = ET.fromstring(content)
        videoUrl=root[0].attrib.get('VideoPlayUrl')
        return videoUrl  
      
def getVideoByVid(vid):
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        return getVideoByUrl(url)
    else:
        return None

def main():
    rows=table.getTopUrls(ctable, 10)
    count=0
    for item in rows:
        count+=1
        print item[0]
        print count,'.',getVideoByUrl(item[0])       
        
if __name__=='__main__':  
    main()
#     print getVideoByVid(r'015041f2-2979-9982-9fb1-950a9390ac64');
#     print getVideoByUrl(r'http://v.ifeng.com/news/world/201410/010c2173-7504-4b25-a13c-8eecf971032b.shtml');
    
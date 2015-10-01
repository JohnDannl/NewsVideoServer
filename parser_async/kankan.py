#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-1

@author: JohnDannl
'''
import sys
sys.path.append(r'../database')
sys.path.append(r'../common')
from common.common import getHtml,r1
from database import table
from database import dbconfig
import logging

import xml.etree.ElementTree as ET

ctable=dbconfig.tableName['kankan']
suffix=[r'.m3u8',r'.mp3',r'mp4',r'.flv',r'.f4v']
def getVideoByUrl(url):
#     tDir=r'e:\tmp'
#     fileName=r'v1.html'
#     filePath=os.path.join(tDir,fileName)  

    content=getHtml(url)
    
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)

    videoUrl=None
    if content:             
        # video, all type should be considered at the last
        videoUrl=r1(r'<source src="(.*?)"',content)
        if not videoUrl:
            # audio
            videoUrl=r1(r'audio src="(.*?)"',content)
            if not videoUrl:                    
                # all type
                videoUrl=getVideoInfoByUrl(url)
#         if videoUrl:
#             if not os.path.splitext(videoUrl)[1] in suffix:                              
#                 print videoUrl    
#                 videoUrl=None                              
    return videoUrl
def getVideoDirectByContent(content):
    videoUrl=None
    if content:         
        # video
        videoUrl=r1(r'<source src="(.*?)"',content)
        if not videoUrl:
            # audio
            videoUrl=r1(r'audio src="(.*?)"',content)
    return videoUrl
def getVideoInfoByUrl(url):
    # url is like : http://domestic.kankanews.com/c/2014-08-04/0015274473.shtml
    # xml url is like : http://www.kankanews.com/vxml/2014-08-04/0015274473.xml
    part1=r1(r'(/\d{4}-\d{2}-\d{2}/\w*?)\.',url)
    xml_url=r'http://www.kankanews.com/vxml%s.xml'%part1
    content=getHtml(xml_url)
    videoUrl=None
    if content:
        root=ET.fromstring(content)
        resolution=root[0].text.replace('h264_1500k_mp4','h264_450k_mp4')   # just a patch
        videoUrl= root[1].text+resolution
    return videoUrl

def getVideoInfoByContent(content):
    if content:
        root=ET.fromstring(content)
        resolution=root[0].text.replace('h264_1500k_mp4','h264_450k_mp4')   # just a patch
        videoUrl= root[1].text+resolution
        return videoUrl

def getUrlByVid(vid):
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        return url
        
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
#         print count,'.',getVideoInfoByUrl(item[0])      
        
if __name__=='__main__':  
    main()
    
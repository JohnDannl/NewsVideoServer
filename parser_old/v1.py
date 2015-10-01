#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-7-29

@author: JohnDannl
'''
from common import getHtml,getGzipHtml,r1
from database import table
from database import dbconfig
import logging
import os
import fileKit

ctable=dbconfig.tableName[2]

def getVideoByUrl(url):
#     tDir=r'e:\tmp'
#     fileName=r'v1.html'
#     filePath=os.path.join(tDir,fileName)  
     
    content=getGzipHtml(url)
#     if content:    
#         fileKit.writeFileBinary(filePath, content)
#     content=fileKit.readFileBinary(filePath)
    videoUrl=None
    if content:
        videoUrl=r1(r'<param.*?videoUrl=(.*?)"',content)
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
        print item[0],item[1]
        print count,'.',getVideoByUrl(item[0])       
        
if __name__=='__main__':  
    main()
#     print getVideoByUrl('http://www.v1.cn/2015-02-03/1593873.shtml')
#     print getVideoByVid(r'1252315')
    
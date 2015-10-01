#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-7-29

@author: JohnDannl
'''
from common.common import getHtml,r1
from database import table
from database import dbconfig
import logging

v1_header=[('Host', 'api.v1.cn'),
         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'),
         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
         ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
         ('Connection', 'keep-alive'),
         ('Referer', 'http://news.v1.cn/')]  

ctable=dbconfig.tableName['v1']

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
        videoUrl=r1(r'<param.*?videoUrl=(.*?)"',content)
    return videoUrl

def getVideoByVid(vid):
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        return getVideoByUrl(url)
    else:
        return None
    
def getUrlByVid(vid):  
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        return url  
    
def main():
    rows=table.getTopUrls(ctable, 10)
    count=0
    for item in rows:
        count+=1
        print item[0],item[1]
        print count,'.',getVideoByUrl(item[0])       
        
if __name__=='__main__':  
    main()
#     print getVideoByVid(r'1252315')
    
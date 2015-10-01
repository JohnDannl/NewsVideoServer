#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-2

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append(r'../common')
import urllib
from common.common import getHtml,r1
from database import table
from database import dbconfig
import logging

import xml.etree.ElementTree as ET

sina_header=[('Host', 'api.roll.news.sina.com.cn'),
             ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'),
             ('Accept', '*/*'), 
             ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
             ('Connection', 'keep-alive'),
             ('Referer', 'http://video.sina.com.cn/news/')]   

ctable=dbconfig.tableName['sina']
             
def getVideoByUrl(url):
#     http://dp.sina.cn/dpool/video/pad/play.php?url=http://video.sina.com.cn/p/news/c/v/2014-09-03/214064108827.html
    ipad_url=r'http://dp.sina.cn/dpool/video/pad/play.php?url='
#     r_url=ipad_url+urllib.quote(url)
    r_url=ipad_url+url
#     print r_url
    content=getHtml(r_url)
    if content:
        url=r1(r'<source.*?src="(.*?)"',content)
        return url

# def getVideoByVid(vid):
#     rows=table.getUrlByVid(ctable, vid)
#     if rows!=-1 and len(rows)>0:
#         url=rows[0][0]
#         print url
#         return getVideoByUrl(url)
#     else:
#         return None
    
def getVideoByVid(vid):
#     http://v.iask.com/v_play_ipad.php?vid=135720066&tags=newsList_web
    ipad_url=r'http://v.iask.com/v_play_ipad.php?vid='
    return ipad_url+vid
       
def main():
    rows=table.getTopUrls(ctable, 10)
    count=0
    for item in rows:
        count+=1
        print item[0],item[1]
        print count,'.',getVideoByUrl(item[0])   
        print getVideoByVid(item[1])
        
if __name__=='__main__':  
    main()
#     print getVideoByVid(r'135565908')
    
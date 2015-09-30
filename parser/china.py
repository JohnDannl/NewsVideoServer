#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-1

@author: JohnDannl
'''
import sys
sys.path.append(r"..")
sys.path.append(r"../database")
from common import getHtml,r1,getHtmlwithKu6Cookie
from database import table
from database import dbconfig
import logging
import json

import xml.etree.ElementTree as ET

ctable=dbconfig.tableName[5]
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
        # video
        videoUrl=r1(r"<video.*?src='(.*?)'",content)
        if not videoUrl:
            sourceWeb=r1(r'src="(.*?)" data-vid',content)
            dataVid=r1(r'data-vid="(.*?)"',content)
            if 'ku6' in sourceWeb and dataVid:
                videoUrl=getKu6VideoByVid(dataVid)         
    return videoUrl

def getKu6VideoByVid(vid):
#     url is like:http://v.ku6.com/fetchVideo4Player/1006yPam-HwD0Azn_tkp7A...html
    url=r'http://v.ku6.com/fetchVideo4Player/'+vid+r'.html'
    content =getHtmlwithKu6Cookie(url)
    if content:
        try:
            info=json.loads(content, encoding='utf-8')
            if info.has_key('data'):
                fUrl=info['data']['f'].split(r',')
                return fUrl
        except:
            logging.error('Video parse error')
    return None

def getVideoByVid(vid):
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        print url
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
#     print getVideoByVid(r'news2245');
#     print getVideoByUrl(r'http://www.chinanews.com/shipin/ku6/paike/2014/09-26/news2246.shtml')
#     print getKu6VideoByVid(r'1006yPam-HwD0Azn_tkp7A..')
#     print getVideoByUrl(r'http://www.chinanews.com/shipin/ku6/paike/2014/09-25/news2245.shtml')
    
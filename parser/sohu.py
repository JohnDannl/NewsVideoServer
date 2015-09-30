#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-2

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
from common import getHtml,r1
from database import table
from database import dbconfig
import json
import logging

import xml.etree.ElementTree as ET

ctable=dbconfig.tableName[1]

def getPram(streamType_id):
    url = "http://hot.vrs.sohu.com/vrs_flash.action?vid=" + str(streamType_id)
    jsonContent = json.loads(getHtml(url))
    allot = jsonContent['allot']
    prot = jsonContent['prot']
    clipsURL = jsonContent['data']["clipsURL"]
    su = jsonContent['data']["su"]
    return allot, prot, clipsURL, su

def getKey(allot_url):
    content = getHtml(allot_url)
    listTmp = content.split('|')
    prefix = listTmp[0]
    key = listTmp[3]
    return prefix, key
             
def getVideoByUrl(url):
#     url=r'http://tv.sohu.com/20140904/n404054190.shtml'
    html = getHtml(url)
    if not html:
        return
    vid = r1(r'share.vrs.sohu.com/(.*?)/',html)
    streamTypes = ["norVid", "highVid", "superVid", "oriVid"]
    streamType_url = "http://hot.vrs.sohu.com/vrs_flash.action?vid=" + vid
    content=getHtml(streamType_url)
    if not content:
        return
    jsonContent = json.loads(content)['data']
    videos=[]
    for streamType in streamTypes:
#         print streamType
        streamType_id = jsonContent[streamType]
        try:
            allot, prot, clipsURL, su = getPram(streamType_id)
            if(len(clipsURL)!=len(su)):
                continue
            else:
                video=[]
                for i in range(len(clipsURL)):
                    allot_url = "http://%s/?prot=%s&file=%s&new=%s"%(allot, prot, clipsURL[i], su[i])
                    prefix, key = getKey(allot_url)
                    realUrl = "%s%s?key=%s"%(prefix[0:-1], su[i], key)
#                     print realUrl
                    video.append(realUrl)
                if video:
                    videos.append(video)
        except:
            pass   
    if len(videos)>0:
        return videos[0]             
    return videos

def getVideoByVid(vid):
    streamTypes = ["norVid", "highVid", "superVid", "oriVid"]
    streamType_url = "http://hot.vrs.sohu.com/vrs_flash.action?vid=" + vid
    content=getHtml(streamType_url)
    if not content:
        return
    jsonContent = json.loads(content)['data']
    videos=[]
    for streamType in streamTypes:
#         print streamType
        streamType_id = jsonContent[streamType]
        try:
            allot, prot, clipsURL, su = getPram(streamType_id)
            if(len(clipsURL)!=len(su)):
                continue
            else:
                video=[]
                for i in range(len(clipsURL)):
                    allot_url = "http://%s/?prot=%s&file=%s&new=%s"%(allot, prot, clipsURL[i], su[i])
                    prefix, key = getKey(allot_url)
                    realUrl = "%s%s?key=%s"%(prefix[0:-1], su[i], key)
#                     print realUrl
                    video.append(realUrl)
                if video:
                    videos.append(video)
        except:
            pass  
    if len(videos)>0:
        return videos[0]              
    return videos
       
def main():
    rows=table.getTopUrls(ctable, 10)
    count=0
    for item in rows:
        count+=1
        print item[0],item[1]
        print count,'.',getVideoByUrl(item[0])   
        
if __name__=='__main__':  
    main()
#     print getVideoByVid(r'1977998')
#     url=r'http://tv.sohu.com/20121109/n357176854.shtml'
#     video=getVideoByUrl(url)
#     for f_url in video:
#         print f_url
    
#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2014-9-2

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../parser')
sys.path.append(r'../database')
import sina,sohu,v1,ifeng,kankan,china,qq
from database import tablemerge,tablerequest
from database.dbconfig import mergetable,requesttable
import timeformat
import logging

parser_call={r'sina':sina,r'sohu':sohu,r'v1':v1,r'ifeng':ifeng,
             r'kankan':kankan,r'china':china,r'qq':qq}
click_mod={'auto':'auto','click':'click','related':'related','search':'search'}

class VideoInfo(object):
    def __init__(self,urls):
        self.urls=urls
     
def getRecords(web,vid,userid,userip,mode):
    trackUser(web,vid,userid,userip,mode)
    records=getVideoInfo(web,vid)
    if not records:
        # if records is none,parse twice in case network crash
        records= getVideoInfo(web,vid)
        if not records:
            # if records is none,parse triple in case network crash
            records=getVideoInfo(web,vid)
            if not records:
                records=[]
    return records
 
def getVideoInfo(web,vid):
    if parser_call.has_key(web):
        resp=parser_call[web]
        urls=resp.getVideoByVid(vid)
        if urls:
#         return should be this format:videoInfos:[videoInfo:[video clips],],if urls is not none,
            if not isinstance(urls,list):
                return [VideoInfo([urls,]),]
            else:
                return [VideoInfo(urls),]
    return None

def trackUser(web,vid,userid,userip,mode):
    # web,vid,vtype,mvid,mtype,userid,userip,requesttime,click
    try:
        if mode in click_mod.values() and mode!=click_mod['auto']:
            tablemerge.increaseClick(web, vid)
        rows=tablemerge.getRecordsByWebVid(mergetable, web, vid)
        if rows !=-1 and len(rows)>0:
            title,vtype,mvid,mtype=rows[0]
            requesttime=timeformat.getTimeStamp()
            data=(web,vid,title,vtype,mvid,mtype,userid,userip,requesttime,mode)
            tablerequest.InsertItem(requesttable, data)
    except:
        logging.error('trackUser database visit error')
        
if __name__=='__main__':
#     mode='search'
#     print mode in click_mod.values() and mode!=click_mod['auto']
    records=getRecords(r'sina',r'135565908')
    for item in records:
        print item.urls    
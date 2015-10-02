#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-2

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append(r'../parser')
sys.path.append(r'../related')

import database.tablemerge as tablemerge
from database.dbconfig import mergetable
from w2v4related import w2vclient
# from related import related
from search import search
import time

merge_en=['newest','hot','world','domestic','society','finance','military','science','entertain','sport','ipai','other']
merge_cn=['最新','最热','国际','国内','社会','财经','军事','科教','娱乐','体育','爱拍','其他']
mtype_map={'newest':'最新','hot':'最热','world':'国际','domestic':'国内','society':'社会','finance':'财经','military':'军事','science':'科教',
           'entertain':'娱乐','sport':'体育','ipai':'爱拍','other':'其他'}
type_new=merge_cn[0]
type_hot=merge_cn[1]
ctable=mergetable

class NewsInfo(object):
    def __init__(self,vid,title,url,thumb,brief,source,loadtime,duration,website,mvid,mtype,click):
        self.vid=vid
        self.title=title
        self.url=url
        self.thumb=thumb
        self.brief=brief    #jinja2.escape(brief)#.replace(r'&nbsp','')
        self.source=source
        self.loadtime=loadtime   
        self.duration=duration     
        self.web=website
        self.mvid=mvid
        self.mtype=mtype
        self.click=click
        
def getTopRecords(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
    vnInfos=[]     
    if mtype not in merge_cn:  
        return vnInfos 
    if mtype == type_new:
        records=tablemerge.getTopRecords(ctable, topnum)
    elif mtype == type_hot:
        records=tablemerge.getTopClickRecords(ctable, topnum)
    else:        
        records=tablemerge.getTopRecords(ctable, topnum, mtype)
    if records!=-1 and len(records)>0:
        for item in records:
        #0id,1webid,2vid,3title,4url,5thumb,6summary,7keywords,8newsid,9vtype,10source,
        #11related,12loadtime,13duration,14web,15mvid,16mtype,17click
        #2vid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
            vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
                                    item[12],item[13],item[14],item[15],item[16],item[17]))
    return vnInfos

def getRefreshRecords(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
    vnInfos=[] 
    if mtype not in merge_cn:
        return vnInfos
    if mtype == type_new:        
        records=tablemerge.getBottomETBVRecords(ctable, loadtime,mvid,topnum)
    elif mtype == type_hot:
#         records=tablemerge.getBottomECBVRecords(ctable, click, mvid, topnum)
        records=[]
    else:        
        records=tablemerge.getBottomETBVRecords(ctable, loadtime,mvid,topnum,mtype)
    if records!=-1 and len(records)>0:
        for item in records:
        #0id,1webid,2vid,3title,4url,5thumb,6summary,7keywords,8newsid,9vtype,10source,
        #11related,12loadtime,13duration,14web,15mvid,16mtype,17click
        #2vid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
            vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
                                    item[12],item[13],item[14],item[15],item[16],item[17]))
    if len(vnInfos)<int(topnum):
        if mtype == type_new:
            records=tablemerge.getBottomBTRecords(ctable, loadtime,topnum-len(vnInfos))
        elif mtype == type_hot:
            records=[]
        else:            
            records=tablemerge.getBottomBTRecords(ctable, loadtime,topnum-len(vnInfos),mtype)
        if records!=-1 and len(records)>0:
            for item in records:
                vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
                                    item[12],item[13],item[14],item[15],item[16],item[17]))
    return vnInfos

def getMoreRecords(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
    vnInfos=[]         
    if mtype not in merge_cn:
        return vnInfos
    if mtype == type_new:
        records=tablemerge.getTopETSVRecords(ctable, loadtime,mvid,topnum)
    elif mtype == type_hot:
        records=tablemerge.getTopECSVRecords(ctable, click, mvid, topnum)
    else:        
        records=tablemerge.getTopETSVRecords(ctable, loadtime,mvid,topnum,mtype)
    if records!=-1 and len(records)>0:
        for item in records:
        #0id,1webid,2vid,3title,4url,5thumb,6summary,7keywords,8newsid,9vtype,10source,
        #11related,12loadtime,13duration,14web,15mvid,16mtype,17click
        #2vid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
            vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
                                    item[12],item[13],item[14],item[15],item[16],item[17]))
    if len(vnInfos)<int(topnum):
        if mtype == type_new:
            records=tablemerge.getTopSTRecords(ctable, loadtime,topnum-len(vnInfos))
        elif mtype ==type_hot:
            records=tablemerge.getTopSCRecords(ctable, click, topnum-len(vnInfos))
        else:
            records=tablemerge.getTopSTRecords(ctable, loadtime,topnum-len(vnInfos),mtype)
        if records!=-1 and len(records)>0:
            for item in records:
                vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
                                    item[12],item[13],item[14],item[15],item[16],item[17]))
    return vnInfos

# def getWordRelated(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
#     vnInfos=[] 
#     rows=tablemerge.getRecordsByMVid(ctable,mvid)
#     if rows==-1 or len(rows)<1:
#         return vnInfos
#     title=rows[0][0]   
#     records=related.getRelatedNewsList(title, 30,None,topnum+1)  # topnum+1 to exclude the news itself
#     if records!=None and len(records)>0:
#         for item in records:
#         #0id,1webid,2vid,3title,4url,5thumb,6summary,7keywords,8newsid,9vtype,10source,
#         #11related,12loadtime,13duration,14web,15mvid,16mtype,17click
#         #2mvid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
#             # pass the same news
#             if item[15]==mvid:
#                 continue
#             vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
#                                     time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item[12])),
#                                     item[13],item[14],item[15],item[16],item[17]))
#     if len(vnInfos)>topnum:
#         return vnInfos[0:topnum]
#     return vnInfos

def getRelatedRecords(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
    vnInfos=getW2vRelated(web,mvid,loadtime,topnum,mtype,click)
    if not vnInfos:  # if esa server is broken,then use searched related
        vnInfos=getSearchedRelated(mvid,loadtime,topnum,mtype,click)  
        print 'using searched related'  
    return vnInfos

def getW2vRelated(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
    vnInfos=[] 
    rows=tablemerge.getTitleByMVid(ctable,mvid)
    if rows==-1 or len(rows)<1:
        return vnInfos
    title=rows[0][0]  
    records=w2vclient.getRelatedRecords2(title)
    if records!=None and len(records)>0:
        for item in records:
        #0id,1webid,2vid,3title,4url,5thumb,6summary,7keywords,8newsid,9vtype,10source,
        #11related,12loadtime,13duration,14web,15mvid,16mtype,17click
        #2vid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
            # pass the same news
            if item[15]==mvid:
                continue
            vnInfos.append(NewsInfo(item[2],item[3],item[4],item[5],item[6],item[10],
                                    item[12],item[13],item[14],item[15],item[16],item[17]))
    if len(vnInfos)>topnum:
        return vnInfos[0:topnum]    
    return vnInfos

def getSearchedRelated(web,mvid,loadtime='0',topnum=10,mtype=None,click=0):
    vnInfos=[] 
    rows=tablemerge.getTitleByMVid(ctable,mvid)
    if rows==-1 or len(rows)<1:
        return vnInfos
    title=rows[0][0]      
#     print title  
    records=search.searchWithLimit(title,limit=topnum+1)
    if records!=None and len(records)>0:
        for item in records:
            if item['mvid']==mvid:
                continue
            #2vid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
            vnInfos.append(NewsInfo(item['vid'],item['title'],item['url'],item['thumb'],item['summary'],item['source'],
                                    item['loadtime'],item['duration'],item['web'],item['mvid'],item['mtype'],item['click']))
    if len(vnInfos)>topnum:
        return vnInfos[0:topnum]
    return vnInfos

def getSearchedPage(keywords,pagenum=1):
    vnInfos=[]     
#     print keywords
    records=search.searchWithPage(keywords,page=pagenum)
    if records!=None and len(records)>0:
        for item in records:
            #2vid,3title,4url,5thumb,6brief,10source,12loadtime,13duration,14web,15mvid,16mtype,17click
            vnInfos.append(NewsInfo(item['vid'],item['title'],item['url'],item['thumb'],item['summary'],item['source'],
                                    item['loadtime'],item['duration'],item['web'],item['mvid'],item['mtype'],item['click']))
    return vnInfos
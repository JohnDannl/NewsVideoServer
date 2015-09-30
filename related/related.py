#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-18

@author: JohnDannl
'''
import sys
sys.path.append(r'../')
sys.path.append(r'../database')
from database import tablemerge,dbconfig
import lcsseq
import lcsstr
import med
import mmc
import hownet
import re
import logging
from operator import itemgetter, attrgetter
import time

class NewsTitle():
    def __init__(self,title,mvid):
        self.title=title
        self.mvid=mvid
        self.similarity=0
    def getTitle(self):
        return self.title
    def getMvid(self):
        return self.mvid
    def getSim(self):
        return self.similarity
    def setSim(self,sim):
        self.similarity=sim
        
def getNewsTitleList(startday=30,enday=None):
    if enday==None: 
        all_rows=tablemerge.getTitleByLoadTime(dbconfig.mergetable, startday)
    else:
        all_rows=tablemerge.getTitleByLoadTime(dbconfig.mergetable, startday,enday)
    if all_rows!=-1 and len(all_rows)>0:        
        newsList=[]
        for row in all_rows:
            newsList.append(NewsTitle(row[0],row[1]))
        return newsList  
     
def getRelatedNewsTitleList(title,startday=30,enday=None,topnum=10):
    time0=time.time()
    newsList=getNewsTitleList(startday,enday)
    time1=time.time()
    print 'time0:',time1-time0
    if newsList==None or len(newsList)<=0:
        msg='newsTitleList is none,maybe the startday is too small.'
        print msg
#         logging.info(msg)
        return
    else:
        msg= 'newsTitlelist has records:%s'%len(newsList)
#         logging.info(msg)
        print msg
    for news in newsList:
        news.setSim(getSimilarity(title,news.getTitle())) 
    time2=time.time()
    print 'time1:',time2-time1
    # reverse:big-->small
    new_newsList=sorted(newsList,key=lambda newsTitle: newsTitle.getSim(),reverse=True) 
    time3=time.time()
    print 'time2:',time3-time2
    print 'Total time:',time3-time0
#     new_newsList=sorted(newsList,key=attrgetter('similarity'))
    # Default is ascending sorted,get the most similar 10 items
    # If is not topnum items enough ,return all
    if topnum>0:        
#         return new_newsList[-topnum:]
        return new_newsList[0:topnum]
     
def getRelatedNewsList(title,startday=30,enday=None,topnum=10):   
    # According to title,find out the related news @param startday: from now,
    # @param topnum: top related number 
    #
    relatedTitleList=getRelatedNewsTitleList(title,startday,enday,topnum) 
    if relatedTitleList==None or len(relatedTitleList)<1:
        return
    relatedNewsList=[]
    for newsTitle in relatedTitleList:
        rows=tablemerge.getRecordsByMVid(dbconfig.mergetable,newsTitle.getMvid())
        if rows !=-1 and len(rows)>0:
            relatedNewsList.append(rows[0])
    return relatedNewsList

def getSimilarity(source,target):
    # replace all noisy number
    source=re.sub(r'\d','',source.decode('utf-8'))
    target=re.sub(r'\d','',target.decode('utf-8'))
#     return lcsseq.getSentenceSim(source, target)
#     return lcsstr.getSentenceSim(source, target)
#     return med.getSentenceSim(source, target)
#     return hownet.getSentenceSim(source, target)
    return mmc.getSentenceSim(source, target)
              
if __name__=='__main__':
    rows=tablemerge.getTopRecords(dbconfig.mergetable)
    if rows!=-1 and len(rows)>0:
        record=rows[1]
        title,web,vid=record[2],record[13],record[1]
        print title,web,vid
        relatedList=getRelatedNewsTitleList(title,10)
        if relatedList==None:
            print 'relatedList is None'
        else:
            for related in relatedList:
                print related.getSim(),related.getTitle()
            
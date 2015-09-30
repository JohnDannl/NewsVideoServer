#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-8

@author: JohnDannl
'''
import logging
import time
import multiprocessing
import urllib2
import sys
sys.path.append('..')
sys.path.append('../database')
from database import table

def getHtml(url): 
    r=urllib2.Request(url)
    r.add_header("Accept-Language","zh-cn,en-us;q=0.7,en;q=0.3")
    r.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0")
    try:
        content=urllib2.urlopen(r, timeout=30).read()
#         time.sleep(0.3)
#         print time.asctime(),'-->',url
        return content
    except:
        return None
    
def main_map(urls):
    oldtime=time.time();
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    results=pool.map(getHtml, urls)    
    pool.close()
    pool.join()     
    for result in results:
        try:
            print result
        except:
            logging.error('encoding not supported')                    
    print 'has crawled %s records time cost: %s (seconds)' % (len(results), time.time()-oldtime)

def main_map_async():
    infoList=[] 
    oldtime=time.time();
    #pool=multiprocessing.Pool(multiprocessing.cpu_count()) 
    pool=multiprocessing.Pool() # if none,will use default :cpu_count() processings
    results=pool.map_async(getHtml, range(0,10))    
    pool.close()
    pool.join()     
    result_list=results.get()
    for result in result_list:
        infoList+=result
    for info in infoList:
        try:          
            print info['title']
        except:
            logging.error('encoding not supported')
    print 'has crawled %s records time cost: %s (seconds)' % (len(infoList), time.time()-oldtime)
    
def main_apply(urls):
    infoList=[] 
    oldtime=time.time();
    pool=multiprocessing.Pool() # will use default :cpu_count() processings
    for url in urls:
        infoList.append(pool.apply(getHtml, (url,)))    
    pool.close()
    pool.join()    
#     for info in infoList:
#         try:          
#             print info
#         except:
#             logging.error('encoding not supported')
    print 'has crawled %s records time cost: %s (seconds)' % (len(infoList), time.time()-oldtime)

def main_apply_async(urls):
    oldtime=time.time();
    pool=multiprocessing.Pool() # if none will use default :cpu_count() processings
    results=[]
    for url in urls:
        results.append(pool.apply_async(getHtml, (url,)))   
    pool.close()
    pool.join()    
#     for result in results:
#         try:
#             print result
#         except:
#             logging.error('encoding not supported')    
    print 'has crawled %s records time cost: %s (seconds)' % (len(results), time.time()-oldtime)
    
def getUrls(web,topnum=10): 
    urls=[]
    rows=table.getTopUrls(web, topnum)
    for item in rows:
#         url=r'http://222.195.78.187:8889/video/a?web=%s&vid=%s'% (web,item[1])
        url=r'http://localhost:8889/video/a?web=%s&vid=%s'% (web,item[1])
        urls.append(url)
    return urls

if __name__ == '__main__':    
    multiprocessing.freeze_support()   
    urls=[r'http://localhost:8889/video/a?web=kankan&vid=0015944750',]
    urls=getUrls('sohu',10)
#     main_apply(urls)
#     main_apply_async(urls)
    main_map(urls)
#     main_map_async()
#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2015-1-22

@author: JohnDannl
'''
from table import dbconn as dbconn
from dbconfig import tableName as tableName
import time

import dbconfig

def InsertItem(tablename, data):    
    if ChkExistRow(tablename, data[0]):
        return
    query = """INSERT INTO """ + tablename + """(
               mvid,title,vec,loadtime)
               values(%s, %s, %s, %s)"""
    dbconn.Insert(query, data)
    
def InsertItemFast(tablename, data):    
    # if you make sure the record is new ,then do no existence check 
    query = """INSERT INTO """ + tablename + """(
               mvid,title,vec,loadtime)
               values(%s, %s, %s, %s)"""
    dbconn.Insert(query, data)
    
def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               mvid,title,vec,loadtime)
               values(%s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['mvid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             mvid,title,vec,loadtime) 
             values(%(mvid)s, %(title)s,%(vec)s,%(loadtime)s)"""
    dbconn.Insert(query, data)
    return 0

def getAllCount(tablename):
    query="select count(*) from "+tablename
    count=dbconn.Select(query,())[0][0]
    return count

def getAllRecords(tablename):
    query = "SELECT * FROM " + tablename
    rows = dbconn.Select(query, ())
    return rows

def getRecordsByLoadTime(tablename, starttime, endtime):
    '''@param tablename: table name
    @param starttime: the start time of query in format:%Y-%m-%d %H:%M:%S
    @param endtime: the end time of query in format:%Y-%m-%d %H:%M:%S
    '''
#     starttime = time.strftime("%Y-%m-%d %H:%M:%S", starttime)
#     endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtime)
    query = "SELECT * FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getTitleByLoadTime(tablename,startday=30,enday=None):
    # return [(mvid,title),] 
    sttuple=time.localtime(time.time()-86400.0*startday)
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", sttuple)
    if enday==None:
        endtime=time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        endtuple=time.localtime(time.time()-86400.0*enday)
        endtime=time.strftime("%Y-%m-%d %H:%M:%S", endtuple)
    query = "SELECT mvid,title FROM " + tablename + """ WHERE loadtime >= %s AND loadtime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getLatestTitle(tablename,topnum=10000):
    # return [(mvid,title),] 
    query = "SELECT mvid,title FROM " + tablename + """ order by loadtime desc limit %s""" 
    rows = dbconn.Select(query, (topnum,))   
    return rows

def getRecordsByMVid(tablename,mvid):
    # return the user clicked video info,should be only one if no accident
    # the return column:id,mvid,title,url,thumb,summary,keywords,newsid,vtype,source,
    # related,loadtime,duration,web,mvid,mtype,click
    query = "SELECT * FROM " + tablename + """ WHERE mvid = %s""" 
    rows = dbconn.Select(query, (mvid,))   
    return rows

def getTopRecords(tablename,topnum=10):
    # return [(mvid,title),] 
    query = "SELECT * FROM " + tablename + """ order by loadtime desc, mvid desc limit %s""" 
    rows = dbconn.Select(query, (topnum,))   
    return rows

def ChkExistRow(tablename, mvid):
    query = "SELECT COUNT(*) FROM " + tablename + " WHERE mvid = %s"
    rows = dbconn.Select(query, (mvid,))
    if rows!=-1 and len(rows)> 0:
        if rows[0][0]>0:
            return True
    return False

def CreateNewsTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key,               
               mvid text,
               title text,
               vec text,          
               loadtime timestamp)"""
    dbconn.CreateTable(query, tablename)

if __name__ == "__main__":    
    CreateNewsTable(dbconfig.esatable)     

    rows=getTopRecords(dbconfig.esatable,10)  
    if rows !=-1:
        for item in rows:
            print item[1],item[0]  
 
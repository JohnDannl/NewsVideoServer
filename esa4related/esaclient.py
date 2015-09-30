#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2015-1-23

@author: JohnDannl
'''
import socket
from config import host,port
from database import tablemerge,dbconfig
import time

def _getRelatedMvids(title):    
    rec_buffer=[]    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.sendall(title)
        while True:
            data = s.recv(1024)
            if not data:
                break
            rec_buffer.append(data)
        s.close()
    except:
        s.close()
        print 'client socket error'
    #print 'Received', repr(''.join(rec_buffer))
    return ''.join(rec_buffer).split(',')

def getRelatedRecords(title):
    # default return 10 most related news if has enough
    mvids=_getRelatedMvids(title)
    records=[]
    for mvid in mvids:
        rows=tablemerge.getRecordsByMVid(dbconfig.mergetable,mvid)
        if rows !=-1 and len(rows)>0:
            records.append(rows[0])
    return records

def getRelatedRecords2(title):  
    # This method is much faster than the above one
    # default return 10 most related news if has enough
    mvids=_getRelatedMvids(title)
    mvids =['\''+mvid+'\'' for mvid in mvids]
    mvids='('+','.join(mvids)+')'
    rows=tablemerge.getRecordsByMVids(dbconfig.mergetable,mvids)  
    if rows==-1:  
        rows=[]
    return rows

if __name__=='__main__':
    oldtime=time.time()
    title='中科大'
    records=getRelatedRecords2(title)
    for record in records:
        print record[2]
    print 'time cost:%s'%(str(time.time()-oldtime))
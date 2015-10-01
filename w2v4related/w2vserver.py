#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-1-23

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
import socket
from config import host,port,index_file,ids_file
import os
import threading
import time
from database import tablew2v,tablemerge,dbconfig
from w2v4related import doc2vec,vec2index

index=None
mids=[]
if os.path.exists(index_file):    
    index = similarities.Similarity.load(index_file)
    for line in open(ids_file):
        mids.append(line.strip())
        
def addNewCorpus():  
    rows=tablemerge.getTitleBiggerId(dbconfig.mergetable, tablew2v.getMaxMid(dbconfig.w2vtable))
    if rows ==-1 or not rows:
        print 'no new corpus added,update ends'
        return False
    for row in rows:
        # id,title
        if row[0]%1000==0:
            logging.info('process document:#%s'%row[0])
        if tablew2v.ChkExistRow(dbconfig.w2vtable, row[0]):
            continue
        data=[]
        data.append(row[0])
        data.append(doc2vec.get_vec_str(row[1]))
        tablew2v.InsertItemFast(dbconfig.w2vtable, data)
    return True
  
def reindex():    
    vec2index.index_latest()

def reloadmodel(): 
    if not os.path.exists(index_file):
        return 
    global index,mids
    index=None     
    index = similarities.Similarity.load(index_file) 
    mids=[]
    for line in open(ids_file):
        mids.append(line.strip())   
           
def update():
    while True:
        oldtime=time.time()
        global index
        if addNewCorpus() or not index: # add new corpus or index does not exist
            reindex()
            reloadmodel()
        print "reindex at time:",time.asctime(),'time cost (s):',str(time.time()-oldtime)
        time.sleep(7200)
    
def server_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    while True:
        sock, addr = s.accept()
        print 'Connected by', addr
        threading.Thread(target=process_query, args=(sock,addr)).start()

def process_query(sock,addr):
    oldtime=time.time()
    data = sock.recv(4096)
    #print data
    global index,mids
    if not index:
        print 'index is none'
        sock.sendall('')
        sock.close()
        return
    vec=doc2vec.get_vec(data)
    sims=index[vec]
    sim_midstr=','.join([mids[item[0]] for item in sims])
    sock.sendall(sim_midstr)
    sock.close()
    print 'cost time:',time.time()-oldtime

if __name__=='__main__':   
    threading.Thread(target=update).start()
    server_listen()
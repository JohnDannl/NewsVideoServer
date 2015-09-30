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
from config import host,port,id_file,index_file,mvids_file
import os
import threading
import time
from database import tableesa,tablemerge,dbconfig
from esa4related import doc2vec,vec2index

index=None
mvids=[]
if os.path.exists(index_file):    
    index = similarities.Similarity.load(index_file)
    for line in open(mvids_file):
        mvids.append(line.strip())
        
def get_last_id():
    if not os.path.exists(id_file):
        print 'Path not exits:',id_file   
        return 0     
    fin=open(id_file)
    last_id= int(fin.readline().strip())
    fin.close()
    return last_id

def dump_id(id_num):
    fout=open(id_file,'w')
    fout.write(str(id_num))
    fout.close()

def addNewCorpus():  
    rows=tablemerge.getRecordsBiggerId(dbconfig.mergetable, get_last_id())
    if rows ==-1 or not rows:
        print 'no new corpus added,update ends'
        return False
    for row in rows:
        # id,mvid,title,loadtime
        if row[0]%1000==0:
            logging.info('process document:#%s'%row[0])
        if tableesa.ChkExistRow(dbconfig.esatable, row[1]):
            continue
        data=[]
        data.append(row[1])
        data.append(row[2])
        data.append(doc2vec.get_vec_str(row[2]))
        data.append(row[3])
        tableesa.InsertItemFast(dbconfig.esatable, data)
    dump_id(rows[len(rows)-1][0])
    return True
  
def reindex():    
    vec2index.index_latest()

def reloadmodel(): 
    if not os.path.exists(index_file):
        return 
    global index,mvids
    index=None     
    index = similarities.Similarity.load(index_file) 
    mvids=[]
    for line in open(mvids_file):
        mvids.append(line.strip())   
           
def update():
    while True:
        oldtime=time.time()
        global index
        if addNewCorpus() or not index: # add new corpus or index does not exist
            reindex()
            reloadmodel()
        print "reindex at time:",time.asctime(),'time cost (s):',str(time.time()-oldtime)
        time.sleep(120)
    
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
    global index,mvids
    if not index:
        print 'index is none'
        sock.sendall('')
        sock.close()
        return
    vec=doc2vec.get_vec(data.decode('utf-8'))
    sims=index[vec]
    sim_mvidstr=','.join([mvids[item[0]] for item in sims])
    sock.sendall(sim_mvidstr)
    sock.close()
    print 'cost time:',time.time()-oldtime

if __name__=='__main__':   
    threading.Thread(target=update).start()
    server_listen()
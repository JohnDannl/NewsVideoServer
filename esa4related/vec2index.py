#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-1-23

@author: JohnDannl
'''
from database import tableesa,dbconfig
import doc2vec
from config import dict_file,news_mm_file,mvids_file,index_prefix,index_file
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities

class MyCorpus(object):
    def __init__(self,topnum):
        self.__topnum=topnum
        self.mvids=[]
    def __iter__(self):
        rows=tableesa.getTopRecords(dbconfig.esatable, self.__topnum)
        for row in rows:    # id,mvid,title,vec,loadtime
            self.mvids.append(row[1])
            yield doc2vec.parse_vec_str(row[3])
            
    def save_mvids(self):
        fout=open(mvids_file,'w')
        fout.write('\n'.join(self.mvids))
        fout.close()
            
def index_latest(topnum=20000):
    vec_corpus=MyCorpus(topnum)
    corpora.MmCorpus.serialize(news_mm_file,vec_corpus ) # store to disk, for later use
    vec_corpus.save_mvids()
    dictionary = corpora.Dictionary.load(dict_file)
    corpus=corpora.MmCorpus(news_mm_file) # now corpus has random access
    index=similarities.Similarity(index_prefix,corpus,num_features=dictionary.num_docs,num_best=10)
    index.save(index_file)
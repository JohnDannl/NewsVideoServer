#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015-1-23

@author: JohnDannl
'''

import jieba
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dict_file,tfidf_md_file,word2docp_mm_file

dictionary = corpora.Dictionary.load(dict_file)
tfidf =models.TfidfModel.load(tfidf_md_file)
word2doc_mat=corpora.MmCorpus(word2docp_mm_file)  

def _get_concept_vec(wordList,prune_at=0.2):
    dic_tfidf={}
    vec_bow = dictionary.doc2bow(wordList)
    if not vec_bow:
        return []
    vec_tfidf=tfidf[vec_bow]
#     for wordid,tfidf_v in vec_bow:
    for wordid,tfidf_v in vec_tfidf:    
        for docid,weight in word2doc_mat[wordid]:
            value=dic_tfidf.get(docid,0)
            value+=tfidf_v*weight
            dic_tfidf[docid]=value
    #print 'tfidf:',vec_tfidf
    #print 'bow:',vec_bow
    if not dic_tfidf.values():        
        print 'Document not recruited:',' '.join(wordList)
    limit_low=prune_at*max(dic_tfidf.iteritems(),key=lambda i:i[1])[1]
    concept_vec=[]
    for item in dic_tfidf.iteritems():
        if item[1]>=limit_low:
            concept_vec.append(item)
    return sorted(concept_vec)    

def get_vec(doc):
    words=jieba.cut(doc.lower())
    return _get_concept_vec(words)

def get_vec_str(doc):
    words=jieba.cut(doc.lower())
    items=[]
    for concept,weight in _get_concept_vec(words):
        items.append(str(concept)+' '+str(weight))
    return ','.join(items)

def parse_vec_str(vec_str):    
    items=vec_str.split(',')
    vec=[]    
    try:
        for item in items:
            concept,weight=item.split()
            vec.append((int(concept),float(weight)))
    except:
        print 'empty vec_str or bad format'
    return vec

if __name__=='__main__':
    print get_vec('a')
    a=get_vec_str('a')
    aa=parse_vec_str(a)
    print a
    print aa

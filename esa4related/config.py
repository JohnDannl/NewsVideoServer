#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2015-1-23

@author: JohnDannl
'''

####### For esa server ###########
host='localhost'               # Symbolic name meaning all available interfaces
port = 8893              # Arbitrary non-privileged port
id_file=r'e:/tmp/wiki/news/id.log'
######## For esa model ###########
dict_file=r'e:/tmp/wiki/esa/wiki.dic'
tfidf_md_file=r'e:/tmp/wiki/esa/tfidf.md'
word2docp_mm_file=r'e:/tmp/wiki/esa/word2docp.mm'
########## For news data dump #############
mvids_file='e:/tmp/wiki/news/mvids'
news_mm_file='e:/tmp/wiki/news/news.mm'
index_prefix='e:/tmp/wiki/news/index'
index_file='e:/tmp/wiki/news/news.index'
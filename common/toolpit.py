#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-4

@author: JohnDannl
'''
import hashlib

def getMid(web,vid):
    #use web and vid to generate a merge id
    if web and vid:
        return web+vid
    
# def getMid(web,url):
#     #use web and url to generate a merge id
#     if web and url:
#         m1=hashlib.md5(url)
#         return web+m1.hexdigest()

if __name__=='__main__':
    web='qq'
    vid='123456789'
    print getMid(web,vid)
    
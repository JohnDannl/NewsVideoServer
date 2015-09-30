#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
The maximum matched character number
Created on 2014-10-23

@author: JohnDannl
'''
def getMMC(sent1,sent2):
    # return the maximum matched character number of target to source
    sent1=sent1.decode('utf-8')
    sent2=sent2.decode('utf-8')
    source,target='',''
    if len(sent1)>len(sent2):
        source=sent1
        target=sent2
    else:
        source=sent2
        target=sent1
    if len(source)==0 or len(target)==0:
        if len(source)==len(target):
            return 1.0 # both are empty
        return 0 # one of them is empty
    source_map={}
    for schar in source:
        if source_map.has_key(schar):
            source_map.get(schar)[0]+=1
        else:
            source_map[schar]=[1,0]  
    count=0
    for tchar in target:
        if source_map.has_key(tchar):
            nums=source_map.get(tchar)
            nums[1]+=1
            if nums[1]<=nums[0]:
                count+=1
    return count

def getSentenceSim(sent1,sent2):    
    sent1=sent1.decode('utf-8')
    sent2=sent2.decode('utf-8')
    length= len(sent1) if len(sent1)>len(sent2) else len(sent2)
    if length==0:
        return 1.0 
    return getMMC(sent1,sent2)/float(length)

if __name__=='__main__':
    X='下面是中文bug'
    Y='这是的一个bug'
    print getMMC(X,Y),getSentenceSim(X,Y)
    print getMMC('',Y),getSentenceSim('',Y)
    print getMMC('',''),getSentenceSim('','')
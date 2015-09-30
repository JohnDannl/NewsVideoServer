#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Calculate the similarity between two sentences using hownet algorithm proposed by liuqun
    
Created on 2014-10-22

@author: JohnDannl
'''
import py4j # This import is necessary to avoid a Type Error Exception Bug when this module called in another
from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
# If the default port 25335 is occupied,set another port
# gateway = JavaGateway(GatewayClient(port=25335))
sentSim=gateway.entry_point

def getSentenceSim(sent1,sent2):
    sent1=sent1.decode('utf-8')
    sent2=sent2.decode('utf-8')
    return sentSim.getSentenceSim(sent1,sent2)

if __name__=='__main__':
    str1='白日依山尽，'
    str2='黄河入海流。'
    str3='欲穷千里目，'
    str4='更上一层楼。'
    print '1,2:',getSentenceSim(str1,str2)
    print '2,3:',getSentenceSim(str2,str3)
    print '3,4:',getSentenceSim(str3,str4)
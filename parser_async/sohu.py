#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-9-2

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append(r'../common')
from common.common import getHtml,r1
from database import table
from database import dbconfig
import json
import logging
import time,random,re
from urlparse import urlparse

import xml.etree.ElementTree as ET

ctable=dbconfig.tableName['sohu']

def getRealUrlByInfo(info,hqvid):
    host = info['allot']
    tvid = info['tvid']
    urls = []
    data = info['data']
    assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
    for new,clip,ck, in zip(data['su'], data['clipsURL'], data['ck']):
        clipURL = urlparse(clip).path
        urls.append(real_url(host,hqvid,tvid,new,clipURL,ck))
    return urls

def real_url(host,vid,tvid,new,clipURL,ck):
    url = 'http://'+host+'/?prot=9&prod=flash&pt=1&file='+clipURL+'&new='+new +'&key='+ ck+'&vid='+str(vid)+'&uid='+str(int(time.time()*1000))+'&t='+str(random.random())
    return json.loads(getHtml(url))['url']
            
def getVideoByUrl(url):
    if re.match(r'http://share.vrs.sohu.com', url):
        vid = r1('id=(\d+)', url)
    else:
        html = getHtml(url)
        vid = r1(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?', html)
    assert vid

    if re.match(r'http://tv.sohu.com/', url):
        info = json.loads(getHtml('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
        for qtyp in ["oriVid","superVid","highVid" ,"norVid","relativeId"]:
            hqvid = info['data'][qtyp]
            if hqvid != 0 and hqvid != vid :
                info = json.loads(getHtml('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid))
                break
        host = info['allot']
        tvid = info['tvid']
        urls = []
        data = info['data']
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new,clip,ck, in zip(data['su'], data['clipsURL'], data['ck']):
            clipURL = urlparse(clip).path
            urls.append(real_url(host,hqvid,tvid,new,clipURL,ck))
        # assert data['clipsURL'][0].endswith('.mp4')

    else:
        info = json.loads(getHtml('http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % vid))
        host = info['allot']
        tvid = info['tvid']
        urls = []
        data = info['data']
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new,clip,ck, in zip(data['su'], data['clipsURL'], data['ck']):
            clipURL = urlparse(clip).path
            urls.append(real_url(host,vid,tvid,new,clipURL,ck))
    return urls

def getUrlByVid(vid):
    rows=table.getUrlByVid(ctable, vid)
    if rows!=-1 and len(rows)>0:
        url=rows[0][0]
        return url
    
def main():
    rows=table.getTopUrls(ctable, 10)
    count=0
    for item in rows:
        count+=1
        print item[0],item[1]
        print count,'.',getVideoByUrl(item[0]) 
        
if __name__=='__main__':  
    main()
    
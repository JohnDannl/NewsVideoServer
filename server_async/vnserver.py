#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-8-28

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../parser_async')
sys.path.append(r'../database')
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
import tornado.gen
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.web import RequestHandler
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import jinja2
import os
import logging
import time,re
from database.dbconfig import tableName as webs,mergetable as mergetable
from database import table
import newsinfo
import videoinfo
from parser_async import china,ifeng,kankan,qq,sina,sohu,v1
from common.common import r1
import json

define ("port", default=8889, help="run on the given port", type=int)

class TemplateRendering:
    """
    A simple class to hold methods for rendering templates.
    """
    def render_template(self, template_name, **kwargs):
        template_dirs = [r'../templates']
        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings["template_path"]
            )
        env = Environment(loader=FileSystemLoader(template_dirs),autoescape=True)

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(RequestHandler, TemplateRendering):
    """
    RequestHandler already has a `render()` method. I'm writing another
    method `render2()` and keeping the API almost same.
    """
    def render2(self, template_name, **kwargs):
        """
        This is for making some extra context variables available to
        the template
        """
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)

class NewsHandler(BaseHandler):
    """The handler to return the recent news records"""
    xtype_calls={r'top':newsinfo.getTopRecords,
           r'refresh':newsinfo.getRefreshRecords,
           r'more':newsinfo.getMoreRecords,
#            r'related':newsinfo.getRelatedRecords}
           r'related':newsinfo.getSearchedRelated}
    def get(self, call):
#         print call
        topnum = self.get_argument('num', '10')
        website=str(self.get_argument('web','merge'))        
        mvid=str(self.get_argument('mvid', '0'))
        loadtime=str(self.get_argument('loadtime', '0'))
        mtype=str(self.get_argument('mtype', 'newest'))
        click=str(self.get_argument('click', '0'))
        
        records = self.getRecords(call,website,mvid,loadtime,topnum,mtype,click)
        #get thte user's ip addr
        self.set_header('Content-Type', 'application/xml')
        #print self.render_string('template.xml',source=source)
        print self.request.remote_ip
        self.render2('news.xml',records=records)

    def getRecords(self,call,website,mvid,loadtime,topnum,mtype,click):
        records=[]
        if (website =='merge' or website in webs) and mtype in newsinfo.merge_en:
            try:
                # params check
#                 top_num=int(unicode.decode(topnum).encode('utf-8'))
                top_num=int(topnum)
                click_num=int(click)
                mtype_cn=newsinfo.mtype_map.get(mtype)
                if self.xtype_calls.has_key(call):
                    resp=self.xtype_calls.get(call)
                    records=resp(website,mvid,loadtime,top_num,mtype_cn,click_num)
            except:
                logging.info('topnum type error!')
        else:
            logging.info('Request error!')
        if not records:
            records=[]
        return records
#         return [VNInfo('movie1','This is movie1'),VNInfo('movie2','This is movie2')]

class VideoHandler(BaseHandler):
    """The handler to return the news video play-back url"""
    @tornado.gen.coroutine
    def get(self, call):
#         print call
        web=str(self.get_argument('web'))        
        vid= str(self.get_argument('vid'))      
        userid=str(self.get_argument('userid', 'anonymous'))        
        userip=str(self.request.remote_ip)
        mode=str(self.get_argument('mode', videoinfo.click_mod['auto']))
        ############# Deal video address parsing and user tracking #################
        videoinfo.trackUser(web,vid,userid, userip, mode)
        ############# Deal video address parsing and user tracking #################
        urls=None
        html_url=None
        try:
            if web=='china':
                url=china.getUrlByVid(vid) 
                html_url=url
                videoUrl=None
                if url:
                    http_client = tornado.httpclient.AsyncHTTPClient()
                    response = yield http_client.fetch(url) 
                    if response: 
                        content=response.body
                        videoUrl=r1(r"<video.*?src='(.*?)'",content)
                        if not videoUrl:
                            sourceWeb=r1(r'src="(.*?)" data-vid',content)
                            dataVid=r1(r'data-vid="(.*?)"',content)
                            if 'ku6' in sourceWeb and dataVid:
                                url=r'http://v.ku6.com/fetchVideo4Player/'+dataVid+r'.html'
                                resp2=yield http_client.fetch(url)
                                if resp2:
                                    content=resp2.body
                                    videoUrl=china.getKu6VideoUrlByContent(content)
                urls=videoUrl
            elif web=='ifeng':
                url=ifeng.getUrlByVid(vid)
                html_url=url
                url=ifeng.getVInfoUrl(url)
                videoUrl=None
                if url:
                    http_client = tornado.httpclient.AsyncHTTPClient()
                    response = yield http_client.fetch(url) 
                    if response: 
                        content=response.body
                        videoUrl=ifeng.getVideoUrlByContent(content)
                urls=videoUrl
            elif web=='kankan':
                url=kankan.getUrlByVid(vid)
                html_url=url
                videoUrl=None
                if url:
                    http_client = tornado.httpclient.AsyncHTTPClient()
                    response = yield http_client.fetch(url) 
                    if response:
                        content=response.body
                        videoUrl=kankan.getVideoDirectByContent(content)
                        if not videoUrl:
                            part1=r1(r'(/\d{4}-\d{2}-\d{2}/\w*?)\.',url)
                            xml_url=r'http://www.kankanews.com/vxml%s.xml'%part1
                            resp2=yield http_client.fetch(xml_url)
                            if resp2:
                                content=resp2.body
                                videoUrl=kankan.getVideoInfoByContent(content)                   
                urls=videoUrl  
            elif web=='qq':
                url = 'http://vv.video.qq.com/geturl?otype=xml&platform=1&vid=%s&format=2' % vid  
                videoUrl=None
                http_client = tornado.httpclient.AsyncHTTPClient()
                response = yield http_client.fetch(url)
                if response:
                    content=response.body
                    if content:
                        videoUrl=r1(r'<url>(.*?)</url>',content)
                urls=videoUrl             
            elif web=='sina':
                urls=sina.getVideoByVid(vid)
            elif web=='sohu':
                url=sohu.getUrlByVid(vid)
                videoUrl=[] 
                if re.match(r'http://tv.sohu.com/', url):                    
                    json_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid                     
                    http_client = tornado.httpclient.AsyncHTTPClient()
                    response = yield http_client.fetch(json_url) 
                    if response:
                        content=response.body                          
                        try:
                            info=json.loads(content)
                            for qtyp in ["oriVid","superVid","highVid" ,"norVid","relativeId"]:
                                hqvid = info['data'][qtyp]
                                if hqvid != 0 and hqvid != vid :
                                    resp2=yield http_client.fetch('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid)
                                    info = json.loads(resp2.body)
                                    break
                            videoUrl=sohu.getRealUrlByInfo(info, hqvid)
                        except:
                            pass 
                else:
                    json_url='http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % vid
                    http_client = tornado.httpclient.AsyncHTTPClient()
                    response = yield http_client.fetch(json_url) 
                    if response:
                        content=response.body 
                        try:
                            info=json.loads(content)
                            videoUrl=sohu.getRealUrlByInfo(info, vid)
                        except:
                            pass                        
                urls=videoUrl  
            elif web=='v1':
                url=v1.getUrlByVid(vid)  
                html_url=url            
                videoUrl=None
                if url:
                    http_client = tornado.httpclient.AsyncHTTPClient()
                    response = yield http_client.fetch(url) 
                    if response:
                        content=response.body
                        if content:
                            videoUrl=r1(r'<param.*?videoUrl=(.*?)"',content)
                urls=videoUrl
        except:
            logging.info('video parse error:%s'%html_url)  
                    
        ############# Deal video address parsing and user tracking #################        
        records = self.getRecords(urls)
        ############# Deal video address parsing and user tracking #################
        #get thte user's ip addr
        self.set_header('Content-Type', 'application/xml')
        #print self.render_string('template.xml',source=source)
        print self.request.remote_ip
        self.render2('video.xml',records=records)

    def getRecords(self,urls):        
        records=videoinfo.toVideoInfos(urls)
        if records:
            return records
        else:       
            return [] 

class SearchHandler(BaseHandler):
    """The handler to return the recent news records"""
    def get(self, call):
#         print call
        keywords=str(self.get_argument('keywords'))        
        pagenum = str(self.get_argument('page', '1'))  
        records = self.getRecords(keywords,pagenum)
        #get thte user's ip addr
        self.set_header('Content-Type', 'application/xml')
        #print self.render_string('template.xml',source=source)
        print self.request.remote_ip
        self.render2('news.xml',records=records)

    def getRecords(self,keywords,pagenum):
        records=[]        
        try:            
            page_num=int(pagenum)
            records=newsinfo.getSearchedPage(keywords, page_num)
        except:
            logging.info('pagenum type error!')
        if not records:
            records=[]
        return records
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
    "static_path": os.path.join(os.path.dirname(os.getcwd()), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
    }
    app = tornado.web.Application(handlers=[(r"/news/(\w+)", NewsHandler), \
                                            (r"/video/(\w+)", VideoHandler), \
                                            (r"/search/(\w+)", SearchHandler), \
                                            (r"/(favicon\.ico|\w+\.py)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))], **settings)
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.httpserver
import ruamel.yaml
import os
import sys
import tornado.options

from tornado.options import options, define
define("port",default=8888,help="running on 8888",type=int)


if not os.environ.has_key('_BASIC_PATH_'):
    _BASIC_PATH_ = os.path.abspath(__file__)
    _BASIC_PATH_ = _BASIC_PATH_[:_BASIC_PATH_.rfind('/bin/')]
    os.environ['_BASIC_PATH_'] = _BASIC_PATH_

if sys.path.count(os.environ['_BASIC_PATH_'] + '/lib') == 0:
    sys.path.append(os.environ['_BASIC_PATH_'] + '/lib')

from db import mydb 

dic={'classes':{},'parameters': {'path':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','puppetserver':'puppet.500boss.com'},'environment':'production'}
#yam="""
#classes: 
#  nginx_new:
#parameters:
#  host: news_int
#"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        puppet_db=mydb()
        node=self.get_argument('node')
        r=puppet_db.getnodeclass(node)
        self.write(r)
        
application = tornado.web.Application([
    (r"/",MainHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()



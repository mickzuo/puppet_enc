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

settings = {
    "static_path" : os.path.join(os.environ['_BASIC_PATH_'],"static"),
    "template_path" : os.path.join(os.environ['_BASIC_PATH_'],"template"),
    "debug" : True,
}

print settings
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
        r=puppet_db.getnodeclass(node.replace('.500x.com',''))
        #r=puppet_db.getnodeclass(node)
        self.write(r)

class AdminHandler(tornado.web.RequestHandler):
    def get(self,filename):
        #logger.debug('testtest')
        #self.write('testtest')
        #print who
        self.render(filename)

class TableHandler(tornado.web.RequestHandler):
    def get(self):
        #logger.debug('testtest')
        #self.write('testtest')
        #print who
        puppet_db=mydb()
        #machines=puppet_db.get_machine_list()
        #self.render("tables.html",machines=({'hostname':'dddd','ip':'testet'},{'hostname':'dfdaf','ip':'etwqtq'}))
        self.render("nodes.html",machines=puppet_db.get_machine_list(),all_node_groups=puppet_db.get_all_node_groups())
        

class ApiAddnode(tornado.web.RequestHandler):
    def post(self):
        puppet_db=mydb()
        self.write(puppet_db.add_node(self.get_argument('hostname'),self.get_argument('node_group')))

class ApiAddmodule(tornado.web.RequestHandler):
    def post(self):
        puppet_db=mydb()
        self.write(puppet_db.add_module(self.get_argument('classname'),self.get_argument('class_group')))


class ApiDelnode(tornado.web.RequestHandler):
    def post(self):
        puppet_db=mydb()
        self.write(puppet_db.delnode(self.get_argument('node')))

class ApiDelmodule(tornado.web.RequestHandler):
    def post(self):
        puppet_db=mydb()
        self.write(puppet_db.delmodule(self.get_argument('module')))


class ModulesHandler(tornado.web.RequestHandler):
    def get(self):
        puppet_db=mydb()
        self.render("modules.html",classes=puppet_db.getnodetoclass(),allclass=puppet_db.getclass())

application = tornado.web.Application(
[
    (r"/",MainHandler),(r"/pages/nodes.html",TableHandler),(r"/api/add_node",ApiAddnode),(r"/api/delnode",ApiDelnode),(r"/pages/modules.html",ModulesHandler),(r"/pages/(.*)",AdminHandler),(r"/api/delmodule",ApiDelmodule),(r"/api/add_module",ApiAddmodule)
],**settings
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(options.port)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()



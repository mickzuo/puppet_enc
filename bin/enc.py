import tornado.ioloop
import tornado.web
import ruamel.yaml
import os
import sys

if not os.environ.has_key('_BASIC_PATH_'):
    _BASIC_PATH_ = os.path.abspath(__file__)
    _BASIC_PATH_ = _BASIC_PATH_[:_BASIC_PATH_.rfind('/bin/')]
    os.environ['_BASIC_PATH_'] = _BASIC_PATH_

if sys.path.count(os.environ['_BASIC_PATH_'] + '/lib') == 0:
    sys.path.append(os.environ['_BASIC_PATH_'] + '/lib')

from db import mydb 

dic={'classes':{'nginx_new':''},'parameters': {'host': 'news_int','path':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','hehe':'test','puppetserver':'puppet.500boss.com'},'environment':'production'}
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
        print "hello python!"
        print r
        self.write(r)
        
application = tornado.web.Application([
    (r"/",MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


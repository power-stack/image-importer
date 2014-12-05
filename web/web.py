import os
import os.path
import random
import string
import cherrypy
import imagechecking as ic
import hadoop_job as hjob


class SimpleWeb(object):
    @cherrypy.expose
    def index(self):
        return file('public/index.html')

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/imagechecking': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/logreader': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/resultreader': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                           })
    webapp = SimpleWeb()
    hj = hjob.HadoopJob()
    webapp.imagechecking = ic.ImageChecking(hj)
    webapp.logreader = ic.LogReader(hj)
    webapp.resultreader = ic.ResultReader(hj)
    cherrypy.quickstart(webapp, '/', conf)

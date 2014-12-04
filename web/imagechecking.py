#coding=utf-8

import os
import os.path
import random
import string
import cherrypy
import sys
import uuid
import image_importer
import hadoop_job as hjob


reload(sys)
sys.setdefaultencoding('utf8')


class ImageChecking(object):
    exposed = True
    _content = None
    _picdir = "./data/pics"
    _hjob = hjob.HadoopJob()

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        htmltpl = self._load_htmltpl()
        content = "<div style='width: 300px'>"
        content += "<p style='font-size: 16px; width: 300px; margin-top: 0px'>"
        content += "请选择需要导入的图片目录：<br></p></div>"
        content += "<form method='post' action=/imagechecking>"
        content += "<table style='width:100%'>"

        if os.path.exists(self._picdir):
            pic_dirs = os.listdir(self._picdir)
            for d in pic_dirs:
                content += "<tr><td><input type='checkbox' name='picdirs' value='%s'>%s</td></tr>" % (d, d)
        content += "<br><tr><td><input type='submit' value='开始导入数据'></td></tr></table></form>"
        cherrypy.response.headers['Content-Type']= 'text/html'
        return htmltpl.replace("$$TOREPLACE$$", content)

    def POST(self, picdirs=""):
        cherrypy.response.headers['Content-Type']= 'text/html'
        self._hjob.start(picdirs, "./hjob.log")
        return "started"

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

    def _load_htmltpl(self):
        if self._content:
            return self._content

        f = open("./html.tpl")
        self._content = f.read()
        f.close()
        return self._content

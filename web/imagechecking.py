#coding=utf-8

import json
import os
import os.path
import random
import string
import cherrypy
import sys
import uuid


reload(sys)
sys.setdefaultencoding('utf8')
MYDIR = os.path.dirname(os.path.realpath(__file__))


class ResultReader(object):
    exposed = True
    _content = None
    _hjob = None

    def __init__(self, hjob):
        self._hjob = hjob

    @cherrypy.tools.accept(media='text/plain')
    def POST(self):
        cherrypy.response.headers['Content-Type']= 'text/html'
        htmltpl = self._load_htmltpl()
        content = "<div style='width: 100%'>"
        content += "<table style='width:90%'><tr><td>"
        content += "<form method='post' action=/resultreader>"
        content += "<input type='submit' value='刷新'></form>"
        content += "</td></tr></table><br>"
        content += "</div>"
        if self._hjob.hadoop_outdir:
            hout_dir = os.path.join(MYDIR, "data", self._hjob.hadoop_outdir)
            if os.path.exists(hout_dir):
                content += "<table border='1' style='width:90%;border: 1px solid black;border-collapse: collapse;'><tr>"
                content += "<th>图片名称</th>"
                content += "<th>是否编辑过</th>"
                content += "<th>检查点</th>"
                content += "<th>编辑软件</th>"
                content += "<th>ELA</th>"
                content += "</tr>"
                results = []
                f = open(os.path.join(hout_dir, "part-00000"))
                while True:
                    line = f.readline()
                    if not line:
                        break
                    try:
                        results.append(json.loads(line))
                    except:
                        pass
                for pic_res in results:
                    if not pic_res:
                        continue
                    pic_name = pic_res.get("name")
                    edited = pic_res.get("edited")
                    reason = pic_res.get("reason") or ""
                    software = pic_res.get("software") or ""
                    ela = pic_res.get("ela") or 0
                    if not pic_name:
                        continue
                    pic_name = pic_name[len(self._hjob.picdir):]
                    content += "<tr><td>" + pic_name + "</td>"
                    if "yes" == edited:
                        content += "<td style='background-color:red;'>" + edited + "</td>"
                    else:
                        content += "<td>" + edited + "</td>"
                    content += "<td>" + reason + "</td>"
                    content += "<td>" + software + "</td>"

                    if ela >= 50:
                        content += "<td style='background-color:yellow;'>%d</td>" % ela
                    else:
                        content += "<td>%d</td>" % ela
                    content += "</tr>"
                content += "</table>"
        return htmltpl.replace("$$TOREPLACE$$", content)

    def _load_htmltpl(self):
        if self._content:
            return self._content

        f = open("./html.tpl")
        self._content = f.read()
        f.close()
        return self._content


class LogReader(object):
    exposed = True
    _content = None
    _hjob = None

    def __init__(self, hjob):
        self._hjob = hjob

    @cherrypy.tools.accept(media='text/plain')
    def POST(self):
        cherrypy.response.headers['Content-Type']= 'text/html'
        htmltpl = self._load_htmltpl()
        content = "<div style='width: 100%'>"
        content += "<table style='width:40%'><tr><td>"
        content += "<form method='post' action=/logreader>"
        content += "<input type='submit' value='刷新'></form></td>"

        if self._hjob.hadoop_outdir:
            hout_dir = os.path.join(MYDIR, "data", self._hjob.hadoop_outdir)
            if os.path.exists(hout_dir):
                content += "<td><form method='post' action=/resultreader>"
                content += "<input type='submit' value='查看运行结果'></form></td>"
        content += "</tr></table><br>"

        if os.path.exists("./hjob.log"):
            content += "<table style='width:80%;border: 1px solid black;border-collapse: collapse;'>"
            f = open("./hjob.log")
            lines = f.readlines()
            f.close()
            for line in lines:
                content += "<tr><td>" + line + "</td></tr>"
            content += "</table><br>"
        content += "</div>"
        return htmltpl.replace("$$TOREPLACE$$", content)

    def _load_htmltpl(self):
        if self._content:
            return self._content

        f = open("./html.tpl")
        self._content = f.read()
        f.close()
        return self._content


class ImageChecking(object):
    exposed = True
    _content = None
    _picdir = "./data/pics"
    _hjob = None

    def __init__(self, hjob):
        self._hjob = hjob

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        if not self._hjob.running:
            htmltpl = self._load_htmltpl()
            content = "<div style='width: 300px'>"
            if self._hjob.hadoop_outdir:
                content += "<table style='width:100%'><tr><td>"
                content += "<form method='post' action=/logreader>"
                content += "<input type='submit' value='查看上次运行日志'></form>"
                content += "<td><form method='post' action=/resultreader>"
                content += "<input type='submit' value='查看上次运行结果'></form>"
                content += "</td></tr></table><br><br>"
            content += "<p style='font-size: 16px; width: 300px; margin-top: 0px'>"
            content += "请选择需要导入的图片目录：</p></div>"
            content += "<form method='post' action=/imagechecking>"
            content += "<table style='width:100%'>"

            if os.path.exists(self._picdir):
                pic_dirs = os.listdir(self._picdir)
                for d in pic_dirs:
                    content += "<tr><td><input type='checkbox' name='picdirs' value='%s'>%s</td></tr>" % (d, d)
            content += "<br><tr><td><input type='submit' value='开始导入数据'></td></tr></table></form>"
            cherrypy.response.headers['Content-Type']= 'text/html'
            return htmltpl.replace("$$TOREPLACE$$", content)
        else:
            htmltpl = self._load_htmltpl()
            content = "<div style='width: 300px'>"
            content += "<p style='font-size: 16px; width: 300px; margin-top: 0px'>"
            content += "已经有job在运行中……<br></p></div>"
            content += "<table style='width:100%'><tr><td>"
            content += "<form method='post' action=/logreader>"
            content += "<input type='submit' value='查看运行日志'></form></td>"
            if self._hjob.hadoop_outdir:
                content += "<td><form method='post' action=/resultreader>"
                content += "<input type='submit' value='查看运行结果'></form>"
                content += "</td>"
            content += "</tr></table>"
            cherrypy.response.headers['Content-Type']= 'text/html'
            return htmltpl.replace("$$TOREPLACE$$", content)

    def POST(self, picdirs=""):
        cherrypy.response.headers['Content-Type']= 'text/html'
        htmltpl = self._load_htmltpl()
        content = "<div style='width: 300px'>"
        content += "<table style='width:100%'><tr><td>"
        content += "<form method='post' action=/logreader>"
        content += "<input type='submit' value='查看运行日志'></form>"
        content += "</td></tr></table><br>"
        if not self._hjob.running:
            if os.path.exists("./hjob.log"):
                os.remove("./hjob.log")
            self._hjob.start(picdirs, "./hjob.log")
            content += "<h2>启动成功</h2>"
        content += "</div>"
        return htmltpl.replace("$$TOREPLACE$$", content)

    def PUT(self, another_string):
        cherrypy.response.headers['Content-Type']= 'text/html'
        return "put"

    def DELETE(self):
        cherrypy.response.headers['Content-Type']= 'text/html'
        return "delete"

    def _load_htmltpl(self):
        if self._content:
            return self._content

        f = open("./html.tpl")
        self._content = f.read()
        f.close()
        return self._content

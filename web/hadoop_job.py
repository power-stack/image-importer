#coding=utf-8
from __future__ import print_function

import subprocess
import os
import os.path
import time
from threading import Thread
import uuid


def write_log(logfile, message):
    print(message, file=logfile)


def run_process_with_log(exe, logfile):

    p = subprocess.Popen(exe,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    while(True):
        retcode = p.poll()
        line = p.stdout.readline()
        if line:
            write_log(line)
        if retcode is not None:
            return retcode


class HadoopJob(object):
    running = False
    failed = False
    err_msg = ""
    job_thread = None

    def start(self, picdirs, logfile):
        self.picdirs = picdirs
        self.job_thread = Thread(target=self.runjob, args=(picdirs, logfile))
        self.job_thread.start()

    def runjob(self, picdirs, logfile):
        self.running = True
        if type(picdirs) is not list:
            picdirs = [picdirs]
        jsonfiles = []
        hadoop_store = "/user/" + str(uuid.uuid4())
        cmd = "sudo su -c -l hadoop 'hadoop fs -mkdir %s'" % hadoop_store
        run_process_with_log(cmd, logfile)
        for picdir in picdirs:
            jsonfilename = str(uuid.uuid4()) + ".json"
            input_dir = os.path.join(self._picdir, picdir)
            out_file = os.path.join("/tmp", jsonfilename)
            image_importer.transfer_pics(input_dir, out_file)
            jsonfiles.append(out_file)
            #upload to hadoop
            cmd = "sudo su -c -l hadoop 'hadoop fs -copyFromLocal %s %s'" % (out_file, hadoop_store)
            ret = run_process_with_log(cmd, logfile)
            if ret != 0:
                self.failed = True
                self.err_msg = "Failed to execute command: " + cmd
                self.running = False
                return
        #submit mapreduce job
        hadoop_outdir = "/user/pa-" + str(uuid.uuid4())
        mydir = os.path.dirname(os.path.realpath(__file__))
        mapper = os.path.join(mydir, "mapper.py")
        reducer = os.path.join(mydir, "reducer.py")
        cmd = "sudo su -c -l hadoop 'hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input %(store)s -output %(out)s -mapper mapper.py -reducer reducer.py -file %(mapper)s -file %(reducer)s'"
        cmd = cmd % dict(store=hadoop_store, out=hadoop_outdir, mapper=mapper, reducer=reducer)
        ret = run_process_with_log(cmd, logfile)
        if ret != 0:
            self.failed = True
            self.err_msg = "Failed to execute command: " + cmd
        self.running = False

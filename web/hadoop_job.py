#coding=utf-8
from __future__ import print_function

import subprocess
import os
import os.path
import time
from threading import Thread
import uuid

import image_importer


def write_log(logfile, message):
    print(message, file=logfile)


def run_process_with_log(exe, logfile):
    print(" ".join(exe))
    p = subprocess.Popen(exe,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    log_fp = open(logfile, "a+")
    while(True):
        retcode = p.poll()
        line = p.stdout.readline()
        if line:
            write_log(log_fp, line)
        if retcode is not None:
            log_fp.flush()
            log_fp.close()
            return retcode


class HadoopJob(object):
    running = False
    failed = False
    err_msg = ""
    job_thread = None
    _picdir = "./data/pics"

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
        mydir = os.path.dirname(os.path.realpath(__file__))
        cmd = ["/usr/bin/hadoop", "fs", "-mkdir", hadoop_store]
        run_process_with_log(cmd, logfile)
        for picdir in picdirs:
            jsonfilename = str(uuid.uuid4()) + ".json"
            input_dir = os.path.join(mydir, self._picdir, picdir)
            out_file = os.path.join("/tmp", jsonfilename)
            image_importer.transfer_pics(input_dir, out_file)
            jsonfiles.append(out_file)
            #upload to hadoop
            cmd = ["/usr/bin/hadoop", "fs", "-copyFromLocal", out_file, hadoop_store]
            ret = run_process_with_log(cmd, logfile)
            if ret != 0:
                self.failed = True
                self.err_msg = "Failed to execute command: " + " ".join(cmd)
                self.running = False
                return
        #submit mapreduce job
        hadoop_outdir = "/user/pa-" + str(uuid.uuid4())
        mapper = os.path.join(mydir, "mapper.py")
        reducer = os.path.join(mydir, "reducer.py")
        cmd = ["/usr/bin/hadoop",
               "jar",
               "/usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar",
               "-input",
               hadoop_store,
               "-output",
               hadoop_outdir,
               "-mapper",
               "mapper.py",
               "-reducer",
               reducer,
               "-file",
               mapper,
               "-file",
               reducer]
        ret = run_process_with_log(cmd, logfile)
        if ret != 0:
            self.failed = True
            self.err_msg = "Failed to execute command: " + " ".join(cmd)
        self.running = False

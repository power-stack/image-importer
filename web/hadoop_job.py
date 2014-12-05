#coding=utf-8

import subprocess
import os
import os.path
import time
from threading import Thread
import uuid

import image_importer


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
            log_fp.write(line)
            log_fp.write("\n")
            log_fp.flush()
        if retcode is not None:
            log_fp.flush()
            log_fp.close()
            return retcode


MYDIR = os.path.dirname(os.path.realpath(__file__))


class HadoopJob(object):
    running = False
    failed = False
    err_msg = ""
    job_thread = None
    picdir = os.path.join(MYDIR, "data", "pics")
    hadoop_outdir = None

    def start(self, picdirs, logfile):
        self.hadoop_outdir = None
        self.local_outdir = None
        self.picdirs = picdirs
        self.job_thread = Thread(target=self.runjob, args=(picdirs, logfile))
        self.job_thread.start()

    def runjob(self, picdirs, logfile):
        self.running = True
        if type(picdirs) is not list:
            picdirs = [picdirs]
        jsonfiles = []
        hadoop_store = "/user/" + str(uuid.uuid4())

        cmd = ["/usr/bin/hadoop", "fs", "-mkdir", hadoop_store]
        run_process_with_log(cmd, logfile)
        for picdir in picdirs:
            jsonfilename = str(uuid.uuid4()) + ".json"
            input_dir = os.path.join(self.picdir, picdir)
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
        hadoop_outdir = "output-" + str(uuid.uuid4())

        mapper = os.path.join(MYDIR, "mapper.py")
        reducer = os.path.join(MYDIR, "reducer.py")
        cmd = ["/usr/bin/hadoop",
               "jar",
               "/usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar",
               "-input",
               hadoop_store,
               "-output",
               "/user/" + hadoop_outdir,
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
        datadir = os.path.join(MYDIR, "data")
        cmd = ["/usr/bin/hadoop", "fs", "-copyToLocal", "/user/" + hadoop_outdir, datadir]
        run_process_with_log(cmd, logfile)
        self.hadoop_outdir = hadoop_outdir
        self.running = False

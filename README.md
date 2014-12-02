image-importer
==============
```
hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input /user/eloancn/ -output /user/output1 -mapper mapper.py -reducer reducer.py -file /tmp/reducer.py -file /tmp/mapper.py
packageJobJar: [/tmp/reducer.py, /tmp/mapper.py, /tmp/hadoop-hadoop/hadoop-unjar4473518186932958303/] [] /tmp/streamjob1401338980956478467.jar tmpDir=null
14/12/02 13:54:11 INFO util.NativeCodeLoader: Loaded the native-hadoop library
14/12/02 13:54:11 WARN snappy.LoadSnappy: Snappy native library not loaded
14/12/02 13:54:11 INFO mapred.FileInputFormat: Total input paths to process : 2
14/12/02 13:54:11 INFO streaming.StreamJob: getLocalDirs(): [/mnt/lib/hadoop/mapred]
14/12/02 13:54:11 INFO streaming.StreamJob: Running job: job_201411190650_0009
14/12/02 13:54:11 INFO streaming.StreamJob: To kill this job, run:
14/12/02 13:54:11 INFO streaming.StreamJob: /usr/libexec/../bin/hadoop job  -Dmapred.job.tracker=TenNode-master-tmpl-001:8021 -kill job_201411190650_0009
14/12/02 13:54:11 INFO streaming.StreamJob: Tracking URL: http://TenNode-master-tmpl-001.novalocal:50030/jobdetails.jsp?jobid=job_201411190650_0009
14/12/02 13:54:12 INFO streaming.StreamJob:  map 0%  reduce 0%
14/12/02 13:54:20 INFO streaming.StreamJob:  map 31%  reduce 0%
14/12/02 13:54:21 INFO streaming.StreamJob:  map 63%  reduce 0%
14/12/02 13:54:23 INFO streaming.StreamJob:  map 68%  reduce 0%
14/12/02 13:54:24 INFO streaming.StreamJob:  map 72%  reduce 0%
14/12/02 13:54:26 INFO streaming.StreamJob:  map 75%  reduce 0%
14/12/02 13:54:27 INFO streaming.StreamJob:  map 80%  reduce 17%
14/12/02 13:54:29 INFO streaming.StreamJob:  map 84%  reduce 17%
14/12/02 13:54:30 INFO streaming.StreamJob:  map 89%  reduce 17%
14/12/02 13:54:32 INFO streaming.StreamJob:  map 98%  reduce 17%
14/12/02 13:54:35 INFO streaming.StreamJob:  map 100%  reduce 17%
14/12/02 13:54:38 INFO streaming.StreamJob:  map 100%  reduce 100%
14/12/02 13:54:40 INFO streaming.StreamJob: Job complete: job_201411190650_0009
14/12/02 13:54:40 INFO streaming.StreamJob: Output: /user/output1
```

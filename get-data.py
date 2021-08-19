#!/usr/bin/env python3
# coding: shift-jis

import redis
import shutil
import os
import datetime
from setenv import RedisPwd

### Redis info
RedisHost = "redis-13849.c9.us-east-1-4.ec2.cloud.redislabs.com"  
RedisPort = "13849"

### Redis connect
r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
r = redis.StrictRedis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)

### Redis data get
with open('result-data.txt', 'wt') as f: # File
    res_keys = r.keys()                     # key
    if res_keys:
        res_mget = r.mget(res_keys)         # mget
        for key, val in zip(res_keys, res_mget):
            print(val, file=f)

### reset vars
ncount = 0

### format data
f = open('result-data.txt', 'r')
line = f.readline()
while line:
    dline = line
    rline = dline.replace('\'', '')
    rline2 = rline.replace('b', '')
    rline3 = rline2.replace('\n', '')
    fline = float(rline3)
    if fline < 0.6:
        ncount += 1
    line = f.readline()
f.close()

### set website file
path1 = "C:\\temp\\p4p\\project\\mysite\\defaultpage.txt"
path2 = "C:\\temp\\p4p\\project\\mysite\\index.html"

### reset website file 
shutil.copy(path1,path2)
ncount = ncount*10
sitcount = datetime.timedelta(seconds=ncount)

### update website file
with open("C:\\temp\\p4p\\project\\mysite\\index.html", "r",encoding='UTF-8') as f2:
    filedata = f2.read()
    filedata=filedata.replace("XXX", str(sitcount))
    if ncount < 18000:
        filedata=filedata.replace("MMMMM","時々立ち上がってストレッチしましょう。")
    else:
        filedata=filedata.replace("MMMMM","長時間座っているため気を付けましょう。")
with open(r"C:\\temp\\p4p\\project\\mysite\\index.html","w",encoding='UTF-8') as f3:
    f3.write(filedata)

### update heroku
os.chdir('mysite')
os.system('git add .')
os.system('git commit -m "auto"')
os.system('git push heroku master')
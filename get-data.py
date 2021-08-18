#!/usr/bin/env python3
# coding: shift-jis

import redis
import shutil
import os
from setenv import RedisPwd

### Redis情報記載
RedisHost = "redis-13849.c9.us-east-1-4.ec2.cloud.redislabs.com"  
RedisPort = "13849"

def get_redis_data():
    ### Redisへ接続
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    r = redis.StrictRedis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    ### Redisからデータを取得し一時ファイルにデータを出力
    with open('result-data.txt', 'wt') as f: # File
        res_keys = r.keys()                     # key
        if res_keys:
            res_mget = r.mget(res_keys)         # mget
            for key, val in zip(res_keys, res_mget):
                print(val, file=f)

### 変数をリセット
ncount = 0

### 取得したデータを整形し、一定距離以下だった期間を合計する。
f = open('result-data.txt', 'r')
line = f.readline()
while line:
    dline = line
    rline = dline.replace('\'', '')
    rline2 = rline.replace('b', '')
    rline3 = rline2.replace('\n', '')
    fline = float(rline3)
    if fline < 0.3:
        ncount += 1
    line = f.readline()
f.close()

### Webサイト用ファイル/変換前ファイルを指定
path1 = "C:\\temp\\p4p\\project\\mysite\\defaultpage.txt"
path2 = "C:\\temp\\p4p\\project\\mysite\\index.html"

### Webサイト用ファイルを変換前ファイルにリセット
shutil.copy(path1,path2)

### Webサイト用ファイルに期間を記載、期間によってメッセージを変更
with open("C:\\temp\\p4p\\project\\mysite\\index.html", "r",encoding='UTF-8') as f2:
    filedata = f2.read()
    filedata=filedata.replace("XXX", str(ncount))
    filedata=filedata.replace("MMMMM","時々立ち上がってストレッチしましょう。")
with open(r"C:\\temp\\p4p\\project\\mysite\\index.html","w",encoding='UTF-8') as f3:
    f3.write(filedata)

### herokuをアップデート
os.chdir('mysite')
os.system('git add .')
os.system('git commit -m "auto"')
os.system('git push heroku master')

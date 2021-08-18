#!/usr/bin/env python3
# coding: shift-jis

import redis
import shutil
import os
from setenv import RedisPwd

### Redis���L��
RedisHost = "redis-13849.c9.us-east-1-4.ec2.cloud.redislabs.com"  
RedisPort = "13849"

### Redis�֐ڑ�
r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
r = redis.StrictRedis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)

### Redis����f�[�^���擾���ꎞ�t�@�C���Ƀf�[�^���o��
with open('result-data.txt', 'wt') as f: # File
    res_keys = r.keys()                     # key
    if res_keys:
        res_mget = r.mget(res_keys)         # mget
        for key, val in zip(res_keys, res_mget):
            print(val, file=f)

### �ϐ������Z�b�g
ncount = 0

### �擾�����f�[�^�𐮌`���A��苗���ȉ����������Ԃ����v����B
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

### Web�T�C�g�p�t�@�C��/�ϊ��O�t�@�C�����w��
path1 = "C:\\temp\\p4p\\project\\mysite\\defaultpage.txt"
path2 = "C:\\temp\\p4p\\project\\mysite\\index.html"

### Web�T�C�g�p�t�@�C����ϊ��O�t�@�C���Ƀ��Z�b�g
shutil.copy(path1,path2)

### Web�T�C�g�p�t�@�C���Ɋ��Ԃ��L�ځA���Ԃɂ���ă��b�Z�[�W��ύX
with open("C:\\temp\\p4p\\project\\mysite\\index.html", "r",encoding='UTF-8') as f2:
    filedata = f2.read()
    filedata=filedata.replace("XXX", str(ncount))
    filedata=filedata.replace("MMMMM","���X�����オ���ăX�g���b�`���܂��傤�B")
with open(r"C:\\temp\\p4p\\project\\mysite\\index.html","w",encoding='UTF-8') as f3:
    f3.write(filedata)

### heroku���A�b�v�f�[�g
os.chdir('mysite')
os.system('git add .')
os.system('git commit -m "auto"')
os.system('git push heroku master')
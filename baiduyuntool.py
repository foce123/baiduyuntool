#coding:utf-8

from baidupcsapi import PCS
import os, json, sys, tempfile
import progressbar

pcs = PCS('username','password')
print pcs.quota().content

class ProgressBar():
    def __init__(self):
        self.first_call = True
    def __call__(self, *args, **kwargs):
        if self.first_call:
            self.widgets = [progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker('>')), ' ', progressbar.ETA()]
            self.pbar = progressbar.ProgressBar(widgets=self.widgets, maxval=kwargs['size']).start()
            self.first_call = False

        if kwargs['size'] <= kwargs['progress']:
            self.pbar.finish()
        else:
            self.pbar.update(kwargs['progress'])

def helpl():
    print "Usage: python %s [-l|-d|-u|-b] [filename | directory]" %sys.argv[0]
    print "    -l  --list      list current directory"
    print "    -d  --download  download files"
    print "    -u  --upload    upload files"
    print "    -b  --big       upload huge files"
    print "    -h  --help      help display"
    print "    -v  --version   version"

def printv():
    print "version 0.0.1"

def list(dirs):
    if len(sys.argv[2]) == 0:
        print pcs.list_files('/').content
    elif sys.argv[2][0] != '/':
        helpl()
    else:
        print pcs.list_files(dirs).content

def download (dirsfile):
    headers = {'Range': 'bytes = 0-99'}
    if sys.argv[2][0] != '/':
        helpl()
    else:
        pcs.download(dirsfile,headers = headers)

def upload (filename):
    test_file = open(filename,'rb').read()
    ret = pcs.upload('/',test_file,filename,callback=ProgressBar())

she = {"-l | --list": list(sys.argv[2]),"-d | --download":download(sys.argv[2]),"-u | --upload":upload(sys.argv[2]),"-b | --big":helpl(), "-h | --help":helpl(), "-v | --version":printv()}

if len(sys.argv[1]) == 0:
    helpl()
elif sys.argv[1] in she:
    try:
        she[sys.argv[1]]
    except KeyError as e:
        helpl()
else:
    helpl()

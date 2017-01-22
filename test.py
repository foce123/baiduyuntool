#coding: utf-8
import os,json,sys,tempfile
import progressbar
from baidupcsapi import PCS

pcs = PCS('username','password')
print pcs.quota().content

fun = {'-l'|'--list':list(sys.argv[2])}

def list ():
    print pcs.list_files('/').content

def download ():
    headers = {'Range': 'bytes = 0-99'}
    pcs.download('/test_sdk/test.txt',headers = headers)

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

def upload ():
    #pcs = PCS('username','password')
    test_file = open('bigfile.pdf','rb').read()
    ret = pcs.upload('/',test_file,'bigfile.pdf',callback=ProgressBar())

pcs = PCS('username','password')
chinksize = 1024*1024*16
fid = 1
md5list = []
tmpdir = tempfile.mkdtemp('bdpcs')
with open(sys.argv[1],'rb') as infile:
    while 1:
        data = infile.read(chinksize)
        if len(data) == 0: break
        smallfile = os.path.join(tmpdir, 'tmp%d' %fid)
        with open(smallfile, 'wb') as f:
            f.write(data)
        print('chunk%d size %d' %(fid, len(data)))
        fid += 1
        print('start uploading...')
        ret = pcs.upload_tmpfile(open(smallfile, 'rb'))
        md5list.append(json.loads(ret.content)['md5'])
        print('md5: %s' %(md5list[-1]))
        os.remove(smallfile)

os.rmdir(tmpdir)
ret = pcs.upload_superfile('/'+os.path.basename(sys.argv[1]), md5list)
print ret.content
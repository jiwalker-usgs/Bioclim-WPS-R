import os
import subprocess
import time
import shlex
src="/Volumes/Striped/cmip5_out"
dest="/Volumes/Striped/cmip5/bcca"
dirs=0
files=0
srcfiles=[ ]
for dirname, dirnames, filenames in os.walk(src):
    for subdirname in dirnames:
        srcdir = os.path.join(dirname, subdirname)
        destdir=dest+srcdir[len(src):len(srcdir)]
    for filename in filenames:
        if filename[len(filename)-7:len(filename)]=='corr.nc':
            parts=filename.split('_')
            path='/'+parts[4].lower()+'/'+parts[5]+'/'+parts[3]+'/'+parts[6]+'/'+parts[2]+'/'
            os.system('mv '+os.path.join(dirname, filename)+' '+dest+path+filename)
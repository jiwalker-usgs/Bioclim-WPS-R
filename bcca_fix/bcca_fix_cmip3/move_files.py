import os
import subprocess
import time
import shlex
pr_src="/Volumes/Scratch/thredds/llnl_archive/bcca_fixed_pr"
tmp_src="/Volumes/Scratch/thredds/llnl_archive/bcca"
dest="/Volumes/Striped/cmip3/bcca"
dirs=0
files=0
srcfiles=[ ]
for dirname, dirnames, filenames in os.walk(tmp_src):
    print dirname
    for filename in filenames:
        if 'tasmax' in filename or 'tasmin' in filename:
            path=dest+dirname[len(tmp_src):len(dirname)]
            command=os.system('mkdir -p '+path)
            command=os.system('rsync -aP '+os.path.join(dirname, filename)+' '+os.path.join(path, filename))
            if command!=0:
                raise Exception('An error occured moving a file.')

for dirname, dirnames, filenames in os.walk(pr_src):
    print dirname
    for filename in filenames:
        if filename[len(filename)-7:len(filename)]=='corr.nc':
            parts=filename.split('.')
            path='/'+parts[0]+'.'+parts[1]+'/'+parts[2]+'/'+parts[3]+'/'+parts[4]+'/bcca/'
            command=os.system('mkdir -p '+path)
            command=os.system('rsync -aP '+os.path.join(dirname, filename)+' '+dest+path+filename)
            if command!=0:
                raise Exception('An error occured moving a file.')
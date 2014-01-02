import os
import subprocess
import time
import shlex
src="/Volumes/Striped/cmip5/bcca/"
PROC_DIR="/Volumes/RAM-Disk/"
dest="/Volumes/Scratch/cmip5_out/"
dirs=0
files=0
srcfiles=[ ]
for dirname, dirnames, filenames in os.walk(src):
    for subdirname in dirnames:
        srcdir = os.path.join(dirname, subdirname)
        destdir=dest+srcdir[len(src):len(srcdir)]
        procdir=PROC_DIR+srcdir[len(src):len(srcdir)]
        if os.access(destdir,os.F_OK):
            pass
        else:
            os.mkdir(destdir)
            print 'made '+destdir
        if os.access(procdir,os.F_OK):
            pass
        else:
            os.mkdir(procdir)
            print 'made '+procdir
    for filename in filenames:
        if filename[len(filename)-6:len(filename)]=='.nc.gz':
            print dest+dirname[len(src):len(dirname)]+'/'+filename[0:len(filename)-7]+'.nc'
            if os.path.isfile(dest+dirname[len(src):len(dirname)]+'/'+filename[0:len(filename)-7]+'.nc'):
                print 'passed'
            else:
                srcfiles.append([dirname, filename])
                files=files+1
        elif filename[len(filename)-7:len(filename)]=='corr.nc':
            print dest+dirname[len(src):len(dirname)]+'/'+filename[0:len(filename)-8]+'_corr.nc'
            if os.path.isfile(dest+dirname[len(src):len(dirname)]+'/'+filename[0:len(filename)-8]+'_corr.nc'):
                print 'passed'
            else:    
                srcfiles.append([dirname, filename])
                files=files+1

files_to_process = len(srcfiles)
processes = []
max_processes = 10
pause_time=2
file_processing = 1
inputs = [['BCCA_0.125deg_pr','pr','10','0.1','-999'],['BCCA_0.125deg_tasmax','tasmax','10','0.1','-999'],['BCCA_0.125deg_tasmin','tasmin','10','0.1','-999']]
for srcfile in srcfiles:
    for input_keys in inputs:
        if input_keys[0] in srcfile[1]:
            var=input_keys[1]
            scale=input_keys[2]
            scale_factor=input_keys[3]
            missing=input_keys[4]
    command=shlex.split('./bin/compress.sh '+var+' '+scale+' '+scale_factor+' '+missing+' '+srcfile[1]+' '+srcfile[0]+' '+PROC_DIR+srcfile[0][28:len(srcfile[0])]+' '+dest+srcfile[0][28:len(srcfile[0])])
    print str(file_processing)+ ' of ' + str(files_to_process)
    file_processing+=1
    processes.append(subprocess.Popen(command))
    if len(processes) < max_processes:
        time.sleep(pause_time)
    while len(processes) >= max_processes:
        time.sleep(pause_time*2)
        processes = [proc for proc in processes if proc.poll() is None]

while len(processes) > 0:
    time.sleep(pause_time)
    processes = [proc for proc in processes if proc.poll() is None]


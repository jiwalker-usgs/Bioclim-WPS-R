import os
import subprocess
import time
import shlex
src='gridmet'
dest='gridmet_compr'
dirs=0
files=0
srcfiles=[ ]
for dirname, dirnames, filenames in os.walk(src):
    for subdirname in dirnames:
        srcdir = os.path.join(dirname, subdirname)
        destdir=dest+srcdir[len(src):len(srcdir)]
        if os.access(destdir,os.F_OK):
            pass
        else:
            os.mkdir(destdir)
            print 'made '+destdir
    for filename in filenames:
        if filename[len(filename)-3:len(filename)]=='.nc':
            srcfiles.append(os.path.join(dirname, filename))
            files=files+1

files_to_process = len(srcfiles)
processes = []
max_processes = 10
pause_time=10
file_processing = 1
for srcfile in srcfiles:
    destfile = dest+srcfile[len(src):len(srcfile)]
    command=shlex.split('ncpdq -O --permute day,lat,lon --pck_map=flt_sht --cnk_plc=g3d --cnk_dmn lat,59 --cnk_dmn lon,139 --cnk_dmn day,1 --fl_fmt=netcdf4 --deflate=1 '+srcfile+' '+destfile)
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


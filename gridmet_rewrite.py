import os
import subprocess
import time
import shlex
src="/Volumes/process/gridmet"
PROC_DIR="/Volumes/RAM-Disk"
dest="/Volumes/Striped/gridmet_out"
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
            #srcfiles.append(os.path.join(dirname, filename))
            srcfiles.append(filename)
            files=files+1

files_to_process = len(srcfiles)
processes = []
max_processes = 5
pause_time=10
file_processing = 1
for srcfile in srcfiles:
    inputs = [['pdur','precipitation_duration_hours','10','-999'],['pr','precipitation_amount','10','-999'],['rmax','relative_humidity','10','-999'],['rmin','relative_humidity','10','-999'],['sph','specific_humidity','10','-999'],['srad','surface_downwelling_shortwave_flux_in_air','10','-999'],['th','wind_from_direction','10','-999'],['tmmn','air_temperature','10','-999'],['tmmx','air_temperature','10','-999'],['vs','wind_speed','10','-999']]
    for input_keys in inputs:
        if input_keys[0] in srcfile:
            var=input_keys[1]
            scale=input_keys[2]
            missing=input_keys[3]
    command=shlex.split('./bin/script.sh '+var+' '+scale+' '+missing+' '+srcfile+' '+src+' '+PROC_DIR+' '+dest)
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


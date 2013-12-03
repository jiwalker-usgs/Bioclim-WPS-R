import os
import subprocess
import time
import shlex
os.chdir('/Users/usgs/temp/')
src='./'
dest='/Volumes/Striped/CA_BCM_Ensemble/'
dirs=0
files=0
srcfiles=[ ]

# First make sure destination directories exist and build list of files to process.
for dirname, dirnames, filenames in os.walk(src):
    print dirname
    # create subdirs first.
    for subdirname in dirnames:
        srcdir = os.path.join(dirname, subdirname)
        destdir=dest+srcdir[len(src):len(srcdir)]
        if os.access(destdir,os.F_OK):
            pass
        else:
            os.mkdir(destdir)
            print 'made '+destdir
    for filename in filenames:
        if '.asc' in filename:
            srcfiles.append(os.path.join(dirname, filename))
            files=files+1
            if files>50:
                break
    if files>50:
        break

files_to_process = len(srcfiles)
processes = []
max_processes = 17
pause_time=0.05
file_processing = 1
timer=time.time()
for srcfile in srcfiles:
    destfile = dest+srcfile[len(src):len(srcfile)-3]+'nc'
    command=shlex.split('gdal_translate -q -of netCDF -co "COMPRESS=DEFLATE" -co FORMAT=NC4C -a_nodata -9999.00 '+srcfile+' '+destfile)
    #print 'doing '+'gdal_translate -q -of netCDF -co "COMPRESS=DEFLATE"  -co FORMAT=NC4C -a_nodata -9999.00 '+srcfile+' '+destfile
    print str(file_processing)+ ' of ' + str(files_to_process)
    file_processing+=1
    processes.append(subprocess.Popen(command))
    while len(processes) >= max_processes:
        time.sleep(pause_time)
        processes = [proc for proc in processes if proc.poll() is None]

while len(processes) > 0:
    time.sleep(pause_time)
    processes = [proc for proc in processes if proc.poll() is None]

print 'Elapsed Time Was '+str(time.time()-timer)


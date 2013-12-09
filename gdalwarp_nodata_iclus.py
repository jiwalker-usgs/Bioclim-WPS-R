import os
import subprocess
import time
import shlex
#os.chdir('/Users/dblodgett/temp/')
src='./in/'
dest='./out/'
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
        if filename[len(filename)-4:len(filename)]=='.tif':
            srcfiles.append(os.path.join(dirname, filename))
            files=files+1
            # if files>50:
            #     break
    # if files>50:
    #     break

files_to_process = len(srcfiles)
processes = []
max_processes = 22
pause_time=2
file_processing = 1
timer=time.time()
for srcfile in srcfiles:
    destfile = dest+srcfile[len(src):len(srcfile)]
    command=shlex.split('python gdal_calc.py -A '+srcfile+' --outfile='+destfile+' --co="compress=DEFLATE" --co="BLOCKXSIZE=128" --co="BLOCKYSIZE=128" --co="TILED=YES" --co="ZLEVEL=6" --calc="A*(A>0)" --NoDataValue=0')
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


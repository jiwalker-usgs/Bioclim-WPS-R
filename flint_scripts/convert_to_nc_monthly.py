import os
import subprocess
import time
import shlex


# All constants in the constants.pr file that needs to live next to this script.
from constants import src, dest, proc_path, time_files_path, start_year, end_year, gdal_translate_path, metadata, file_keys, creator, creator_email, metadata_wy

# Untar package to scratch.
    # mv (targz?) summary to holding folder.
    # rsync monthly and wateryear to striped (one at a time).
        # unique processing rules for wateryear and striped.
            # order monthly files chronologically
            # loop through file keys
                # process with bash script

### Monthly Historical Parameters
folder='HST'
time_res="WaterYears"
time_res="Monthly"
time_file_base='times_monthly_hst'
input_folder='{0}{1}/{2}/'.format(src,folder,time_res)
dest_folder='{0}{1}/{2}/'.format(dest,folder,time_res)
if os.access(dest_folder,os.F_OK):
    pass
else:
    os.makedirs(dest_folder)

months={'oct':'01','nov':'02','dec':'03','jan':'04','feb':'05','mar':'06','apr':'07','may':'08','jun':'09','jul':'10','aug':'11','sep':'12'}
for filenames in os.walk(input_folder):
    for filename in filenames[2]:
        for month_key in months.keys():
            if month_key in filename:
                os.rename(input_folder+filename, input_folder+filename[0:7]+months[month_key]+filename[10:len(filename)])

years=range(1895,2011)

###End Monthly Historical Parameters

processes = []
max_processes = 10
pause_time=2
wait_time=10
file_processing = 1
files_to_process=len(file_keys[time_res])*len(years)
file_processing=1
for key in file_keys[time_res]:
    for year in years:
        title='CA BCM {0} {1} {2}'.format(folder,time_res,metadata[key]['long_name']).replace(' ', '\ ')
        long_name=metadata[key]['long_name'].replace(' ', '\ ')
        units=metadata[key]['units']
        output_file='CA_BCM_{0}_{1}_{2}_{3}.nc'.format(folder,time_res,key,str(year))
        scale_factor=str(metadata[key]['scale_factor'])
        scale=str(1/metadata[key]['scale_factor'])
        missing_value='-9999'
        time_file=time_file_base+str(year)+'.nc'
        command=shlex.split('./bin/script.sh {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14}'.format(key+str(year),scale,scale_factor,missing_value,output_file,input_folder,proc_path,dest_folder,time_files_path,time_file,title,long_name,units,creator,creator_email))
        print str(file_processing)+ ' of ' + str(files_to_process)
        file_processing+=1
        processes.append(subprocess.Popen(command))
        if len(processes) < max_processes:
            time.sleep(wait_time)
        while len(processes) >= max_processes:
            time.sleep(pause_time)
            processes = [proc for proc in processes if proc.poll() is None]

while len(processes) > 0:
    time.sleep(pause_time)
    processes = [proc for proc in processes if proc.poll() is None]


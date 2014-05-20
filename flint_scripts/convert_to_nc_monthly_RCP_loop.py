import os
import subprocess
import time
import shlex


# All constants in the constants.pr file that needs to live next to this script.
from constants import src, unzip_to, dest, proc_path, time_files_path, gdal_translate_path, metadata, file_keys, creator, creator_email, metadata, folders

# Untar monthly from package to striped.
    # move folder to common processing root (out of /Volume/...).
    # order monthly files chronologically
    # loop through file keys
        # process with bash script

# Need to implement a simple verification of where the files are, move from where it is found to where we want it to be.
for folder in folders.keys():
    ### Monthly RCP Parameters
    # folder='CCSM4_rcp85' # Should be a list from constants.py eventually.
    time_res="Monthly"
    time_file_base='times_monthly_'
    input_folder='{0}{1}/{2}/'.format(unzip_to,folder,time_res)
    dest_folder='{0}{1}/{2}/'.format(dest,folder,time_res)
    years=range(2007,2100)
    ###End Monthly RCP Parameters
    
    if os.access(dest_folder,os.F_OK):
        pass
    else:
        os.makedirs(dest_folder)
    
    # if os.access(input_folder,os.F_OK):
    #     pass
    # else:
    #     os.makedirs(input_folder)
    
    if os.access(unzip_to+folders[folder]+'/',os.F_OK)==False and os.access(unzip_to+folder,os.F_OK)==False:
        args=['tar', '-zxvf', src+folder+'.tar.gz', '-C', unzip_to, folders[folder]+'/Monthly/*']
        print args
        subprocess.call(args)
    
    if os.access(unzip_to+folder,os.F_OK)==False:
        args= ['mv', unzip_to+folders[folder], unzip_to]
        print args
        subprocess.call(args)
    
    months={'oct':'01','nov':'02','dec':'03','jan':'04','feb':'05','mar':'06','apr':'07','may':'08','jun':'09','jul':'10','aug':'11','sep':'12'}
            
    for filenames in os.walk(input_folder):
        for filename in filenames[2]:
            for month_key in months.keys():
                if int(months[month_key])<=3:
                    year_mod=1
                else:
                    year_mod=0
                if month_key in filename:
                    os.rename(input_folder+filename, input_folder+filename[0:3]+str(int(filename[3:7])+year_mod)+months[month_key]+filename[10:len(filename)])
    
    processes = []
    max_processes = 10
    pause_time=.5
    wait_time=0.01
    file_processing = 1
    files_to_process=len(file_keys[time_res])*len(years)
    file_processing=1
    for key in file_keys[time_res]:
        print key
        for year in years:
            title='CA BCM {0} {1} {2}'.format(folder,time_res,metadata[key]['long_name']).replace(' ', '\ ')
            long_name=metadata[key]['long_name'].replace(' ', '\ ')
            units=metadata[key]['units']
            output_file='CA_BCM_{0}_{1}_{2}_{3}.nc'.format(folder,time_res,key,str(year))
            scale_factor=str(metadata[key]['scale_factor'])
            scale=str(1/metadata[key]['scale_factor'])
            missing_value='-32768'
            time_file=time_file_base+str(year)+'.nc'
            if os.access(dest_folder+output_file,os.F_OK)==False:
                command=shlex.split('./bin/script.sh {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14}'.format(key+str(year),scale,scale_factor,missing_value,output_file,input_folder,proc_path,dest_folder,time_files_path,time_file,title,long_name,units,creator,creator_email))
                print str(file_processing)+ ' of ' + str(files_to_process)
                print str(year)
                file_processing+=1
                processes.append(subprocess.Popen(command))
                if len(processes) < max_processes:
                    time.sleep(wait_time)
                while len(processes) >= max_processes:
                    time.sleep(pause_time)
                    processes = [proc for proc in processes if proc.poll() is None]
            else:
                print str(file_processing)+ ' of ' + str(files_to_process)
                file_processing+=1
    while len(processes) > 0:
        time.sleep(pause_time)
        processes = [proc for proc in processes if proc.poll() is None]
    args=['rm', '-r', unzip_to+folder+'/Monthly/']
    subprocess.call(args)

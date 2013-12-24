src='/Volumes/process/hobbins/ftp.cdc.noaa.gov/pub/Public/mhobbins/Dave_Blodgett/2013/src/' # Location of source tar.gz files.
dest='/Volumes/process/hobbins/ftp.cdc.noaa.gov/pub/Public/mhobbins/Dave_Blodgett/2013/dest/' # Location where output .nc file should be placed.
proc='/Volumes/process/hobbins/ftp.cdc.noaa.gov/pub/Public/mhobbins/Dave_Blodgett/2013/proc/' # Location where processing should take place. This script will wipe files from this folder. IT SHOULD BE A NEW EMPTY FOLDER!!!
time_files_path='/Volumes/process/hobbins/ftp.cdc.noaa.gov/pub/Public/mhobbins/Dave_Blodgett/2013/time/' # Where the water year .nc files are. The are checked into the git hub repository and need to be local to the script somewhere.
input_tarballz=["2012.tar.gz"] # List of tar.gz files containing data for oct1-sep30 of the year being processed.
start_year=2012 # Year to start at ie. Oct 1 2012
end_year=2013 # Year to end at ie. Sept 20 2013
gdal_translate_path="/opt/local/bin/gdal_translate" # The path where the correct gdal_translate is installed. enthought python installed gdal without netcdf and modified to path to have that one take precendence. This allows the script to hit the system gdal_translate.
import os
import subprocess
import time
import shlex
# All constants in the constants.pr file that needs to live next to this script.
from constants import src, dest, proc, time_files_path, input_tarballz, start_year, end_year, gdal_translate_path

files=0
srcfiles=[ ]

for tarball in input_tarballz:
    # Untar source tarball to processing directory.
    os.system('tar -C '+proc+' -xzf '+src+tarball)
    # Find all the .asc files from the tarball.
    for dirname, dirnames, filenames in os.walk(proc):
        for filename in filenames:
            if '.asc' in filename:
                srcfiles.append(os.path.join(dirname, filename))
                files=files+1

# Use gdal_translate to create deflated netcdf files out of each asc file.
files_to_process = len(srcfiles)
print 'Processing '+str(files_to_process)+' files.'
for srcfile in srcfiles:
    tempfile = proc+srcfile[len(proc):len(srcfile)-3]+'nc'
    command=os.system(gdal_translate_path+" -q -of netCDF -co 'COMPRESS=DEFLATE' -co FORMAT=NC4 "+srcfile+" "+tempfile)

# Remove the .asc files from the processing directory.
os.system('rm '+proc+'*.asc')

# Find each water year worth of files and create a netCDF file per year.
for year in range(start_year,end_year):
    file_list=[]
    water_year=year
    # This will gauruntee that things end up in the right chronological order.
    for month in ["10","11","12","01","02","03","04","05","06","07","08","09"]:
        if month=="01":
            water_year+=1
        file_pattern='ETrs_'+str(water_year)+month
        for filenames in os.walk(proc):
            for filename in filenames[2]:
                if file_pattern in filename:
                    file_list.append(filename)
    # Create specific string list of files to concatenate with ncecat.
    files_to_cat=""
    for filename in file_list:
        files_to_cat=files_to_cat+proc+filename+' '
    # Create file name for output nc file.
    nc_file_name='ETrs'+str(year)+'.nc'
    print nc_file_name
    # ncecat with a record dimension named time.
    os.system('ncecat -h -O -u time '+files_to_cat+proc+nc_file_name)
    # ncrename the gdal default variable Band1 to ETrs
    os.system('ncrename -h -O -v Band1,ETrs '+proc+nc_file_name)
    # ncks to add the time coordinate variable. 
    os.system('ncks -h -A '+time_files_path+str(year)+'.nc '+proc+nc_file_name)
    # ncap2 to convert data to shorts with fixed precision of 0.01mm
    os.system('ncap2 -h -O --fl_fmt=netcdf4 -s "ETrs=short(100*ETrs)" '+proc+nc_file_name+' '+proc+nc_file_name)
    # ncatted to manipulate attributes of the file appropriately.
    os.system('ncatted -h -O -a scale_factor,ETrs,c,f,0.01 \
                -a _FillValue,ETrs,o,f,31082 \
                -a missing_value,ETrs,o,f,31082 \
                -a Metadata_Conventions,global,o,c,"Unidata Dataset Discovery v1.0" \
                -a title,global,o,c,"Reference Evapotranspiration for the Conterminous US" \
                -a creator_name,global,o,c,"Mike Hobbins" \
                -a creator_email,global,o,c,"mike.hobbins@noaa.gov" \
                -a long_name,ETrs,o,c,"Reference Evapotranspiration for a tall reference crop (0.5-m alfalfa)" \
                -a units,ETrs,o,c,mm \
                -a history,global,d,, \
                -a GDAL,global,d,, \
                -a NCO,global,d,, ' \
                +proc+nc_file_name+' '+proc+nc_file_name)
    # ncks to chunk, deflate, and fix the unlimited dimension for read optimization.
    os.system('ncks -h -O --cnk_plc=g3d --cnk_dmn lat,40 --cnk_dmn lon,80 --cnk_dmn time,1 --fl_fmt=netcdf4 \
                --deflate=1 --fix_rec_dmn time '+proc+nc_file_name+' '+dest+nc_file_name)
    # Clean up the processing folder.
    os.system('rm '+proc+'*.nc')

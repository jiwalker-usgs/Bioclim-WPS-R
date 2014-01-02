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
    command=os.system('tar -C {0} -xzf {1}{2}'.format(proc,src,tarball))
    if command != 0:
        raise Exception('There was an error untarring %s.' % (tarball))
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
    command=os.system("{0} -q -of netCDF -co 'COMPRESS=DEFLATE' -co FORMAT=NC4 {1} {2}".format(gdal_translate_path,srcfile,tempfile))
    if command != 0:
        raise Exception('There was an error executing gdal_translate.')
    else:
        os.system('rm '+srcfile)

# Remove the .asc files from the processing directory that were not used/removed above.
os.system('x=$(find {0} -name "*.asc"); for f in $x; do rm $f; done'.format(proc))
print 'Completed gdal_translate'

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
    command=os.system('ncecat -h -O -u time {0}{1}{2}'.format(files_to_cat,proc,nc_file_name))
    # Clean up
    if command != 0:
        raise Exception('There was an error with ncecat.')
    else:
        for rm_file in file_list:
            command=os.system('rm '+proc+rm_file)
    # ncrename the gdal default variable Band1 to ETrs
    command=os.system('ncrename -h -O -v Band1,ETrs {0}{1}'.format(proc,nc_file_name))
    if command != 0:
        raise Exception('There was an error with ncrename.')
    # ncks to add the time coordinate variable. 
    command=os.system('ncks -h -A {0}{1}.nc {2}{3}'.format(time_files_path,str(year),proc,nc_file_name))
    if command != 0:
        raise Exception('There was an error with ncks adding time to the file.')
    # ncap2 to convert data to shorts with fixed precision of 0.01mm
    command=os.system('ncap2 -h -O --fl_fmt=netcdf4 -s "ETrs=short(100*ETrs)" {0}{1} {0}{1}'.format(proc,nc_file_name))
    if command != 0:
        raise Exception('There was an error with ncap2.')
    # ncatted to manipulate attributes of the file appropriately.
    command=os.system('ncatted -h -O -a scale_factor,ETrs,c,f,0.01 \
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
                -a NCO,global,d,, \
                {0}{1} {0}{1}'.format(proc,nc_file_name))
    if command != 0:
        raise Exception('There was an error with ncatted.')
    # ncks to chunk, deflate, and fix the unlimited dimension for read optimization.
    command=os.system('ncks -h -O --cnk_plc=g3d --cnk_dmn lat,40 --cnk_dmn lon,80 --cnk_dmn time,1 --fl_fmt=netcdf4 \
                --deflate=1 --fix_rec_dmn time {0}{1} {2}{1}'.format(proc,nc_file_name,dest))
    if command != 0:
        raise Exception('There was an error with ncks deflating the file.')
    else:
        command=os.system('rm {0}{1}'.format(proc,nc_file_name))

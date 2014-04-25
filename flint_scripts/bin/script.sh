#!/bin/bash

var=$1
scale=$2
scale_factor=$3
newmissing=$4
file=$5
SRC_DIR=$6
PROC_DIR=$7
DEST_DIR=$8
TIME_DIR=$9
t_nc_file=${10}
title=${11}
long_name=${12}
units=${13}
creator_name=${14}
creator_email=${15}

files=$(find ${SRC_DIR} -name "${var}*")

echo ${files}

var=${var:0:3}

if [[ -z "${files}" ]]; then
    echo "Didn't find any files for ${var}"
    exit 0
fi

files_to_cat=""

for f in $files; do
    outfile=${f//${SRC_DIR}/${PROC_DIR}}
    outfile=${outfile//.asc/.nc}
    /opt/local/bin/gdal_translate -q -of netCDF -co "FORMAT=NC4" -a_nodata -32768 -a_srs "+proj=aea +lat_1=34 +lat_2=40.5 +lat_0=0 +lon_0=-120 +x_0=0 +y_0=-4000000 +ellps=GRS80 +datum=NAD83 +units=m +no_defs" -scale 0 1 0 ${scale} -ot int16 ${f} ${outfile}
    files_to_cat="${files_to_cat} ${outfile}"
    ncrename -h -O -v Band1,${var} ${outfile}
    ncatted -h -O -a scale_factor,${var},c,f,${scale_factor} -a _FillValue,${var},o,f,${newmissing} -a missing_value,${var},o,f,${newmissing} -a Metadata_Conventions,global,o,c,'Unidata Dataset Discovery v1.0' -a title,global,o,c,"${title}" -a creator_name,global,o,c,"${creator_name}" -a creator_email,global,o,c,${creator_email} -a long_name,${var},o,c,"${long_name}" -a units,${var},o,c,${units} -a history,global,d,, -a GDAL,global,d,, -a NCO,global,d,, ${outfile}
done
ncecat -h -O -u time ${files_to_cat} ${PROC_DIR}${file}
for f in $files; do
    outfile=${f//${SRC_DIR}/${PROC_DIR}}
    outfile=${outfile//.asc/.nc}
    rm ${outfile}
done
ncks -h -A ${TIME_DIR}${t_nc_file} ${PROC_DIR}${file}
ncks -h -O --cnk_plc=g3d --cnk_dmn lat,45 --cnk_dmn lon,35 --cnk_dmn time,1 --fl_fmt=netcdf4 --deflate=1 --fix_rec_dmn time ${PROC_DIR}${file} ${DEST_DIR}${file}
rm ${PROC_DIR}${file}
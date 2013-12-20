#!/bin/bash

# For CMIP3 BCCA! Note that some CMIP5 accronynms are used in variables.
#Uses output from fix_bcca_pr_bias_derive_ratios.sh (provided)
#applies a smoothed monthly bias correction to the mean

source etc/config
# source $4

GCM=$1
ENS=$2
RCP=$3

V="pr"

#warning cdo ymonmul (Warning): Grid longitudes differ!
#becuase of mixing -180 -> 180 and 0 -> 360 grids. Seems to work fine anyway.
[ -d ${OUTROOTDIR} ] || mkdir ${OUTROOTDIR}

#Directory structure like this: bcca/cccma_cgcm3_1.gregorian/20c3m/run1/pr/bcca/
GCMLOWER=$(echo ${GCM} | tr '[:upper:]' '[:lower:]')

#These files are provided and should be placed in the working directory.
CORRF=${WORKINGDIR}/${GCMLOWER}_${V}_${ENS}_1961-1999_monthly_12correctionratios.nc

#locations of daily GCM data
GCMD=${GCMROOTDIR}/${GCMLOWER}/${RCP}/${ENS}/${V}/bcca

#create list of files to apply correction to daily historical files
FLIST=`ls -1 ${GCMD} | grep \.nc | grep BCCA`

#To output a flat structure
OD=${OUTROOTDIR}/${GCMLOWER}

#To output the same folder structure.
#OD=${OUTROOTDIR}/${GCMLOWER}/${RCP}/day/${ENS}/${V}

#Create directories as needed. 
[ -d ${OD} ] || mkdir -p ${OD}

for IF in ${FLIST}; do
    echo "correcting ${IF}"
    #Temp File
    TF=${IF/'.nc.gz'/'.nc'}
    #Output File
    OF=${TF/'.nc'/'_corr.nc'}
    #I had the data gzipped at rest, this should come out in general.
    gunzip -c ${GCMD}/${IF} > ${WORKINGDIR}/${TF}
    #Apply correction.
    cdo -s -O ymonmul ${WORKINGDIR}/${TF} ${CORRF} ${WORKINGDIR}/${OF}
    #Use ncks to fix the time dimension and deflate the data in a chunked netcdf4 file. This is optimized for read performance.
    ncks --cnk_plc=g3d --cnk_dmn latitude,40 --cnk_dmn longitude,80 --cnk_dmn time,1 --fl_fmt=netcdf4 --deflate=1 --fix_rec_dmn time -O ${WORKINGDIR}/${OF} ${WORKINGDIR}/${OF}
    #Overwrite the history attribute to indicate what was done, not the big verbose message from CDO/NCO.
    ncatted -h -O -a history,global,o,c,"12/2013 corrected the historical bias in the mean"  ${WORKINGDIR}/${OF} ${OD}/${OF}
    #Remove Temp File, this could come out if not ungzipping.
    rm ${WORKINGDIR}/${TF}
    rm ${WORKINGDIR}/${OF}
    #exit
done


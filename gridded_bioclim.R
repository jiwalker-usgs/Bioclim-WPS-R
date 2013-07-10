# Define Inputs (will come from external call)
start <- "1961"
end <- "1962"
bbox_in<-c(-90,41,-90.5,41.5)
bioclims<-c(1,2)

OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/wicci/cmip3/20c3m"
tmax_var  <- "20c3m-cccma_cgcm3_1-tmax-01"
tmin_var <- "20c3m-cccma_cgcm3_1-tmin-01"
prcp_var <- "20c3m-cccma_cgcm3_1-prcp-01"
tave_var <- "NULL"


OPeNDAP_URI<-"http://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet"
tmax_var  <- "tmax"
tmin_var <- "tmin"
prcp_var <- "prcp"
tave_var <- "NULL"

OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/dcp/conus"
tmax_var  <- "ccsm-a1b-tmax-NAm-grid"
tmin_var <- "ccsm-a1b-tmin-NAm-grid"
prcp_var <- "ccsm-a1fi-pr-NAm-grid"
tave_var <- "NULL"

OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/prism"
tmax_var  <- "tmx"
tmin_var <- "tmn"
prcp_var <- "ppt"
tave_var <- "NULL"

library("ncdf4")
library("climates")
library("rgdal")
library("stats")
library("utils")
library("chron")
library("zoo")
dods_data <- nc_open(OPeNDAP_URI)
# Need to check if specified inputs exist in specified dataset and throw errors acordingly. 
# Get time index time origin.
time_units<-strsplit(dods_data$dim$time$units, " ")[[1]]
time_step<-time_units[1]
date_origin<-time_units[3]
time_origin<-"00:00:00"
if(length(time_units)==4) time_origin<-time_units[4]
cal_origin <- paste(date_origin, time_origin)
year_origin=as.numeric(strsplit(date_origin,'-')[[1]][1])
month_origin=as.numeric(strsplit(date_origin,'-')[[1]][2])
day_origin=as.numeric(strsplit(date_origin,'-')[[1]][3])
years=as.numeric(end)-as.numeric(start)
t_1 <- julian(strptime(paste(start,'-01-01 12:00',sep=''), '%Y-%m-%d %H:%M'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
t_2 <- julian(strptime(paste(end, '-01-01 00:00', sep=''), '%Y-%m-%d %H:%M'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
# Some simple time and bbox validation.
if (t_1<head(dods_data$dim$time$vals,1)) stop(paste("Submitted start date,",start, "is before the dataset's start date,",chron(head(dods_data$dim$time$vals,1),out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin))))
if (t_2>tail(dods_data$dim$time$vals,1)) stop(paste("Submitted end date,",end, "is after the dataset's end date,",chron(tail(dods_data$dim$time$vals,1),out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin))))
if (t_1>t_2) stop('Start date must be before end date.')
request_indices<-request_bbox(dods_data,tmax_var,bbox_in)
t_ind1 <- min(which(abs(dods_data$dim$time$vals-t_1)==min(abs(dods_data$dim$time$vals-t_1))))
t_ind2 <- max(which(abs(dods_data$dim$time$vals-t_2)==min(abs(dods_data$dim$time$vals-t_2))))
#Pull out data needed for calculations and writing geotiffs. 
# A loop should be introduced here to the end of the script to only pull in one year of data at a time.
lons<-dods_data$dim$lon$vals[lon1_index:lon2_index]
lats<-dods_data$dim$lat$vals[lat1_index:lat2_index]
time<-dods_data$dim$time$vals[t_ind1:t_ind2-1]
# Check for regular grid.
dif_lons = mean(diff(lons))
dif_lats = mean(diff(lats))
if (abs(abs(dif_lats)-abs(dif_lons))>0.00001)
  stop('The data source appears to be an irregular grid, this datatype is not supported.')
#tmax_data <- ncvar_get(dods_data, tmax_var, c(t_ind1,min(lat1_index,lat2_index),min(lon1_index,lon2_index)),c((t_ind2-t_ind1),(abs(lat1_index-lat2_index)+1),(abs(lon1_index-lon2_index)+1)),verbose=TRUE)
tmax_data <- ncvar_get(dods_data, tmax_var, c(min(lon1_index,lon2_index),min(lat1_index,lat2_index),t_ind1),c((abs(lon1_index-lon2_index)+1),(abs(lat1_index-lat2_index)+1),(t_ind2-t_ind1)))
tmin_data <- ncvar_get(dods_data, tmin_var, c(min(lon1_index,lon2_index),min(lat1_index,lat2_index),t_ind1),c((abs(lon1_index-lon2_index)+1),(abs(lat1_index-lat2_index)+1),(t_ind2-t_ind1)))
prcp_data <- ncvar_get(dods_data, prcp_var, c(min(lon1_index,lon2_index),min(lat1_index,lat2_index),t_ind1),c((abs(lon1_index-lon2_index)+1),(abs(lat1_index-lat2_index)+1),(t_ind2-t_ind1)))
if (tave_var!="NULL") tave_data <- ncvar_get(dods_data, tave_var, c(min(lon1_index,lon2_index),min(lat1_index,lat2_index),t_ind1),c((abs(lon1_index-lon2_index)+1),(abs(lat1_index-lat2_index)+1),(t_ind2-t_ind1))) else tave_data <- (tmax_data+tmin_data)/2
# The loops below calculate bioclim for each time series and assemble a matrix 'out_data' that is lon*lat X time steps X bioclim stats.
out_data <- array(dim=c(nrow(tmax_data)*ncol(tmax_data),years,length(bioclims)))
ind<-1
for (row in 1:nrow(tmax_data))
{
  for (col in 1:ncol(tmax_data))
  {
    if (dim(time)>12)
    {
      # Convert daily data to monthly in preperation for bioclim functions.
      tmax<-zoo(tmax_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin)))
      tmax<-aggregate(tmax, as.yearmon, mean)
      tmax<-matrix(fortify.zoo(tmax)$tmax,years,12)
      tmin<-zoo(tmin_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin)))
      tmin<-aggregate(tmin, as.yearmon, mean)
      tmin<-matrix(fortify.zoo(tmin)$tmin,years,12)
      prcp<-zoo(prcp_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin)))
      prcp<-aggregate(prcp, as.yearmon, mean)
      prcp<-matrix(fortify.zoo(prcp)$prcp,years,12)
      tave<-zoo(tave_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin)))
      tave<-aggregate(tave, as.yearmon, mean)
      tave<-matrix(fortify.zoo(tave)$tave,years,12)
    }
    else
    {
      tmax <- matrix(tmax_data[row,col,],years,12)
      tmin <- matrix(tmin_data[row,col,],years,12)
      prcp <- matrix(prcp_data[row,col,],years,12)
      tave <- matrix(tave_data[row,col,],years,12)
    }
    if (length(bioclims)==1 || years==1) # bioclim returns a vector rather than a dataFrame if only asked for one output.
    {
      bioclim<-bioclim(tmin=tmin, tmax=tmax, prec=prcp, tmean=tave, bioclims)
      dim(bioclim)<-c(years,length(bioclims))
      colnames(bioclim)<-paste('bioclim_',bioclims, sep='')
      bioclim<-data.frame(bioclim)
    }
    else
    {
      bioclim<-data.frame(bioclim(tmin=tmin, tmax=tmax, prec=prcp, tmean=tave, bioclims))
    }
    for (bclim in 1:length(bioclims))
    {
      for (t in 1:years)
      {
        out_data[ind,t,bclim] <- bioclim[t,bclim]
      }
    }
    ind<-ind+1
  }
}
# Create lat/lon points for cells for geotiff files to be written.
coords <- array(dim=c(length(lons)*length(lats),2))
ind<-1
for (row in 1:length(lons)) {
  for (col in length(lats):1)
  {coords[ind,1]<-lons[row]+dif_lons/2
   coords[ind,2]<-lats[col]-dif_lats/2
   ind<-ind+1
  }
}
# Step through bclims and time, one year at a time, writing out geotiff files.
for (bclim in 1:length(bioclims))
{
  file_bclim<-names(bioclim)[bclim]
  file_year<-as.numeric(start)
  for (t in 1:(years))
  {
    grid_data <- data.frame(out_data[,t,bclim])
    names(grid_data) <- names(bioclim)[bclim]
    data_to_write <- SpatialPixelsDataFrame(SpatialPoints(coords, proj4string = CRS("+init=epsg:4326")), grid_data, tolerance=0.0001)
    file_name<-paste(file_bclim,'_',file_year,'.tif',sep='')
    writeGDAL(data_to_write,file_name)
    file_year=file_year+1
  }
}
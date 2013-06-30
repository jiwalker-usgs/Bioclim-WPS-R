# Define Inputs (will come from external call)
start <- "1950"
end <- "1960"
bbox<-c(-88,41,-84,44)
OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/prism"
tmax_var  <- "tmx"
tmin_var <- "tmn"
prcp_var <- "ppt"
tave_var <- "NULL"
bioclims<-c(1,2,3)

library("ncdf4")
library("climates")
library("rgdal")
library("stats")
library("utils")
library("chron")
dods_data <- nc_open(OPeNDAP_URI)
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
t_1 <- julian(strptime(paste(start,'-01-01',sep=''), '%Y-%m-%d'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
t_2 <- julian(strptime(paste(end, '-01-01', sep='') '%Y-%m-%d'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
# Some simple time and bbox validation.
if (t_1<head(dods_data$dim$time$vals,1)) stop(paste("Submitted start date,",start, "is before the dataset's start date,",chron(head(dods_data$dim$time$vals,1),out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin))))
if (t_2>tail(dods_data$dim$time$vals,1)) stop(paste("Submitted end date,",end, "is after the dataset's end date,",chron(tail(dods_data$dim$time$vals,1),out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin))))
if (t_1>t_2) stop('Start date must be before end date.')
if (bbox[1]<min(dods_data$dim$lon$vals)) stop(paste("Submitted minimum longitude",bbox[1], "is outside the dataset's minimum",min(dods_data$dim$lon$vals)))
if (bbox[2]<min(dods_data$dim$lat$vals)) stop(paste("Submitted minimum latitude",bbox[2], "is outside the dataset's minimum",min(dods_data$dim$lat$vals)))
if (bbox[3]>max(dods_data$dim$lon$vals)) stop(paste("Submitted maximum longitude",bbox[3], "is outside the dataset's maximum",max(dods_data$dim$lon$vals)))
if (bbox[4]>max(dods_data$dim$lat$vals)) stop(paste("Submitted maximum latitude",bbox[4], "is outside the dataset's maximum",max(dods_data$dim$lat$vals)))
# Search for time and lot/lon indices cooresponding to start and end dates.
t_ind1 <- min(which(abs(dods_data$dim$time$vals-t_1)==min(abs(dods_data$dim$time$vals-t_1))))
t_ind2 <- max(which(abs(dods_data$dim$time$vals-t_2)==min(abs(dods_data$dim$time$vals-t_2))))
lon1_index <- which(abs(dods_data$dim$lon$vals-bbox[1])==min(abs(dods_data$dim$lon$vals-bbox[1])))
lat1_index <- which(abs(dods_data$dim$lat$vals-bbox[2])==min(abs(dods_data$dim$lat$vals-bbox[2])))
lon2_index <- which(abs(dods_data$dim$lon$vals-bbox[3])==min(abs(dods_data$dim$lon$vals-bbox[3])))                 
lat2_index <- which(abs(dods_data$dim$lat$vals-bbox[4])==min(abs(dods_data$dim$lat$vals-bbox[4])))
# Check to see if multiple indices were found and buffer out if they were.
if(length(lon1_index)==2) if((bbox[1]-dods_data$dim$lon$vals[lon1_index[1]])>(bbox[1]-dods_data$dim$lon$vals[lon1_index[2]])) lon1_index<-lon1_index[1] else lon1_index<-lon1_index[2]  
if(length(lat1_index)==2) if((bbox[2]-dods_data$dim$lat$vals[lat1_index[1]])>(bbox[2]-dods_data$dim$lat$vals[lat1_index[2]])) lat1_index<-lat1_index[1] else lat1_index<-lat1_index[2]
if(length(lon2_index)==2) if((bbox[3]-dods_data$dim$lon$vals[lon2_index[1]])>(bbox[3]-dods_data$dim$lon$vals[lon2_index[2]])) lon2_index<-lon2_index[1] else lon2_index<-lon2_index[2]
if(length(lat2_index)==2) if((bbox[4]-dods_data$dim$lat$vals[lat2_index[1]])>(bbox[4]-dods_data$dim$lat$vals[lat2_index[2]])) lat2_index<-lat2_index[1] else lat2_index<-lat2_index[2]
#Pull out data needed for calculations and writing geotiffs. 
# A loop should be introduced here to the end of the script to only pull in one year of data at a time.
lons<-dods_data$dim$lon$vals[lon1_index:lon2_index]
lats<-dods_data$dim$lat$vals[lat1_index:lat2_index]
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
    tmax <- matrix(tmax_data[row,col,],years,12)
    tmin <- matrix(tmin_data[row,col,],years,12)
    prcp <- matrix(prcp_data[row,col,],years,12)
    tave <- matrix(tave_data[row,col,],years,12)
    if (length(bioclims)==1) # bioclim returns a vector rather than a dataFrame if only asked for one output.
    {
      bioclim<-bioclim(tmin=tmin, tmax=tmax, prec=prcp, tmean=tave, bioclims)
      dim(bioclim)<-c(years,1)
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
        out_data[ind,t,bclim] <- (bioclim[t,1])
      }
    }
    ind<-ind+1
  }
}
# Create lat/lon points for cells for geotiff files to be written.
coords <- array(dim=c(length(lons)*length(lats),2))
ind<-1
dif_lons = mean(diff(lons))
dif_lats = mean(diff(lats))
if (abs(dif_lats-dif_lons)>0.00001)
  stop('The data source appears to be an irregular grid, this datatype is not supported.')
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
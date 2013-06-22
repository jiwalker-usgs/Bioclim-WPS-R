# Define Inputs (will come from external call)
# The OPeNDAP Calendar or Time Variable Name.
cal_var = "time"
# Start and end dates in '%Y-%m-%d format
start = "1950-01-01"
end = "1990-12-31"
lat_var = "latitude"
lon_var = "longitude"
lat_in = 43.00
lon_in=-90.00
bbox=c(-90,43,-89,44)
# The variable of interest
data_var  = "sresa1b_bccr-bcm2-0_1_Tavg"
# The OPeNDAP URI of interest
OPeNDAP_URI="http://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml"

library("ncdf4")
gmo = nc_open(OPeNDAP_URI)
# Get time index time origin.
time_units<-strsplit(ncatt_get(gmo, cal_var, 'units')[2]$value, " ")[[1]]
time_step<-time_units[1]
date_origin<-time_units[3]
time_origin<-"00:00:00"
if(length(time_units)==4) time_origin<-time_units[4]
cal_origin <- paste(date_origin, time_origin)
t_1 <- julian(strptime(start, '%Y-%m-%d'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
t_2 <- julian(strptime(end, '%Y-%m-%d'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
t <- ncvar_get(gmo, cal_var, 1, -1)
inds <- (1:dim(t))
t_ind1 <- min(which(abs(t-t_1)==min(abs(t-t_1))))
t_ind2 <- max(which(abs(t-t_2)==min(abs(t-t_2))))
lat <- ncvar_get(gmo, lat_var, 1, -1)
lon <- ncvar_get(gmo, lon_var, 1, -1)
lon1_index = which(abs(lon-bbox[1])==min(abs(lon-bbox[1])))
lat1_index = which(abs(lat-bbox[2])==min(abs(lat-bbox[2])))
lon2_index = which(abs(lon-bbox[3])==min(abs(lon-bbox[3])))                 
lat2_index = which(abs(lat-bbox[4])==min(abs(lat-bbox[4])))
if(length(lon1_index)==2) if((bbox[1]-lon[lon1_index[1]])>(bbox[1]-lon[lon1_index[2]])) lon1_index<-lon1_index[1] else lon1_index<-lon1_index[2]  
if(length(lat1_index)==2) if((bbox[2]-lat[lat1_index[1]])>(bbox[2]-lat[lat1_index[2]])) lat1_index<-lat1_index[1] else lat1_index<-lat1_index[2]
if(length(lon2_index)==2) if((bbox[3]-lon[lon2_index[1]])>(bbox[3]-lon[lon2_index[2]])) lon2_index<-lon2_index[1] else lon2_index<-lon2_index[2]
if(length(lat2_index)==2) if((bbox[4]-lon[lat2_index[1]])>(bbox[4]-lat[lat2_index[2]])) lat2_index<-lat2_index[1] else lat2_index<-lat2_index[2]

data = ncvar_get(gmo, data_var, c(min(lon1_index,lon2_index),min(lat1_index,lat2_index),t_ind1),c((abs(lon1_index-lon2_index)),(abs(lat1_index-lat2_index)),(t_ind2-t_ind1)))

# wps.des: id = bioclim_prism, title = Annual BioClim from PRISM Data for a Single Point, abstract = Calculates 19 BioClim indices from the PRISM dataset for the specified time period for the specified lat/lon location. The time period must resolve to a whole number of years If the lat/lon is outside the PRISM dataset the nearest grid cell to the point of interest will be used; 
# wps.in: start, string, Start Date, Start Date in %Y-%m-%d (ie. 1950-01-01) format.;
# wps.in: end, string, End Date, End Date in %Y-%m-%d (ie. 2000-01-01) format.;
# wps.in: lat_in, string, Latitude, Latitude of point of interest.;
# wps.in: lon_in, string, Longitude, Longitude of point of interest.;
#wps.in: ids, string, Point Ids, Identifiers for points entered as lat/lon pairs.;

# *** Comment out inputs for use with the WPS framework. ***
# Start and end dates in '%Y-%m-%d format
# start = "1950-01-01"
# end = "2000-01-01"

# Latitude and Longitude in Decimal Degrees in WGS84 or compatible datum.
# lat_in <- '43.00, 42.00'
# lon_in <- '-90.00, -91.00'
lat_in <- read.csv(header=F,colClasses=c("character"),text=lat_in)
lat_in <- as.double(lat_in)
lon_in <- read.csv(header=F,colClasses=c("character"),text=lon_in)
lon_in <- as.double(lon_in)
# ids list to correspond to lat lon lists.
# ids = 'a, b'
ids = read.csv(header=F,colClasses=c("character"),text=ids)
if (length(lat_in)!=length(lon_in)) {
	stop('Latitude longitude lists are not the same length')
}
if (length(lat_in)!=length(ids)) {
	stop('ids list must be the same length as the latitude longitude lists.')
}
# The OPeNDAP Calendar or Time Variable Name.
cal_var = "time"
# The starting date and time in '%Y-%m-%d %H:%M:%S' format
cal_origin = "1858-11-17 00:00:00"
# OPeNDAP lat and lon variables.
lat_var = "lat"
lon_var = "lon"

# The variables of interest
tmax_var  = "tmx"
tmin_var = "tmn"
prcp_var = "ppt"
tave_var = "NULL"

# The OPeNDAP URI of interest
OPeNDAP_URI="http://cida.usgs.gov/qa/thredds/dodsC/prism"

library("ncdf4")
library("climates")
# Load the OPeNDAP URI as a ncdf4 object.
dods_data = nc_open(OPeNDAP_URI)
# get the time dimension of the ncdf4 object.
t = ncvar_get(dods_data, cal_var, 1, -1)
# find the nearest index to the specified start and end time.
inds=(1:dim(t))
t_1 = julian(strptime(start, '%Y-%m-%d'), origin=strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
if (end!="NULL") t_2 = julian(strptime(end, '%Y-%m-%d'), 
                                 origin=strptime(cal_origin, '%Y-%m-%d %H:%M:%S')) else t_2 = t_1+t[dim(t)]
t_ind1=which(abs(t-as.integer(t_1))==min(abs(t-as.integer(t_1))))
if(length(t_ind1)==2)
  t_ind1=min(t_ind1)
t_ind2=which(abs(t-as.integer(t_2))==min(abs(t-as.integer(t_2))))
if(length(t_ind2)==2)
  t_ind2=min(t_ind2)
# Check if the time period returned makes up a whole number of years, if not, stop and return an error.
years = (t_ind2-t_ind1)/12
if (as.integer(years)==years)
  print(paste(as.character(years), "years will be processed")) else 
    stop(paste("A whole number of years must be submitted for processing. ", years, "were returned for the time period requested"))
for (point in 1:length(lat_in)) {
	# Find lat and lon indices.
	lat = ncvar_get(dods_data, lat_var, 1, -1)
	lon = ncvar_get(dods_data, lon_var, 1, -1)
	lat_index = which(abs(lat-lat_in[point])==min(abs(lat-lat_in[point])))
	if(length(lat_index)==2)
	  lat_index=min(lat_index)
	lon_index = which(abs(lon-lon_in[point])==min(abs(lon-lon_in[point])))
	if(length(lon_index)==2)
	  lon_index=min(lon_index)
	# Get data for lat/lon and time period.
	tmax = ncvar_get(dods_data, tmax_var, c(lon_index,lat_index,t_ind1),c(1,1,(t_ind2-t_ind1)))
	tmin = ncvar_get(dods_data, tmin_var, c(lon_index,lat_index,t_ind1),c(1,1,(t_ind2-t_ind1)))
	prcp = ncvar_get(dods_data, prcp_var, c(lon_index,lat_index,t_ind1),c(1,1,(t_ind2-t_ind1)))
	if (tave_var!="NULL") tave = ncvar_get(dods_data, tave_var, 
	                                       c(lon_index,lat_index,t_ind1),
	                                       c(1,1,(t_ind2-t_ind1))) else tave = (tmax+tmin)/2
	# Calculate BioClim
	tmax = matrix(tmax,dim(tmax)/12,12)
	tmin = matrix(tmin,dim(tmin)/12,12)
	prcp = matrix(prcp,dim(prcp)/12,12)
	tave = matrix(tave,dim(tave)/12,12)
	bioclim=bioclim(tmin=tmin, tmax=tmax, prec=prcp, tmean=tave)
	write(toString(ids[point]),file="output.txt", append=TRUE)
	write.table(bioclim,file="output.txt", append=TRUE)
}
output="output.txt"
#wps.out: output, text, output_file, A file containing 19 BioClim indices and one row per year of data processed.;
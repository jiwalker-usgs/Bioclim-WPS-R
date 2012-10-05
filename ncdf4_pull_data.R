# Define Inputs (will come from external call)
# The OPeNDAP Calendar or Time Variable Name.
cal_var = "time"
# The starting date and time in '%Y-%m-%d %H:%M:%S' format
cal_origin = "1950-01-01 00:00:00"
# Start and end dates in '%Y-%m-%d format
start = "1950-01-01"
end = "1990-12-31"
lat_var = "latitude"
lon_var = "longitude"
lat_in = 43.00
lon_in=-90.00
# The variable of interest
data_var  = "Tavg"
# The OPeNDAP URI of interest
OPeNDAP_URI="http://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml"

library("ncdf4")
gmo = nc_open(OPeNDAP_URI)
t_1 = julian(strptime(start, '%Y-%m-%d'),
                        origin=strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
t_2 = julian(strptime(end, '%Y-%m-%d'),
                origin=strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
t = ncvar_get(gmo, cal_var, 1, -1)
inds=(1:dim(t))
t_ind1=inds[t_1 == t]
t_ind2=inds[t_2 == t]
lat = ncvar_get(gmo, lat_var, 1, -1)
lon = ncvar_get(gmo, lon_var, 1, -1)
lat_index = which(abs(lat-lat_in)==min(abs(lat-lat_in)))
if(length(lat_index)==2)
  lat_index=min(lat_index)
lon_index = which(abs(lon-lon_in)==min(abs(lon-lon_in)))
if(length(lon_index)==2)
  lon_index=min(lon_index)

data = ncvar_get(gmo, data_var, c(lon_index,lat_index,t_ind1),c(1,1,(t_ind2-t_ind1)))

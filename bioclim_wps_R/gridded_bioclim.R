# wps.des: id = gridded_bioclim, title = A generalized bioclim algorithm, abstract = TBD; 
# wps.in: start, string, Start Year, Start Year (ie. 1950);
# wps.in: end, string, End Year, End Year (ie. 2000);
# wps.in: bbox_in, string, BBOX, Format, comma seperated min lat/lon max lat/lon;
# wps.in: bioclims, string, bioclims, list of bioclims of interest.;
# wps.in: OPeNDAP_URI, string, OPeNDAP URI, An OPeNDAP (dods) url for the climate dataset of interest.;
# wps.in: tmax_var, string, Tmax Variable, The variable from the OPeNDAP dataset to use as tmax.;
# wps.in: tmin_var, string, Tmin Variable, The variable from the OPeNDAP dataset to use as tmin.;
# wps.in: tave_var, string, Tave Variable, The variable from the OPeNDAP dataset to use as tave, can be "NULL".;
# wps.in: prcp_var, string, Prcp Variable, The variable from the OPeNDAP dataset to use as prcp.;
library("ncdf4")
library("climates")
library("rgdal")
library("stats")
library("chron")
library("zoo")

request_bbox<-function(ncdf4_handle,rep_var,bbox_in) {
  grid_mapping<-ncatt_get(ncdf4_handle, rep_var,'grid_mapping')
  if (!is.null(grid_mapping) && !is.null(ncdf4_handle$dim$x$vals))
  {
    grid_mapping_name<-grid_mapping$value
    grid_mapping_atts<-ncatt_get(ncdf4_handle, grid_mapping_name)
    x_vals<-ncdf4_handle$dim$x$vals
    y_vals<-ncdf4_handle$dim$y$vals
    bbox_indices<-CF_bbox_grid(x_vals,y_vals,bbox_in,grid_mapping_name,grid_mapping_atts)
  # Supports lat/lon that is NOT a 2D coordinate variable.
  } else if (!is.null(ncdf4_handle$dim$lon$vals) && length(dim(ncdf4_handle$dim$lon$vals)==1))
  {
    x_vals<-ncdf4_handle$dim$lon$vals
    y_vals<-ncdf4_handle$dim$lat$vals
    bbox_indices<-CF_bbox_grid(x_vals,y_vals,bbox_in)
  }
  return(bbox_indices)
}

dailyToMonthly<-function(daily_data, time, origin, cells)
{
  daily_data<-zoo(daily_data,chron(time,out.format=c(dates="year-m-day"), origin=origin))
  daily_data<-aggregate(daily_data, as.yearmon, mean)
  daily_data<-t(data.matrix(fortify.zoo(daily_data),cells)[1:12,2:(cells+1)])
  return(daily_data)
}

request_time_bounds<-function(ncdf4_handle,start,end){
  if (!is.null(ncdf4_handle$dim$time$units)) {
    time_units<-strsplit(ncdf4_handle$dim$time$units, " ")[[1]]
    time_dim<-ncdf4_handle$dim$time$vals
  } else if (!is.null(ncdf4_handle$dim$day$units)) {
    time_units<-strsplit(ncdf4_handle$dim$day$units, " ")[[1]]
    time_dim<-ncdf4_handle$dim$day$vals
  } else stop(paste("No time dimension found. Time dimensions called time and day are supported."))
  return(CF_date_range(time_units, time_dim, start, end))
}

bbox_in <- as.double(read.csv(header=F,colClasses=c("character"),text=bbox_in))
bioclims <- as.double(read.csv(header=F,colClasses=c("character"),text=bioclims))

tryCatch(ncdf4_handle <- nc_open(OPeNDAP_URI), error = function(e) 
  {
  cat("An error was encountered trying to open the OPeNDAP resource."); print(e)
  })
variables<-as.character(sapply(ncdf4_handle$var,function(x) x$name))
#Check if variables exist.
if (!tmax_var %in% variables) stop(paste("The given tmax variable wasn't found in the OPeNDAP dataset"))
if (!tmin_var %in% variables) stop(paste("The given tmin variable wasn't found in the OPeNDAP dataset"))
if (!prcp_var %in% variables) stop(paste("The given prcp variable wasn't found in the OPeNDAP dataset"))
if (tave_var!="NULL") if (!tmax_var %in% variables) stop(paste("The given tave variable wasn't found in the OPeNDAP dataset"))
#Set temperature unit conversion to 1 unless units are K or F.
t_unit_multiplier<-function(t) {t}
if (grepl('k',ncatt_get(ncdf4_handle, tmax_var,'units')$value, ignore.case = TRUE)) {t_unit_multiplier <- function(t) {t-273} }
if (grepl('f',ncatt_get(ncdf4_handle, tmax_var,'units')$value, ignore.case = TRUE)) {t_unit_multiplier <- function(t) {(t-32)*(5/9)} }
#Check if Bioclims in allowable set
valid_bioclims<-c(1:19)
if (any(!bioclims %in% valid_bioclims)) stop("Invalid Bioclim ids were submitted.")

request_bbox_indices<-request_bbox(ncdf4_handle,tmax_var,bbox_in)
x1<-request_bbox_indices$x1
y1<-request_bbox_indices$y1
x2<-request_bbox_indices$x2
y2<-request_bbox_indices$y2
x_index<-request_bbox_indices$x_index
y_index<-request_bbox_indices$y_index
prj<-request_bbox_indices$prj

# Check for regular grid.
dif_xs = mean(diff(x_index))
dif_ys = mean(diff(y_index))
if (abs(abs(dif_ys)-abs(dif_xs))>0.00001) stop('The data source appears to be an irregular grid, this datatype is not supported.')

# Create x/y points for cells for geotiff files to be written.
coords_master <- array(dim=c(length(x_index)*length(y_index),2))
coords_master[,1]<-rep(rev(x_index)+dif_ys/2,length(y_index))
coords_master[,2]<-rep(rev(y_index)-dif_ys/2,each=length(x_index))

fileNames<-array(dim=(as.numeric(end)-as.numeric(start))*length(bioclims))
fileStep<-1
for (year in as.numeric(start):(as.numeric(end)))
{
  #Call for time indices for this year
  request_time_indices<-request_time_bounds(ncdf4_handle,year,year+1)
  t_ind1 <- request_time_indices$t_ind1
  t_ind2<-request_time_indices$t_ind2
  time<-request_time_indices$time
  origin<-request_time_indices$origin
  # !!! Make sure this is robust for network failures. !!!
  tmax_data <- t_unit_multiplier(ncvar_get(ncdf4_handle, tmax_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1))))
  tmin_data <- t_unit_multiplier(ncvar_get(ncdf4_handle, tmin_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1))))
  prcp_data <- ncvar_get(ncdf4_handle, prcp_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  if (tave_var!="NULL") tave_data <- t_unit_multiplier(ncvar_get(ncdf4_handle, tave_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))) else tave_data <- (tmax_data+tmin_data)/2
  cells<-nrow(tmax_data)*ncol(tmax_data)
  #Convert result to matrix.
  tmax_data <- matrix(tmax_data,t_ind2-t_ind1,cells,byrow = TRUE)
  tmin_data <- matrix(tmin_data,t_ind2-t_ind1,cells,byrow = TRUE)
  prcp_data <- matrix(prcp_data,t_ind2-t_ind1,cells,byrow = TRUE)
  tave_data <- matrix(tave_data,t_ind2-t_ind1,cells,byrow = TRUE)
  if (dim(time)>12)
  {
    # Convert daily data to monthly in preperation for bioclim functions.
    time<-floor(time)
    tmax_data<-dailyToMonthly(tmax_data, time, origin, cells)
    tmin_data<-dailyToMonthly(tmin_data, time, origin, cells)
    prcp_data<-dailyToMonthly(prcp_data, time, origin, cells)
    tave_data<-dailyToMonthly(tave_data, time, origin, cells)
  }
  else
  {
    #Transpose
    tmax_data<-t(tmax_data)
    tmin_data<-t(tmin_data)
    prcp_data<-t(prcp_data)
    tave_data<-t(tave_data)
  }
  #remove cells that are NaNs.
  mask<-!is.na(prcp_data[,1])
  masked_coords<-coords_master[mask,]
  tmax_data<-tmax_data[mask,]
  tmin_data<-tmin_data[mask,]
  prcp_data<-prcp_data[mask,]
  tave_data<-tave_data[mask,]
  # Run BioClim
  bioclim_out<-data.frame(bioclim(tmin=tmin_data, tmax=tmax_data, prec=prcp_data, tmean=tave_data, bioclims))
  colnames(bioclim_out)<-paste('bioclim_',bioclims, sep='')
  for (bclim in names(bioclim_out))
  {
    file_name<-paste(bclim,'_',as.character(year),'.tif',sep='')
    fileNames[fileStep]<-file_name
    fileStep<-fileStep+1
    writeGDAL(SpatialPixelsDataFrame(SpatialPoints(masked_coords, proj4string = CRS(prj)), bioclim_out[bclim], tolerance=0.0001),file_name)
  }
}
name<-'bioclim.zip'
bioclim_zip<-zip(name,fileNames)
#wps.out: name, zip, bioclim_zip, A zip pf the resulting bioclim getiffs..;
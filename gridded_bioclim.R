library("ncdf4")
library("climates")
library("rgdal")
library("stats")
library("utils")
library("chron")
library("zoo")
download_time<-0
process_time<-0
file_time<-0
if (bioclims==-1)
  bioclims<-sequence(19)
# Define Inputs (will come from external call)
dods_data <- nc_open(OPeNDAP_URI)
# Need to check if specified inputs exist in specified dataset and throw errors acordingly. 
request_bbox_indices<-request_bbox(dods_data,tmax_var,bbox_in)
x1<-request_bbox_indices[1][[1]]
y1<-request_bbox_indices[2][[1]]
x2<-request_bbox_indices[3][[1]]
y2<-request_bbox_indices[4][[1]]
x_index<-request_bbox_indices[5][[1]]
y_index<-request_bbox_indices[6][[1]]
prj<-request_bbox_indices[7][[1]]
# Check for regular grid.
dif_xs = mean(diff(x_index))
dif_ys = mean(diff(y_index))
if (abs(abs(dif_ys)-abs(dif_xs))>0.00001)
  stop('The data source appears to be an irregular grid, this datatype is not supported.')
# Create x/y points for cells for geotiff files to be written.
coords <- array(dim=c(length(x_index)*length(y_index),2))
coords[,1]<-rep(x_index+dif_ys/2,each=length(y_index))
coords[,2]<-rep(rev(y_index)-dif_ys/2,length(x_index))
#Pull out data needed for calculations and writing geotiffs. 
years<-as.numeric(end)-as.numeric(start)
for (year in as.numeric(start):(as.numeric(end)-1))
{
  # Get time index time origin.
  request_time_indices<-request_time_bounds(dods_data,year,year+1)
  t_ind1 <- request_time_indices$t_ind1
  t_ind2<-request_time_indices$t_ind2
  time<-request_time_indices$time
  origin<-request_time_indices$origin
  t<-proc.time()
  # Make sure this is robust for network failures.
  #tmax_data <- ncvar_get(dods_data, tmax_var, c(t_ind1,min(y1,y2),min(x1,x2)),c((t_ind2-t_ind1),(abs(y1-y2)+1),(abs(x1-x2)+1)),verbose=TRUE)
  tmax_data <- ncvar_get(dods_data, tmax_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  tmin_data <- ncvar_get(dods_data, tmin_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  prcp_data <- ncvar_get(dods_data, prcp_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  if (tave_var!="NULL") tave_data <- ncvar_get(dods_data, tave_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1))) else tave_data <- (tmax_data+tmin_data)/2
  download_time<-download_time+proc.time()-t
  # The loops below calculate bioclim for each time series and assemble a matrix 'out_data' that is lon*lat X time steps X bioclim stats.
  out_data <- array(dim=c(nrow(tmax_data)*ncol(tmax_data),length(bioclims)))
  ind<-1
  t<-proc.time()
  cells<-nrow(tmax_data)*ncol(tmax_data)
  tmax_data <- matrix(tmax_data,t_ind2-t_ind1,cells)
  tmin_data <- matrix(tmin_data,cells)
  prcp_data <- matrix(prcp_data,cells)
  tave_data <- matrix(tave_data,cells)
  if (dim(time)>12)
  {
    # Convert daily data to monthly in preperation for bioclim functions.
    time<-floor(time)
    tmax_data<-zoo(tmax_data,chron(time,out.format=c(dates="year-m-day"), origin=origin))
    tmax_data<-aggregate(tmax_data, as.yearmon, mean)
    tmax_data<-matrix(fortify.zoo(tmax_data),cells,12) # This is close, not sure why this is getting the date values too.
    tmin_data<-zoo(tmin_data,chron(time,out.format=c(dates="year-m-day"), origin=origin))
    tmin_data<-aggregate(tmin_data, as.yearmon, mean)
    tmin_data<-matrix(fortify.zoo(tmin_data)$tmin,1,12)
    prcp_data<-zoo(prcp_data,chron(time,out.format=c(dates="year-m-day"), origin=origin))
    prcp_data<-aggregate(prcp_data, as.yearmon, mean)
    prcp_data<-matrix(fortify.zoo(prcp_data)$prcp,1,12)
    tave_data<-zoo(tave_data,chron(time,out.format=c(dates="year-m-day"), origin=origin))
    tave_data<-aggregate(tave_data, as.yearmon, mean)
    tave_data<-matrix(fortify.zoo(tave_data)$tave,1,12)
  }
  bioclim<-bioclim(tmin=tmin, tmax=tmax, prec=prcp, tmean=tave, bioclims)
  dim(bioclim)<-c(1,length(bioclims))
  colnames(bioclim)<-paste('bioclim_',bioclims, sep='')
  bioclim<-data.frame(bioclim)
  #for (bclim in 1:length(bioclims))
  out_data[ind,1,] <- bioclim[1,]
  ind<-ind+1
  process_time<-process_time+proc.time()-t
  # Step through bclims.
  t<-proc.time()
  for (bclim in 1:length(bioclims))
  {
    file_bclim<-names(bioclim)[bclim]
    grid_data <- data.frame(out_data[,1,bclim])
    names(grid_data) <- names(bioclim)[bclim]
    data_to_write <- SpatialPixelsDataFrame(SpatialPoints(coords, proj4string = CRS(prj)), grid_data, tolerance=0.0001)
    file_name<-paste(file_bclim,'_',as.character(t),'.tif',sep='')
    writeGDAL(data_to_write,file_name)
  }
  file_time<-file_time+proc.time()-t
  #also index the start time!
}
download_time
process_time
file_time
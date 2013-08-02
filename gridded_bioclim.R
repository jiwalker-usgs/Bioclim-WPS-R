<<<<<<< HEAD
# Define Inputs (will come from external call)
start <- "1980"
end <- "2020"
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

=======
>>>>>>> 1adb4746159735f17dfcf6e34ec1a908e0834af7
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
#if (bioclims==-1)
#  bioclims<-sequence(19)
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
# A loop should be introduced here to the end of the script to only pull in one year of data at a time.
years<-as.numeric(end)-as.numeric(start)
file_year<-as.numeric(start)
for (t in 1:(years))
{
  # Get time index time origin.
  request_time_indices<-request_time_bounds(dods_data,start,as.character(as.numeric(start)+1))
  t_ind1<-request_time_indices[1][[1]]
  t_ind2<-request_time_indices[2][[1]]
  time<-request_time_indices[3][[1]]
  origin<-request_time_indices[4][[1]]
  t<-proc.time()
  #tmax_data <- ncvar_get(dods_data, tmax_var, c(t_ind1,min(y1,y2),min(x1,x2)),c((t_ind2-t_ind1),(abs(y1-y2)+1),(abs(x1-x2)+1)),verbose=TRUE)
  tmax_data <- ncvar_get(dods_data, tmax_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  tmin_data <- ncvar_get(dods_data, tmin_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  prcp_data <- ncvar_get(dods_data, prcp_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  if (tave_var!="NULL") tave_data <- ncvar_get(dods_data, tave_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1))) else tave_data <- (tmax_data+tmin_data)/2
  download_time<-download_time+proc.time()-t
  # The loops below calculate bioclim for each time series and assemble a matrix 'out_data' that is lon*lat X time steps X bioclim stats.
  out_data <- array(dim=c(nrow(tmax_data)*ncol(tmax_data),1,length(bioclims)))
  ind<-1
  t<-proc.time()
  for (row in 1:nrow(tmax_data))
  {
    for (col in 1:ncol(tmax_data))
    {
      if (dim(time)>12)
      {
        # Convert daily data to monthly in preperation for bioclim functions.
        time<-floor(time)
        tmax<-zoo(tmax_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=origin))
        tmax<-aggregate(tmax, as.yearmon, mean)
        tmax<-matrix(fortify.zoo(tmax)$tmax,1,12)
        tmin<-zoo(tmin_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=origin))
        tmin<-aggregate(tmin, as.yearmon, mean)
        tmin<-matrix(fortify.zoo(tmin)$tmin,1,12)
        prcp<-zoo(prcp_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=origin))
        prcp<-aggregate(prcp, as.yearmon, mean)
        prcp<-matrix(fortify.zoo(prcp)$prcp,1,12)
        tave<-zoo(tave_data[row,col,],chron(time,out.format=c(dates="year-m-day"), origin=origin))
        tave<-aggregate(tave, as.yearmon, mean)
        tave<-matrix(fortify.zoo(tave)$tave,1,12)
      }
      else
      {
        tmax <- matrix(tmax_data[row,col,],1,12)
        tmin <- matrix(tmin_data[row,col,],1,12)
        prcp <- matrix(prcp_data[row,col,],1,12)
        tave <- matrix(tave_data[row,col,],1,12)
      }
      bioclim<-bioclim(tmin=tmin, tmax=tmax, prec=prcp, tmean=tave, bioclims)
      dim(bioclim)<-c(1,length(bioclims))
      colnames(bioclim)<-paste('bioclim_',bioclims, sep='')
      bioclim<-data.frame(bioclim)
      for (bclim in 1:length(bioclims))
        out_data[ind,1,bclim] <- bioclim[1,bclim]
      ind<-ind+1
    }
  }
  process_time<-process_time+proc.time()-t
  # Step through bclims.
  t<-proc.time()
  for (bclim in 1:length(bioclims))
  {
    file_bclim<-names(bioclim)[bclim]
    grid_data <- data.frame(out_data[,1,bclim])
    names(grid_data) <- names(bioclim)[bclim]
    data_to_write <- SpatialPixelsDataFrame(SpatialPoints(coords, proj4string = CRS(prj)), grid_data, tolerance=0.0001)
    file_name<-paste(file_bclim,'_',file_year,'.tif',sep='')
    writeGDAL(data_to_write,file_name)
  }
  file_year=file_year+1
  file_time<-file_time+proc.time()-t
}
download_time
process_time
file_time

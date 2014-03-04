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
library('rgdal')
request_bbox<-function(ncdf4_handle,rep_var,bbox_in) 
{
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

request_time_bounds<-function(ncdf4_handle,start,end)
{
  if (!is.null(ncdf4_handle$dim$time$units)) {
    time_units<-strsplit(ncdf4_handle$dim$time$units, " ")[[1]]
    time_dim<-ncdf4_handle$dim$time$vals
  } else if (!is.null(ncdf4_handle$dim$day$units)) {
    time_units<-strsplit(ncdf4_handle$dim$day$units, " ")[[1]]
    time_dim<-ncdf4_handle$dim$day$vals
  } else stop(paste("No time dimension found. Time dimensions called time and day are supported."))
  return(CF_date_range(time_units, time_dim, start, end))
}

init_dap_bclim<-function(OPeNDAP_URI,tmax_var,tmin_var,prcp_var,bioclims)
{
  tryCatch(ncdf4_handle <- nc_open(OPeNDAP_URI), error = function(e) 
  {
    cat("An error was encountered trying to open the OPeNDAP resource."); print(e)
  })
  
  variables<-as.character(sapply(ncdf4_handle$var,function(x) x$name))
  
  #Check if variables exist.
  if (!tmax_var %in% variables) stop(paste("The given tmax variable wasn't found in the OPeNDAP dataset"))
  if (!tmin_var %in% variables) stop(paste("The given tmin variable wasn't found in the OPeNDAP dataset"))
  if (!prcp_var %in% variables) stop(paste("The given prcp variable wasn't found in the OPeNDAP dataset"))
  if (!is.null(tave_var)) if (!tmax_var %in% variables) stop(paste("The given tave variable wasn't found in the OPeNDAP dataset"))
  
  #Set temperature unit conversion to 1 unless units are K or F.
  temp_unit_func<-function(t) {t}
  if (grepl('k',ncatt_get(ncdf4_handle, tmax_var,'units')$value, ignore.case = TRUE)) {temp_unit_func <- function(t) {t-273} }
  if (grepl('f',ncatt_get(ncdf4_handle, tmax_var,'units')$value, ignore.case = TRUE)) {temp_unit_func <- function(t) {(t-32)*(5/9)} }
  
  #Check if Bioclims in allowable set
  valid_bioclims<-c(1:19)
  if (any(!bioclims %in% valid_bioclims)) stop("Invalid Bioclim ids were submitted.")
  return(list(ncdf4_handle=ncdf4_handle,temp_unit_func=temp_unit_func))
}

get_dap_data<-function(ncdf4_handle,x1,y1,x2,y2,time,t_ind1,t_ind2,time_indices,origin,tmax_var,tmin_var,prcp_var,tave_var=NULL,temp_unit_func=NULL)
{
  #Can optionally pass in a function that will convert temperature on the fly.
  if (!is.null(temp_unit_func)) temp_unit_func<-function(t) {t}
  # !!! Make sure this is robust for network failures. !!!
  tmax_data <- temp_unit_func(ncvar_get(ncdf4_handle, tmax_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1))))
  tmin_data <- temp_unit_func(ncvar_get(ncdf4_handle, tmin_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1))))
  prcp_data <- ncvar_get(ncdf4_handle, prcp_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))
  if (!is.null(tave_var)) tave_data <- temp_unit_func(ncvar_get(ncdf4_handle, tave_var, c(min(x1,x2),min(y1,y2),t_ind1),c((abs(x1-x2)+1),(abs(y1-y2)+1),(t_ind2-t_ind1)))) else tave_data <- (tmax_data+tmin_data)/2
  cells<-nrow(tmax_data)*ncol(tmax_data)
  #Convert result to matrix.
  tmax_data <- matrix(tmax_data,t_ind2-t_ind1,cells,byrow = TRUE)
  tmin_data <- matrix(tmin_data,t_ind2-t_ind1,cells,byrow = TRUE)
  prcp_data <- matrix(prcp_data,t_ind2-t_ind1,cells,byrow = TRUE)
  tave_data <- matrix(tave_data,t_ind2-t_ind1,cells,byrow = TRUE)
  if (dim(time_indices)>12)
  {
    # Convert daily data to monthly in preperation for bioclim functions.
    time_indices<-floor(time_indices)
    tmax_data<-daily2monthly(tmax_data, time_indices, origin, cells)
    tmin_data<-daily2monthly(tmin_data, time_indices, origin, cells)
    prcp_data<-daily2monthly(prcp_data, time_indices, origin, cells)
    tave_data<-daily2monthly(tave_data, time_indices, origin, cells)
  }
  else
  {
    #Transpose
    tmax_data<-t(tmax_data)
    tmin_data<-t(tmin_data)
    prcp_data<-t(prcp_data)
    tave_data<-t(tave_data)
  }
  return(list(tmax_data=tmax_data,tmin_data=tmin_data,prcp_data=prcp_data,tave_data=tave_data))
}

dap_bioclim<-function(start,end,bbox_in,bioclims,OPeNDAP_URI,tmax_var,tmin_var,tave_var,prcp_var)
{
  te<-init_dap_bclim(OPeNDAP_URI,tmax_var,tmin_var,prcp_var,bioclims)
  ncdf4_handle<-te$ncdf4_handle; temp_unit_func<-te$temp_unit_func
  
  te2<-request_bbox(ncdf4_handle,tmax_var,bbox_in); x1<-te2$x1; y1<-te2$y1; x2<-te2$x2; 
  y2<-te2$y2; coords_master<-te2$coords_master; prj<-te2$prj
  
  fileNames<-c()
  for (year in as.numeric(start):(as.numeric(end)))
  {
    #Call for time indices for this year
    te3<-request_time_bounds(ncdf4_handle,year,year+1); t_ind1 <- te3$t_ind1; t_ind2<-te3$t_ind2; 
    time_indices<-te3$time; origin<-te3$origin
    
    #Get the dap data
    te4<-get_dap_data(ncdf4_handle,x1,y1,x2,y2,time,t_ind1,t_ind2,time_indices,origin,tmax_var,tmin_var,prcp_var,tave_var=NULL,temp_unit_func)
    tmax_data<-te4$tmax_data; tmin_data<-te4$tmin_data; prcp_data<-te4$prcp_data; tave_data<-te4$tave_data
    
    #Run Bioclim and write to geotiff.
    fileNames<-append(fileNames,bioclim2geotiff(tmax_data,tmin_data,prcp_data,tave_data,bioclims, coords_master, prj, year))
  }
  return(fileNames)
}

bbox_in <- as.double(read.csv(header=F,colClasses=c("character"),text=bbox_in))
bioclims <- as.double(read.csv(header=F,colClasses=c("character"),text=bioclims))
if (tave_var=="NULL") tave_var=NULL
fileNames<-dap_bioclim(start,end,bbox_in,bioclims,OPeNDAP_URI,tmax_var,tmin_var,tave_var,prcp_var)

name<-'bioclim.zip'
bioclim_zip<-zip(name,fileNames)
#wps.out: name, zip, bioclim_zip, A zip pf the resulting bioclim getiffs..;
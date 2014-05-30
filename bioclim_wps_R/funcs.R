

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

init_dap<-function(OPeNDAP_URI,tmax_var,tmin_var,prcp_var)
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
  
  return(list(ncdf4_handle=ncdf4_handle,temp_unit_func=temp_unit_func))
}

get_dap_data<-function(ncdf4_handle,x1,y1,x2,y2,time,t_ind1,t_ind2,origin,tmax_var,tmin_var,prcp_var,tave_var=NULL,temp_unit_func=NULL)
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
  return(list(tmax_data=tmax_data,tmin_data=tmin_data,prcp_data=prcp_data,tave_data=tave_data))
}

dap_daily_stats<-function(start,end,bbox_in,thresholds,OPeNDAP_URI,tmax_var,tmin_var,tave_var,prcp_var)
{
  
  te<-init_dap(OPeNDAP_URI,tmax_var,tmin_var,prcp_var)
  ncdf4_handle<-te$ncdf4_handle; temp_unit_func<-te$temp_unit_func
  
  te2<-request_bbox(ncdf4_handle,tmax_var,bbox_in); x1<-te2$x1; y1<-te2$y1; x2<-te2$x2; 
  y2<-te2$y2; coords_master<-te2$coords_master; prj<-te2$prj
  
  fileNames<-c()
  for (year in as.numeric(start):(as.numeric(end)))
  {
    #Call for time indices for this year
    te3<-request_time_bounds(ncdf4_handle,year,year+1); t_ind1 <- te3$t_ind1; t_ind2<-te3$t_ind2; 
    time_indices<-te3$time; origin<-te3$origin; time_PCICt<-as.PCICt(te3$time_posix,cal="gregorian")
    
    #Get the dap data
    te4<-get_dap_data(ncdf4_handle,x1,y1,x2,y2,time,t_ind1,t_ind2,origin,tmax_var,tmin_var,prcp_var,tave_var=NULL,temp_unit_func)
    tmax_data<-te4$tmax_data; tmin_data<-te4$tmin_data; prcp_data<-te4$prcp_data; tave_data<-te4$tave_data
    
    tmax_data<-t(tmax_data)
    tmin_data<-t(tmin_data)
    prcp_data<-t(prcp_data)
    tave_data<-t(tave_data)
    #Run stats and write to geotiff.
    fileNames<-append(fileNames,daily_indices2geotiff(tmax_data,tmin_data,prcp_data,tave_data,thresholds, coords_master, prj, year, time_PCICt))
  }
}

dap_bioclim<-function(start,end,bbox_in,bioclims,OPeNDAP_URI,tmax_var,tmin_var,tave_var,prcp_var)
{
  #Check if Bioclims in allowable set
  valid_bioclims<-c(1:19)
  if (any(!bioclims %in% valid_bioclims)) stop("Invalid Bioclim ids were submitted.")
  
  te<-init_dap(OPeNDAP_URI,tmax_var,tmin_var,prcp_var)
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
    te4<-get_dap_data(ncdf4_handle,x1,y1,x2,y2,time,t_ind1,t_ind2,origin,tmax_var,tmin_var,prcp_var,tave_var=NULL,temp_unit_func)
    tmax_data<-te4$tmax_data; tmin_data<-te4$tmin_data; prcp_data<-te4$prcp_data; tave_data<-te4$tave_data
    if (dim(time_indices)>12)
    {
      # Convert daily data to monthly in preperation for bioclim functions.
      time_indices<-floor(time_indices)
      tmax_data<-daily2monthly(tmax_data, time_indices, origin)
      tmin_data<-daily2monthly(tmin_data, time_indices, origin)
      prcp_data<-daily2monthly(prcp_data, time_indices, origin)
      tave_data<-daily2monthly(tave_data, time_indices, origin)
    }
    else
    {
      #Transpose
      tmax_data<-t(tmax_data)
      tmin_data<-t(tmin_data)
      prcp_data<-t(prcp_data)
      tave_data<-t(tave_data)
    }
    #Run Bioclim and write to geotiff.
    fileNames<-append(fileNames,bioclim2geotiff(tmax_data,tmin_data,prcp_data,tave_data,bioclims, coords_master, prj, year))
  }
  return(fileNames)
}
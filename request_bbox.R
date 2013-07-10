library("ncdf4")
library("rgdal")
request_bbox<-function(ncdf4_handle,rep_var,bbox)
{
  if (!is.null(ncatt_get(ncdf4_handle, rep_var,'grid_mapping')) && !is.null(ncdf4_handle$dim$x$vals))
  {
    if (ncatt_get(ncdf4_handle, ncatt_get(ncdf4_handle, rep_var,'grid_mapping')$value, 'grid_mapping_name')$value=='lambert_conformal_conic')
    {
      grid_mapping_name<-ncatt_get(ncdf4_handle, rep_var,'grid_mapping')$value
      longitude_of_central_meridian<-ncatt_get(ncdf4_handle, grid_mapping_name, 'longitude_of_central_meridian')$value
      latitude_of_projection_origin<-ncatt_get(ncdf4_handle, grid_mapping_name, 'latitude_of_projection_origin')$value
      standard_parallel<-ncatt_get(ncdf4_handle, grid_mapping_name, 'standard_parallel')$value
      false_easting<-ncatt_get(ncdf4_handle, grid_mapping_name, 'false_easting')$value
      false_northing<-ncatt_get(ncdf4_handle, grid_mapping_name, 'false_northing')$value
      longitude_of_prime_meridian<-ncatt_get(ncdf4_handle, grid_mapping_name, 'longitude_of_prime_meridian')$value
      semi_major_axis<-ncatt_get(ncdf4_handle, grid_mapping_name, 'semi_major_axis')$value
      inverse_flattening<-ncatt_get(ncdf4_handle, grid_mapping_name, 'inverse_flattening')$value
      if (length(standard_parallel==2))
      {
        prj <- paste("+proj=lcc +lat_1=", standard_parallel[1],
                     " +lat_2=", standard_parallel[2],
                     " +lat_0=", latitude_of_projection_origin,
                     " +lon_0=", longitude_of_central_meridian,
                     " +x_0=", false_easting,
                     " +y_0=", false_northing,
                     " +a=", semi_major_axis,
                     " +f=", (1/inverse_flattening),
                     sep='')
      }
      else
      {
        prj <- paste("+proj=lcc +lat_1=", standard_parallel[1],
                     " +lat_2=", standard_parallel[1],
                     " +lat_0=", latitude_of_projection_origin,
                     " +lon_0=", longitude_of_central_meridian,
                     " +x_0=", false_easting,
                     " +y_0=", false_northing,
                     " +a=", semi_major_axis,
                     " +f=", (1/inverse_flattening),
                     sep='') 
      }
      # Project bbox and unproject data-source range to check intersection.
      # preparing bbox for projection.
      bbox_unproj<-data.frame(matrix(c(bbox, bbox[1],bbox[4],bbox[3],bbox[2]),ncol=2,byrow=TRUE))
      colnames(bbox_unproj)<-c("x","y")
      coordinates(bbox_unproj)<-c("x","y")
      proj4string(bbox_unproj) <- CRS("+init=epsg:4326")
      bbox_proj<-spTransform(bbox_unproj,CRS(prj)) # Project bbox.
      bbox_proj_coords<-coordinates(bbox_proj)
      # Get projected bounds
      min_dods_x<-min(ncdf4_handle$dim$x$vals)
      max_dods_x<-max(ncdf4_handle$dim$x$vals)
      min_dods_y<-min(ncdf4_handle$dim$y$vals)
      max_dods_y<-max(ncdf4_handle$dim$y$vals)
      # Prepare projected bounds to be unprojected.
      ncdf4_handle_range<-data.frame(matrix(c(min_dods_x,min_dods_y,max_dods_x,max_dods_y,min_dods_x,max_dods_y,max_dods_x,min_dods_y),ncol=2,byrow=TRUE))
      colnames(ncdf4_handle_range)<-c("x","y")
      coordinates(ncdf4_handle_range)<-c("x","y")
      proj4string(ncdf4_handle_range) <- CRS(prj)
      ncdf4_handle_range_unproj<-spTransform(ncdf4_handle_range,CRS("+init=epsg:4326"))
      ncdf4_handle_range_unproj_coords<-coordinates(ncdf4_handle_range_unproj)
      # Coding against daymet for now, need to find a way to identify the coordinate variable for requested variables and use that name rather than the hardcoded x and y.
      # Check lower left.
      if (bbox_proj_coords[1]<min_dods_x || bbox_proj_coords[1]>max_dods_x) stop(paste("Submitted minimum longitude",bbox[1], "is outside the dataset's minimum",ncdf4_handle_range_unproj_coords[1]))
      if (bbox_proj_coords[3]<min_dods_y || bbox_proj_coords[3]>max_dods_y) stop(paste("Submitted minimum latitude",bbox[2], "is outside the dataset's minimum",ncdf4_handle_range_unproj_coords[2]))
      # Check upper right.
      if (bbox_proj_coords[2]<min_dods_x || bbox_proj_coords[2]>max_dods_x) stop(paste("Submitted maximum longitude",bbox[3], "is outside the dataset's maximum",ncdf4_handle_range_unproj_coords[3]))
      if (bbox_proj_coords[4]<min_dods_y || bbox_proj_coords[4]>max_dods_y) stop(paste("Submitted maximum latitude",bbox[4], "is outside the dataset's maximum",ncdf4_handle_range_unproj_coords[4]))
      # Check upper left.
      if (bbox_proj_coords[5]<min_dods_x || bbox_proj_coords[5]>max_dods_x) stop(paste("Submitted minimum longitude",bbox[1], "is outside the dataset's minimum",ncdf4_handle_range_unproj_coords[1]))
      if (bbox_proj_coords[6]<min_dods_y || bbox_proj_coords[6]>max_dods_y) stop(paste("Submitted minimum latitude",bbox[2], "is outside the dataset's minimum",ncdf4_handle_range_unproj_coords[2]))
      # Check lower right.
      if (bbox_proj_coords[7]<min_dods_x || bbox_proj_coords[7]>max_dods_x) stop(paste("Submitted maximum longitude",bbox[3], "is outside the dataset's maximum",ncdf4_handle_range_unproj_coords[3]))
      if (bbox_proj_coords[8]<min_dods_y || bbox_proj_coords[8]>max_dods_y) stop(paste("Submitted maximum latitude",bbox[4], "is outside the dataset's maximum",ncdf4_handle_range_unproj_coords[4]))
      bbox<-bbox_proj_coords
      x1 <- which(abs(ncdf4_handle$dim$x$vals-bbox[1])==min(abs(ncdf4_handle$dim$x$vals-bbox[1])))
      y1 <- which(abs(ncdf4_handle$dim$y$vals-bbox[2])==min(abs(ncdf4_handle$dim$y$vals-bbox[2])))
      x2 <- which(abs(ncdf4_handle$dim$x$vals-bbox[3])==min(abs(ncdf4_handle$dim$x$vals-bbox[3])))                 
      y2 <- which(abs(ncdf4_handle$dim$y$vals-bbox[4])==min(abs(ncdf4_handle$dim$y$vals-bbox[4])))
      # Check to see if multiple indices were found and buffer out if they were.
      if(length(x1)==2) if((bbox[1]-ncdf4_handle$dim$x$vals[x1[1]])>(bbox[1]-ncdf4_handle$dim$x$vals[x1[2]])) x1<-x1[1] else x1<-x1[2]  
      if(length(y1)==2) if((bbox[2]-ncdf4_handle$dim$y$vals[y1[1]])>(bbox[2]-ncdf4_handle$dim$y$vals[y1[2]])) y1<-y1[1] else y1<-y1[2]
      if(length(x2)==2) if((bbox[3]-ncdf4_handle$dim$x$vals[x2[1]])>(bbox[3]-ncdf4_handle$dim$x$vals[x2[2]])) x2<-x2[1] else x2<-x2[2]
      if(length(y2)==2) if((bbox[4]-ncdf4_handle$dim$y$vals[y2[1]])>(bbox[4]-ncdf4_handle$dim$y$vals[y2[2]])) y2<-y2[1] else y2<-y2[2]
      x_index<-dods_data$dim$x$vals[x1:x2]
      y_index<-dods_data$dim$y$vals[y1:y2]
    }
    else
    {
      stop('Unsupported Projection Found in Source Data.')
    }
  }
  if (!is.null(ncdf4_handle$dim$lat$vals) && length(dim(ncdf4_handle$dim$lat$vals)==1))
  {
    if (max(ncdf4_handle$dim$lon$vals)>180 || max(ncdf4_handle$dim$lat$vals)>180) 
    {
      bbox[1]=bbox[1]+360
      bbox[3]=bbox[3]+360
    }
    if (bbox[1]<min(ncdf4_handle$dim$lon$vals)) stop(paste("Submitted minimum longitude",bbox[1], "is outside the dataset's minimum",min(ncdf4_handle$dim$lon$vals)))
    if (bbox[2]<min(ncdf4_handle$dim$lat$vals)) stop(paste("Submitted minimum latitude",bbox[2], "is outside the dataset's minimum",min(ncdf4_handle$dim$lat$vals)))
    if (bbox[3]>max(ncdf4_handle$dim$lon$vals)) stop(paste("Submitted maximum longitude",bbox[3], "is outside the dataset's maximum",max(ncdf4_handle$dim$lon$vals)))
    if (bbox[4]>max(ncdf4_handle$dim$lat$vals)) stop(paste("Submitted maximum latitude",bbox[4], "is outside the dataset's maximum",max(ncdf4_handle$dim$lat$vals)))
    # Search for x/y indices cooresponding to start and end dates.
    lon1_index <- which(abs(ncdf4_handle$dim$lon$vals-bbox[1])==min(abs(ncdf4_handle$dim$lon$vals-bbox[1])))
    lat1_index <- which(abs(ncdf4_handle$dim$lat$vals-bbox[2])==min(abs(ncdf4_handle$dim$lat$vals-bbox[2])))
    lon2_index <- which(abs(ncdf4_handle$dim$lon$vals-bbox[3])==min(abs(ncdf4_handle$dim$lon$vals-bbox[3])))                 
    lat2_index <- which(abs(ncdf4_handle$dim$lat$vals-bbox[4])==min(abs(ncdf4_handle$dim$lat$vals-bbox[4])))
    # Check to see if multiple indices were found and buffer out if they were.
    if(length(lon1_index)==2) if((bbox[1]-ncdf4_handle$dim$lon$vals[lon1_index[1]])>(bbox[1]-ncdf4_handle$dim$lon$vals[lon1_index[2]])) lon1_index<-lon1_index[1] else lon1_index<-lon1_index[2]  
    if(length(lat1_index)==2) if((bbox[2]-ncdf4_handle$dim$lat$vals[lat1_index[1]])>(bbox[2]-ncdf4_handle$dim$lat$vals[lat1_index[2]])) lat1_index<-lat1_index[1] else lat1_index<-lat1_index[2]
    if(length(lon2_index)==2) if((bbox[3]-ncdf4_handle$dim$lon$vals[lon2_index[1]])>(bbox[3]-ncdf4_handle$dim$lon$vals[lon2_index[2]])) lon2_index<-lon2_index[1] else lon2_index<-lon2_index[2]
    if(length(lat2_index)==2) if((bbox[4]-ncdf4_handle$dim$lat$vals[lat2_index[1]])>(bbox[4]-ncdf4_handle$dim$lat$vals[lat2_index[2]])) lat2_index<-lat2_index[1] else lat2_index<-lat2_index[2]
    x_index<-dods_data$dim$lon$vals[lon1_index:lon2_index]
    y_index<-dods_data$dim$lat$vals[lat1_index:lat2_index]
    x1<-lon1_index
    y1<-lat1_index
    x2<-lon2_index
    y2<-lat2_index
  }
  return(list(x1,y1,x2,y2,x_index,y_index))
}
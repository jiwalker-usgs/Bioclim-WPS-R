request_time_bounds<-function(ncdf4_handle, start, end)
{
  time_units<-strsplit(ncdf4_handle$dim$time$units, " ")[[1]]
  time_step<-time_units[1]
  date_origin<-time_units[3]
  time_origin<-"00:00:00"
  if(length(time_units)==4) time_origin<-time_units[4]
  cal_origin <- paste(date_origin, time_origin)
  year_origin=as.numeric(strsplit(date_origin,'-')[[1]][1])
  month_origin=as.numeric(strsplit(date_origin,'-')[[1]][2])
  day_origin=as.numeric(strsplit(date_origin,'-')[[1]][3])
  years=as.numeric(end)-as.numeric(start)
  t_1 <- julian(strptime(paste(start,'-01-01 12:00',sep=''), '%Y-%m-%d %H:%M'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
  t_2 <- julian(strptime(paste(end, '-01-01 00:00', sep=''), '%Y-%m-%d %H:%M'), origin<-strptime(cal_origin, '%Y-%m-%d %H:%M:%S'))
  # Some simple time and bbox validation.
  if (t_1<head(ncdf4_handle$dim$time$vals,1)) stop(paste("Submitted start date,",start, "is before the dataset's start date,",chron(head(ncdf4_handle$dim$time$vals,1),out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin))))
  if (t_2>tail(ncdf4_handle$dim$time$vals,1)) stop(paste("Submitted end date,",end, "is after the dataset's end date,",chron(tail(ncdf4_handle$dim$time$vals,1),out.format=c(dates="year-m-day"), origin=c(month=month_origin, day=day_origin, year=year_origin))))
  if (t_1>t_2) stop('Start date must be before end date.')
  t_ind1 <- min(which(abs(ncdf4_handle$dim$time$vals-t_1)==min(abs(ncdf4_handle$dim$time$vals-t_1))))
  t_ind2 <- max(which(abs(ncdf4_handle$dim$time$vals-t_2)==min(abs(ncdf4_handle$dim$time$vals-t_2))))
  time<-dods_data$dim$time$vals[t_ind1:t_ind2-1]
  return(list(t_ind1, t_ind2, time))
}
library("ncdf")
library("chron")
nc_filename<-'times_monthly.nc'
originDate<-strptime("2006-04-01","%Y-%m-%d")
endDate<-strptime("2100-01-01","%Y-%m-%d")
times<-seq(from=originDate,to=endDate,by='months')
times<-round(julian(times,origin=originDate))
time_vec<-1:length(times)
nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
nc_time_var <- var.def.ncdf('time','days since 2006-04-01', nc_time_dim, -999, prec='integer')
nc_file<-create.ncdf(nc_filename,list(nc_time_var))
var<-put.var.ncdf(nc_file,nc_time_var,times)
close.ncdf(nc_file)

nc_filename<-'times_monthly_hst'
originDate<-strptime("1895-10-01","%Y-%m-%d")
inc_originDate<-strptime("1895-10-01","%Y-%m-%d")
years=1895:2010
for (i in 1:length(years))
{
  endDate<-strptime(paste(years[i],"-12-01",sep=""),"%Y-%m-%d")
  times<-seq(from=inc_originDate,to=endDate,by='months')
  inc_originDate<-strptime(paste((years[i]+1),"-01-01",sep=""),"%Y-%m-%d")    
  times<-round(julian(times,origin=originDate))
  time_vec<-1:length(times)
  nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
  nc_time_var <- var.def.ncdf('time','days since 1895-10-01', nc_time_dim, -999, prec='integer')
  nc_file<-create.ncdf(paste(nc_filename,years[i],'.nc',sep=""),list(nc_time_var))
  var<-put.var.ncdf(nc_file,nc_time_var,times)
  close.ncdf(nc_file)
}

nc_filename<-'times_climatology.nc'
originDate<-strptime("2006-04-01","%Y-%m-%d")
times<-c(strptime("2010-01-01","%Y-%m-%d"),strptime("2040-01-01","%Y-%m-%d"),strptime("2070-01-01","%Y-%m-%d"))
times<-round(julian(times,origin=originDate))
time_vec<-1:length(times)
nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
nc_time_var <- var.def.ncdf('time','days since 2006-04-01', nc_time_dim, -999, prec='integer')
nc_file<-create.ncdf(nc_filename,list(nc_time_var))
var<-put.var.ncdf(nc_file,nc_time_var,times)
close.ncdf(nc_file)

nc_filename<-'times_climatology_hst.nc'
originDate<-strptime("1951-04-01","%Y-%m-%d")
times<-c(strptime("1951-01-01","%Y-%m-%d"),strptime("1981-01-01","%Y-%m-%d"))
times<-round(julian(times,origin=originDate))
time_vec<-1:length(times)
nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
nc_time_var <- var.def.ncdf('time','days since 1951-04-01', nc_time_dim, -999, prec='integer')
nc_file<-create.ncdf(nc_filename,list(nc_time_var))
var<-put.var.ncdf(nc_file,nc_time_var,times)
close.ncdf(nc_file)

nc_filename<-'times_wy.nc'
originDate<-strptime("2000-10-01","%Y-%m-%d")
endDate<-strptime("2099-10-01","%Y-%m-%d")
times<-seq(from=originDate,to=endDate,by='years')
times<-round(julian(times,origin=originDate))
time_vec<-1:length(times)
nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
nc_time_var <- var.def.ncdf('time','days since 2000-10-01', nc_time_dim, -999, prec='integer')
nc_file<-create.ncdf(nc_filename,list(nc_time_var))
var<-put.var.ncdf(nc_file,nc_time_var,times)
close.ncdf(nc_file)

nc_filename<-'times_wy_hst.nc'
originDate<-strptime("1896-10-01","%Y-%m-%d")
endDate<-strptime("2010-10-01","%Y-%m-%d")
times<-seq(from=originDate,to=endDate,by='years')
times<-round(julian(times,origin=originDate))
time_vec<-1:length(times)
nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
nc_time_var <- var.def.ncdf('time','days since 1896-10-01', nc_time_dim, -999, prec='integer')
nc_file<-create.ncdf(nc_filename,list(nc_time_var))
var<-put.var.ncdf(nc_file,nc_time_var,times)
close.ncdf(nc_file)


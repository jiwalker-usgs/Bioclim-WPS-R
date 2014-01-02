library("ncdf")
library("chron")
setwd("/Users/davidblodgett/Documents/Projects/GDP/netcdf_wrok/hobbins")
start_year<-1979
end_year<-2015
for (year in start_year:end_year)
{
nc_filename<-paste(year,".nc",sep="")
originDate<-strptime(paste(year,"-10-01",sep=""),"%Y-%m-%d")
endDate<-strptime(paste(year+1,"-09-30",sep=""),"%Y-%m-%d")
times<-seq(from=originDate,to=endDate,by='days')
times<-round(julian(times,origin=originDate))
time_vec<-1:length(times)
nc_time_dim <- dim.def.ncdf('time','',time_vec,create_dimvar=FALSE)
nc_time_var <- var.def.ncdf('time',paste('days since ',year,'-10-01',sep=""), nc_time_dim, -999, prec='integer')
nc_file<-create.ncdf(nc_filename,list(nc_time_var))
var<-put.var.ncdf(nc_file,nc_time_var,times)
close.ncdf(nc_file)
}
library("dapClimates")
library("climates")

bbox_in <- as.double(read.csv(header=F,colClasses=c("character"),text=bbox_in))
if (tave_var=="NULL") tave_var=NULL
fileNames<-dap_daily_stats(start,end,bbox_in,thresholds,OPeNDAP_URI,tmax_var,tmin_var,tave_var,prcp_var)

name<-'dailyInd.zip'
dailyInd_zip<-zip(name,fileNames)
#wps.out: name, zip, bioclim_zip, A zip pf the resulting bioclim getiffs..;
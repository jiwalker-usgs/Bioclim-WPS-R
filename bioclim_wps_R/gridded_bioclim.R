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
library("dapClimates")

bbox_in <- as.double(read.csv(header=F,colClasses=c("character"),text=bbox_in))
bioclims <- as.double(read.csv(header=F,colClasses=c("character"),text=bioclims))
if (tave_var=="NULL") tave_var=NULL
fileNames<-dap_bioclim(start,end,bbox_in,bioclims,OPeNDAP_URI,tmax_var,tmin_var,tave_var,prcp_var)

name<-'bioclim.zip'
bioclim_zip<-zip(name,fileNames)
#wps.out: name, zip, bioclim_zip, A zip pf the resulting bioclim getiffs..;
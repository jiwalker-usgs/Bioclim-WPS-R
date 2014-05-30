# Define Inputs (will come from external call)
start <- "1961"
end <- "1962"
bbox_in<-"-87,41,-89,43"
OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/wicci/cmip3/20c3m"
tmax_var  <- "20c3m-cccma_cgcm3_1-tmax-01"
tmin_var <- "20c3m-cccma_cgcm3_1-tmin-01"
prcp_var <- "20c3m-cccma_cgcm3_1-prcp-01"
tave_var <- "NULL"
thresholds=list(days_tmax_abv_thresh=c(32.2222,35,37.7778),
                days_tmin_blw_thresh=c(-17.7778,-12.2222,0),
                days_prcp_abv_thresh=c(25.4,50.8,76.2,101.6),
                longest_run_tmax_abv_thresh=c(32.2222,35,37.7778),
                longest_run_prcp_blw_thresh=c(76.2),
                growing_degree_day_thresh=c(15.5556),
                heating_degree_day_thresh=c(18.3333),
                cooling_degree_day_thresh=c(18.3333),
                growing_season_lngth_thresh=c(0))

start <- "1980"
end <- "1980"
bbox_in<-"-90,40,-91,41"
bioclims<-"1"
OPeNDAP_URI<-"http://thredds.daac.ornl.gov/thredds/dodsC/daymet-agg/daymet-agg.ncml"
tmax_var  <- "tmax"
tmin_var <- "tmin"
prcp_var <- "prcp"
tave_var <- "NULL"

start <- "1965"
end <- "1970"
bbox_in<-"-90,41,-90.5,41.5"
OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/dcp/conus"
tmax_var  <- "ccsm-a1b-tmax-NAm-grid"
tmin_var <- "ccsm-a1b-tmin-NAm-grid"
prcp_var <- "ccsm-a1fi-pr-NAm-grid"
tave_var <- "NULL"
thresholds=list(days_tmax_abv_thresh=c(32.2222,35,37.7778),
                days_tmin_blw_thresh=c(-17.7778,-12.2222,0),
                days_prcp_abv_thresh=c(25.4,50.8,76.2,101.6),
                longest_run_tmax_abv_thresh=c(32.2222,35,37.7778),
                longest_run_prcp_blw_thresh=c(76.2),
                growing_degree_day_thresh=c(15.5556),
                heating_degree_day_thresh=c(18.3333),
                cooling_degree_day_thresh=c(18.3333),
                growing_season_lngth_thresh=c(0))

start <- "1990"
end <- "1991"
bbox_in<-"-87,41,-89,43"
bioclims<-"1,2,3,4,5,6,7"
OPeNDAP_URI<-"http://cida.usgs.gov/thredds/dodsC/UofIMETDATA"
tmax_var  <- "max_air_temperature"
tmin_var <- "min_air_temperature"
prcp_var <- "precipitation_amount"
tave_var <- "NULL"


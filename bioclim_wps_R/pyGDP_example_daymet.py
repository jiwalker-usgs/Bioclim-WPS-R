import pyGDP
pyGDP.WPS_URL    = 'http://cida-eros-gdpdev.er.usgs.gov:8080/gdp-process-wps/WebProcessingService'
processid = 'org.n52.wps.server.r.gridded_bioclim'

start = "1985"
end = "2005"
#bbox_in="-100,36,-110,42"
bbox_in="-90,40,-91,41"
bioclims="1,2,3,4,5,6,7"
OPeNDAP_URI="http://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet"
tmax_var  = "tmax"
tmin_var = "tmin"
prcp_var = "prcp"
tave_var = "NULL"

inputs = [("start",start),
            ("end",end),
            ("bbox_in",bbox_in),
            ("bioclims",bioclims),
            ("OPeNDAP_URI",OPeNDAP_URI),
            ("tmax_var",tmax_var),
            ("tmin_var",tmin_var),
            ("prcp_var",prcp_var),
            ("tave_var",tave_var)]
            
output="name"

verbose=True

pyGDP = pyGDP.pyGDPwebProcessing()
gotime=pyGDP._executeRequest(processid, inputs, output, verbose)
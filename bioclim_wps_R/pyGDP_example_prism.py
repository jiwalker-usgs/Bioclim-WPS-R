import pyGDP
import os
pyGDP.WPS_URL    = 'http://cida-eros-gdpdev.er.usgs.gov:8080/gdp-process-wps/WebProcessingService'
processid = 'org.n52.wps.server.r.gridded_bioclim'

filename = 'test_prism.zip'

start = "1950"
end = "1952"
bbox_in="-100,36,-110,42"
bioclims="1,2,3,4,5,6,7"
OPeNDAP_URI="http://cida.usgs.gov/thredds/dodsC/prism"
tmax_var  = "tmx"
tmin_var = "tmn"
prcp_var = "ppt"
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
os.rename(gotime, filename)


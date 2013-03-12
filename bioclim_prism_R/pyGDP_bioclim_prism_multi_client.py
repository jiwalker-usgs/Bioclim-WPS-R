# This example will execute the bioclim_prism script deployed on a local host wps server.
import pyGDP
# Set this to remote server once the algorithm is published.
pyGDP.WPS_URL='http://cida-wiwsc-wsdev.er.usgs.gov:8080/wps/WebProcessingService'
testpyGDP=pyGDP.pyGDPwebProcessing()
processid='org.n52.wps.server.r.bioclim_prism_multi_latlon'
inputs = [("OPeNDAP_URI",'http://cida.usgs.gov/thredds/dodsC/prism'),
	("start",'1950-01-01'), 
  ("end", '2000-01-01'), 
  ("lat_in", '43.00, 42.00'), 
  ("lon_in",'-90.00, -91.00'),
  ("ids", 'a, b')]
output = "output"
verbose=True
filehandle=testpyGDP._executeRequest(processid, inputs, output, verbose)
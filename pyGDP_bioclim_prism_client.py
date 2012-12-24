# This example will execute the bioclim_prism script deployed on a local host wps server.
import pyGDP
# Set this to remote server once the algorithm is published.
pyGDP.WPS_URL='http://localhost:8080/wps/WebProcessingService'
testpyGDP=pyGDP.pyGDPwebProcessing()
processid='org.n52.wps.server.r.bioclim_prism'
inputs = [("start",'1950-01-01'), 
  ("end", '2000-01-01'), 
  ("lat_in", '43.00'), 
  ("lon_in",'-90.00')]
output = "output"
verbose=True
filehandle=testpyGDP._executeRequest(processid, inputs, output, verbose)
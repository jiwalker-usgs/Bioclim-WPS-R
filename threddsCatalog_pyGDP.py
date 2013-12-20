from lxml import etree
import pyGDP
import os
# Given a thredds catalog.xml
thredds_catalog="http://dataserver.nccs.nasa.gov/thredds/catalog/bypass/NEX-DCP30/bcsd/rcp85/r1i1p1/catalog.xml"
# Parse the tree and find all dataset members.
tree=etree.parse(thredds_catalog)
datasets=[]
root=tree.getroot()
datasets = root.findall(".//{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset")
# Build a list of all urlPaths found in the catalog
urlPaths=[]
for dataset in datasets:
    try:
        urlPaths.append(dataset.attrib['urlPath'])
    except Exception:
        pass

print 'Found '+str(len(urlPaths))+' urlPaths in thredds catalog.'

# Run pyGDP for each one of the datasets found. 
OpendapBaseUrl = 'dods://dataserver.nccs.nasa.gov/thredds/dodsC/'
pyGDP=pyGDP.pyGDPwebProcessing()
for path in urlPaths:
    dataset_url = OpendapBaseUrl+path
    shapefile  = 'sample:nps_boundary_2013'
    attribute  = 'UNIT_NAME'
    value 	   = 'Glacier'
    dataType   = path.split('/')[-1][0:-1-4]
    timeStart  = '2000-01-01T00:00:00.000Z'
    timeEnd    = '2110-01-01T00:00:00.000Z'
    outputFile_handle = pyGDP.submitFeatureCoverageOPenDAP(shapefile, dataset_url, dataType, timeStart, timeEnd, attribute, value,verbose=True)
    outputFileName=path.split('/')[3]+'-'+path.split('/')[4]+'-'+path.split('/')[5][0:-1-4]+'-'+value+'.csv'
    os.rename(outputFile_handle,outputFileName)
f=open('./bcca.ls')
lines=f.readlines()
f.close()
daily_ncml_1='<?xml version="1.0"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation dimName="time" type="joinExisting">\n <scan location='
daily_ncml_2=' regExp=".*(?&lt;!monthly)\.\d{4}.nc" subdirs="false"/>\n </aggregation>\n</netcdf>'
monthly_ncml_1='<?xml version="1.0"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation dimName="time" type="joinExisting">\n <scan location='
monthly_ncml_2=' regExp=".*monthly.*.nc" subdirs="false"/>\n </aggregation>\n</netcdf>'
for line in lines: # Loop through all lines, build unions and joinexistings as we go through.
        if line[0]=='/': #if line is a path, do some union stuff if the path is terminal.
                path=line[0:-1-2] # Paths end in :\n so take off last two characters.
                print path
                path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
        elif '.nc' in line:
                if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
                        path_switch=0 # # Turn off path switch.
                        # write a joinExisting aggregation for current path.
                        name=line[0:-1-8]+'ncml' # create name for join file.
                        name_monthly=line[0:-1-8]+'monthly.ncml' # Create name for monthly join file.
                        f=open('./ncmls/joins/'+name,'w')
                        f.write(daily_ncml_1+'"'+path+'"'+daily_ncml_2)
                        f.close()
                        f=open('./ncmls/joins/'+name_monthly,'w')
                        f.write(monthly_ncml_1+'"'+path+'"'+monthly_ncml_2)
                        f.close()


f=open('./bcca.ls')
lines=f.readlines()
f.close()
# 3 grids, 2 time resolutions, 5 calendars, 3 time periods.
grids=('BC_2deg','BCCA_0.125deg','REGRID_2deg','OBS_2deg','OBS_125deg')
calendars=('365_day','gregorian','360_day','noleap','obs')
time_prds=('20c3m','sres','obs')
runs=('run1','run2','run3','run4','run5','obs')
# two time resolutions for all, no search needed.
for grid in grids:
        for calendar in calendars:
                for time_prd in time_prds:
                        open_switch=0
                        for run in runs:
                                for line in lines: # This loops through everything a lot of times and is slow, but it doesn't take long and it was easy to write this way. Probably a better way, but it does the job.
                                        if line[0]=='/': #if line is a path, do some union stuff if the path is terminal.
                                                path=line[0:-1-2] # Paths end in :\n so take off last two characters.
                                                path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
                                        elif '.nc' in line:
                                                if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
                                                        path_switch=0 # Turn off path switch.
                                                        # open and write start of union files
                                                        if grid in line and calendar in path and time_prd in path and run in path:
                                                                if open_switch==0:
                                                                        if 'obs' in run:
                                                                                d=open('./ncmls/unions/'+grid+'.ncml','a')
                                                                                m=open('./ncmls/unions/'+grid+'.monthly.ncml','a')
                                                                        else:                                                                                        
                                                                                d=open('./ncmls/unions/'+grid+'.'+calendar+'.'+time_prd+'.ncml','a')
                                                                                m=open('./ncmls/unions/'+grid+'.'+calendar+'.'+time_prd+'.monthly.ncml','a')
                                                                        d.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
                                                                        m.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
                                                                        open_switch=1
                                                                print open_switch
                                                                print path
                                                                name=line[0:-1-8]+'ncml' # create name of join file.
                                                                name_monthly=line[0:-1-8]+'monthly.ncml' # Create name for monthly join file.
                                                                var_name=line[0:-1-9].replace('.','-') # create unique name for variable.
                                                                var_name_monthly=line[0:-1-8].replace('.','-')+'monthly' # Create unique name for monthly variables.
                                                                if 'pr' in path:
                                                                        orgName='pr'
                                                                if 'tasmax' in path:
                                                                        orgName='tasmax'
                                                                if 'tasmin' in path:
                                                                        orgName='tasmin'
                                                                if open_switch==1:
                                                                        d.write(' <netcdf location="../joins/'+name+'">\n <variable orgName="'+orgName+'" name="'+var_name+'" />\n </netcdf>\n')
                                                                        m.write(' <netcdf location="../joins/'+name_monthly+'">\n <variable orgName="'+orgName+'" name="'+var_name_monthly+'" />\n </netcdf>\n')
                        if open_switch==1:
                                d.write(' </aggregation>\n</netcdf>')
                                m.write(' </aggregation>\n</netcdf>')
                                d.close()
                                m.close()
                                
                                
f=open('./bcca.ls')
lines=f.readlines()
f.close()
# 3 grids, 2 time resolutions, 5 calendars, 3 time periods.
grids=('BC_2deg','BCCA_0.125deg','REGRID_2deg','OBS_2deg','OBS_125deg')
calendars=('365_day','gregorian','360_day','noleap','obs')
time_prds=('20c3m','sres','obs')
time_prds_1={'20c3m': '1961-01-01T00:00','sres': '2046-01-01T00:00','obs': '1950-01-01T00:00'}
time_prds_2={'20c3m': '2000-12-31T00:00','sres': '2100-01-01T00:00','obs': '1999-01-01T00:00'}
runs=('run1','run2','run3','run4','run5','obs')
c=open('./bcca_catalog.xml','w')
c.write('<?xml version="1.0" encoding="UTF-8"?> <catalog xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink" name="BCCA Climate Projections by Maurer, Brekke, Pruitt, and Duffy"> <service name="Services" serviceType="Compound" base=""> <service name="ncdods" serviceType="OpenDAP" base="/thredds/dodsC/"/> <service name="ncml" serviceType="NCML" base="/thredds/ncml/"/> <service name="uddc" serviceType="UDDC" base="/thredds/uddc/"/> <service name="iso" serviceType="ISO" base="/thredds/iso/"/> </service> <dataset name="BCCA Climate Projections by Maurer, Brekke, Pruitt, and Duffy" ID="llnl.gov/bcca/"> <metadata inherited="true"> <documentation href="http://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html" title="Bias Corrected and Downscaled WCRP CMIP3 Climate and Hydrology Projections Home"/> <documentation href="http://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#Projections: Complete Archives" title="Originating Data Repository"/> <documentation type="Rights">Freely Available</documentation> <documentation type="Summary"> This archive contains fine spatial-resolution translations of 53 contemporary climate projections over the contiguous United States. The original projections are from the World Climate Research Programme\'s (WCRP\'s) Coupled Model Intercomparison Project phase 3 (CMIP3) multi-model dataset, which was referenced in the Intergovernmental Panel on Climate Change Fourth Assessment Report.</documentation> <documentation type="Reference">Maurer, E.P., H.G. Hidalgo, T. Das, M.D. Dettinger, and D.R. Cayan, 2010, The utility of daily large-scale climate data in the assessment of climate change impacts o n daily streamflow in California, Hydrology and Earth System Sciences 14, 1125-1138, doi:10.5194/hess-14-1125-2010</documentation> <keyword>Surface Winds Atmosphere</keyword> <keyword>Air Temperature Atmosphere</keyword> <keyword>Precipitation</keyword> <keyword>Rain</keyword> <keyword>Downscaled Climate Projection</keyword> <creator> <name>Bridget Thrasher</name> <contact url="http://www.climateanalyticsgroup.org/" email="bridget@climateanalyticsgroup.org"/> </creator> <creator> <name>Ed Maurer</name> <contact url="http://www.engr.scu.edu/~emaurer/index.shtml" email="emaurer@engr.scu.edu"/> </creator> <publisher> <name>LLNL-PCMDI</name> <contact url="http://www-pcmdi.llnl.gov/" email="webmaster@pcmdi.llnl.gov"/> </publisher> <publisher> <name>CIDA</name> <contact url="http://cida.usgs.gov" email="dblodgett@usgs.gov"/> </publisher> <geospatialCoverage> <northsouth> <start>53</start> <size>-28</size> <units>degrees_north</units> </northsouth> <eastwest> <start>-125</start> <size>58</size> <units>degrees_east</units> </eastwest> </geospatialCoverage> </metadata>\n')
# two time resolutions for all, no search needed.
obs_count=0
sres_count=0
for grid in grids:
        for calendar in calendars:
                for time_prd in time_prds:
                        open_switch=0
                        for run in runs:
                                for line in lines: # This loops through everything a lot of times and is slow, but it doesn't take long and it was easy to write this way. Probably a better way, but it does the job.
                                        if line[0]=='/': #if line is a path, do some union stuff if the path is terminal.
                                                path=line[0:-1-2] # Paths end in :\n so take off last two characters.
                                                path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
                                        elif '.nc' in line:
                                                if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
                                                        path_switch=0 # Turn off path switch.
                                                        if grid in line and calendar in path and time_prd in path and run in path:
                                                                if open_switch==0:
                                                                        if 'obs' in run:
                                                                                # Write two obs datasets into the catalog.
                                                                                obs_count=obs_count+1
                                                                                c.write('<dataset name="'+grid+'" ID="llnl.gov/bcca/'+grid+'" serviceName="Services" urlPath="bcca/'+grid+'"> <dataType>Grid</dataType> <dataFormat>NcML</dataFormat> <timeCoverage> <start>'+time_prds_1[time_prd]+'</start> <end>'+time_prds_2[time_prd]+'</end> <resolution>1 Day</resolution> </timeCoverage> <netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2" location="/esg/content/thredds/bcsd/bcca/unions/'+grid+'.ncml"/> </dataset>\n')
                                                                                c.write('<dataset name="'+grid+' monthly" ID="llnl.gov/bcca/'+grid+'.monthly" serviceName="Services" urlPath="bcca/'+grid+'-monthly"> <dataType>Grid</dataType> <dataFormat>NcML</dataFormat> <timeCoverage> <start>'+time_prds_1[time_prd]+'</start> <end>'+time_prds_2[time_prd]+'</end> <resolution>1 Month</resolution> </timeCoverage> <netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2" location="/esg/content/thredds/bcsd/bcca/unions/'+grid+'.monthly.ncml"/> </dataset>\n')
                                                                        else:
                                                                                sres_count=sres_count+1
                                                                                # Write two datasets into the catalog.
                                                                                c.write('<dataset name="'+grid+' '+calendar+' '+time_prd+'" ID="llnl.gov/bcca/'+grid+'.'+calendar+'.'+time_prd+'" serviceName="Services" urlPath="bcca/'+grid+'-'+calendar+'-'+time_prd+'"> <dataType>Grid</dataType> <dataFormat>NcML</dataFormat> <timeCoverage> <start>'+time_prds_1[time_prd]+'</start> <end>'+time_prds_2[time_prd]+'</end> <resolution>1 Day</resolution> </timeCoverage> <netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2" location="/esg/content/thredds/bcsd/bcca/unions/'+grid+'.'+calendar+'.'+time_prd+'.ncml"/> </dataset>\n')
                                                                                c.write('<dataset name="'+grid+' '+calendar+' '+time_prd+' monthly" ID="llnl.gov/bcca/'+grid+'.'+calendar+'.'+time_prd+'.monthly" serviceName="Services" urlPath="bcca/'+grid+'-'+calendar+'-'+time_prd+'-monthly"> <dataType>Grid</dataType> <dataFormat>NcML</dataFormat> <timeCoverage> <start>'+time_prds_1[time_prd]+'</start> <end>'+time_prds_2[time_prd]+'</end> <resolution>1 Month</resolution> </timeCoverage> <netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2" location="/esg/content/thredds/bcsd/bcca/unions/'+grid+'.'+calendar+'.'+time_prd+'.monthly.ncml"/> </dataset>\n')
                                                                        open_switch=1

c.write('</dataset></catalog>')
c.close()
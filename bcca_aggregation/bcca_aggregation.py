f=open('./bcca.ls')
lines=f.readlines()
f.close()
daily_ncml_1='<?xml version="1.0"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation dimName="time" type="joinExisting">\n  <scan location='
daily_ncml_2=' regExp=".*(?&lt;!monthly)\.\d{4}.nc" subdirs="false"/>\n </aggregation>\n</netcdf>'
monthly_ncml_1='<?xml version="1.0"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation dimName="time" type="joinExisting">\n  <scan location='
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
									d.write('  <netcdf location="../joins/'+name+'">\n   <variable orgName="'+orgName+'" name="'+var_name+'" />\n  </netcdf>\n')
									m.write('  <netcdf location="../joins/'+name_monthly+'">\n   <variable orgName="'+orgName+'" name="'+var_name_monthly+'" />\n  </netcdf>\n')
			if open_switch==1:
				d.write(' </aggregation>\n</netcdf>')
				m.write(' </aggregation>\n</netcdf>')
				d.close()
				m.close()
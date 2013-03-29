f=open('./bcca.ls')
lines=f.readlines()
f.close()
daily_ncml_1='<?xml version="1.0"?><netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"><aggregation dimName="time" type="joinExisting"><scan location='
daily_ncml_2=' regExp=".*monthly.*.nc" subdirs="false"/></aggregation></netcdf>'
monthly_ncml_1='<?xml version="1.0"?><netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"><aggregation dimName="time" type="joinExisting"><scan location='
monthly_ncml_2=' regExp=".*monthly.*.nc" subdirs="false"/></aggregation></netcdf>'
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
# 3 grids, 2 time resolutions, 5 calendars, 3 time periods.
grids=('bc','bcca','regrid')
calendars=('365_day','gregorian','360_day','noleap','OBS')
time_prds=('20c3m','sresa1b','sresa2','sresb1')
# two time resolutions for all, no search needed.
for grid in grids:
	for calendar in calendars:
		for time_prd in time_prds:
			open_switch=0
			for line in lines: # This loops through everything a lot of times and is slow, but it doesn't take long and it was easy to write this way. Probably a better way, but it does the job.
				if line[0]=='/': #if line is a path, do some union stuff if the path is terminal.
					path=line[0:-1-2] # Paths end in :\n so take off last two characters.
					path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
				elif '.nc' in line: 
					if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
						path_switch=0 # Turn off path switch.
						# open and write start of union files
						if open_switch==0:
							d=open('./ncmls/unions/'+grid+'.'+calendar+'.'+time_prd+'','w')
							m=open('./ncmls/unions/'+grid+'.'+calendar+'.'+time_prd+'.monthly','w')
							d.write('<?xml version="1.0" encoding="UTF-8"?><netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"><aggregation type="union">')
							m.write('<?xml version="1.0" encoding="UTF-8"?><netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"><aggregation type="union">')
							open_switch=1
						if grid and calendar and time_prd in path:
							name=line[0:-1-8]+'ncml' # create name of join file.
							name_monthly=line[0:-1-8]+'monthly.ncml' # Create name for monthly join file.
							var_name=line[0:-1-9] # create unique name for variable.
							var_name_monthly=line[0:-1-8]+'monthly' # Create unique name for monthly variables.
							if 'pr' in path:
								orgName='pr'
							if 'tasmax' in path:
								orgName='tasmax'
							if 'tasmin' in path:
								orgName='tasmin'
							d.write('<netcdf location="'+name+'"><variable orgName="'+orgName+'" name="'+var_name+'" /></netcdf>')
							m.write('<netcdf location="'+name_monthly+'"><variable orgName="'+orgName+'" name="'+var_name_monthly+'" /></netcdf>')
			d.write('</aggregation></netcdf>')
			m.write('</aggregation></netcdf>')
			d.close()
			m.close()

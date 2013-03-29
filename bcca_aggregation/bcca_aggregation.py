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
			# write a joinExisting aggregation for current path or pass.
			name=line[0:-1-8]+'ncml' # create name for join file.
			name_monthly=line[0:-1-8]+'monthly.ncml' # Create name for monthly join file.
			f=open('./ncmls/'+name,'wb')
			f.write(daily_ncml_1+'"'+path+'"'+daily_ncml_2)
			f.close()
			f=open('./ncmls/'+name_monthly,'wb')
			f.write(monthly_ncml_1+'"'+path+'"'+monthly_ncml_2)
			f.close()

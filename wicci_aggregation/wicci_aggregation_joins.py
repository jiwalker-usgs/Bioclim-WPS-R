s = open('../tree.txt','r')
inlines = s.readlines()
for line in inlines:
	if line[0]=='.':
		path='../../'+line[2:-1-1]
		print path
		# than construct joinexisting header.
		name='joins/'+path[6:len(path)].replace('/','-')
		print name
		f1=open(name+'-temp-01.ncml','w')
		f2=open(name+'-temp-02.ncml','w')
		f3=open(name+'-temp-03.ncml','w')
		f1p=open(name+'-prcp-01.ncml','w')
		f2p=open(name+'-prcp-02.ncml','w')
		f3p=open(name+'-prcp-03.ncml','w')
		# Write header of data temporal aggregations.
		f1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f1.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
		f1.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
		f2.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f2.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
		f2.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
		f3.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f3.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
		f3.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
		f1p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f1p.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
		f1p.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
		f2p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f2p.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
		f2p.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
		f3p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f3p.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
		f3p.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
		# Write late period for folders that are not the past period. Past period only contains one time period, future contains two.
		if path.find('20c3m')==-1:
			f11=open(name+'-temp-01-2.ncml','w')
			f22=open(name+'-temp-02-2.ncml','w')
			f33=open(name+'-temp-03-2.ncml','w')
			f11p=open(name+'-prcp-01-2.ncml','w')
			f22p=open(name+'-prcp-02-2.ncml','w')
			f33p=open(name+'-prcp-03-2.ncml','w')
			f11.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f11.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
			f11.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
			f22.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f22.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
			f22.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
			f33.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f33.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
			f33.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
			f11p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f11p.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
			f11p.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
			f22p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f22p.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
			f22p.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
			f33p.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f33p.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
			f33p.write(' <aggregation dimName="time" type="joinExisting" timeUnitsChange="true">\n')
	if line=='\n':
		print 'close'
		f1.write('</aggregation>\n')
		f1.write('</netcdf>\n')
		f2.write('</aggregation>\n')
		f2.write('</netcdf>\n')
		f3.write('</aggregation>\n')
		f3.write('</netcdf>\n')
		f1.close()
		f2.close()
		f3.close()
		f1p.write('</aggregation>\n')
		f1p.write('</netcdf>\n')
		f2p.write('</aggregation>\n')
		f2p.write('</netcdf>\n')
		f3p.write('</aggregation>\n')
		f3p.write('</netcdf>\n')
		f1p.close()
		f2p.close()
		f3p.close()
		if path.find('20c3m')==-1:
			print 'close_inner'
			f11.write('</aggregation>\n')
			f11.write('</netcdf>\n')
			f22.write('</aggregation>\n')
			f22.write('</netcdf>\n')
			f33.write('</aggregation>\n')
			f33.write('</netcdf>\n')
			f11.close()
			f22.close()
			f33.close()
			f11p.write('</aggregation>\n')
			f11p.write('</netcdf>\n')
			f22p.write('</aggregation>\n')
			f22p.write('</netcdf>\n')
			f33p.write('</aggregation>\n')
			f33p.write('</netcdf>\n')
			f11p.close()
			f22p.close()
			f33p.close()
	else:
		# Build join existing lists
		# the three lines below are for the three runs that are available for each scenario/gcm. 
		# The two time periods are written into separate joins because they get unioned into separate files later.
		file_path = path+'/'+line[0:-1] 
		if line.find('_01_')!=-1:
			# Run 1
			if int(line[8:12])<2080:
				# Late Period
				if line.find('prcp')!=-1:
					# Precip
					f1p.write('  <netcdf location="'+file_path+'"/>\n')
				else:
					# Temp
					f1.write('  <netcdf location="'+file_path+'"/>\n')
			else:
				# Early Period
				if line.find('prcp')!=-1:
					# Precip
					f11p.write('  <netcdf location="'+file_path+'"/>\n')
				else:
					# Temp
					f11.write('  <netcdf location="'+file_path+'"/>\n')					
		elif line.find('_02_')!=-1:
			# Run 2
			if int(line[8:12])<2080:
				# Late Period
				if line.find('prcp')!=-1:
					# Precip
					f2p.write('  <netcdf location="'+file_path+'"/>\n')
				else:
					# Temp
					f2.write('  <netcdf location="'+file_path+'"/>\n')
			else:
					# Early Period
				if line.find('prcp')!=-1:
					# Precip
					f22p.write('  <netcdf location="'+file_path+'"/>\n')
				else:
					# Temp
					f22.write('  <netcdf location="'+file_path+'"/>\n')
		elif line.find('_03_')!=-1:
			# Run 3
			if int(line[8:12])<2080:
				# Late Period
				if line.find('prcp')!=-1:
					# Precip
					f3p.write('  <netcdf location="'+file_path+'"/>\n')
				else:
					# Temp
						f3.write('  <netcdf location="'+file_path+'"/>\n')
			else:
				# Early Period
				if line.find('prcp')!=-1:
					# Precip
					f33p.write('  <netcdf location="'+file_path+'"/>\n')
				else:
					# Temp
					f33.write('  <netcdf location="'+file_path+'"/>\n')

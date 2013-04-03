s = open('../tree.txt','r')
u1 = open('20c3m.ncml','w')
u2 = open('sres_01.ncml','w')
u3 = open('sres_02.ncml','w')
u4 = open('20c3m_mean_cdf.ncml','w')
u5 = open('sres_01_mean_cdf.ncml','w')
u6 = open('sres_02_mean_cdf.ncml','w')
u1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
u1.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
u1.write('	<aggregation type="union">\n')
u2.write('<?xml version="1.0" encoding="UTF-8"?>\n')
u2.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
u2.write('	<aggregation type="union">\n')
u3.write('<?xml version="1.0" encoding="UTF-8"?>\n')
u3.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
u3.write('	<aggregation type="union">\n')
u4.write('<?xml version="1.0" encoding="UTF-8"?>\n')
u4.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
u4.write('	<aggregation type="union">\n')
u5.write('<?xml version="1.0" encoding="UTF-8"?>\n')
u5.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
u5.write('	<aggregation type="union">\n')
u6.write('<?xml version="1.0" encoding="UTF-8"?>\n')
u6.write('<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n')
u6.write('	<aggregation type="union">\n')
inlines = s.readlines()
for line in inlines:
	if line[0]=='.':
		path='../'+line[2:-1-1]
		print path
		# than construct joinexisting header.
		name=path[3:len(path)].replace('/','-')
		print name
		if line.find('20c3m')!=-1:
			u1.write('		<netcdf location="joins/'+name+'-temp-01.ncml">\n')
			u1.write('			<variable orgName="tmin" name="'+name+'-tmin-01" />\n')
			u1.write('			<variable orgName="tmax" name="'+name+'-tmax-01" />\n')
			u1.write('		</netcdf>\n')
			u1.write('		<netcdf location="joins/'+name+'-prcp-01.ncml">\n')
			u1.write('			<variable orgName="prcp" name="'+name+'-prcp-01" />\n')
			u1.write('		</netcdf>\n')
			u4.write('		<netcdf location="'+path+'/temp_cdf_1961_2000.nc">\n')
			u4.write('			<variable orgName="cdftmin" name="'+name+'-cdftmin" />\n')
			u4.write('			<variable orgName="cdftmax" name="'+name+'-cdftmax" />\n')
			u4.write('		</netcdf>\n')
			u4.write('		<netcdf location="'+path+'/prcp_cdf_1961_2000.nc">\n')
			u4.write('			<variable orgName="ccdf" name="'+name+'-cdfprcp" />\n')
			u4.write('		</netcdf>\n')
			u4.write('		<netcdf location="'+path+'/temp_mean_1961_2000.nc">\n')
			u4.write('			<variable orgName="tmin" name="'+name+'-meantmin" />\n')
			u4.write('			<variable orgName="tmax" name="'+name+'-meantmax" />\n')
			u4.write('		</netcdf>\n')
			u4.write('		<netcdf location="'+path+'/prcp_mean_1961_2000.nc">\n')
			u4.write('			<variable orgName="prcp" name="'+name+'-meanprcp" />\n')
			u4.write('		</netcdf>\n')
		else:
			# Early Period Data
			u2.write('		<netcdf location="joins/'+name+'-temp-01.ncml">\n')
			u2.write('			<variable orgName="tmin" name="'+name+'-tmin-01" />\n')
			u2.write('			<variable orgName="tmax" name="'+name+'-tmax-01" />\n')
			u2.write('		</netcdf>\n')
			u2.write('		<netcdf location="joins/'+name+'-prcp-01.ncml">\n')
			u2.write('			<variable orgName="prcp" name="'+name+'-prcp-01" />\n')
			u2.write('		</netcdf>\n')
			# Late period data
			u3.write('		<netcdf location="joins/'+name+'-temp-01-2.ncml">\n')
			u3.write('			<variable orgName="tmin" name="'+name+'-tmin-01" />\n')
			u3.write('			<variable orgName="tmax" name="'+name+'-tmax-01" />\n')
			u3.write('		</netcdf>\n')
			u3.write('		<netcdf location="joins/'+name+'-prcp-01-2.ncml">\n')
			u3.write('			<variable orgName="prcp" name="'+name+'-prcp-01" />\n')
			u3.write('		</netcdf>\n')
			# early period mean_cdf
			u5.write('		<netcdf location="'+path+'/temp_cdf_2046_2065.nc">\n')
			u5.write('			<variable orgName="cdftmin" name="'+name+'-cdftmin" />\n')
			u5.write('			<variable orgName="cdftmax" name="'+name+'-cdftmax" />\n')
			u5.write('		</netcdf>\n')
			u5.write('		<netcdf location="'+path+'/prcp_cdf_2046_2065.nc">\n')
			u5.write('			<variable orgName="ccdf" name="'+name+'-cdfprcp" />\n')
			u5.write('		</netcdf>\n')
			u5.write('		<netcdf location="'+path+'/temp_mean_2046_2065.nc">\n')
			u5.write('			<variable orgName="tmin" name="'+name+'-meantmin" />\n')
			u5.write('			<variable orgName="tmax" name="'+name+'-meantmax" />\n')
			u5.write('		</netcdf>\n')
			u5.write('		<netcdf location="'+path+'/prcp_mean_2046_2065.nc">\n')
			u5.write('			<variable orgName="prcp" name="'+name+'-meanprcp" />\n')
			u5.write('		</netcdf>\n')
			# Late period mean_cdf
			u6.write('		<netcdf location="'+path+'/temp_cdf_2081_2100.nc">\n')
			u6.write('			<variable orgName="cdftmin" name="'+name+'-cdftmin" />\n')
			u6.write('			<variable orgName="cdftmax" name="'+name+'-cdftmax" />\n')
			u6.write('		</netcdf>\n')
			u6.write('		<netcdf location="'+path+'/prcp_cdf_2081_2100.nc">\n')
			u6.write('			<variable orgName="ccdf" name="'+name+'-cdfprcp" />\n')
			u6.write('		</netcdf>\n')
			u6.write('		<netcdf location="'+path+'/temp_mean_2081_2100.nc">\n')
			u6.write('			<variable orgName="tmin" name="'+name+'-meantmin" />\n')
			u6.write('			<variable orgName="tmax" name="'+name+'-meantmax" />\n')
			u6.write('		</netcdf>\n')
			u6.write('		<netcdf location="'+path+'/prcp_mean_2081_2100.nc">\n')
			u6.write('			<variable orgName="prcp" name="'+name+'-meanprcp" />\n')
			u6.write('		</netcdf>\n')

for line in inlines:
	if line[0]=='.':
		path='../'+line[2:-1-1]
		print path
		# than construct joinexisting header.
		name=path[3:len(path)].replace('/','-')
		print name
		if line.find('20c3m')!=-1:
			u1.write('		<netcdf location="joins/'+name+'-temp-02.ncml">\n')
			u1.write('			<variable orgName="tmin" name="'+name+'-tmin-02" />\n')
			u1.write('			<variable orgName="tmax" name="'+name+'-tmax-02" />\n')
			u1.write('		</netcdf>\n')
			u1.write('		<netcdf location="joins/'+name+'-prcp-02.ncml">\n')
			u1.write('			<variable orgName="prcp" name="'+name+'-prcp-02" />\n')
			u1.write('		</netcdf>\n')
		else:
			# Early Period Data
			u2.write('		<netcdf location="joins/'+name+'-temp-02.ncml">\n')
			u2.write('			<variable orgName="tmin" name="'+name+'-tmin-02" />\n')
			u2.write('			<variable orgName="tmax" name="'+name+'-tmax-02" />\n')
			u2.write('		</netcdf>\n')
			u2.write('		<netcdf location="joins/'+name+'-prcp-02.ncml">\n')
			u2.write('			<variable orgName="prcp" name="'+name+'-prcp-02" />\n')
			u2.write('		</netcdf>\n')
			# Late period data
			u3.write('		<netcdf location="joins/'+name+'-temp-02-2.ncml">\n')
			u3.write('			<variable orgName="tmin" name="'+name+'-tmin-02" />\n')
			u3.write('			<variable orgName="tmax" name="'+name+'-tmax-02" />\n')
			u3.write('		</netcdf>\n')
			u3.write('		<netcdf location="joins/'+name+'-prcp-02-2.ncml">\n')
			u3.write('			<variable orgName="prcp" name="'+name+'-prcp-02" />\n')
			u3.write('		</netcdf>\n')

for line in inlines:
	if line[0]=='.':
		path='../'+line[2:-1-1]
		print path
		# than construct joinexisting header.
		name=path[3:len(path)].replace('/','-')
		print name
		if line.find('20c3m')!=-1:
			u1.write('		<netcdf location="joins/'+name+'-temp-03.ncml">\n')
			u1.write('			<variable orgName="tmin" name="'+name+'-tmin-03" />\n')
			u1.write('			<variable orgName="tmax" name="'+name+'-tmax-03" />\n')
			u1.write('		</netcdf>\n')
			u1.write('		<netcdf location="joins/'+name+'-prcp-03.ncml">\n')
			u1.write('			<variable orgName="prcp" name="'+name+'-prcp-03" />\n')
			u1.write('		</netcdf>\n')
		else:
			# Early Period Data
			u2.write('		<netcdf location="joins/'+name+'-temp-03.ncml">\n')
			u2.write('			<variable orgName="tmin" name="'+name+'-tmin-03" />\n')
			u2.write('			<variable orgName="tmax" name="'+name+'-tmax-03" />\n')
			u2.write('		</netcdf>\n')
			u2.write('		<netcdf location="joins/'+name+'-prcp-03.ncml">\n')
			u2.write('			<variable orgName="prcp" name="'+name+'-prcp-03" />\n')
			u2.write('		</netcdf>\n')
			# Late period data
			u3.write('		<netcdf location="joins/'+name+'-temp-03-2.ncml">\n')
			u3.write('			<variable orgName="tmin" name="'+name+'-tmin-03" />\n')
			u3.write('			<variable orgName="tmax" name="'+name+'-tmax-03" />\n')
			u3.write('		</netcdf>\n')
			u3.write('		<netcdf location="joins/'+name+'-prcp-03-2.ncml">\n')
			u3.write('			<variable orgName="prcp" name="'+name+'-prcp-03" />\n')
			u3.write('		</netcdf>\n')

u1.write('</aggregation>\n')
u1.write('</netcdf>\n')
u2.write('</aggregation>\n')
u2.write('</netcdf>\n')
u3.write('</aggregation>\n')
u3.write('</netcdf>\n')
u4.write('</aggregation>\n')
u4.write('</netcdf>\n')
u5.write('</aggregation>\n')
u5.write('</netcdf>\n')
u6.write('</aggregation>\n')
u6.write('</netcdf>\n')
u1.close()
u2.close()
u3.close()
u4.close()
u5.close()
u6.close()
f=open('./ls.txt')
lines=f.readlines()
f.close()
c=open('./union_conus.ncml','w')
a=open('./union_alaska.ncml','w')
c.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n  <aggregation type="union">\n')
a.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n  <aggregation type="union">\n')
for line in lines:
    if '.nc' in line and '.nc.gz' not in line:
        new_name = line[0:-1-13].replace('.','-')
        if 'pr' in new_name:
            orgName = 'pr' 
        if 'tmin' in new_name:
            orgName = 'tmin' 
        if 'tmax' in new_name:
            orgName = 'tmax' 
        if 'Alas' in line:
            a.write('       <netcdf location="../'+line[0:-1]+'">\n         <variable orgName="'+orgName+'" name="'+new_name+'" />\n        </netcdf>\n')            
        else:
            c.write('       <netcdf location="../'+line[0:-1]+'">\n         <variable orgName="'+orgName+'" name="'+new_name+'" />\n        </netcdf>\n')

c.write('   </aggregation>\n</netcdf>')
a.write('   </aggregation>\n</netcdf>')
c.close()
a.close()
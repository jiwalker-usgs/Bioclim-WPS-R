f=open('./ls-R.txt')
lines=f.readlines()
f.close()
f=open('./historical_1.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
f=open('./historical_2.ncml','a')        
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')   
f.close()                                                                       
f=open('./future_1.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
f=open('./future_2.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
f=open('./future_3.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
f=open('./future_4.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
f=open('./future_5.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
f=open('./future_6.ncml','a')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
f.close()
open_switch=0
path_switch=0
for line in lines:
    if "cmip5" in line:
        if open_switch==1:
            f.close()
            open_switch=0    
        path=line[0:-1-1] # Paths end in :\n so take off last two characters.
        path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
    if '.nc' in line:
        if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
            path_switch=0 # Turn off path switch.
            # open and write start of union files
            if open_switch==0:
                if line[-1-16:-1-3] == '195001-200512':
                    f=open('./historical_1.ncml','a')
                elif line[-1-16:-1-3] == '195001-200511':
                    f=open('./historical_2.ncml','a')
                elif line[-1-16:-1-3] == '200512-209911':                                                                                      
                    f=open('./future_1.ncml','a')
                elif line[-1-16:-1-3] == '200601-210012':
                    f=open('./future_2.ncml','a')
                elif line[-1-16:-1-3] == '200601-209912':
                    f=open('./future_3.ncml','a')
                elif line[-1-16:-1-3] == '200601-203512':
                    f=open('./future_4.ncml','a')
                elif line[-1-16:-1-3] == '200512-209912':
                    f=open('./future_5.ncml','a')
                elif line[-1-16:-1-3] == '200512-210012':
                    f=open('./future_6.ncml','a')
                elif line[-1-16:-1-3] == '200601-210011':
                    f=open('./future_6.ncml','a')
                elif line[-1-16:-1-3] == '200512-210011':
                    f=open('./future_6.ncml','a')
                else:
                    print 'Missed a time period: '+line
                open_switch=1
            var_name=line[0:-1-3].replace('.','-') # create unique name for variable.
            if 'pr' in line:
                orgName='pr'
            elif 'tasmax' in line:
                orgName='tasmax'
            elif 'tasmin' in line:
                orgName='tasmin'
            elif '_tas_' in line:
                orgName='tas'
            else:
                'Missed a variable ' + line
            if open_switch==1:
                f.write(' <netcdf location="../'+path+'/'+line[0:-1]+'">\n <variable orgName="'+orgName+'" name="'+var_name+'" />\n </netcdf>\n')

f.close()
f=open('./historical_1.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./historical_2.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./future_1.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./future_2.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./future_3.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./future_4.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./future_5.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()
f=open('./future_6.ncml','a')    
f.write(' </aggregation>\n</netcdf>')
f.close()

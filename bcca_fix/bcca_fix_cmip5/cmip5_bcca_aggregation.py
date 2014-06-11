f=open('./etc/ls-cmip5.txt')
lines=f.readlines()
f.close()
count=0
daily_ncml_1='<?xml version="1.0"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation dimName="time" type="joinExisting">\n  <scan location='
daily_ncml_2=' regExp='
daily_ncml_3=' subdirs="false"/>\n </aggregation>\n</netcdf>'
for line in lines: # Loop through all lines, build unions and joinexistings as we go through.
    if line[0]=='.': #if line is a path, do some union stuff if the path is terminal.
        path=line[0:-1-1] # Paths end in :\n so take off last two characters.
        path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
    elif '.nc' in line: 
        if path_switch==1: # If the last line was a path, write a join file.
            print path
            path_switch=0 # # Turn off path switch.
            # write a joinExisting aggregations for current path.
            grid = 'BCCA_0.125deg_'
            name=line[0:len(line)-22]+'.ncml' # create name for join file.
            if 'pr' in line:
                name=line[0:len(line)-27]+'.ncml'
            count+=1
            print name
            f=open('./ncmls/joins/'+name,'w')
            f.write(daily_ncml_1+'"../../'+path+'"'+daily_ncml_2+'"'+grid+'.*"'+daily_ncml_3)
            f.close()


f=open('./etc/ls-cmip5.txt')
lines=f.readlines()
f.close()
grids=['BCCA_0.125deg']
time_prds=('historical','rcp')
runs=('r1i','r2i','r3i','r4i','r5i','r6i','r7i','r8i','r9i','r10i')
count=0
for grid in grids:
    for time_prd in time_prds:
        open_switch=0
        for run in runs:
            for line in lines: # This loops through everything a lot of times and is slow, but it doesn't take long and it was easy to write this way. Probably a better way, but it does the job.
                if line[0]=='.': #if line is a path, do some union stuff if the path is terminal.
                    path=line[0:-1-1] # Paths end in :\n so take off last two characters.
                    path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
                    #print path
                elif '.nc' in line: 
                    if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
                        path_switch=0 # Turn off path switch.
                        #print path
                        # open and write start of union files
                        if time_prd in path and run in path:
                            if open_switch==0:                                           
                                d=open('./ncmls/unions/'+grid+'.'+time_prd+'.ncml','a')
                                d.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
                                open_switch=1
                            #print path
                            name=line[0:len(line)-22]+'.ncml' # create name for join file.
                            if 'pr' in line:
                                name=line[0:len(line)-27]+'.ncml'
                            var_name=name[0:-1-4].replace('.','-') # create unique name for variable.
                            if 'pr' in path:
                                orgName='pr'
                            if 'tasmax' in path:
                                orgName='tasmax'
                            if 'tasmin' in path:
                                orgName='tasmin'
                            if open_switch==1:
                                d.write('  <netcdf location="../joins/'+name+'">\n   <variable orgName="'+orgName+'" name="'+var_name+'">\n    <remove type="attribute" name="valid_range" />\n   </variable>\n  </netcdf>\n')
                                count+=1
        if open_switch==1:
            d.write(' </aggregation>\n</netcdf>')
            d.close()
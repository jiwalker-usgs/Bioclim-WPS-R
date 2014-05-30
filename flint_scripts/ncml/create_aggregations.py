file_keys=['aet','cwd','exc','mlt','pck','pet','ppt','rch','run','sbl','snw','str','tmn','tmx']
metadata={'tmx':{"long_name":"Maximum Temperature","description":"The maximum monthly temperature averaged annually","units":"C","scale_factor":0.01},
            'tmn':{"long_name":"Minimum Temperature","description":"The minimum monthly temperature averaged annually","units":"C","scale_factor":0.01},
            'ppt':{"long_name":"Precipitation","description":"Total monthly precipitation (rain or snow) summed annually","units":"mm","scale_factor":0.1},
            'pet':{"long_name":"Potential Evapotranspiration","description":"Total amount of water that can evaporate from the ground surface or be transpired by plants, summed annually","units":"mm","scale_factor":0.1},
            'run':{"long_name":"Runoff","description":"Amount of water that becomes stream flow, summed annually","units":"mm","scale_factor":0.1},
            'rch':{"long_name":"Recharge","description":"Amount of water that penetrates below the root zone, summed annually","units":"mm","scale_factor":0.1},
            'cwd':{"long_name":"Climatic Water Deficit","description":"Annual evaporative demand that exceeds available water, summed annually","units":"mm","scale_factor":0.1},
            'aet':{"long_name":"Actual Evapotranspiration","description":"Amount of water that evaporates from the surface and is transpired by plants if the total amount of water is not limited, summed annually","units":"mm","scale_factor":0.1},
            'sbl':{"long_name":"Sublimation","description":"Amount of snow lost to sublimation (snow to water vapor) summed annually","units":"mm","scale_factor":0.1},
            'str':{"long_name":"Soil Water Storage","description":"Average amount of water stored in the soil summed annually","units":"mm","scale_factor":0.1},
            'snw':{"long_name":"Snowfall","description":"Amount of snow that fell summed annually","units":"mm","scale_factor":0.1},
            'pck':{"long_name":"Snowpack","description":"Amount of snow that accumulated per month summed annually (if divided by 12 would be average monthly snowpack)","units":"mm","scale_factor":0.1},
            'mlt':{"long_name":"Snowmelt","description":"Amount of snow that melted summed annually (snow to liquid water)","units":"mm","scale_factor":0.1},
            'exc':{"long_name":"Excess Water","description":"Amount of water that remains in the system, assuming evapotranspiration consumes the maximum possible amount of water, summed annually for positive months only","units":"mm","scale_factor":0.1},
            'djf':{"long_name":"Winter Minimum Are Temperature","description":"","units":"C","scale_factor":0.01},
            'jja':{"long_name":"Summer Maximum Air Temperature","description":"","units":"C","scale_factor":0.01},
}

ncml='<?xml version="1.0"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation dimName="time" type="joinExisting">\n <scan location="{0}" regExp=".*{1}.*\.nc" subdirs="false"/>\n </aggregation>\n</netcdf>'
for key in file_keys:
    f=open('./flint_ls.txt')
    lines=f.readlines()
    f.close()
    for line in lines: # Loop through all lines, build unions and joinexistings as we go through.
            if line[0]=='.': #if line is a path, do some union stuff if the path is terminal.
                    path="."+line[0:-1-1] # Paths end in :\n so take off last two characters.
                    print path
                    path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
            elif '.nc' in line:
                if key in line:
                    if path_switch==1: # If the last line was a path, write two join files, monthly and daily.
                            path_switch=0 # # Turn off path switch.
                            # write a joinExisting aggregation for current path.
                            name=line[0:-1-11]+key+'.ncml' # create name for join file.
                            print name
                            f=open('./joins/'+name,'w')
                            f.write(ncml.format(path, key))
                            f.close()

scenarios=("CCSM4_rcp85","CNRM_rcp85","CSIRO_A1B","FGOALS_rcp85","GFDL_A2","GFDL_B1","GISS_AOM_A1B","GISS_rcp26","HST","MIROC5_rcp26","MIROC_rcp45","MIROC_rcp60","MIROC_rcp85","MPI_rcp45","MRI_rcp26","PCM_A2")
d=open('./unions/union.ncml','a')
d.write('<?xml version="1.0" encoding="UTF-8"?>\n<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n <aggregation type="union">\n')
for scenario in scenarios:
    for key in file_keys:
        f=open('./flint_ls.txt')
        lines=f.readlines()
        f.close()
        for line in lines:
            if line[0]=='.': #if line is a path, do some union stuff if the path is terminal.
                path="."+line[0:-1-1] # Paths end in :\n so take off last two characters.
                path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
            elif '.nc' in line:
                if key in line:
                    print line
                    if path_switch==1:
                        path_switch=0
                        name=line[0:-1-11]+key+'.ncml'
                        var_name=line[7:-1-8]
                        d.write(' <netcdf location="../joins/'+name+'">\n <variable orgName="'+key+'" name="'+var_name+'" />\n </netcdf>\n')

d.write(' </aggregation>\n</netcdf>')
d.close()

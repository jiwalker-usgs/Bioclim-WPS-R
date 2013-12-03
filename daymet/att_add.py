ncks -h -v lat,lon daymet_ex.nc daymet_latlon.nc

import os
dir_contents=os.listdir('./')
for _file in dir_contents:
    if '.nc' in _file:
        os.system('ncatted -h -a history,global,a,c,"Spatially aggregated by the U.S. Geological Survey Center for Integrated Data Analytics 11/2012\n" '+_file)
        os.system('ncatted -h -a standard_name,x,c,c,"projection_x_coordinate" '+_file)
        os.system('ncatted -h -a standard_name,y,c,c,"projection_y_coordinate" '+_file)
        os.system('ncatted -h -a longitude_of_prime_meridian,lambert_conformal_conic,c,d,0 '+_file)
        os.system('ncatted -h -a semi_major_axis,lambert_conformal_conic,c,d,6378137.0 '+_file)
        os.system('ncatted -h -a inverse_flattening,lambert_conformal_conic,c,d,298.257223563 '+_file)
        os.system('ncatted -h -a add_offset,time,c,d,-0.5 '+_file)
        if 'prcp' in _file:
            os.system('ncatted -h -a scale_factor,prcp,c,d,1.0 '+_file)
src='/Volumes/Scratch/CA_BCM_Ensemble_asc/' # Location of source tar.gz files.
unzip_to='/Volumes/Striped/CA_BCM/' # Location where tar.gz files will be unzipped to.
dest='/Volumes/process/flint_out/' # Location where output .nc file should be placed.
proc_path='/Volumes/RAM_DISK/' # Location where processing should take place. This script will wipe files from this folder. IT SHOULD BE A NEW EMPTY FOLDER!!!
time_files_path='/Users/usgs/temp/flint/etc/' # Where the water year .nc files are. The are checked into the git hub repository and need to be local to the script somewhere.
start_year=2012 # Year to start at ie. Oct 1 2012
end_year=2013 # Year to end at ie. Sept 20 2013
gdal_translate_path="/opt/local/bin/gdal_translate" # The path where the correct gdal_translate is installed. enthought python installed gdal without netcdf and modified to path to have that one take precendence. This allows the script to hit the system gdal_translate.
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

metadata_wy={'tmx':{"long_name":"Maximum Temperature","description":"The maximum monthly temperature averaged annually","units":"C","scale_factor":0.01},
            'tmn':{"long_name":"Minimum Temperature","description":"The minimum monthly temperature averaged annually","units":"C","scale_factor":0.01},
            'ppt':{"long_name":"Precipitation","description":"Total monthly precipitation (rain or snow) summed annually","units":"mm","scale_factor":1},
            'pet':{"long_name":"Potential Evapotranspiration","description":"Total amount of water that can evaporate from the ground surface or be transpired by plants, summed annually","units":"mm","scale_factor":1},
            'run':{"long_name":"Runoff","description":"Amount of water that becomes stream flow, summed annually","units":"mm","scale_factor":1},
            'rch':{"long_name":"Recharge","description":"Amount of water that penetrates below the root zone, summed annually","units":"mm","scale_factor":1},
            'cwd':{"long_name":"Climatic Water Deficit","description":"Annual evaporative demand that exceeds available water, summed annually","units":"mm","scale_factor":1},
            'aet':{"long_name":"Actual Evapotranspiration","description":"Amount of water that evaporates from the surface and is transpired by plants if the total amount of water is not limited, summed annually","units":"mm","scale_factor":1},
            'sbl':{"long_name":"Sublimation","description":"Amount of snow lost to sublimation (snow to water vapor) summed annually","units":"mm","scale_factor":1},
            'str':{"long_name":"Soil Water Storage","description":"Average amount of water stored in the soil summed annually","units":"mm","scale_factor":1},
            'snw':{"long_name":"Snowfall","description":"Amount of snow that fell summed annually","units":"mm","scale_factor":1},
            'pck':{"long_name":"Snowpack","description":"Amount of snow that accumulated per month summed annually (if divided by 12 would be average monthly snowpack)","units":"mm","scale_factor":1},
            'mlt':{"long_name":"Snowmelt","description":"Amount of snow that melted summed annually (snow to liquid water)","units":"mm","scale_factor":1},
            'exc':{"long_name":"Excess Water","description":"Amount of water that remains in the system, assuming evapotranspiration consumes the maximum possible amount of water, summed annually for positive months only","units":"mm","scale_factor":1},
            'djf':{"long_name":"Winter Minimum Are Temperature","description":"","units":"C","scale_factor":0.01},
            'jja':{"long_name":"Summer Maximum Air Temperature","description":"","units":"C","scale_factor":0.01},
}

stat_metadata={}
#'aet',
file_keys={"Monthly":['aet','cwd','exc','mlt','pck','pet','ppt','rch','run','sbl','snw','str','tmn','tmx'],
            "Summary":['aet','aprpck','cwd','djf','jja','pet','ppt','rch','run','tmn','tmx'],
            "WaterYears":['aet','cwd','djf','jja','pet','ppt','rch','run','sbl','snw','str','tmn','tmx'],
            "summary_stats":['ave','dsd','std']}

creator='David Blodgett'.replace(' ', '\ ')
creator_email='dblodgett@usgs.gov'

folders={"CNRM_rcp85":"Volumes/CA_BCM_Ensemble Copy III/CNRM_rcp85",
    "GFDL_B1":"../../CA_BCM_Ensemble Copy II/GFDL_B1",
    "GISS_AOM_A1B":"Volumes/CA_BCM_Ensemble Copy II/GISS_AOM_A1B",
    "GISS_rcp26":"Volumes/CA_BCM_Ensemble Copy III/GISS_rcp26",
    "MIROC5_rcp26":"Volumes/CA_BCM_Ensemble Copy III/MIROC5_rcp26",
    "MIROC_rcp45":"Volumes/CA_BCM_Ensemble Copy III/MIROC_rcp45",
    "MIROC_rcp60":"Volumes/CA_BCM_Ensemble Copy III/MIROC_rcp60",
    "MIROC_rcp85":"Volumes/CA_BCM_Ensemble Copy III/MIROC_rcp85",
    "MRI_rcp26":"Volumes/CA_BCM_Ensemble Copy III/MRI_rcp26",
    "PCM_A2":"Volumes/CA_BCM_Ensemble Copy II/PCM_A2"}

Done={"MPI_rcp45":"Volumes/CA_BCM_Ensemble Copy III/MPI_rcp45",
    "FGOALS_rcp85":"Volumes/CA_BCM_Ensemble Copy I/FGOALS_rcp85",
    "GFDL_A2":"GFDL_A2",
    "CSIRO_A1B":"CSIRO_A1B"}
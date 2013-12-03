import os
os.chdir('/Volumes/CA_BCM_Ensemble Copy I')
src='./'
dest='/Volumes/Scratch/CA_BCM_Ensemble/'
inter='/Volumes/Striped/temp/'
dirs=0
files=0
# This loops through all the files on the disk in the line 2. It only works on the specified scenario and only works on the monthly stuff.
# The first for loop steps through and verifies that the directory structure that's needed is in place.
# The second loop steps through all the files in the directory, moves them to a temp disk then processes them.
# This is setup to run in parallel thus the cp then process, not sure it will make a difference, but worth a shot.
for dirname, dirnames, filenames in os.walk(src):
    if 'PCM_B1' in dirname and 'Monthly' in dirname:
        print dirname
        # create subdirs first.
        for subdirname in dirnames:
            srcdir = os.path.join(dirname, subdirname)
            destdir=dest+srcdir[len(src):len(srcdir)]
            intdir=inter+srcdir[len(src):len(srcdir)]
            if os.access(destdir,os.F_OK):
                print destdir+' already exists'
            else:
                os.mkdir(destdir)
                print 'made '+destdir
            if os.access(intdir,os.F_OK):
                print intdir+' already exists'
            else:
                os.mkdir(intdir)
                print 'made '+intdir
        
        # Walk through all files and write to netcdf
        for filename in filenames:
            srcfile = os.path.join(dirname, filename)
            intfile = inter+srcfile[len(src):len(srcfile)]
            destfile = dest+srcfile[len(src):len(srcfile)-3]+'nc'
            #print 'doing gdal_translate -of netCDF -co "COMPRESS=DEFLATE" -a_nodata -9999.00 '+srcfile+' '+destfile
            if '.asc' in filename:
                print 'copying'
                os.system('cp '+srcfile+' '+intfile)
                print 'converting'
                os.system('gdal_translate -q -of netCDF -co "COMPRESS=DEFLATE" -a_nodata -9999.00 '+intfile+' '+destfile)
                print 'cleaning'
                os.system('rm '+intfile)

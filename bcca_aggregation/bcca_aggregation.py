f=open('./bcca.ls')
lines=f.readlines()
f.close()
# Loop through all lines, build unions and joinexistings as we go through.
for line in lines:
	if line[0]=='/': # Is a path, do some union stuff if the path is terminal.
		path=line[0:-1-1] # Paths end in :\n so take off last two characters.
		path_switch=1 # Set the "path switch". If its on, and the next line is a file, will write a union.
	elif '.nc' in line: 
		if path_switch=1: # If the last line was a path, write two union files, monthly and daily.
			# write a joinExisting aggregation for current path or pass.
			name=line[0:-1-1]
			
			

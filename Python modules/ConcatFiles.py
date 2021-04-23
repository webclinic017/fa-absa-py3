import ael, string


def ConcatFiles(filename, outfile, *rest):
    try:
    	f = open(filename)
    except:
    	print('File ', filename, 'could not be found or opened')
	break
	
    line = f.readline()
    while line:
#    	print line
	outfile.write(line)
	line = f.readline()
	
    f.close()	
    ael.poll()
    
    return 

	

    	

### main ###
print('Starting...')
sdate = ael.date_from_string('2005-07-20')
edate = ael.date_from_string('2006-03-20')
d = sdate

outfile = open('C:\\agris\daydeals_ael.asc', 'w')

while d >= sdate and d <= edate:
    print('Adding file for ', d)
    parts = d.to_string().split('-')
    filename = 'c:\\agris\AGRIS_DAYDEALS_' + parts[1] + '-' + parts[2] + '-' + parts[0] + '.ASC'
#    print filename
    ConcatFiles(filename, outfile)

    d = d.add_days(1)
    
outfile.close()
print('Fin...')

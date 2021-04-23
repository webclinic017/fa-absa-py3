import ael, string


def BuildFile(filename, outfile, *rest):
    try:
    	f = open(filename)
    except:
    	print('File ', filename, 'could not be found or opened')
	return

    count = 0
    line = f.readline()
    while line:
	outfile.write('go\n')
	line = '\ndelete price_hst where prinbr = ' + line + '\n' 
    	count = count + 1
	outfile.write(line)
	line = f.readline()
	
    print(count)
    f.close()	
    ael.poll()
    
    return 

	

    	

### main ###
print('Starting...')
outfile = open('C:\shaun_prices.txt', 'w')
filename = 'c:\prices.txt'
BuildFile(filename, outfile)

outfile.close()
print('Fin...')

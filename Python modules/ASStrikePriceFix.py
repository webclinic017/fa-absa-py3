#ASStrikePriceFix reads strike prices from a csv and updates the Instrument table
# .csv file: C:\\Updated Strikes1.CSV

import ael, string, os


def strike_fix(file,*rest):

    f = open(file)
#    ael.log('Started loading from %s.' % file)
    
    #read first line with column headings
    line = f.readline()
    FenicsNo, AtlasNo, Strike = string.split(line, ',')
    
    #read first line with data
    line = f.readline()
    
    while line <> "":
    	FenicsNo, AtlasNo, Strike = string.split(line, ',')
		
	t = ael.Trade[int(AtlasNo)]
	if t != None:
	    print('Trade Number:', t.trdnbr)
    	
	    ins = ael.Instrument[t.insaddr.insid]
	    i = ins.clone()

    	    print('New strike price:', float(Strike))
	    print('Old strike price:', i.strike_price)
	    
	    i.strike_price = float(Strike)
	    i.commit()
	    ael.poll
	    
	    print('Updated strike price:', i.strike_price)
	    print()
   	
	line = f.readline()
    


#main ael
print('Starting Strike Price Fix...')
strike_fix('C:\\Updated Strikes1.CSV')    
print('Finished Strike Price Fix...')

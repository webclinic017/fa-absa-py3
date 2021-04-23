import ael, string

def STXOTC(file, *rest):

    # This function reads trade numbers and prices from a csv file and updates the 
    # corresponding trades in Front Arena with the respective prices. The premium is 
    # recalculated based on the new price.

    # COUNTERPARTY should be ABSA INVESTMENT MANAGEMENT SERVICES
    AIMSparty = ael.Party[1520]
    
    # create two lists, one to store update insids and trades and one for not updated
    # based on the file
    updated=[]
    notupdated=[]
    
    if not file: file = 'c:\stxotc.csv'
    f = open(file)
    line = f.readline()
    ael.log('Started loading from %s.' %file)
    
    while line:
    	# the first column is trade number, the second column is price
    	a, b = string.split(line, ',')
	if a != 'trdnbr':
	    t = ael.Trade.read("trdnbr = '%s'" %a)
	    try:
		tc = t.clone()
    		tc.price = float(b)
		tc.counterparty_ptynbr = AIMSparty
		# recalc premium based on fact quote type is per 100 units
		tc.premium = float(b) * t.quantity/100
		tc.commit()
		tuple = (t.trdnbr, t.insaddr.insid)
		updated.append(tuple)

	    except:
		tuple = (t.trdnbr, t.insaddr.insid)
		notupdated.append(tuple)
     	line = f.readline()
	
    print updated, notupdated

    msg = 'The following trades were updated with new prices:' + str(updated) \
    	+ 'The following instruments were not updated with new prices:' + str(notupdated) 

    msg = ael.log(msg)	    
	
#STXOTC('C:\stxotc.csv')

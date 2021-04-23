import ael, string

def Price_Entry(temp,*rest):

    f = open('f:\\Prices_20090724.csv') 
    
    #read first line with column headings
    line = f.readline()
    #name, price, day = string.split(line, ',')
    
    #read first line with data
    line = f.readline()
    line = f.readline()
    
#    count = 0
    while line != "":
        try:
            name, settle_price, day = string.split(line, '\t')
        except:
            print('error with ', line)

	#print Index, ResetDay, ResetValue
	
	ins = ael.Instrument[name]
        d = ael.date_from_string(day) #ael.date_from_string(ResetDay)
        try:
            ccy = ael.Instrument[name].curr.insaddr
        except:
            ccy = None
	pty = ael.Party['internal'].ptynbr
	set = float(settle_price)
	
        new = ael.Price.new()
        new.insaddr = ins
        new.day = d
        new.curr = ccy
	new.ptynbr = pty
	new.settle = set
	#print new.pp()
	try:
	    new.commit()
	    #pass
	except:
	    print('Price Entry already exists for ', name, day)
	
    	line = f.readline()	
    
    return('Success')
	
	

print(Price_Entry(123))

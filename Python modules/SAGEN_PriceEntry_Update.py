import ael, string

def Price_Entry(temp,*rest):

    f = open('C:\\Top_20.CSV') 
    
    #read first line with column headings
    line = f.readline()
    fIndex, fResetDay, fResetValue = string.split(line, ',')
    
    #read first line with data
    line = f.readline()
    
#    count = 0
    while line != "":
    	Index, ResetDay, ResetValue = string.split(line, ',')

	#print Index, ResetDay, ResetValue
	
	ins = ael.Instrument[Index].insaddr
        rday = ael.date_from_string(ResetDay)
        ccy = ael.Instrument['ZAR'].insaddr
	pty = ael.Party['SPOT'].ptynbr
	rval = float(ResetValue)
	
        new = ael.Price.new()
        new.insaddr = ael.Instrument[Index].insaddr
        new.day = ael.date_from_string(ResetDay)
        new.curr = ael.Instrument['ZAR'].insaddr
	new.ptynbr = ael.Party['SPOT'].ptynbr
	ResetVal = float(ResetValue)
	new.bid = ResetVal
	new.ask = ResetVal
	new.settle = ResetVal
	new.last = ResetVal
	
	try:
	    new.commit()
	except:
	    print('Price Entry already exists for ', rday)
	
    	line = f.readline()	
    
    return('Success')
	
	

print(Price_Entry(123))

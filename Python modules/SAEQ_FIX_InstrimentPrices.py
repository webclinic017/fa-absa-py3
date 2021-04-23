#AS_InstrumentFix reads Instruments from a .csv 
#c:\\ins.csv  to fix their historical prices

import ael, string, os


def ins_fix(file,*rest):

    f = open(file)
    
    #read first line with data
    count = 0
    line = f.readline()
    
    while line <> "":
    	trdnbr, instr = string.split(line, ',')
#	print trdnbr, instr
	count = count + 1
	
    	t = ael.Trade[int(trdnbr)]
	if t != None:
	    print
	    print
    	
	    ins = ael.Instrument[t.insaddr.insid]
    	    print 'Instrument:', ins.insid
	    
	    trds = ins.trades()
	    for t in trds:
	    	t_clone = t.clone()
		t_clone.price = t.price / 10
		print 'Trade ', t.trdnbr, ' price changed from ', t.price, ' to ', t_clone.price
    	    	t_clone.commit()
		ael.poll()		
		
	    print
	    hp = ins.historical_prices()
	    
            for h in hp:
	    	if h.curr == ael.Instrument['ZAR']:
#		    and h.day != '2004/11/05' and h.ptynbr.ptyid != 'internal':
		    price = ael.Price[h.prinbr]
		    
		    p_clone = price.clone()
		    p_clone.settle = p_clone.settle / 10
		    
		    print 'Price ', h.prinbr, ' changed from ', price.settle, ' to ', p_clone.settle
		    
		    p_clone.commit()
		    ael.poll()
  	
    	line = f.readline()

    print 'Instruments read ', count
	
#main ael
#i = ael.Instrument['ZAR/EQ/ALSI/15SEP05/C/11841.68/OTC']
print 'Starting Instrument Price Fix...'
ins_fix('C:\\ins12.CSV')    
print 'Finished Instrument Price Fix...'


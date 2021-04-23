import ael
def movepricehist(fromtrd, totrd):
    trade1 = ael.Trade[fromtrd]
    trade2 = ael.Trade[totrd]
    insfrom = trade1.insaddr
    insto = trade2.insaddr
    for p in insfrom.historical_prices():
        pc = ael.Price.new()
    	pc.insaddr = insto
    	pc.day = p.day
    	pc.settle = p.settle
    	pc.curr = p.curr
    	pc.ptynbr = p.ptynbr
    	try:
	    pc.commit()
	except:
	    print 'duplicate: ', pc.pp()
    	#print pc.pp()
    if insfrom.prices() > 0:
    	for p in insfrom.prices():
	    pc = ael.Price.new()
    	    pc.insaddr = insto
    	    pc.day = p.day
    	    pc.settle = p.settle
    	    pc.curr = p.curr
    	    pc.ptynbr = p.ptynbr
    	    try:
	    	pc.commit()
	    except:
	    	print 'duplicate: ', pc.pp()
    
movepricehist(415754, 426251)

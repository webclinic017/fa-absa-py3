import ael, string
f = open('C:\\eq_mtm_price.csv')
line = f.readline()
line = f.readline()
mkt = ael.Party['internal']
while line:
    l = []
    line = line.rstrip()
    print line
    l = string.split(line, ',')
    ins = ael.Instrument[l[0]]
    pr = ins.historical_prices()
    for p in pr:
    	if p.day == ael.date_from_string('2005-03-03'):
	    if p.settle != (float)(l[1]):
	    	print l[0], p.settle, ' ', l[1]   
	    	pc = p.clone()   
	    	pc.settle = (float)(l[1])
	    	pc.commit()
    line = f.readline()
f.close()

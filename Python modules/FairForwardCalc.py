import ael

def FairForwardDates(date,*rest):
    Options = ael.Instrument.select('und_insaddr.insid = %s' % 'ZAR/ALSI')
    SAFEXFuturesOptions = []
    SAFEXDates = []
    SAFEXPrices = []
    for o in Options:
    	if o.otc == 0:
    	    SAFEXFuturesOptions.append(o)
    	    #SAFEXDates.append(o.exp_day)
	    prices = ael.Price.select('insaddr=%s' % o.insaddr)
	    if prices:
	    	LatestPrice = prices[0].settle
	    	LatestDate = prices[0].day
	    	for p in prices:
	    	    if p.day > LatestDate:
	    	    	LatestDate = p.day
		    	LatestPrice = p.settle
	    	SAFEXDates.append([o.exp_day, LatestPrice])
	    	SAFEXPrices.append(LatestPrice)
    
    FinalPrices = []
    length = len(SAFEXDates)
    for i in range(length):
    	min = SAFEXDates[0][0]
    	minprice = SAFEXDates[0][1]
    	for d in SAFEXDates:
	    if d[0] < min:
	    	min = d[0]
	    	minprice = d[1]
    	FinalPrices.append([min, minprice])
    	#print [min,minprice]
    	SAFEXDates.remove([min, minprice])
    #print 'FinalPrices', FinalPrices
    
    before = 0
    length = len(FinalPrices)
    for i in range(length-1):
    	if (date >= FinalPrices[i][0] and date < FinalPrices[i+1][0]):
	    before = FinalPrices[i][1]
	    beforedate = FinalPrices[i][0]
	    after = FinalPrices[i+1][1]
	    afterdate = FinalPrices[i+1][0]
	    #print before,after
	#print 'Inputted', date
    if before == 0:
    	before = FinalPrices[length-2][1]
	#print before
	beforedate = FinalPrices[length-2][0]
	after = FinalPrices[length-1][1]
	afterdate = FinalPrices[length-1][0]
    leg1 = beforedate.days_between(date)
    leg2 = date.days_between(afterdate)
    total = beforedate.days_between(afterdate)
    #print leg1,leg2,total,before,after
    return round(float(leg2)/float(total)*float(before) + float(leg1)/float(total)*float(after), 0)
FairForwardDates(ael.date_today().add_months(8))

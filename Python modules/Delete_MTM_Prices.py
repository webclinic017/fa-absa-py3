import ael
def displayMkt():
    ml = []
    for m in ael.Party.select('type="MtM Market"'):
    	ml.append(m.ptyid)
    return ml	
ael_variables = [('datem', 'DATE', 'string', None, None, 1, 0), ('market', 'MARKET', 'string', displayMkt(), None, 1, 0)]
def ael_main(params):
    pdat = params.get('datem')
    mark = params.get('market')
    print pdat, mark
    for i in ael.Instrument:
    	for p in i.historical_prices():
	    if p.ptynbr:
	    	if (p.ptynbr.ptyid == mark and p.day == ael.date_from_string(pdat)):
	    	    print p.insaddr.insid
	    	    p.delete()
    	    	    print 'Price Deleted'

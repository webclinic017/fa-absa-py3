import ael
def update_yc(ycs):
    for name in ycs:
        yc = ael.YieldCurve[name]
	if yc == None:
            log(1, "The Yield Curve %s does not exist" % name)
            continue
    	try:
            ycc = yc.clone()
            ycc.calculate()
            ycc.commit()
    	    ycc.simulate()
	    print 'YIELD_CURVE:', ycc.yield_curve_name
    	except RuntimeError, msg:
    	    print "not enough price information on included instruments "\
	    	"in %s." % (name)
list = ['ZAR-SWAP', 'USD-SWAP']

update_yc(list)

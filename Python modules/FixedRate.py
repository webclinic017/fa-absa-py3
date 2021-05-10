import ael
def getFixedRate(i,* rest):
    legs = i.legs()
    for l in legs: 
    	if l.type == 'Fixed':
	    return l.fixed_rate
    return 0.0

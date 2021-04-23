import ael
def changeOTC(temp, ins, *rest):
    i = ael.Instrument[ins]
    found = i.insid.find('OTC')
    if found != -1:
    	if i.otc == 0:
	    i_clone = i.clone()
	    i_clone.otc = 1
#	    i_clone.commit()
	    print(i_clone.insid, ' changed to OTC = ', i_clone.otc)

    	ael.poll()

    return 'Success'
    






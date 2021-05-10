import ael, time

def Instr_Info(ins, dsp, *rest):
        trds = ins.trades()
        if len(trds) == 0:
    	    return 'No Trades'
        else:
    	    if dsp == 'Portfolio':
    	    	data = ''
            	for t in trds:
		    if t.prfnbr:
		    	data = data + ',' + t.prfnbr.prfid
    	    	#removes comma at the beginning of the string			
	    	data = '' + data[1:]
	    	return data
	    else:
	    	#gets the last trade
	    	a = trds[len(trds)-1]
		#formats the time
    	    	tradetime = time.strftime('%a %b %d %H:%M:%S %Y', time.localtime(a.time))
    	    	data = tradetime + ', ' + a.prfnbr.prfid
	    	return data

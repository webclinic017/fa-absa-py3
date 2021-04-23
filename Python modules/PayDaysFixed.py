import ael
import InstrType

def conDate(t,*rest):
    

    try: outfile=open('c:\kexport.txt', 'a')
    except: raise 'can open'
    
    ins = t.insaddr.legs()
    
    for i in ins:
    
    	InsSubType = InstrType.InstrumentType(t, *rest)	 
	print InsSubType
	
    	if InsSubType == 'PrimeBS' or InsSubType == 'AmortisingPrimeBS':
	    fixpyday = ''
	    strfix = 9.9999999999
	    
	    if i.type == 'Float':
	    
	    	if i.payleg == 'Yes':
	    	
    	    	    cshflws = i.cash_flows()
	    	    
    	    	    flag = 0
    	    	    for c in cshflws:
    	    	    	if flag == 0:
	    	    	    fixpyday = fixpyday + str(c.pay_day)
	 
	    	    	    flag = 1
	    	    	else:
	    	    	    fixpyday = fixpyday + '; ' + str(c.pay_day)
    	
	    
		    	
 		    
	    
	
			
	    
			
    	    			    		    

    	
    outfile.write('%s,%s,%s,%s,%s,  %s, %s, %s,%s, %s,  %s, %s, %s, %s, %s\n' 
    %(t.trdnbr, fixpyday, i.curr.insid, ael.date_from_time(t.time),
    strfix, i.rolling_period, i.daycount_method, 
    i.pay_calnbr.calid,  InsSubType,
    i.start_day, i.end_day, i.nominal_amount()*t.quantity, 
    i.float_rate.insid, i.spread, t.premium))
	     
	    
    outfile.close()

		
			
    return fixpyday
	    
	


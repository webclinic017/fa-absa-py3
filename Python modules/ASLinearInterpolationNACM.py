import ael

def LinearInter(test, x, liquidcost, *rest):
    
    
    
    #check if x is within range
    if x > 180:
    	return 0


    #build dictionary of instruments	
    values = {12:'ZAR-JIBAR-12M',
    	      24:'ZAR/IRS/GEN/2Y',
       	      36:'ZAR/IRS/GEN/3Y',
    	      48:'ZAR/IRS/GEN/4Y',
    	      60:'ZAR/IRS/GEN/5Y',
    	      72:'ZAR/IRS/GEN/6Y',
    	      84:'ZAR/IRS/GEN/7Y',
    	      96:'ZAR/IRS/GEN/8Y',
    	      108:'ZAR/IRS/GEN/9Y',
    	      120:'ZAR/IRS/GEN/10Y',
    	      132:'ZAR/IRS/GEN/11Y',
    	      144:'ZAR/IRS/GEN/12Y',	      	      	      	      	      	      	      	      
    	      156:'ZAR/IRS/GEN/13Y',
    	      168:'ZAR/IRS/GEN/14Y',
    	      180:'ZAR/IRS/GEN/15Y'}


    #get list of sorted keys
    keylist = values.keys()
    keylist.sort()


    #find keys on either side of x
    flag = 'true'
    count = -1
    while flag == 'true':
	count = count + 1
	if count < len(keylist):
	    B = keylist[count]
	    if B >= x:
	    	flag = 'false'
	else:
	    flag = 'false'
    
    A = keylist[count-1]
    
    
    #get instruments and corresponding rates
    insA = ael.Instrument[values[A]]
    insB = ael.Instrument[values[B]]
    
        
    # base = ael.date_today()
    # today = base.add_banking_day(insA.curr,-1)
    today = ael.date_today()
    
    AA = insA.used_price(today, 'ZAR', None, None, 'SPOT') + liquidcost
    BB = insB.used_price(today, 'ZAR', None, None, 'SPOT') + liquidcost
    
    if B==12:
    	rateA = (((1+(AA/400.0))**(4.0/12.0))-1)*1200
    	rateB = (((1+(BB/100.0))**(1.0/12.0))-1)*1200
    elif A==12:	   
    	rateA = (((1+(AA/100.0))**(1.0/12.0))-1)*1200
    	rateB = (((1+(BB/400.0))**(4.0/12.0))-1)*1200
    else:
    	rateA = (((1+(AA/400.0))**(4.0/12.0))-1)*1200
    	rateB = (((1+(BB/400.0))**(4.0/12.0))-1)*1200
    
    

    #print A, x, B
    #print 'A', insA.insid, AA, rateA
    #print 'B', insB.insid, BB, rateB
    #print

    #apply interpolation
    #f(x) = f(x0) + (f(x1)-f(x0)) * (x - x0) / (x1 - x0)
    y = rateA + (rateB-rateA) * (x - A) / (B - A)
    
    
    
    return y


#main
x = 12
print 'x = ', x
liquidcost = 0
y = LinearInter(x, x, liquidcost)

print 'y = ', y

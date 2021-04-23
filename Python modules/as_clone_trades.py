import ael


def CopyTrade(temp, t, *rest):
    new_i = ael.Instrument.new(t.insaddr.instype)
    new_t = ael.Trade.new(new_i)
    
    #i_clone = t.insaddr.clone()
    t_clone = t.clone()
    print('BEFORE', new_t.pp())
    #new_i = i
    new_t = t
    new_t.quantity = t_clone.quantity + 1
    print(new_t.pp())
    print('\n\n\n')
    print(t_clone.pp())
    
    #new_i.commit()
    new_t.commit()
    t_clone.commit()
    #i_clone.commit()
    '''
    try:
        new_i.commit()
        new_t.commit()
        print new_t.pp()
        print 'Done'
        
    except:
        print 'Error committing Trade'
    '''
    return 'Success'


#main
t = ael.Trade[906659]
print(CopyTrade(1, t))






def add_cashflow(trd, type, value, factor, dat, subtype):
    legs = trd.insaddr.legs()
    l = legs[0].clone()
    
    if abs(value) > 0.000000001:
    	cf = ael.CashFlow.new(l)
    	cf.type = type 
    else:
    	return 'No Cashflow Booked'
    
    if type in ('Fixed Amount'):
    	cf.fixed_amount = value
     	cf.nominal_factor = 1
    	cf.pay_day = dat

    try:
    	cf.commit()
	#print 'Cashflow committed'
	return 'Success'
    except:
    	print('Error commiting cashflow')
    	return 'Error'
 
    


import ael
 
def ADD_DAILY_PRICE(*rest):
    ins = ael.Instrument['SACPI Daily']
    index = ael.Instrument['SACPI']
    today = ael.date_today()
    for p in ins.prices():
        if p.ptynbr != None:
            if p.ptynbr.ptyid == 'SPOT':
                #if p.day == ael.date_today():
                new_price = p.clone()
                cpi_ref = index.cpi_reference(today)
                new_price.bid = cpi_ref 
                new_price.ask = cpi_ref
                new_price.settle = cpi_ref
                new_price.last = cpi_ref
                new_price.day = today
                try:
                    new_price.commit()
                    ael.log('SUCCESS - PRICE UPDATED')
                    return 'SUCCESS - PRICE UPDATED'
                except:
                    ael.log('FAIL - Could not update SPOT price for today')
                    return 'FAIL - Could not update SPOT price for today'
                    
    '''            
    new_price = ael.Price.new()
    new_price.day = ael.date_today()  
    new_price.insaddr = ins.insaddr
    new_price.curr = ael.Instrument['ZAR'].insaddr
    new_price.ptynbr = ael.Party['SPOT'].ptynbr
    cpi_ref = index.cpi_reference(ael.date_today())
    new_price.bid = cpi_ref
    new_price.ask = cpi_ref
    new_price.settle = cpi_ref
    new_price.last = cpi_ref
    try:
        new_price.commit()
        ael.log('SUCCESS - PRICE ADDED')
        return 'SUCCESS - PRICE ADDED'
        
    except:
        ael.log('FAIL - Could not create SPOT price for today')
        return 'FAIL - Could not create SPOT price for today'
                        
    return
    '''
#print ADD_DAILY_PRICE()                        
    
  


 





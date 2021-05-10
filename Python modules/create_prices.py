'''
this is called from the ASQL, PriceCreator

it copies an existing price (p) into a new price entry in a different market for the day. 

please check that the day is correct
p_clone.day = ael.date_today().add_days(-1)
'''


import ael


def create_p(temp, i, p, m, *rest):

    fnd_sob = 0                
    for prc in ael.Instrument[i].historical_prices():    
    #for prc in ael.Instrument[i].prices():
        if prc.ptynbr != None:            
            if prc.ptynbr.ptyid == 'SPOT' and p.curr == prc.curr and p.day == prc.day:
            #if prc.ptynbr.ptyid == 'SPOT_SOB' and p.curr == prc.curr and prc.day == ael.date_today():  
                fnd_sob = 1
                psob = prc

    if fnd_sob == 1:
        #if psob.day <= i.maturity_date:               
        sob_clone = psob.clone()
    else:
        sob_clone = ael.Instrument[i].historical_prices()[0].new()
        
       
    sob_clone.bid = p.settle
    sob_clone.ask = p.settle
    sob_clone.settle = p.settle
    sob_clone.last = p.settle
    sob_clone.day = ael.date_today().add_days(-1)
    sob_clone.ptynbr = ael.Party[m]
    sob_clone.curr = p.curr

    try:
        sob_clone.commit()
        sobflag = 1
        return 'Success'
    except:
        err = err + ' Could not copy SPOT to SOB'
        return 'Failed'




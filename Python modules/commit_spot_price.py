import ael

"""
coded by anil April 2009
function takes an insid as an argument and commits a spot price to the latest price table
a combination instrument calls the function
"""

def commitprice(i, *rest):

    ins = ael.Instrument[i]
    pv = ins.present_value()
    b = pv*100
    #print 'price', b   
    #print 'ins insaddr', ins.insaddr
    
    party = ael.Party['SPOT']
    c = party.ptynbr
    
    currency = ael.Instrument['ZAR']
    d = currency.insaddr
    
    prices = ins.prices()
        
    
    if len(prices)>0:
        for lp in prices:
            if lp.ptynbr.ptyid == 'SPOT':
                np = lp.clone()
                np.settle = b
                np.day = ael.date_today()
                
                try:
                    np.commit()
                except:    
                    ael.log("existing spot not restated")
        
    elif len(prices) == 0:                 
        p = ael.Price.new()
        p.insaddr = ins.insaddr #link the price to the instrument
        p.day = ael.date_today()
        p.curr = d #insaddr of the 'ZAR' currency
        p.settle = b #PV of ins * 100
        p.ptynbr = c #ptynbr of the SPOT party
        p.bid = 0
        p.ask = 0
        p.last = 0
                
        try:
            p.commit()
        except:    
            ael.log("could not commit new spot")
        

    
    return
   
   


commitprice('ZAR/KNOCKINSWAP//12.53/11.0500')

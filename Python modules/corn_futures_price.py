import ael

"""
ael that requires an corn futures instrument ID and the resated SAFEX price
the ael commits this new resated price to the price entry for each inisid passed to it
from the ASQL SAAGRI_Corn_Futures
"""


def corn (temp,i,np, *rest):
    insonly = ael.Instrument[i]   
    
    insprices = insonly.prices()
    
    for p in insprices:
        today = ael.date_today()
        date = today.add_banking_day(ael.Instrument[i].curr, 0)
        if p.day == date:
            if p.ptynbr.ptyid == 'SPOT':
                b = p.settle
                
                print 'insid effected = ', insonly.insid
                print 'for date', date
                print 'old price', p.settle
                clonep = p.clone()
                clonep.settle = np
                
                try:
                    clonep.commit()
                    print 'new price', clonep.settle
                except:
                    print insonly.insid, 'new price not committed'
    
       
    return b
        
            

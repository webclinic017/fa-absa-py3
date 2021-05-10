'''
Name      : GM_Spot_Days
Developer : Tshepo Mabena
Date      : 04/12/2009
Purpose   : This AEL changes the CurrSwap Spot Days to zero for non-zero Spot Days, as per Gavin's request.  
'''

import ael

def Spot_Offset(t,*rest):
        
    if t.insaddr.instype in ('CurrSwap'):
        Spot_Clone = t.insaddr.clone()
        Spot_Clone.spot_banking_days_offset = 0
        try:
            Spot_Clone.commit()
        except:
            ael.log('Could not commit Spot Days for trade number '+ t.trdnbr)

    return 'success'        


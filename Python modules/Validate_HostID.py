'''

Developer   : Tshepo Mabena
Date        : 08 September 2009
Description : Validates UNEXCOR CODE known as Hostid in Front for counterparties
 
'''

import ael

def ValidateUnexcor(temp,party,*rest):
    
    CodeList = []
    
    p = ael.Party[party].hostid
    
    if len(p) == 6:
        return 'Host ID Correct'
    
    else:
        return 'ERROR'

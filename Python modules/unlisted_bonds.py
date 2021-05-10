'''
this module is called by the ASQL 'FO_Confirmed_Unlisted_Bond_Trades'
to remove the thousand sepertor of the absolute value of Nominal and premium 
but still maintaining the precesion to 2 decimail plaes

CHG0122823 - Coded by Anil - deployed on 3 September 2020

'''

import acm

def trade_details(ael_trade, details, *rest):
    t = acm.FTrade[ael_trade.trdnbr]
    
    if details == 'nom':
        return '%.2f' % abs(t.Nominal())
    elif details == 'prem':
        return '%.2f' % abs(t.Premium())

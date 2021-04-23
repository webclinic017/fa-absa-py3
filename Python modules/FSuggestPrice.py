"""-----------------------------------------------------------------------------
PROJECT:                : Core Front Arena
PURPOSE                 : The hook function is called when the Suggest button 
                          is clicked in the Repo Reverse window. This hook can 
                          be used to customise the default reference price that 
                          should be applied for the repo trade.
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer              Description
--------------------------------------------------------------------------------
2010-08-23 409966    Francois Truter        Return FInstrument.SLPrice for 
                                            Security Loan instruments
2011-01-12 581108    Rohan vd Walt          Print rolling base date suggestion for sec loans on bonds                                            
"""

import ael
import FBDPCommon

def suggest_undprice(trade):
    "Use the theoretical price rounded to 3rd decimal"
    price = 0
    undins = trade.insaddr.und_insaddr
    if (undins == None):
        return price
    elif trade.insaddr.instype == 'SecurityLoan':
        if trade.insaddr.und_insaddr.instype in ('Bond', 'IndexLinkedBond'): 
            rollBaseDate = trade.insaddr.legs()[0].start_day.add_days(7).first_day_of_week()
            print('Suggested Rolling Base Date from start date', trade.insaddr.legs()[0].start_day, 'is: (Monday)', rollBaseDate)
        acmUndIns = FBDPCommon.ael_to_acm(undins)
        price = acmUndIns.SLPrice()
    else:
        price = undins.theor_price()
    
    price = round(price, 3)
    print(undins.insid, price)
    return price

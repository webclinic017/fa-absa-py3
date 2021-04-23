"""-----------------------------------------------------------------------------
PURPOSE                 :  This script will check if a price has been set for today in specified markets. If found, 
                           it will override T-1's price with this one.
                            - We assume the price coming in for today is in fact T-1's closing price. As in the case 
                              for the Reuters feed for MSCI WD Index.
DEPATMENT AND DESK      :  AAM
REQUESTER               :  Suvarn Naidoo
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no  Developer                 Description
--------------------------------------------------------------------------------
2015-08-11  XXXXXXX    Rohan vd Walt             Initial Implementation
"""

import acm
from at_price import set_instrument_price
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()

ael_variables.add('InstrumentQF',
                  mandatory=True,
                  cls='FStoredASQLQuery',
                  collection=acm.FStoredASQLQuery.Instances(),
                  multiple=True,
                  label='Instrument Filter',
                  alt='The Query Folder that returns the instruments for which prices should be lagged')
                  
                  
def ael_main(params):
    #Check if latest price entry for each instrument for SPOT market value is set (for today)
    
    #Update Price Entry for T-1, with above price.
    #Update SPOT_SOB price with above price.
    instruments = params['InstrumentQF'][0].Query().Select()
    today = acm.Time().DateToday()
    
    for ins in instruments:
        print(ins.Name())
        previousBusinessDay = ins.Currency().Calendar().AdjustBankingDays(today, -1)
        print(previousBusinessDay)
        for p in ins.Prices():
            if p.Day() == today and p.Market() == acm.FParty['SPOT']:
                print('Price found - moving to T-1 and updating SOB')
                set_instrument_price(ins, acm.FParty['SPOT_SOB'], p.Settle(), date_string = today)
                set_instrument_price(ins, acm.FParty['SPOT'], p.Settle(), date_string = previousBusinessDay)
                set_instrument_price(ins, acm.FParty['SPOT_MID'], p.Settle(), date_string = previousBusinessDay)
                set_instrument_price(ins, acm.FParty['internal'], p.Settle(), date_string = previousBusinessDay)
    print('Completed Successfully')

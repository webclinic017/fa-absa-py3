"""-----------------------------------------------------------------------
MODULE
    SAFI_update_TRS_yields__

DESCRIPTION
    Specification:
        ZAR-TRS-INFLATION-BOND curve yields need to be automatically updated whenever 
    the ZAR-INFLATION-BOND yields are updated.

    Implementation:
        For all the benchmarks of ZAR-INFLATION-BOND, find corresponding instrument with 
    'TRS_' prefix and copy prices from primary index-linked bonds to their 'TRS_' prefixed
    counterparts
        
    


    Project             : ABCAP IT Front Arena Minor Works
    Date                : 2012-01-20
    Purpose             : Update yields on the ZAR-TRS-INFLATION-BOND curve according to ZAR-INFLATION-BOND curve
    Department and Desk : Fixed Income   Bond Desk
    Requester           : Thalia Petousis
    Developer           : Peter Fabian
    CR Number           : C879940

HISTORY
================================================================================
Date         Change no    Developer           Description
--------------------------------------------------------------------------------
2012-01-20   C879940      Peter Fabian        Initial implementation 
ENDDESCRIPTION
-----------------------------------------------------------------------"""

import ael, acm
import SAGEN_PriceCopy # for update_price function
from at_ael_variables import AelVariableHandler

def _find_price(prices, market):
    """ Returns price on specified market if there is any in prices list.
    """
    for price in prices:
        if price.Market().Name() == market:
            return price

# create a list of markets for user to choose
marketList = []
for market in acm.FParty.Select('type = "Market"'):
        marketList.append(str(market.Name()))
    
for market in acm.FParty.Select('type = "MtM Market"'):
        marketList.append(str(market.Name()))
marketList.sort()
ael_variables = AelVariableHandler()

ael_variables.add('curve',
                  label='curve',
                  cls=acm.FYieldCurve,
                  default='ZAR-Gov-Bonds-Disc',
                  mandatory=True)

ael_variables.add('Markets',
                  label='Markets',
                  cls='string',
                  collection = marketList,
                  default='SPOT,SPOT_SOB,PRICETEST',
                  mandatory=True,
                  multiple=True)
def ael_main(parameters):

    # find all the instruments that are benchmarks for ZAR-INFLATION-BOND curve 
    
    curve = parameters['curve']
    benchmarks = curve.Benchmarks()
    instruments = map(lambda benchmark: benchmark.Instrument(), benchmarks)

    # read the markets for which we will change prices (specified by the user)
    markets = parameters['Markets']
    markets = map(lambda market: market.strip(), markets)
    
    # for each of the instruments
    for instrument in instruments:
        # get the name of auxiliary instrument (TRS_sth) 
        instr_name = instrument.Name()
        trs_instr_name = 'TRS_' + instr_name
        
        acm.Log('Processing instrument %s (corresponding to %s)' % (trs_instr_name, instr_name))
        
        # then the TRS_instrument itself
        trs_instrument = acm.FInstrument[trs_instr_name]
        
        # if the TRS_instrument exists 
        if trs_instrument:
            prices = instrument.Prices()
            # update price on each of the specified markets
            for market in markets:
                price_on_market = _find_price(prices, market)
                if price_on_market:
                    day_for_price = price_on_market.Day()
                    # since SAGEN_PriceCopy.update_price works with AEL date (and not string)
                    # we have to create AEL date object
                    if day_for_price:
                        date_for_price = ael.date_from_string(price_on_market.Day())
                    else:
                        date_for_price = ael.date_today()

                    # update TRS_instrument's price
                    SAGEN_PriceCopy.update_price(instrument, date_for_price, market, trs_instrument, date_for_price, market)
                else:
                    acm.Log('No price on %s market for instrument %s' % (market, instr_name))
        else:
            acm.Log('Instrument %s (corresponding to %s) not found, can not update its price' % (trs_instr_name, instr_name))
    
    print("Completed Successfully")

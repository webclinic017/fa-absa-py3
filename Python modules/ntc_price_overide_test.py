"""-----------------------------------------------------------------------------
PROJECT                 : NTC Convertible Option Price Overide 
PURPOSE                 : Intra day price moveover of instrument theoretical price onto spot price field for valuation control on mtm from feed option
DEPATMENT AND DESK      : FO Equity Derivatives Trading, Options Desk
REQUESTER               : Nivash Suknununn 
DEVELOPER               : Marko Milutinovic 
CR NUMBER               :  446045
-----------------------------------------------------------------------------"""

import acm
print 'hallo'
class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FOrderBookSheet')
    
    @classmethod
    def get_price( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
        
def overide_spot(ins, update_ins):
    print 'hallo'
    i = acm.FInstrument[ins]
    try:
        val = SheetCalcSpace.get_price(i, 'Price Theor')
        theo_price = val.Value().Number()
        print 'THEOR CALC'
    except exception, e:
        val = SheetCalcSpace.get_price(i, 'Internal Market Price')
        theo_price = val.Value().Number()
           
    updat = acm.FInstrument[update_ins]
    print theo_price
    '''
    for price in updat.Prices():
        if price.Market().Name() == 'SPOT':
            if price.Day() == acm.Time().DateToday():
                price.Bid(theo_price)
                price.Ask(theo_price)
                price.Last(theo_price)
                price.Settle(theo_price)
                price.Currency(updat.Currency())
                price.Commit()
    '''
    return

try:
    overide_spot('ZAR/NTC/OTC/22SEP11/C/15.33', 'ZAR/NTC/OTC/22SEP11/C/15.33')
except Exception, ex:
    print str(ex)


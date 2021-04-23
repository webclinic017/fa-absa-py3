import ael
import acm

'''---------------------------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------------------'''
class OrderBookSheetCalcSpace( object ):

    CALC_SPACE = acm.FCalculationSpace('FOrderBookSheet' )
  
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = OrderBookSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
       
       
class PortfolioSheetCalcSpace( object ):

    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
  
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = PortfolioSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
        
'''---------------------------------------------------------------------------------------------------------------------------
M.KLIMKE Probably better just to call ael.PresentValue() but then this could be directly done from ASQL
---------------------------------------------------------------------------------------------------------------------------'''
def getPV(trade, *rest):

    #trd = acm.CreateTradeRow(acm.FTrade[trade.trdnbr],1)
    #eval = acm.GetCalculatedValueFromString(trd, 'Standard', 'object:*"valPLEnd"', acm.CreateEBTag())
    #return eval.Value()
    i       = acm.FInstrument[trade.insaddr.insid]
    calc    = PortfolioSheetCalcSpace.get_column_calc(i, 'Portfolio Value End')
    return  calc.Value().Number()

'''---------------------------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------------------'''
def getDelta(trade, *rest):
    return trade.delta_implicit()

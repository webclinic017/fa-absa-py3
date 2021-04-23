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
M.KLIMKE
---------------------------------------------------------------------------------------------------------------------------'''


def get_deltaCash(ins, *rest):
    i = acm.FInstrument[ins.insid]
    #eval = acm.GetCalculatedValueFromString(i, 'Standard', 'object:*"deltaPct"[useDatabasePrice=1]', acm.CreateEBTag())
    #return (eval.Value() * 100)
    calc    = PortfolioSheetCalcSpace.get_column_calc(i, 'Portfolio Delta Cash')
    return  calc.Value().Number()

def get_gammaCash(ins, *rest):
    i = acm.FInstrument[ins.insid]
    #eval = acm.GetCalculatedValueFromString(i, 'Standard', 'object:*"gammaCash"[useDatabasePrice=1]', acm.CreateEBTag())
    #return eval.Value()
    calc    = PortfolioSheetCalcSpace.get_column_calc(i, 'Portfolio Gamma Cash')
    return  calc.Value().Number()

def get_vega(ins, *rest):
    i = acm.FInstrument[ins.insid]
    #eval = acm.GetCalculatedValueFromString(i, 'Standard', 'object:*"vega"[useDatabasePrice=1]', acm.CreateEBTag())
    #return eval.Value()
    calc    = OrderBookSheetCalcSpace.get_column_calc(i, 'Vega')
    return  calc.Value().Number()

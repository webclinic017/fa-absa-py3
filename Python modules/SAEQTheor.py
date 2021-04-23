import acm
'''-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------'''
class OrderBookSheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FOrderBookSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = OrderBookSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------'''
def Prices(temp,Instr,*rest):

    '''M.KLIMKE
    adfl="portPriceSourceTheorPrice"
    context = acm.GetDefaultContext()
    tag = acm.CreateEBTag()
    eval = acm.GetCalculatedValueFromString(ins, context, adfl, tag)
    return eval.Value()'''
    i       = acm.FInstrument[str(Instr)]
    calc    = OrderBookSheetCalcSpace.get_column_calc(i, 'Price Theor')
    return  calc.Value().Number()
'''-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------'''
#print Prices(None,'USD/XAU')

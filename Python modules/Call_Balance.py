import acm

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    
class SheetCalcSpace( object ):
    
    CALC_SPACE = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
        
def get_CallBalance(trade, *rest):

    try:    
        column_id = 'Deposit balance'
        
        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        value = calc.Value().Number()
       
        CallBalance = float(value)
           
    except:
        CallBalance = 0.0    
        
    return round(CallBalance, 2)



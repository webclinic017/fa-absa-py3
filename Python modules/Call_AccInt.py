import ael, acm

'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
def get_AccInt(temp,trd,startDate,endDate,*rest):

    t = acm.FTrade[trd]
    
    SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
    SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
    SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)
    
    calc    = SheetCalcSpace.get_column_calc(t, 'Portfolio Accrued Call Interest')
    
    x = calc.Value().Number()
    
    SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
    SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    
    return  x

'''---------------------------------------------------------------------------------------------------
print get_AccInt(1,1581354,'1970-01-01','2009-11-23')
---------------------------------------------------------------------------------------------------'''


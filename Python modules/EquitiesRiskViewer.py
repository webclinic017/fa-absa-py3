'''===========================================================================
==================== EquitiesRiskViewer supporting module ====================
==========================================================================='''
import acm
     
class PortfolioSheetCalcSpace(object):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
  
    @classmethod
    def get_column_calc(cls, obj, column_id):
        calc = PortfolioSheetCalcSpace.CALC_SPACE.CreateCalculation(obj, column_id)
        return calc

def getInstrumentPrice(ins, *rest):
    # ins is assumed to be an ael_entity
    i = acm.FInstrument[ins.insid]
    calc = PortfolioSheetCalcSpace.get_column_calc(i, 'Portfolio Value End')
    retVal = calc.Value().Number()

    return retVal

def getInstrumentCashDelta(ins, *rest):
    # ins is assumed to be an ael_entity
    i = acm.FInstrument[ins.insid]
    calc = PortfolioSheetCalcSpace.get_column_calc(i, 'Portfolio Delta Cash')
        
    return  calc.Value().Number()

def getInstrumentCashGamma(ins, *rest):
    # ins is assumed to be an ael_entity
    i = acm.FInstrument[ins.insid]
    calc = PortfolioSheetCalcSpace.get_column_calc(i, 'Portfolio Gamma Cash')

    return  calc.Value().Number()



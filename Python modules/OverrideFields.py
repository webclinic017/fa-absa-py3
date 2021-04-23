"""---------------------------------------------------------------------------------------------------------------
Project                 : Client Valuation Project
Purpose                 : Developed the feed for Exposure Management. 
                           
Department and Desk     : IT - CTB Primary Markets  
Requester               : Phil Ledwaba
Developer               : Tshepo Mabena
CR Number               : 829680  
------------------------------------------------------------------------------------------------------------------"""
import ael, acm, csv, time
import ael, acm

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def FXRate(i, date, toCurr, *rest):    
    
    curr1 = acm.FCurrency[i]
    curr2 = acm.FCurrency[ toCurr ]
    baseCurr = acm.FCurrency[ 'USD' ]
    if curr1.Name() != baseCurr.Name():
        fxRateCurr1 = curr1.Calculation().FXRate( StandardCalcSpace.CALC_SPACE, baseCurr, date ).Number()
    else:
        fxRateCurr1 = 1
    if curr2.Name() != baseCurr.Name():
        fxRateCurr2 = baseCurr.Calculation().FXRate( StandardCalcSpace.CALC_SPACE, curr2, date ).Number()
    else:
        fxRateCurr2 = 1
    return fxRateCurr2 * fxRateCurr1

class SheetCalcSpace( object ):
    
    CALC_SPACE = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc

def get_Vega(trade,date,toCurr, *rest):

    try:    
        column_id = 'Portfolio Vega'
            
        calc   = SheetCalcSpace.get_column_calc(trade, column_id)
        tradeCurrency = trade.Currency().Name()
        
        FxRate  = FXRate(tradeCurrency, date, toCurr)
        
        Value   = calc.Value().Number()
        VegaZar = round(Value*FxRate, 0)
        
    except:
        VegaZar = 0.0
        
    return VegaZar
    
def get_Gamma(trade,date,toCurr,*rest):
    
    try:
        column_id = 'Portfolio Gamma'
        
        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        Value = calc.Value().Number()
        
        tradeCurrency = trade.Currency().Name()
            
        FxRate   = FXRate(tradeCurrency, date, toCurr)
        GammaZar = round(Value/FxRate, 0)
        
        if abs(GammaZar) > 1000000000000:
            GammaZar = 0.0
        else:
            GammaZar
    except:
        GammaZar = 0.0
    
    return GammaZar
    
def get_EQDelta(trade, *rest):

    try:    
        column_id = 'Portfolio Delta Implicit Equity'
        
        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        Value = calc.Value()
        EQDelta = float(Value)
        
    except:
        EQDelta = 0.0    
        
    return round(EQDelta, 0)

def get_YDelta(trade,date,ToCurr,*rest):

    try:
        column_id = 'Portfolio Delta Yield'
            
        tradeCurrency = trade.Currency().Name()
            
        FxRate   = FXRate(tradeCurrency, date, ToCurr)

        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        Value = calc.Value().Number()
        
        YDelta = round(FxRate*Value, 0)
        
    except:
        YDelta = 0.0
        
    return YDelta

def get_Volatility(trade, *rest):

    try:    
        column_id = 'Portfolio Volatility'
        
        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        Value = calc.Value()
        
        Volatility = round(Value*100, 2)
        
    except:
        Volatility = 0.0
        
    return Volatility

def get_DivDelta(trade, *rest):
    
    try:
        column_id = 'Portfolio Dividend Delta %'
        
        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        Value = calc.Value().Number()
        
    except:
        Value = 0.0
        
    return round(Value, 0)
    
def get_EQGamma_Cash(trade, *rest):

    try:
        column_id = 'Portfolio Gamma Implicit Cash Equity'
        
        calc  = SheetCalcSpace.get_column_calc(trade, column_id)
        Value = calc.Value().Number()
        
    except:
        Value = 0.0
        
    return round(Value, 0)



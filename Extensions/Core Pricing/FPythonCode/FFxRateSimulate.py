"""
    This module contains hooks to simulate Instrument FX Rate in Deal Sheet.
    Triggered from the column 'Instrument FX Rate'
"""
import acm

def changeFxRate(row, col, calcval, val, operation):
    
    instrument = row.Instrument()
    fromCurrency = instrument.PayLeg().Currency()
    toCurrency = instrument.RecLeg().Currency()
    if None == val or fromCurrency == toCurrency:
        return
    
    if acm.FCurrencySwap == instrument.Class():
        eval = calcval.GetEvaluator()
        fxMatrixEval = eval.FindAdHoc('fxMatrix', acm.FObject).Value()[0]
        fxMatrixEval.Unsimulate()
        
        if acm.FSymbol('remove') == operation:
            return
        
        space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        unShiftedVal = fromCurrency.Calculation().FXRate(space, toCurrency)
        
        fxMatrix = fxMatrixEval.Value()
        if fxMatrix.BaseCurrency().IsEqual(fromCurrency):
            shiftCurrency = toCurrency
            shiftFactor = unShiftedVal.Number() / val.Number() -1
        else:
            shiftCurrency = fromCurrency
            shiftFactor = val.Number() / unShiftedVal.Number() -1
        shiftFactor *= 100
        shiftFXMatrixRelativePercent = acm.GetFunction('shiftFXMatrixRelativePercent', 4)
        shiftedFxMatrix = shiftFXMatrixRelativePercent(fxMatrix, shiftCurrency, shiftFactor, 0)
        fxMatrixEval.Simulate(shiftedFxMatrix, 0)
            
   
           
            

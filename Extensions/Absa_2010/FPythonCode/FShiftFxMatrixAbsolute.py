
import acm

def shiftFXMatrixAbsolute(fxMatrix, currency, absoluteShift):
    shiftFXMatrixRelativePercent = acm.GetFunction('shiftFXMatrixRelativePercent', 3)
    valdate = acm.Time().DateValueDay()
    baseCurrency = fxMatrix.BaseCurrency().Name()
    S = fxMatrix.GetCell(baseCurrency, currency).CellValue(valdate).Number()
    relativeShift = -100.0*absoluteShift/(S+absoluteShift)
    fxMatrixShifted = shiftFXMatrixRelativePercent(fxMatrix, currency, relativeShift)
    return fxMatrixShifted

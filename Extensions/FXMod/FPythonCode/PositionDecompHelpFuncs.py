import acm
import FUxCore
from math import floor
from math import log10
from math import fabs


# ^^^^^^ Help Functions ^^^^^^

def FxRate(insPair, date):
    space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    ins1 = insPair.Instrument1()
    ins2 = insPair.Instrument2()
    fxRate = ins1.Calculation().FXRate(space, ins2, date).Value().Number()
    space.Clear()
    space = None
    return fxRate

def PMRate(insPair, date):
    space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    ins1 = insPair.Instrument1()
    ins2 = insPair.Instrument2()
    invFxRate = 1.0 / ins1.Currency().Calculation().FXRate(space, ins2, date).Value().Number()
    fwdPrice = ins1.Calculation().ForwardPrice(space, date).Value().Number()
    space.Clear()
    return fwdPrice / invFxRate

def DeriveRateFromPoints(currPair, fromRate, points, deriveSpot):
    rate = fromRate	
    if currPair and points and fromRate:
        if deriveSpot:
            sign = -1 
        else: 
            sign = 1			
        rate = fromRate + sign * points * currPair.PointValue()
    return rate

def PrecisionForCurrencyObject(currencyOrPair):
    if currencyOrPair.IsKindOf(acm.FInstrumentPair):
	return int(floor(fabs(log10(currencyOrPair.PointValue())))+2)
    precision = 2
    rs = currencyOrPair.RoundingSpecification()
    if rs and rs.Oid():
        rounding = acm.FRounding.Select("roundingSpec = %s"%rs.Oid())
	if rounding:
            rounding = rounding[0]
        precision = rounding.Decimals()
    return precision
	
def AdjustingForDifferentSpotDaysEnabled():
    return acm.ObjectServer().UsedValuationParameters().FxCrossSplittingIfSpotDiffer()

# Use this function instead for FromPairNeedsSwap, ToPairNeedsSwap, SplitPairNeedsSwap
def NeedsSwap(isSpotTrade, spotDate, moveDate):
    if(isSpotTrade and AdjustingForDifferentSpotDaysEnabled()):
        return spotDate and spotDate != moveDate
    else:
        return False
	
def CurrencyObjectFormatter(currencyOrPair ):
    numFormatter = acm.FNumFormatter('').Clone()
    prec = 0
    if type(currencyOrPair) == int:
        prec = currencyOrPair
    elif currencyOrPair and currencyOrPair.IsKindOf(acm.FBusinessObject):
        prec = PrecisionForCurrencyObject(currencyOrPair)
    numFormatter.NumDecimals(prec)
    return numFormatter

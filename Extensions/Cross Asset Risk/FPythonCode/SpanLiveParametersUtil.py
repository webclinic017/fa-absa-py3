import acm

def updateLiveParam(data, liveParam):
    (id, risk_array, delta) = (data.At(0), data.At(1), data.At(2))
    liveParam.AddOrReplaceRiskArray(id, risk_array)
    liveParam.AddOrReplaceDelta(id, delta)
    
def createSpanLiveParameters(liveData):
    spanLiveParameters = acm.FSpanLiveParameters()
    if liveData:
        try:
            for el in liveData:
                updateLiveParam(el, spanLiveParameters)
        except AttributeError:
            updateLiveParam(liveData, spanLiveParameters)
    
    return spanLiveParameters
    
def spanVectorSupplier(vectorName):
    spanRAWeights = 14 * [1.0] + 2 * [0.35]
    spanVolScaling = 7 * [1.0, -1.0]+ 2* [0]
    spanPriceScaling = [0,              0, 
                        1.0 / 3,        1.0 / 3, 
                        -1.0 / 3,       -1.0 / 3, 
                        2.0 / 3,        2.0 / 3, 
                        -2.0 / 3,       -2.0 / 3, 
                        1,              1, 
                        -1,             -1, 
                        2,               -2]
    
    assertionErrorString = "All vectors used in the calculation of risk arrays must be of equal length"
    vectorLength = len(spanRAWeights)
    assert len(spanVolScaling) == len(spanPriceScaling) == vectorLength, assertionErrorString
    
    spanRADisplayVector = ["Scenario %i" % (i+1) for i in range(vectorLength)]
    
    return locals()[vectorName]

def getCombinedCommodityCurrencyFromInstrument(instrument, spanParameters):
    instrumentRecord = spanParameters.GetInstrument(instrument.Oid())
    currencySymbol = spanParameters.GetCurrency(instrumentRecord[4])
    return currencySymbol


import acm
import AquaMarketPriceUpdate

class TimeSeriesInformation:
    def __init__(self, name):
        self.name = name
        values = self.find_time_series_spec(name)
        self.has_time_series_spec = False
        if len(values) == 1:
            self.time_series_spec = values[0].Oid()
            self.has_time_series_spec = True

    def get_series_value(self, instrument_id, date):
        points = self.find_time_series(instrument_id, date, self.time_series_spec)
        if len(points) == 0:
            raise Exception("Sigma data not available")
            
        ins = acm.FInstrument[instrument_id]
        print 'Retrieving ---> %s %s for instrument %s' % (self.name, points[0].TimeValue(), ins.Name())
        return points[0].TimeValue()
            

    @staticmethod
    def find_time_series_spec(v):
        s = "fieldName=%s" % v
        return acm.FTimeSeriesSpec.Select(s)

    @staticmethod
    def find_time_series(instrument_oid, date, series_spec):
        s = "recaddr=%s and day='%s' and timeSeriesSpec=%s" % (instrument_oid, date, series_spec)
        points = acm.FTimeSeries.Select(s)

        return points

    @staticmethod
    def update_time_series_point(point_oid, value):
        time_series_point = acm.FTimeSeries[point_oid]
        time_series_point.TimeValue(value)
        time_series_point.Commit()

    @staticmethod
    def add_time_series_point(instrument_oid, date, value, series_spec):
        ts = acm.FTimeSeries()
        ts.Day(date)
        ts.TimeSeriesSpec(series_spec)
        ts.TimeValue(value)
        ts.Recaddr(instrument_oid)
        ts.Commit()

        return ts


SigmaPVSeries = TimeSeriesInformation("SigmaPV")
SigmaEquityDeltaSeries = TimeSeriesInformation("SigmaEqDelta")
SigmaEquityGammaSeries = TimeSeriesInformation("SigmaEqGamma")
SigmaEquityVegaSeries = TimeSeriesInformation("SigmaEqVega")
SigmaEquityVommaSeries = TimeSeriesInformation("SigmaEqVomma")
SigmaEquityVannaSeries = TimeSeriesInformation("SigmaEqVanna")
SigmaEquityRateDeltaSeries = TimeSeriesInformation("SigmaEqRateDelta")
SigmaThetaSeries = TimeSeriesInformation("SigmaTheta")

def GetContractSizeMultiplier(instrument):
    if instrument.QuoteType() == 'Per Contract':
        return instrument.ContractSize()
    else:
        return 1
        
def _isNumber(object):
    try:
        object = float(object)
        isNumber = True
    except:
        isNumber = False
    
    return isNumber

def theor_model_pv(ins, currency):
    result    = acm.FVariantDictionary()
    dateToday = acm.Time().DateToday()
    pv = SigmaPVSeries.get_series_value(ins.Oid(), dateToday)
    
    result.AtPut("result", pv)
    
    return result

def theor(ins, currency, date, underlyingValue, volatilityValueModel, discountRate):
    instrument = acm.FInstrument[ins.Name()]
    
    result    = acm.FVariantDictionary()
    dateToday = acm.Time().DateToday()
    if date > dateToday:
        oldPvValue = SigmaPVSeries.get_series_value(instrument.Oid(), dateToday)
        thetaValue = SigmaThetaSeries.get_series_value(instrument.Oid(), dateToday)
        
        oldPv = acm.DenominatedValue(oldPvValue, currency, dateToday)
        theta = acm.DenominatedValue(thetaValue, currency, dateToday)
        
        newResult = oldPv + theta
        result.AtPut("result", newResult)
        return result
    
    # get value from time series
    pvValue = SigmaPVSeries.get_series_value(instrument.Oid(), date)
    deltaValue = SigmaEquityDeltaSeries.get_series_value(instrument.Oid(), date)
    gammaValue = SigmaEquityGammaSeries.get_series_value(instrument.Oid(), date)
    vegaValue = SigmaEquityVegaSeries.get_series_value(instrument.Oid(), date)
    volgaValue = SigmaEquityVommaSeries.get_series_value(instrument.Oid(), date)
    vannaValue = SigmaEquityVannaSeries.get_series_value(instrument.Oid(), date)
    rhoValue = SigmaEquityRateDeltaSeries.get_series_value(instrument.Oid(), date)

    # create DenominatedValue
    pv = acm.DenominatedValue(pvValue, currency, date)
    delta = acm.DenominatedValue(deltaValue, currency, date)
    gamma = acm.DenominatedValue(gammaValue, currency, date)
    vega = acm.DenominatedValue(vegaValue, currency, date)
    volga = acm.DenominatedValue(volgaValue, currency, date)
    vanna = acm.DenominatedValue(vannaValue, currency, date)
    rho = acm.DenominatedValue(rhoValue, currency, date)

    # create result and populate
    result.AtPut("result", pv)
    result.AtPut("delta", delta)
    result.AtPut("gamma", gamma)
    result.AtPut("vega", vega)
    result.AtPut("volga", volga)
    result.AtPut("vanna", vanna)
    result.AtPut("rho", rho)
    
    if str(acm.Class()) == 'FTmServer':
        theoreticalPrice = pv.Number() * GetContractSizeMultiplier(ins)
        if theoreticalPrice and _isNumber(theoreticalPrice):
            AquaMarketPriceUpdate.AddPriceAel(ins, dateToday, theoreticalPrice)

    return result


def isDifferent(inp, inpShift):
    """Check if two arrays are different"""
    diff = []
    for i in range(len(inpShift)):
        if inp[i] != inpShift[i]:
            diff.append(i)
            
    return diff

    
def simpleRiskFunction(model, modelOutput, input, inputShift):
    """Risk function for model returning price greeks"""
    #Underlying differential
    dS = inputShift[3].Number() - input[3].Number()
    dv = inputShift[4] - input[4]
    dr = inputShift[5] - input[5]

    diff = isDifferent(input, inputShift)
    
    theorPrice = modelOutput.At("result")
    modelDelta = modelOutput.At("delta").Number()
    modelGamma = modelOutput.At("gamma").Number()
    modelVega  = modelOutput.At("vega").Number()
    modelVolga = modelOutput.At("volga").Number()
    modelVanna = modelOutput.At("vanna").Number()
    modelRho   = modelOutput.At("rho").Number()

    #Taylor approximation 
    if diff == [3]:
        recalcPrice = theorPrice.Number() + modelDelta * dS +  0.5 * modelGamma * dS * dS 
    elif diff == [4]:
        recalcPrice = theorPrice.Number() + modelVega * dv +  0.5 * modelVolga * dv * dv
    elif diff == [3, 4]:
        recalcPrice = theorPrice.Number() + modelDelta * dS +  0.5 * modelGamma * dS * dS + modelVega * dv +  0.5 * modelVolga * dv * dv + modelVanna * dv * dS
    elif diff == [5]:
        recalcPrice = theorPrice.Number() + modelRho * 0.00001
        
    else:
        return model.Call(inputShift)
    
    result = acm.FVariantDictionary()
    newResult = acm.DenominatedValue(recalcPrice, theorPrice.Unit(), theorPrice.DateTime())
    result.AtPut("result", newResult)
    return result

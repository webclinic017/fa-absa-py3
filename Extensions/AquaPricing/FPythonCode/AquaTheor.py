
import acm
import mx_connector
import aqua_stored_values
import AquaMarketPriceUpdate

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False
    
    return isNumber

def GetContractSizeMultiplier(instrument):
    if instrument.QuoteType() == 'Per Contract':
        return instrument.ContractSize()
    else:
        return 1

def theor_model_pv(ins, currency):
    result    = acm.FVariantDictionary()
    dateToday = acm.Time().DateToday()
    if aqua_stored_values.read_values():
        result = aqua_stored_values.get_result_pv(ins, currency, dateToday)
        return result
    mxData = mx_connector.MXInstrumentReader(ins, dateToday)
    pv = acm.DenominatedValue(mxData.GetMetric('Instrument/()/PresentValue'), currency, dateToday)
    result.AtPut("result", pv)
    return result

def theor(ins, currency, date, underlyingValue, volatilityValueModel, discountRate):
    result    = acm.FVariantDictionary()
    dateToday = acm.Time().DateToday()
    if date > dateToday:
        mxData = mx_connector.MXInstrumentReader(ins, dateToday)
        oldPV = acm.DenominatedValue(mxData.GetMetric('Instrument/()/PresentValue'), currency, dateToday) 
        theta = acm.DenominatedValue(mxData.GetMetric('Instrument/()/Theta'), currency, dateToday)
        newResult = oldPV + theta
        result.AtPut("result", newResult)
        return result
    
    if aqua_stored_values.read_values():
        result = aqua_stored_values.get_result(ins, currency, date)
        return result
    mxData = mx_connector.MXInstrumentReader(ins, date)
    newResult = acm.DenominatedValue(mxData.GetMetric('Instrument/()/PresentValue'), currency, date) 
    delta = acm.DenominatedValue(mxData.GetMetric('Instrument/(asset)/AssetDelta'), currency, date)
    gamma = acm.DenominatedValue(mxData.GetMetric('Instrument/(asset)/AssetGamma'), currency, date)
    vega = acm.DenominatedValue(mxData.GetMetric('Instrument/(asset)/AssetVega'), currency, date)
    volga = acm.DenominatedValue(mxData.GetMetric('Instrument/(asset)/AssetVolga'), currency, date)
    vanna = acm.DenominatedValue(mxData.GetMetric('Instrument2/(asset,asset1)/AssetVanna'), currency, date)
    rho = acm.DenominatedValue(mxData.GetMetric('Instrument/(currency)/RateDelta'), currency, date)
    result.AtPut("result", newResult)
    result.AtPut("delta", delta)
    result.AtPut("gamma", gamma)
    result.AtPut("vega", vega)
    result.AtPut("volga", volga)
    result.AtPut("vanna", vanna)
    result.AtPut("rho", rho)
    if str(acm.Class()) == 'FTmServer':
        theoreticalPrice = newResult.Number() * GetContractSizeMultiplier(ins)
        if theoreticalPrice and _isNumber(theoreticalPrice):
            AquaMarketPriceUpdate.AddPriceAel(ins, dateToday, theoreticalPrice)
            aqua_stored_values.save_result(result, ins, date)
    return result
    
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

def isDifferent(inp, inpShift):
    """Check if two arrays are different"""
    diff = []
    for i in range(len(inpShift)):
        if inp[i] != inpShift[i]:
            diff.append(i)
            
    return diff






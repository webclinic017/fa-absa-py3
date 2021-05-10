
import acm

#------------------------------------------------------------------------------
def FutureCashFlows(instrument):
    cfs = instrument.Legs().First().CashFlows()
    
    return [cf for cf in cfs if cf.SACCRLatestExercise() > 0]
    
#------------------------------------------------------------------------------
def SACCRParametersDict(aggregationValues, start, end, maturity, latestExercise, duration, delta, source, maturityFactor, notional, adjustedNotional):
    d = acm.FDictionary()
    
    for key in aggregationValues.Keys():
        d[key] = aggregationValues[key]
    
    d['Start'] = start
    d['End'] = end
    d['Maturity'] = maturity
    d['Latest Exercise'] = latestExercise
    d['Duration'] = duration
    d['Delta'] = delta
    d['Maturity Factor'] = maturityFactor
    d['Notional'] = notional
    d['Adjusted Notional'] = adjustedNotional
    d['Source'] = source
    
    return d

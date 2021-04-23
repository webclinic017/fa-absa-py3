
import acm
import math
import ael

def getValuationData(legInformations, staticLegInformations,today, valuationDate,FXDates, FXValues, riskFreeDiscountCurves,undRiskFreeDiscountCurve,fxRate, inclContractSize = False):
#TODO: add different averaging behavior, which will get triggered by certain criteria which still needs
#to be defined: going down, to calculate the average rate, instead of going across to calculate the 
#average of rate * underlying
#TODO: change spot date handling, spot is not always the correct date to pv, especially not, if the
#position that is valued is already in our books; current workaround: set spot offset to zero days on
#the instrument

    out = {}
    cfs = acm.FArray()
    cfPVs = acm.FArray()
    spotValue = 0.0
    for legInfo, staticLegInfo, insYC,in zip(legInformations, staticLegInformations, riskFreeDiscountCurves):
        currency = staticLegInfo.CurrencySymbol()
        infos = staticLegInfo.CashFlowInformations()
        for cfInfo in infos:
            rate = cfInfo.Rate(legInfo)
            # storage of rate is inconsistent
            if math.isnan(staticLegInfo.AcmLeg().UniqueCoupon()):
                rate = rate * 100
            fixingValues = cfInfo.FixingValues(legInfo)
            fixingDates = cfInfo.FixingDays()
            fixing_is_fixed = cfInfo.FixingIsFixed(today)
            if fixingValues.Size() != 0:
                sum=0
                for value, date, is_fixed in zip(fixingValues, fixingDates, fixing_is_fixed):
                    date = date[0:10]
                    index = FXDates.IndexOfFirstEqual(date)
                    #2017 Upgrade: FixingValues of the future are returned already multiplied
                    if not is_fixed:
                        sum+=value
                    else:
                        sum+=value*FXValues.At(index).Number()
                rate = sum / fixingValues.Size() 
            nominal = cfInfo.Nominal(legInfo).Number()
            
            if inclContractSize == False:
                proj = rate * nominal
            else:
                proj = rate * (nominal * staticLegInfo.ContractSize())
            
            # due to inconsistent cash handling between RPL and Cash columns:
            # if cash flow is not in Cash, it should be in Val
            if ael.date(valuationDate) < ael.date(cfInfo.PayDate()):
                cfPV = proj * insYC.Discount(valuationDate, cfInfo.PayDate())
            else:
                cfPV = 0.0
            #spotValue += cfPV
            
            # AR 675899: filter out cash flows end date >= cash flow end date not pay date,
            # due to unexpected filtering logic in FCashFlowInformation.MoveValue
            #if ael.date(valuationDate) < ael.date(cfInfo.EndDate()):
            #    cfPV = proj * insYC.Discount(valuationDate, cfInfo.PayDate())
            #else:
            #    cfPV = 0.0
            cfs.Add(acm.DenominatedValue(proj, currency, cfInfo.Id(), cfInfo.PayDate()))
            cfPVs.Add(acm.DenominatedValue(cfPV, currency, cfInfo.Id(), valuationDate))

    out['result'] = acm.DenominatedValue(spotValue, currency, valuationDate)
    out['cashFlowProjected'] = cfs
    out['cashFlowResult'] = cfPVs
    return out
    
#Theoretical valuation
def propValFxPriceSwap(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate):

    out = getValuationData(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate, False)
    return out
        
#Cash flow instrument historical cash
def propValFxPriceSwapCashForPL(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate):

    out = getValuationData(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate, True)
    return out['cashFlowProjected']

#Cash flow instrument projected
def propValFxPriceSwapProjected(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate):

    out = getValuationData(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate, False)
    return out['cashFlowProjected']

#Cash flow instrument pv
def propValFxPriceSwapResult(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate):

    out = getValuationData(legInformations, staticLegInformations, today, valuationDate, FXDates, FXValues, riskFreeDiscountCurves, undRiskFreeDiscountCurve, fxRate, False)
    return out['cashFlowResult']
    
def getFxPriceSwapExoticEventsPerType(object, type):

    dates =acm.FArray()
    values =acm.FArray()
    result =acm.FArray()

    if type == "Not Compo":
        for l in object.Legs():
            for r in l.Resets():
                dates.Add(r.Day())
                values.Add(1.0)
                
        result.Add(dates)
        result.Add(values)
        return result
        
    else:
        events  = acm.FExoticEvent.Select('type="Fx Rate" and instrument="{0}"'.format(object.Name()))
        events = events.SortByProperty('Date', True)
        
        for event in events:
            dates.Add(event.Date())
            values.Add(event.EventValue())

        result.Add(dates)
        result.Add(values)
        return result
   
def getFxPriceSwapFixingsValues(fxRates, instrument):
    values =acm.FArray()
    for a in fxRates:
        date = ael.date(a.DateTime()[0:10])
        event = acm.FExoticEvent.Select('type="FX Rate" and instrument="%s" and date = %s' % (instrument.Name(), date))

        if date >= ael.date_today():
            if event and event[0].EventValue() != -1:
                values.Add(acm.DenominatedValue(event[0].EventValue(), None, "Exotic Event", event[0].Date()))
            else:
                values.Add(acm.DenominatedValue(a.Number(), None, "Live Rate", event[0].Date()))
        else:
            if event and event[0].EventValue() != -1:
                values.Add(acm.DenominatedValue(event[0].EventValue(), None, "Exotic Event", event[0].Date())) 
            else:
                values.Add("#")
                
    return values

def getFxPriceSwapFxFixingsOnCashFlow(dates, fxRates, fixingIsFixed):
    allExoticEvents = {}
    cashFlowExoticEvents = []
    for rate in fxRates:
        date = ael.date(rate.DateTime()[0:10])
        allExoticEvents[str(date)] = rate.Number()
        
    for d, fixed in zip(dates, fixingIsFixed):
        date = ael.date(d[0:10])
        if not fixed:
            cashFlowExoticEvents.append(1.0)
        elif str(date) in allExoticEvents.keys():
            cashFlowExoticEvents.append(allExoticEvents[str(date)])
    return cashFlowExoticEvents
        
def getFxPriceSwapFxFixingAtDate(array, reset):
    
    for event in array:
        if ael.date(event.DateTime()[0:10]) == ael.date(reset.Day()):
            return [event.Number(), event.Type(), reset.Day()]
    return 0
    
def getFxPriceSwapUnderlyingCurrency(ins):
    for leg in ins.Legs():
        if leg.FloatRateReference():
            currency = leg.FloatRateReference().Currency()
    return currency

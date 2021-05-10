
from itertools import groupby

import acm

import CreditRiskCustomOverrides

ConvertToCurrencyAndReturnMax = acm.GetFunction('convertToCurrencyAndReturnMax', 4)

#-------------------------------------------------------------------------
def DocumentType(instrument):
    documentType = instrument.AdditionalInfo().CVADocument()
    if documentType:
        correct_list = 'Standard Document'
        correct_entry = acm.FChoiceList.Select('name="%s" and list="%s"' %(documentType, correct_list))
        return correct_entry[0]
    return documentType

#-------------------------------------------------------------------------
def PositionNotional(instrument, defaultPositionNotional, tradesInPosition, positionQuantity):    
    positionNotional = CreditRiskCustomOverrides.Custom_PositionNotional(instrument, tradesInPosition, positionQuantity)
    
    if positionNotional:
        dateToday = acm.Time.DateToday()
        return acm.DenominatedValue(positionNotional, instrument.Currency(), dateToday)
    
    return defaultPositionNotional
    
#-------------------------------------------------------------------------
def PositionNotionalFXData( fxRateInstrument, fxRates, toCurr, buySellFlows, accCurr ):
    notionalData = GetNotionalDataDict()
    
    keyfunc = lambda x: x.DateTime()
    sortedFlows = sorted(buySellFlows, key=keyfunc)
    
    for date, flows in groupby(sortedFlows, key=keyfunc):
        flowsOnDate = list(flows)
        
        assert len(flowsOnDate) == 2
        
        notional = PositionNotionalFX( fxRateInstrument, date, flowsOnDate, fxRates, toCurr, accCurr )
        
        notionalData['notionals'].Add(notional)
        notionalData['maturities'].Add( DateDifferenceInYears(acm.Time.AsDate(date), acm.Time.DateToday()) )
        notionalData['deltas'].Add(SupervisoryDeltaAdjustment( fxRateInstrument, flowsOnDate ) )
    
    return notionalData

#-------------------------------------------------------------------------
def PositionNotionalFX( fxRateInstrument, date, flowsOnDate, fxRates, toCurr, accCurr ):
    notional = CreditRiskCustomOverrides.Custom_PositionNotionalFX(fxRateInstrument, flowsOnDate, fxRates, toCurr, accCurr)
    
    if not notional:
        notional = DefaultPositionNotionalFX( date, flowsOnDate, fxRates, toCurr, accCurr )
        
    return notional

#-------------------------------------------------------------------------
def DefaultPositionNotionalFX( date, flowsOnDate, fxRates, toCurr, accCurr ):
    absFlowOnDate = [acm.Math.Abs( flow ) for flow in flowsOnDate if accCurr.AsSymbol() != flow.Unit()]
    
    notional = ConvertToCurrencyAndReturnMax( absFlowOnDate, fxRates, toCurr.AsSymbol() )
    
    return acm.DenominatedValue( float( notional ), toCurr.AsSymbol(), date )

#-------------------------------------------------------------------------
def SupervisoryDeltaAdjustment(fxInstrument, buySellFlows):
    
    if fxInstrument.IsKindOf(acm.FFxRate):
        currencyPair = fxInstrument.CurrencyPair(True)
    elif fxInstrument.IsKindOf(acm.FCurrencySwap):
        payCurrency = fxInstrument.FirstPayLeg().Currency()
        receiveCurrency = fxInstrument.FirstReceiveLeg().Currency()
        currencyPair = payCurrency.CurrencyPair(receiveCurrency)
       
    curr1 = currencyPair.Currency1()
    
    if curr1.AsSymbol() == buySellFlows[0].Unit():
        return 1 if float(buySellFlows[0]) > 0 else -1
    else:
        delta = 1 if float(buySellFlows[1]) > 0 else -1
        if fxInstrument.IsKindOf(acm.FCurrencySwap):
            delta = delta * -1
        return delta

#-------------------------------------------------------------------------
def PositionNotionalFxOption( option, positionQuantity, strikePrice, fxRates, toCurr, accCurr ):
    dateToday = acm.Time.DateToday()

    foreignCurrency = option.Underlying().AsSymbol()
    domesticCurrency = option.Currency().AsSymbol()

    foreignAmount = acm.DenominatedValue( positionQuantity, foreignCurrency, dateToday )
    domesticAmount = acm.DenominatedValue( positionQuantity * strikePrice, domesticCurrency, dateToday )
    
    flowsOnDate = [foreignAmount, domesticAmount]
    return DefaultPositionNotionalFX( dateToday, flowsOnDate, fxRates, toCurr, accCurr )
    
#-------------------------------------------------------------------------
def SupervisoryDeltaAdjustmentCurrencySwap(swap, positionQuantity, payAndReceiveNominalScaleFactors): 
    flowsOnDate = NotionalFlowsOnDateForCurrencySwap(swap, positionQuantity, payAndReceiveNominalScaleFactors)
    return SupervisoryDeltaAdjustment(swap, flowsOnDate)
    
#-------------------------------------------------------------------------
def NotionalFlowsOnDateForCurrencySwap(currencySwap, positionQuantity, payAndReceiveNominalScaleFactors):
    dateToday = acm.Time.DateToday()
    receiveLeg = currencySwap.FirstReceiveLeg()
    payLeg = currencySwap.FirstPayLeg()
    
    receiveCurrency = receiveLeg.Currency().AsSymbol()
    payCurrency = payLeg.Currency().AsSymbol()

    payLegNominalScaleFactor = payAndReceiveNominalScaleFactors[0]
    receiveLegNominalScaleFactor = payAndReceiveNominalScaleFactors[1]
    
    receiveAmount = acm.DenominatedValue( positionQuantity * receiveLegNominalScaleFactor, receiveCurrency, dateToday )
    payAmount = acm.DenominatedValue( positionQuantity * payLegNominalScaleFactor, payCurrency, dateToday)
    
    flowsOnDate = [receiveAmount, payAmount]
    return flowsOnDate
    
#-------------------------------------------------------------------------
def PositionNotionalCurrencySwap( currencySwap, positionQuantity, payAndReceiveNominalScaleFactors, fxRates, toCurr, accCurr ):
    dateToday = acm.Time.DateToday()
    flowsOnDate = NotionalFlowsOnDateForCurrencySwap(currencySwap, positionQuantity, payAndReceiveNominalScaleFactors)
    return DefaultPositionNotionalFX( dateToday, flowsOnDate, fxRates, accCurr, accCurr )

#-------------------------------------------------------------------------
def ODFDealtCurrency(instrument):
    if instrument.InsType() == 'FXOptionDatedFwd':
        
        if instrument.Currency() == instrument.GetCurrencyOne():
            return instrument.GetCurrencyTwo()
        else:
            return instrument.GetCurrencyOne()
            
    return None 

#-------------------------------------------------------------------------
def GetNotionalDataDict():
    notionalData = acm.FDictionary()
    notionalData.AtPut("notionals", acm.FArray())
    notionalData.AtPut("maturities", acm.FArray())
    notionalData.AtPut("deltas", acm.FArray())
    return notionalData

#-------------------------------------------------------------------------
def TimeToMaturity( maturityDate ):
    dateToday = acm.Time.DateToday()
    return DateDifferenceInYears( maturityDate, dateToday )
    
#-------------------------------------------------------------------------
def DateDifferenceInYears(date1, date2):
    dateDifference = float(acm.Time().DateDifference(date1, date2)) / 365
    return max(dateDifference, 0.0)
    

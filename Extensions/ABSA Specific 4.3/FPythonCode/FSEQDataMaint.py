""" Compiled: 2016-12-08 11:17:27 """

#__src_file__ = "extensions/structured_eq/admin/FSEQDataMaint.py"
import acm
import ael

"""
UPGRADE 2016.5 (H)

Custom code
"""
DRY_RUN = False
CHECK_FUTURE = False

F_FUTURE_VALUE = -1
UPDATE_HISTORICAL = False
        
''' 
Changing the variable below to True means that the script should change the Stike type  
from Rel Spot Pct or Rel Spot Pct 100 to Absolute for instruments of type Forward Start. 
If the instrument has both Forward Start and Barrier properties than also the relative 
Barrier settings will be changed to Absolute. Note that this is only applicable for 
Forward Start and not for Forward Start Performance. 
'''
changeStrikeToAbsolute = False

'''
The list below should contain Valuation Functions, used only for Forward Start Instruments. 
If the list is included; Forward Start Instruments with a mapped Valuation Function equal to 
a Function in the list will get Initial Fixings generated for every component Instrument of 
the underlying (Basket valuation). 
'''

'''multiUnderlyingList = [
    'Basket As Single Underlying', 
    'Moment Matching',
    'Gentle-Vorst',
    'Monte Carlo Basket Underlying', 
    'Quasi Monte Carlo',
    'Kirk'] 
'''   

exotic_options = acm.FOption.Select("exoticType=Other")
exotic_warrants = acm.FWarrant.Select("exoticType=Other")
variance_swaps = acm.FVarianceSwap.Select("")
volatility_swaps = acm.FVolatilitySwap.Select("")
certificates = acm.FCertificate.Select("")

class FExoticEventUpdateResult:
    def __init__(self):
        self.nHistoricalSuccess = 0
        self.nHistoricalFailed = 0
        self.nFutureSuccess = 0
        self.nFutureFailed = 0

    def addResult(self, anotherResult):
        self.nHistoricalSuccess += anotherResult.nHistoricalSuccess
        self.nHistoricalFailed += anotherResult.nHistoricalFailed
        self.nFutureSuccess += anotherResult.nFutureSuccess
        self.nFutureFailed += anotherResult.nFutureFailed
        
    def hasFailedUpdates(self):
        return (self.nHistoricalFailed > 0)
    
    def logResult(self):
        ael.log_all("Historical updates performed: " + str(self.nHistoricalSuccess))
        ael.log_all("Historical updates failed:    " + str(self.nHistoricalFailed))
        ael.log_all("Future updates performed:     " + str(self.nFutureSuccess))
        ael.log_all("Future updates failed:        " + str(self.nFutureFailed))
        
def GetExoticEventsOfKindForDate(derivative, eventType, dateToday, getHistorical):
    events = []
    allEventsOfType = derivative.GetExoticEventsOfKind(eventType)
    for event in allEventsOfType:
        if (event.Date() == dateToday or (getHistorical and event.Date() < dateToday)) and event.EventValue() == F_FUTURE_VALUE:
            events.append(event)
        elif CHECK_FUTURE and event.Date() > dateToday and event.EventValue() != F_FUTURE_VALUE:
            events.append(event)
    return events

def LogEventWritten(derivative, underlying, updatedEvent, oldValue, newValue):
    ael.log_all("\nInstrument:    " + derivative.Name())
    ael.log_all("Underlying:    " + updatedEvent.ComponentInstrument().Name())
    ael.log_all("Event date:    " + str(updatedEvent.Date()))
    ael.log_all("Old Value:     " + str(oldValue))
    ael.log_all("New Value:     " + str(newValue))
    ael.log_all("Event type:    " + str(updatedEvent.Type()))
    ael.log_all("---------------------------------------")

def WriteNewExoticEvent(eventValue, eventDate, eventType, derivative, underlying):
    newEvent = acm.FExoticEvent()
    newEvent.EventValue(eventValue)
    newEvent.Date(eventDate)
    newEvent.Type(eventType)
    newEvent.Instrument(derivative)
    newEvent.ComponentInstrument(underlying)
    try:
        newEvent.Commit()
        return newEvent
    except Exception, e:
        ael.log_all("Could not commit a new Exotic Event for instrument " + derivative.Name() + " of type " + eventType + " at date " + eventDate)
        return None

# Should be method on FExoticEvent
def ExoticEventCurrency(derivative, exoticEvent):
    underlying = derivative.Underlying()
    componentInstrument = exoticEvent.ComponentInstrument()

    if derivative.IsKindOf("FVolatilityFuture"):
        currency = derivative.Currency()
    else:
        if derivative.QuantoOptionType() == 'Quanto' and not underlying.IsEqual(componentInstrument):
            currency = componentInstrument.Currency()
        else: 
            currency = derivative.StrikeCurrency()
    return currency.Name()

def ExoticEventMtMPrice(derivative, exoticEvent): 
    currency = ExoticEventCurrency(derivative, exoticEvent)
    price = exoticEvent.ComponentInstrument().MtMPrice(exoticEvent.Date(), currency, 0)    
    return price

def UpdateExoticEventValue(exoticEvent, eventValue):
    oldValue = exoticEvent.EventValue()
    eClone = exoticEvent.Clone()
    eClone.EventValue = eventValue
    exoticEvent.Apply(eClone)
    try:
        if not DRY_RUN:
            exoticEvent.Commit()   
        LogEventWritten(exoticEvent.Instrument(), exoticEvent.Instrument().Underlying(), exoticEvent, oldValue, eventValue)
    except Exception, e:
        ael.log_all("Could not update Exotic Event Value, due to: %s" % str(e))
        
def UpdateExoticEventValueSecond(exoticEvent, eventValue):
    oldValue = exoticEvent.EventValueSecond()
    eClone = exoticEvent.Clone()
    eClone.EventValueSecond = eventValue
    exoticEvent.Apply(eClone)
    try:
        exoticEvent.Commit()
        LogEventWritten(exoticEvent.Instrument(), exoticEvent.Instrument().Underlying(), exoticEvent, oldValue, eventValue)
    except Exception, e:
        ael.log_all("Could not update Exotic Event Value 2, due to: %s" % str(e))

def UpdateExoticEventValueWithMtMPrice(exoticEvent):
    updateResult = FExoticEventUpdateResult()

    """
    UPGRADE 2016.5 (H)
    Copied from ABSA specific code
    """
    dateToday = acm.Time().DateNow()
    if exoticEvent.Date() > dateToday:
        updateResult.nFutureSuccess = 1
        UpdateExoticEventValue(exoticEvent, F_FUTURE_VALUE)
        return updateResult
    option = exoticEvent.Instrument()
    price = ExoticEventMtMPrice(option, exoticEvent)
    
    if price:
        UpdateExoticEventValue(exoticEvent, price)
        updateResult.nHistoricalSuccess = 1
    else:
        currency = ExoticEventCurrency(option, exoticEvent)
        underlying = option.Underlying()
        ael.log_all(underlying.Name() + 
                ": ERROR: No MtM price in exists in " + currency + \
                " at " + str(exoticEvent.Date()) + \
                " for component " + exoticEvent.ComponentInstrument().Name())
        updateResult.nHistoricalFailed = 1
    return updateResult

def UpdateExoticEventsForOption(exoticEvents):
    updateResult = FExoticEventUpdateResult()
    for e in exoticEvents:
        result = UpdateExoticEventValueWithMtMPrice(e)
        updateResult.addResult(result)
    return updateResult

def UpdateExoticEventsForCertificate(calcSpace, exoticEvents, instrument):
    updateResult = FExoticEventUpdateResult()
    for exoticEvent in exoticEvents:
        try:
            theoreticalPrice = instrument.Calculation().TheoreticalPrice(calcSpace).Value()
            feeAmount = theoreticalPrice.Number() / (100 / exoticEvent.EventValue() - 1)
            UpdateExoticEventValueSecond(exoticEvent, feeAmount)
            updateResult.nHistoricalSuccess = 1
            updateResult.addResult(updateResult)            
        except Exception, e:
            ael.log_all(instrument.Name() + ": ERROR: %s" % str(e))
            updateResult.nHistoricalFailed = 1
    return updateResult    
    
# Method to calculate values with strikes Rel Spot, Rel Spot Pct and Rel Spot Pct 100
# to Absolute terms
def CalcRelSpotToAbsolute(strikeType, relativeValue, fixingPrice):
    absoluteValue = 0
    if strikeType == 'Rel Spot':
        print("relativeValue: ", relativeValue)
        absoluteValue = fixingPrice + relativeValue
        print("absoluteValue: ", absoluteValue) 
    else:
        factor = 0
        if strikeType == 'Rel Spot Pct':
            factor = 100    
        absoluteValue = fixingPrice * ((factor + relativeValue) / 100) 
    return absoluteValue

    
# Method to have the Barrier options with strike of type Rel Spot, Rel Spot Pct and Rel Spot Pct 100
# valued or converted to Absolute terms
def RelSpotBarrierToAbsoluteIfForwardStart(instrument, fixingPrice):
    if instrument.Barrier() != 0:
        instrument.Barrier = CalcRelSpotToAbsolute(instrument.StrikeType(), \
                                                    instrument.Barrier(), \
                                                    fixingPrice)    
    
    if instrument.Exotic().DoubleBarrier() != 0:    
        instrument.Exotic().DoubleBarrier = CalcRelSpotToAbsolute(instrument.StrikeType(), \
                                                                    instrument.Exotic().DoubleBarrier(), \
                                                                    fixingPrice)    
        
    if instrument.Exotic().BarrierRiskManagement() != 0:    
        instrument.Exotic().BarrierRiskManagement = CalcRelSpotToAbsolute(instrument.StrikeType(), \
                                                                            instrument.Exotic().BarrierRiskManagement(), \
                                                                            fixingPrice)     

    if instrument.Exotic().SecondBarrierRiskMgmt() != 0:  
        instrument.Exotic().SecondBarrierRiskMgmt = CalcRelSpotToAbsolute(instrument.StrikeType(), \
                                                                            instrument.Exotic().SecondBarrierRiskMgmt(), \
                                                                            fixingPrice)    
    """ 
    UPGRADE 2016.5 (H)
    Old code:
    return instrument
    """
    

def UpdateStrikeTypeForForwardStart(instrument, dateToday):
    underlying = instrument.Underlying()
    undPrice = underlying.MtMPrice(dateToday, underlying.Currency(), 0)
    
    if undPrice > 0:
        if instrument.StrikeCurrency() == underlying.Currency() or (instrument.StrikeCurrency() != underlying.Currency() \
        	and instrument.StrikeCurrency().MtMPrice(dateToday, underlying.Currency(), 0) > 0.0):
            insClone = instrument.Clone()
            newStrikePrice = CalcRelSpotToAbsolute(insClone.StrikeType(), \
                                                    insClone.StrikePrice(), \
                                                    undPrice)
            if instrument.StrikeCurrency() != underlying.Currency():
                insClone.StrikePrice = newStrikePrice / instrument.StrikeCurrency().MtMPrice(dateToday, underlying.Currency(), 0)            
            else:
                insClone.StrikePrice = newStrikePrice
                    
            if instrument.IsBarrier():
                insClone = RelSpotBarrierToAbsoluteIfForwardStart(insClone, undPrice)
                ael.log_all(instrument.Name() + ": Changed relative Barrier properties to absolute.")
            
            insClone.StrikeType = 'Absolute'         
            instrument.Apply(insClone)
        
            try:
                instrument.Commit()
                ael.log_all(instrument.Name() + ": Changed strike from Rel Spot Pct to Absolute.")
            except:
                ael.log_all(instrument.Name() + ": ERROR: Could not Commit a strike change from Rel Spot Pct to Absolute.")            
        else:
            ael.log_all("ERROR: No MtM price in exists between " + underlying.Currency().Name() + " and " + instrument.StrikeCurrency().Name()) 
    else:
        ael.log_all(underlying.Name() + ": ERROR: No MtM price exists in " + underlying.Currency().Name() + " at " + dateToday)
                                        

def GenerateExoticEventsForForwardStart(instrument, dateToday, eventsForUpdate):
    generateEvents = True
    generatePerUnderlying = False
    e = instrument.GetExoticEventsOfKind('Price Fixing')
    for events in e:
        if events.Date() == dateToday and events.Value() != -1:
            ael.log_all("Fixing for " + instrument.Name() + " is already set.")
            generateEvents = False
            break
                
    if generateEvents == True: 
        underlying = instrument.Underlying()    
        if underlying.InsType() == 'EquityIndex' or underlying.InsType() == 'Combination':
            valFuncString = instrument.MappedCoreValuationFunction().Parameter()  
            
            # If the list (multiUnderlyingList) is used then the try statement is executed. 
            try:
                if valFuncString in multiUnderlyingList:
                    generatePerUnderlying = True
            except:
                func = acm.GetFunction('isEquityBasketModel', 1)      
                generatePerUnderlying = func(valFuncString)
            
        if generatePerUnderlying:
            insInBasket = underlying.Instruments()
            for ins in insInBasket:
                event = WriteNewExoticEvent(-1, dateToday, 'Price Fixing', instrument, ins.Oid())
                eventsForUpdate.append(event)
            
        else:
            event = WriteNewExoticEvent(-1, dateToday, 'Price Fixing', instrument, underlying.Oid())
            eventsForUpdate.append(event)
    
    return eventsForUpdate


def GetForwardStartInstruments(instrumentList, dateToday, getHistorical):
    forwardStarts = []
    for instrument in instrumentList: 
        if instrument.IsForwardStart() and (instrument.ExpiryDate() > dateToday): 
            forwardStartDate = instrument.Exotic().ForwardStartDate()
            if forwardStartDate == dateToday or (getHistorical and forwardStartDate < dateToday):
                if instrument.StrikeType() not in ('Rel Frw', 'Rel Frw Pct', 'Rel Frw Pct 100'):
                    forwardStarts.append(instrument)
                else:
                    ael.log_all(instrument.Name() + ": Instrument " + " must be updated manually.")
    return forwardStarts
    
def UpdateForwardStartInstruments(instrumentCollection, dateToday, updateHistorical, *rest): 
    ael.log_all("\nUpdating Forward Start options ...")
    fwdstarts = GetForwardStartInstruments(instrumentCollection, dateToday, updateHistorical)
    updateResult = FExoticEventUpdateResult()
    
    for instrument in fwdstarts:
        eventsForUpdate = GetExoticEventsOfKindForDate(instrument, 'Price Fixing', dateToday, updateHistorical)
        if (len(eventsForUpdate) == 0 and not changeStrikeToAbsolute) or (len(eventsForUpdate) == 0 and changeStrikeToAbsolute and instrument.Exotic().ForwardStartType() == 'Forward Start Perf'):
            eventsForUpdate = GenerateExoticEventsForForwardStart(instrument, dateToday, eventsForUpdate)
        
        result = UpdateExoticEventsForOption(eventsForUpdate)
        
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)
        if changeStrikeToAbsolute and (instrument.StrikeType() in ('Rel Spot', 'Rel Spot Pct', 'Rel Spot Pct 100')) and instrument.Exotic().ForwardStartType() == 'Forward Start': 
            UpdateStrikeTypeForForwardStart(instrument, dateToday) 
        
    ael.log_all("\n==============================")
    ael.log_all("FORWARD START OPTIONS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")
    
def GetAsianInstruments(instrumentList, dateToday, getHistorical):
    asianInstruments = []
    for instrument in instrumentList:
        if instrument.IsAsian() and instrument.ExpiryDate() >= dateToday:
            asianInstruments.append(instrument)
    return asianInstruments
    
def UpdateAsianInstruments(instrumentCollection, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Average options ...")
    asianInstruments = GetAsianInstruments(instrumentCollection, dateToday, updateHistorical)
    updateResult = FExoticEventUpdateResult()
    for instrument in asianInstruments:
        averagePriceEvents = GetExoticEventsOfKindForDate(instrument, 'Average price', dateToday, updateHistorical)
        averageStrikeEvents = GetExoticEventsOfKindForDate(instrument, 'Average strike', dateToday, updateHistorical)
        eventsForUpdate = averagePriceEvents + averageStrikeEvents
        result = UpdateExoticEventsForOption(eventsForUpdate)
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)

    ael.log_all("\n==============================")
    ael.log_all("AVERAGE OPTIONS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")

def GetBarrierInstruments(instrumentList, dateToday, getHistorical):
    barrierInstruments = []
    for instrument in instrumentList: 
        if instrument.IsBarrier() and (not instrument.IsKikoOption()) and instrument.ExpiryDate() > dateToday and \
            (instrument.Exotic().BarrierMonitoring() == "Discrete"):
            if not instrument.IsForwardStart() or (instrument.IsForwardStart() and \
                instrument.Exotic().ForwardStartDate() <= dateToday and \
                instrument.StrikeType() not in ('Rel Frw', 'Rel Frw Pct', 'Rel Frw Pct 100')):
                barrierStatus = instrument.Exotic().BarrierCrossedStatus()
                if barrierStatus != 'Crossed' and barrierStatus != 'Confirmed':
                    barrierInstruments.append(instrument)
    return barrierInstruments

def BarrierValueInUndQuotation(barrier, instrument, undQuotation, dateToday):
    strikeQuotation = instrument.StrikeQuotation()
    if undQuotation and strikeQuotation and (not undQuotation.IsEqual(strikeQuotation)):
        double = acm.GetFunction('double', 1)
        dv = acm.GetFunction('denominatedvalue', 4)
        barrierDV = dv(barrier, instrument.StrikeCurrency(), None, dateToday)
        
        """ 
        UPGRADE 2016.5 (H)
        Old code:
        return double(instrument.QuoteToQuote(barrierDV, dateToday, None, None, strikeQuotation, undQuotation))
        """
        roundingInformation = None
        roundingSpecification = instrument.RoundingSpecification()
        if roundingSpecification:
            roundingInformation = roundingSpecification.RoundingInformation()
        return double(instrument.QuoteToQuote(barrierDV, dateToday, None, None, strikeQuotation, undQuotation, False, roundingInformation))
        
    return barrier

def UpdateBarrierInstruments(instrumentCollection, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Barrier options ...")
    barrierInstruments = GetBarrierInstruments(instrumentCollection, dateToday, updateHistorical)
    nbrSaved = 0 
    for instrument in barrierInstruments:
        success = False
        eventList = GetExoticEventsOfKindForDate(instrument, 'Barrier date', dateToday, updateHistorical)
        
        if len(eventList) > 0:
            monitoringEvent = eventList[0]
            underlyingPrice = ExoticEventMtMPrice(instrument, monitoringEvent)
            if underlyingPrice:
                
                if instrument.StrikeType() in ('Rel Spot', 'Rel Spot Pct', 'Rel Spot Pct 100') and instrument.IsForwardStart():
                    forwardStartFixings = instrument.GetExoticEventsOfKind('Price Fixing')
                    if len(forwardStartFixings) == 1 and forwardStartFixings[0].Date() == instrument.Exotic().ForwardStartDate():
                        iClone = instrument.Clone()
                        fixingPrice = forwardStartFixings[0].EventValue()
                        iClone = RelSpotBarrierToAbsoluteIfForwardStart(iClone, fixingPrice)
                        
                        barrier = iClone.Barrier()
                        if iClone.IsDoubleBarrier():
                            doubleBarrier = iClone.Exotic().DoubleBarrier()
                    else:
                        ael.log("Problems adjusting Forward Start Barrier: " + instrument.Name())
                        ael.log("Too many Price Fixings, multiunderlying or no fixing on Forward Start date")
                        continue                
                elif instrument.StrikeType() in ('Rel Spot', 'Rel Spot Pct', 'Rel Spot Pct 100') and not instrument.IsForwardStart():
                    ael.log("Cannot adjust relative Barrier which is not Forward Start: " + instrument.Name())
                    continue
                else:
                    barrier = instrument.Barrier()
                    if instrument.IsDoubleBarrier():
                        doubleBarrier = instrument.Exotic().DoubleBarrier()
                
                undQuotation = monitoringEvent.ComponentInstrument().Quotation()
                barrier = BarrierValueInUndQuotation(barrier, instrument, undQuotation, dateToday)
                barrierIsCrossed = False
                crossedBarrier = None
                if instrument.IsDoubleBarrier():
                    doubleBarrier = BarrierValueInUndQuotation(doubleBarrier, instrument, undQuotation, dateToday)
                    lowerBarrier = min(barrier, doubleBarrier)
                    upperBarrier = max(barrier, doubleBarrier)
                    if lowerBarrier >= underlyingPrice:
                        crossedBarrier = lowerBarrier
                        barrierIsCrossed = True
                    elif upperBarrier <= underlyingPrice:
                        crossedBarrier = upperBarrier
                        barrierIsCrossed = True
                else:
                    barrierType = instrument.Exotic().BarrierOptionType()
                    if barrierType == "Down & Out" or barrierType == "Down & In":
                        barrierIsCrossed = (barrier >= underlyingPrice)
                        crossedBarrier = barrier
                    elif barrierType == "Up & Out" or barrierType == "Up & In":
                        barrierIsCrossed = (barrier <= underlyingPrice)
                        crossedBarrier = barrier
                if barrierIsCrossed:
                    insClone = instrument.Clone()
                    insClone.Exotic().BarrierCrossedStatus('Confirmed')
                    insClone.Exotic().BarrierCrossDate(monitoringEvent.Date())
                    try:
                        instrument.Apply(insClone)
                        instrument.Commit()
                        ael.log('%s: Spot price has crossed barrier: %f, underlying price: %f'\
                            % (instrument.Name(), crossedBarrier, underlyingPrice))
                        nbrSaved = nbrSaved + 1
                    except RuntimeError:
                        ael.log(instrument.Name() + ": The instrument has already been updated.")
            else:
                ael.log(instrument.Name() + ": No MtM price exists for component " 
                        + monitoringEvent.ComponentInstrument().Name())
        
        
    ael.log_all("\n==============================")
    ael.log_all("BARRIER OPTIONS")
    ael.log_all("Updated Barrier status:   " + str(nbrSaved))
    ael.log_all("==============================")

def GetCliquetInstruments(instrumentList, dateToday, getHistorical):
    cliquets = []
    for instrument in instrumentList:
        if instrument.IsCliquet() and instrument.ExpiryDate() > dateToday:
            cliquets.append(instrument)
    return cliquets
    
def UpdateCliquetInstruments(instrumentCollection, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Cliquet options ...")
    cliquetInstruments = GetCliquetInstruments(instrumentCollection, dateToday, updateHistorical)
    updateResult = FExoticEventUpdateResult()
    for instrument in cliquetInstruments:
        eventsForUpdate = GetExoticEventsOfKindForDate(instrument, 'Cliquet date', dateToday, updateHistorical)
        result = UpdateExoticEventsForOption(eventsForUpdate)
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)

    ael.log_all("\n==============================")
    ael.log_all("CLIQUET OPTIONS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")

def GetLadderInstruments(instrumentList, dateToday, getHistorical):
    ladders = []
    for instrument in instrumentList:
        if instrument.IsLadder() and instrument.ExpiryDate() > dateToday and \
            instrument.Exotic().LadderDiscreteMonitoring():
            ladders.append(instrument)
    return ladders
    
def UpdateLadderInstruments(instrumentCollection, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Ladder options ...")
    ladderInstruments = GetLadderInstruments(instrumentCollection, dateToday, updateHistorical)
    nbrSaved = 0 
    dateCastFunction = acm.GetFunction('date', 1)
    for instrument in ladderInstruments:
        ladderMonitoringEvents = GetExoticEventsOfKindForDate(instrument, 'Ladder date', dateToday, updateHistorical)
        if len(ladderMonitoringEvents) > 0:
            monitoringEvent = ladderMonitoringEvents[0]
            underlyingPrice = ExoticEventMtMPrice(instrument, monitoringEvent)
            if underlyingPrice:
                ladderRungEvents = instrument.GetExoticEventsOfKind('Ladder rung')
                for lre in ladderRungEvents:
                    if lre.Date() == dateCastFunction(instrument.ExpiryDate()):
                        rungValue = lre.EventValue()
                        if instrument.IsCallOption():
                            diffRung = rungValue - underlyingPrice
                        else:
                            diffRung = underlyingPrice - rungValue
                        if diffRung <= 0.0:
                            eClone = lre.Clone()
                            eClone.Date(dateToday)
                            lre.Apply(eClone)
                            lre.Commit()
                            ael.log_all("The rung " + str(rungValue) + " for the option " + instrument.Name() + " has been updated.")
                            ael.log_all("---------------------------------------")
                            nbrSaved = nbrSaved + 1
            else:
                ael.log(instrument.Name() + 
                ": No MtM price exists for component " + 
                monitoringEvent.ComponentInstrument().Name())

    ael.log_all("\n==============================")
    ael.log_all("LADDER OPTIONS")
    ael.log_all("Updated Rungs:   " + str(nbrSaved))
    ael.log_all("==============================")  
            
def GetVarianceSwapInstruments(varianceSwapList, dateToday, updateHistorical):
    varianceSwaps = []
    for instrument in varianceSwapList:
        if instrument.ExpiryDate() > dateToday:
            varianceSwaps.append(instrument)
    return varianceSwaps
    
def GetVolatilitySwapInstruments(volatilitySwapList, dateToday, updateHistorical):
    volatilitySwaps = []
    for instrument in volatilitySwapList:
        if instrument.ExpiryDate() > dateToday:
            volatilitySwaps.append(instrument)
    return volatilitySwaps
            
def UpdateVarianceSwapInstruments(varianceSwapList, dateToday, updateHistorical, *rest):
    """
    UPGRADE 2016.5 (H)
    
    #CR: 212697 - Rohan van der Walt - External Module to check for initial fixing of VarSwaps
    """
    from VarSwapInitialFixingFunctions import checkPriceFixingForVarianceSwapInstrument  

    ael.log_all("\nUpdating Variance Swaps ...")
    varianceSwaps = GetVarianceSwapInstruments(varianceSwapList, dateToday, updateHistorical)
    updateResult = FExoticEventUpdateResult()
    for instrument in varianceSwaps:
        variancePriceEvents = GetExoticEventsOfKindForDate(instrument, 'Variance price', dateToday, updateHistorical)
        
        """
        UPGRADE 2016.5 (H)
        
        #CR: 212697
        """
        variancePriceEvents = checkPriceFixingForVarianceSwapInstrument(variancePriceEvents)
        
        result = UpdateExoticEventsForOption(variancePriceEvents)
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)

    ael.log_all("\n==============================")
    ael.log_all("VARIANCE SWAPS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")
    
def UpdateVolatilitySwapInstruments(volatilitySwapList, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Volatility Swaps ...")
    volatilitySwaps = GetVolatilitySwapInstruments(volatilitySwapList, dateToday, updateHistorical)
    updateResult = FExoticEventUpdateResult()
    for instrument in volatilitySwaps:
        priceEvents = GetExoticEventsOfKindForDate(instrument, 'Price fixing', dateToday, updateHistorical)
        result = UpdateExoticEventsForOption(priceEvents)
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)

    ael.log_all("\n==============================")
    ael.log_all("VOLATILITY SWAPS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")
    
def GetRangeAccrualInstruments(instrumentList, dateToday, updateHistorical):
    rangeAccruals = []
    for instrument in instrumentList:
        if instrument.IsRangeAccrual() and instrument.ExpiryDate() > dateToday:
            rangeAccruals.append(instrument)
    return rangeAccruals
            
def UpdateRangeAccrualInstruments(instrumentCollection, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Range Accruals ...")
    rangeAccruals = GetRangeAccrualInstruments(instrumentCollection, dateToday, updateHistorical)
    updateResult = FExoticEventUpdateResult()
    for instrument in rangeAccruals:
        priceFixingEvents = GetExoticEventsOfKindForDate(instrument, 'Price Fixing', dateToday, updateHistorical)
        result = UpdateExoticEventsForOption(priceFixingEvents)
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)

    ael.log_all("\n==============================")
    ael.log_all("RANGE ACCRUALS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================") 

def GetCertificateInstruments(instrumentList, dateToday):
    certificates = []
    for instrument in instrumentList:
        if instrument.ExpiryDate() > dateToday:
            certificates.append(instrument)
    return certificates

def UpdateCertificateInstruments(instrumentList, dateToday, *rest):
    ael.log_all("\nUpdating Certificates ...")
    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    certificates = GetCertificateInstruments(instrumentList, dateToday)
    updateResult = FExoticEventUpdateResult()
    for instrument in certificates:
        relativeFeeEvents = []
        allEventsOfType = instrument.GetExoticEventsOfKind('Relative Monitoring Fee')
        for event in allEventsOfType:
            if event.Date() == dateToday:
                if event.EventValueSecond() == F_FUTURE_VALUE:
                    relativeFeeEvents.append(event)
                
        result = UpdateExoticEventsForCertificate(calcSpace, relativeFeeEvents, instrument)
        if result.hasFailedUpdates():
            ael.log_all("\n" + instrument.Name() + ": Failed to update all exotic events for instrument.")
            result.logResult()
            ael.log_all("---------------------------------------")
        updateResult.addResult(result)

    ael.log_all("\n==============================")
    ael.log_all("CERTIFICATES")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")     
    
def GetCustomInstruments(instrumentList, dateToday):
    returnList = []
    for ins in instrumentList:
        customInsDef = acm.DealCapturing().CustomInstrumentDefinition(ins)
        try:
            hook = customInsDef.GetExoticFixingsHook()
        except Exception, e:
            hook = None
            ael.log_all("\n" + ins.Name() + ": Exception in GetExoticFixingsHook: " + str(e))
        if hook:
            returnList.append((ins, hook))
    return returnList

def UpdateCustomInstruments(instrumentList, dateToday, updateHistorical, *rest):
    ael.log_all("\nUpdating Custom Instruments ...")
    insAndHookList = GetCustomInstruments(instrumentList, dateToday)
    updateResult = FExoticEventUpdateResult()
    for ins, hook in insAndHookList:
        exoticEventTypesToBeUpdated = hook(ins, dateToday, updateHistorical, updateResult)
        for eventType in exoticEventTypesToBeUpdated:
            events = GetExoticEventsOfKindForDate(ins,
                    eventType, dateToday, updateHistorical)
            result = UpdateExoticEventsForOption(events)
            if result.hasFailedUpdates():
                ael.log_all("\n" + ins.Name() + 
                    ": Failed to update exotic events for instrument.")
                result.logResult()
                ael.log_all("---------------------------------------")
            updateResult.addResult(result)
    ael.log_all("\n==============================")
    ael.log_all("CUSTOM INSTRUMENTS")
    ael.log_all("Summary:")
    updateResult.logResult()
    ael.log_all("==============================")

def AllExoticUpdateMethods(instrumentCollection):
    dateToday = acm.Time().DateNow()
    UpdateForwardStartInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    UpdateAsianInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    UpdateBarrierInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    UpdateCliquetInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    UpdateLadderInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    UpdateVarianceSwapInstruments(variance_swaps, dateToday, UPDATE_HISTORICAL)
    UpdateRangeAccrualInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    UpdateCertificateInstruments(certificates, dateToday)
    # CUSTOM
    
    """
    UPGRADE 2016.5 (H)
    
    Note: These were removed in the ABSA specific code.
    
    UpdateVolatilitySwapInstruments(volatility_swaps, dateToday, UPDATE_HISTORICAL)
    UpdateCustomInstruments(instrumentCollection, dateToday, UPDATE_HISTORICAL)
    """
    
def UpdateAllExoticOptions():
    instrumentCollection = list(exotic_options) + list(exotic_warrants)
    try:
        AllExoticUpdateMethods(instrumentCollection)        
        ael.log_all("\n==============================")
        ael.log_all("ALL EXOTIC MAINTENANCE IS DONE")
        ael.log_all("==============================")
        
    except Exception, e:
        ael.log_all("\n************************************************")
        ael.log_all("Could not preform updates for all exotics due to: %s" % str(e))
        ael.log_all("Will try to run the script again ")
        ael.log_all("*************************************************")
        UpdateAllExoticOptions()
        
ael_variables = []

def ael_main(dict):
    UpdateAllExoticOptions()

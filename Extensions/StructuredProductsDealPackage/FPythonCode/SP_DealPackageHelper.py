import acm
import math
from AttributeMetaData import ChoiceListSourceAttribute
import ChoicesExprInstrument, ChoicesExprExotic

# ######################
# General
# ######################

def SafeDivision(x, y, fallback):
    def SetFallback(fallback):
        if fallback is None:
            raise Exception('SafeDivision fallback value is None')
        return fallback 
    return x / y if y else SetFallback(fallback)

def MergeDictionaries(dict1, dict2):
    # Merge two dictionaries
    # dict2 will win when there is a key confict
    dictTemp = dict1.copy()
    dictTemp.update(dict2)
    return dictTemp

def StringValueIsInteger(value):
    try:
        int(value)
    except:
        return False
    return True

def InstrumentAndDealPackageId(dealPackage, trade = None):
    if trade is None:
        return '%s (Oid: %i)' % (dealPackage.InstrumentPackage().Name(), dealPackage.Originator().Oid())
    else:
        return '%s (Trade: %i)' % (dealPackage.InstrumentPackage().Name(), trade.Originator().Oid())

def AddFArrayItemToFDictionary(fDict, dictKey, value):
    if not fDict.HasKey(dictKey):
        fDict.AtPut(dictKey, acm.FArray())
    fDict[dictKey].Add(value)
    return fDict

def SuggestInstrumentName(name):
    if acm.FInstrument[name]:
        splitName = name.split('#')
        if len(splitName) == 1 or splitName[len(splitName) - 1].find('DP') < 0:
            return '%s#DP' % name
        else:
            last = splitName[len(splitName) - 1]
            if last == 'DP':
                return '%s1' % name 
            splitNbr = last.split('DP')
            try:
                number = int(splitNbr[len(splitNbr) - 1])
                nbrLength = len(splitNbr[len(splitNbr) - 1])
                return '%s%i' % (name[:-nbrLength], number + 1)
            except Exception as e:
                return '%s#DP' % name
    else:
        return name

# ######################
# Setup needed for the Structured Products module
# (i.e. not product specific)
# ######################
def SetupStructuredProductsBase():
    from DealCaptureSetup import DataSetUpUxShell
    definitionSetUp = DataSetUpUxShell('Structured Products', 0)
    
    setUpAddInfos    = [('Instrument', 'StructureType', 'ChoiceList', 'StructureType', 'RecordRef', [], None, False)]
    setUpChoiceLists = [('StructureType', 'Target Redemption Forward', 'TargetRedemptionForward'),
                        ('StructureType', 'Target Pivot Forward', 'TargetPivotForward'),
                        ('StructureType', 'Structured Forward', 'StructuredForward'),
                        ('StructureType', 'Accumulator', 'Accumulator'),
                        ('StructureType', 'BasketAutocall', 'BasketAutocall')]

    from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp

    for addinfo in setUpAddInfos:
        addInfoSetupObject = AddInfoSetUp(  recordType      = addinfo[0],
                                            fieldName       = addinfo[1],
                                            dataType        = addinfo[2],
                                            description     = addinfo[3],
                                            dataTypeGroup   = addinfo[4],
                                            subTypes        = addinfo[5],
                                            defaultValue    = addinfo[6],
                                            mandatory       = addinfo[7]
                                        )
        definitionSetUp.AddSetupItem( addInfoSetupObject )

    for choiceList in setUpChoiceLists:
        choiceListSetupObject = ChoiceListSetUp( list   = choiceList[0],
                                                 entry  = choiceList[1],
                                                 descr  = choiceList[2]
                                               )
        definitionSetUp.AddSetupItem( choiceListSetupObject )

    definitionSetUp.SetUp(True)

# ######################
# Date time handling
# ######################
def DatePeriodToDate(newDate, startDate = acm.Time().DateToday()):
    date = newDate
    if acm.Time().PeriodSymbolToDate(newDate):
        date = acm.Time.DateAdjustPeriod(startDate, newDate)
    return date

def DatePeriodToDateTime(newDate, startTime = acm.Time().TimeNow()):
    date = newDate
    if acm.Time().PeriodSymbolToDate(newDate):
        date = acm.Time.DateTimeAdjustPeriod(startTime, newDate, None, 'Following')
    return date

def IsDateTime(value):
    try:
        return acm.Time.IsValidDateTime(value)
    except RuntimeError:
        return False

def AddHalfPeriod(startDate, timePeriod):
    periodDate = acm.Time.DateAdjustPeriod(startDate, timePeriod)
    dateDifference = acm.Time.DateDifference(periodDate, startDate)
    return acm.Time.DateAdjustPeriod(startDate, '%iD' % (dateDifference / 2))

def FirstDate(date1, date2):
    if acm.Time.DateDifference(date1, date2) > 0:
        return date2
    return date1

def LastDate(date1, date2):
    if acm.Time.DateDifference(date1, date2) < 0:
        return date2
    return date1


# ######################
# Exotic Event Handling
# ######################

def AddExoticEvent(ownerInstrument, componentInstrument, type, date, value = None, endDate = None, valueSecond = None):

    ee = acm.FExoticEvent()
    ee.Instrument(ownerInstrument.Instrument())
    ee.ComponentInstrument(componentInstrument)
    ee.Type(type)
    ee.Date(date)
    if endDate:
        ee.EndDate(endDate)
    if value is not None:
        ee.EventValue(value)
    if valueSecond is not None: #Must check agains None as 0.0 could be a valid entry
        ee.EventValueSecond(valueSecond)
    ownerInstrument.ExoticEvents().Add(ee)
    ee.RegisterInStorage()

def GetInitialFixingEvent(ownerInstrument):
    events = ownerInstrument.GetExoticEventsOfKind('Initial Fixing')
    
    return events[0] if events else None

def GetInitialFixingEvents(ownerInstrument):
    events = ownerInstrument.GetExoticEventsOfKind('Initial Fixing')
    return events

def GetSpecificInitialFixingEvent(ownerInstrument, componentInstrument):
    events = ownerInstrument.GetExoticEventsOfKind('Initial Fixing')
    for event in events:
        if event.ComponentInstrument() == componentInstrument:
            return event
    return None
    
def GetInitialFixingValue(ownerInstrument, componentInstrument):
    event = GetInitialFixingEvent(ownerInstrument)
    
    if event:
        return event.EventValue()
    else:
        return -1.0

def GetInitialFixingDate(ownerInstrument, componentInstrument):
    event = GetInitialFixingEvent(ownerInstrument)
    if event:
        return event.Date()
    else:
        return acm.Time.SmallDate()

def SetInitialFixingValue(ownerInstrument, componentInstrument, value):
    event = GetInitialFixingEvent(ownerInstrument)
    if event:
        event.EventValue(value)
        if componentInstrument:
            event.ComponentInstrument(componentInstrument)
    else:
        AddExoticEvent(ownerInstrument, componentInstrument, 'Initial Fixing', acm.Time.SmallDate(), value)

def SetInitialFixingDate(ownerInstrument, componentInstrument, date):
    event = GetInitialFixingEvent(ownerInstrument)
    if event:
        event.Date(date)
        if componentInstrument:
            event.ComponentInstrument(componentInstrument)
    else:
        AddExoticEvent(ownerInstrument, componentInstrument, 'Initial Fixing', date, 1.0)

def SetInitialFixingUnderlying(ownerInstrument, componentInstrument):
    event = GetInitialFixingEvent(ownerInstrument)
    if event:
        event.ComponentInstrument(componentInstrument)
    else:
        AddExoticEvent(ownerInstrument, componentInstrument, 'Initial Fixing', acm.Time.SmallDate(), 1.0)

def ExoticEventDates(instrument, type):
    exoticDates =  acm.FArray()
    for exoticEvent in instrument.GetExoticEventsOfKind(type):
        exoticDates.Add(exoticEvent.Date())
    return exoticDates


# ######################
# Choice List Sources
# ######################

def BarrierTypeChoices():
    return ChoicesExprExotic.getBarrierOptionTypeChoices()

def BarrierMonitoringChoices(exotic):
    return ChoicesExprExotic.getBarrierMonitoringChoices(exotic)

def BarrierSingleChoices():
    return [e for e in acm.FEnumeration['enum(BarrierOptionType)'].Enumerators() if (e.upper().find('DOUBLE') < 0 and e != 'Custom' and e.upper().find('KIKO') < 0)]

def DoubleBarrierChoices():
    return [e for e in acm.FEnumeration['enum(BarrierOptionType)'].Enumerators() if (e.upper().find('DOUBLE')>=0 or e == 'None')]

def SettlementTypeChoices(instrument):
    return ChoicesExprInstrument.getSettlementTypeChoices(instrument)

def OptionTypeChoices(instrument):
    undType     = instrument.Underlying().InsType()
    return ChoicesExprInstrument.getOptionTypeChoices(undType)

def TradeTypeChoices():
    return acm.FEnumeration['enum(TradeType)'].Enumerators()

def FixingSourceChoices():
    return ChoicesExprInstrument.getFixingSources(True)

def RainbowTypeChoices():
    return [x for x in acm.FEnumeration['enum(rainbowOptionType)'].Enumerators() if x not in ('None', 'Custom')]

def BarrierStatusChoices():
    return acm.FEnumeration['enum(BarrierCrossedStatus)'].Enumerators()

def AveragePriceTypeChoices(averageStrikeType):
    return ChoicesExprExotic.getAveragePriceTypeChoices(averageStrikeType)

def AverageStrikeTypeChoices(averagePriceType):
    return ChoicesExprExotic.getAverageStrikeTypeChoices(averagePriceType)
    
def AverageMethodTypeChoices():
    return ChoicesExprExotic.getAverageMethodTypeChoices()

def DayMethodOnlyFollowingPreceding():
    return [x for x in acm.FEnumeration['enum(BusinessDayMethod)'].Enumerators() if x.find("Following") >= 0 or x.find("Preceding") >= 0]

# #########################
# Business Event Handling
# #########################
def CreateBusinessEvent(eventType):
    event = acm.FBusinessEvent()
    event.EventType(eventType)
    return event

def CreateTradeLink(busEvent, trade, tradeEventType = None):
    trdLink = acm.FBusinessEventTradeLink()
    trdLink.Trade(trade)
    trdLink.BusinessEvent(busEvent)
    if tradeEventType is not None:
        trdLink.TradeEventType(tradeEventType)
    return trdLink

def CreatePaymentLink(busEvent, payment):
    pmtLink = acm.FBusinessEventPaymentLink()
    pmtLink.Payment(payment)
    pmtLink.BusinessEvent(busEvent)
    return pmtLink

def CreateInstrumentLink(busEvent, ins):
    insLink = acm.FBusinessEventInstrumentLink()
    insLink.Instrument(ins)
    insLink.BusinessEvent(busEvent)
    return insLink

def CreateAndAddTradeLink(busEvent, trade, tradeEventType = None):
    trdLink = CreateTradeLink(busEvent, trade, tradeEventType)
    busEvent.TradeLinks().Add(trdLink)

def CreateAndAddPaymentLink(busEvent, payment):
    pmtLink = CreatePaymentLink(busEvent, payment)
    busEvent.PaymentLinks().Add(pmtLink)

def CreateAndAddInstrumentLink(busEvent, ins):
    insLink = CreateInstrumentLink(busEvent, ins)
    busEvent.InstrumentLinks().Add(insLink)

def CreateBusinessEventAndLinks(eventType, trades = [], payments = [], instruments = []):
    busEvent = CreateBusinessEvent(eventType)
    for trade in trades:
        CreateAndAddTradeLink(busEvent, trade)
    for pmt in payments:
        CreateAndAddPaymentLink(busEvent, pmt)
    for ins in instruments:
        CreateAndAddInstrumentLink(busEvent, ins)
    return busEvent

# #########################
# FX Rate Formatter
# #########################

def GetFXSpotForwardFormatter(currPair, inverse):
    if currPair:
        pointValue = currPair.PointValueInverse() if inverse else currPair.PointValue()
    else:
        pointValue = 0.0001
    numOfDecimals = int(-math.log10(pointValue))
    
    formatter = acm.Get('formats/FXRate').Clone()
    formatter.NumDecimals(numOfDecimals)
    return formatter

# return a formatter where the number of decimals is set 
# based on the points value or points value inverse of the currency pair.
# Number of decimals is returned based on curr2 per curr1.
def GetFxFormatter(curr1, curr2):
    if curr1 and curr2:
        currPair = curr1.CurrencyPair(curr2)
        if currPair:
            inverse = currPair.Currency2() == curr1
            return GetFXSpotForwardFormatter(currPair, inverse)
    return acm.Get('formats/FXRate')

def DefaultFxRateDecimals():
    return 4

def GetPointValueAsNumDecimals(pointValue):
    if pointValue == 0.0:
        return 0
    else:
        return -int(math.log10(pointValue))

def GetPointValueInverse(pair):
    return pair.PointValueInverse() if pair.PointValueInverse() else pair.PointValue()

def GetCurrencyPairPointsDomesticPerForeign(curr1, curr2):
    if curr1 and curr2:
        pair = curr1.CurrencyPair(curr2)
        if pair:
            if pair.Currency1() == curr1:
                return GetPointValueAsNumDecimals(pair.PointValue())
            else:
                return GetPointValueAsNumDecimals(GetPointValueInverse(pair))
    return DefaultFxRateDecimals()

def GetCurrencyPairPointsForeignPerDomestic(curr1, curr2):
    if curr1 and curr2:
        pair = curr1.CurrencyPair(curr2)
        if pair:
            if pair.Currency1() == curr2:
                return GetPointValueAsNumDecimals(pair.PointValue())
            else:
                return GetPointValueAsNumDecimals(GetPointValueInverse(pair))
    return DefaultFxRateDecimals()



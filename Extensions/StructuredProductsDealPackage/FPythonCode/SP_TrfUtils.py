
from __future__ import print_function
import acm, ael, math
from CompositeAttributeDevKit import CompositeAttributeDefinition
from DealPackageDevKit import ReturnDomainDecorator, Str, DealPackageUserException
from SP_BusinessCalculations import GetHistoricalFxRate


class SelectPackageType(CompositeAttributeDefinition):
    
    def OnInit(self, label, choiceListSource, definitionPrefix):
        self._label = label
        self._choiceListSource = choiceListSource
        self._currentlyOpeningen = None
        self._definitionPrefix = definitionPrefix
    
    def Attributes(self):
        return { 'packageType' : Str( label=self._label,
                                      objMapping=self.UniqueCallback('PackageType'),
                                      choiceListSource=self._choiceListSource)
               }
    
    @ReturnDomainDecorator('string')
    def PackageType(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.TrimPrefix(self.Owner().DealPackage().DefinitionDisplayName())
        else:
            definitionDisplayName = self.AddPrefixToDefinition(value)
            self._currentlyOpeningen = definitionDisplayName
            obj = acm.DealPackage.New(definitionDisplayName)
            self.OpenObject(obj)

    def TrimPrefix(self, displayName):
        nameNoPrefix = displayName.replace(self._definitionPrefix, '')
        nameNoSpace = nameNoPrefix.strip()
        return nameNoSpace

    def AddPrefixToDefinition(self, selectedDefinition):
        definitionName = '%s%s' % (self._definitionPrefix, selectedDefinition)
        return definitionName

    def OpenObject(self, obj):
        uxCallbacks = self.Owner().GetAttribute('uxCallbacks')
        if uxCallbacks:
            openCb = uxCallbacks.At('open')
            if openCb:
                acm.AsynchronousCall(openCb, [obj, self.OnOpenFail])

    def OnOpenFail(self):
        print ('Failed to open package of type "%s"'%self._currentlyOpeningen)
        
    def GetLayout(self):
        return self.UniqueLayout(""" 
            vbox(;
                packageType;
            );
            """)

def GetAllTRFProductTypes():
    subTypes = []
    #subTypes.append('Structured Forward')
    #subTypes.append('Target Pivot Forward')
    subTypes.append('Target Redemption Forward')
    return subTypes

def ExpiryPeriodToDate(ins, periodOrDate, startDate = acm.Time.DateToday()):
    # Note: ExpiryDateFromPeriod will create a pop up if called with
    #       a period that ends on a non banking day.
    #       In order to avoid pop-up, call this method with an instrment decorator
    #       that has AskAdjustToFollowingBusinessDay set to False
    value = periodOrDate
    if acm.Time.PeriodSymbolToDate(periodOrDate):
        if ins.UnderlyingType() == 'Curr':
            if ins.ForeignCurrency() and ins.DomesticCurrency():
                ccyPair = ins.ForeignCurrency().CurrencyPair(ins.DomesticCurrency())
                returnDate = ccyPair.ExpiryDate(startDate, periodOrDate)
            else:
                returnDate = ins.ExpiryDateFromPeriod(periodOrDate)
                if ins.ForeignCurrency():
                    returnDate = ins.ForeignCurrency().Calendar().ModifyDate(None, None, returnDate)
                elif ins.DomesticCurrency():
                    returnDate = ins.DomesticCurrency().Calendar().ModifyDate(None, None, returnDate)
            return returnDate
        else:
            returnDate = ins.ExpiryDateFromPeriod(periodOrDate)
            if ins.Underlying() and ins.Underlying().SettlementCalendar():
                returnDate = ins.Underlying().SettlementCalendar().ModifyDate(None, None, returnDate)
            elif ins.Currency() and ins.Currency().Calendar():
                returnDate = ins.Currency().Calendar().ModifyDate(None, None, returnDate)
            return returnDate
    return value

def TransformUsingDecorator(obj, value, inputField, outputField = None):
    tempObjDecorator = acm.FBusinessLogicDecorator.WrapObject(obj.StorageNew())
    if hasattr(tempObjDecorator, inputField):
        getattr(tempObjDecorator, inputField)(value)
        outputField = inputField if outputField is None else outputField
        transformedValue = getattr(tempObjDecorator, outputField)()
        return transformedValue
    return value

def GetInverseRate(value):
    if value == 0.0 or value is None:
        return 0.0
    return 1.0 / value

def StrikeToUseForAccumulation(ins, inverted):
    if ins.UnderlyingType() == 'Curr':
        if inverted:
            return -ins.StrikeForeignPerDomestic()
        else:
            return ins.StrikeDomesticPerForeign()
    else:
        return ins.StrikePrice()

def GetValueForeignPerDomestic(ins, storedValue):
    if ins.StrikeQuotation() is None or ins.StrikeQuotation().Name() != 'Per Unit Inverse':
        return GetInverseRate(storedValue)
    return storedValue

def GetValueDomesticPerForeign(ins, storedValue):
    if ins.StrikeQuotation() is not None and ins.StrikeQuotation().Name() == 'Per Unit Inverse':
        return GetInverseRate(storedValue)
    return storedValue

def Strike2ToUseForAccumulation(ins, inverted):
    if inverted:
        return -GetValueForeignPerDomestic(ins, ins.AdditionalInfo().Sp_Strike2())
    else:
        return GetValueDomesticPerForeign(ins, ins.AdditionalInfo().Sp_Strike2())

def FixingToUseForAccumulation(ee, inverted):
    if inverted and ee.ComponentInstrument() and ee.ComponentInstrument().InsType() == 'Curr':
        return -GetInverseRate(ee.EventValue())
    else:
        return ee.EventValue()

def PivotUseLower(ee):
    epsilon = 0.000001
    distanceFromPivot = abs(GetValueDomesticPerForeign(ee.Instrument(), ee.EventValue()) - GetValueDomesticPerForeign(ee.Instrument(), ee.Instrument().AdditionalInfo().Sp_PivotRate()))
    if distanceFromPivot < epsilon:
        return ee.Instrument().AdditionalInfo().Sp_PivotRateStrike() == 'Lower' 
    else:
        return GetValueDomesticPerForeign(ee.Instrument(), ee.EventValue()) < GetValueDomesticPerForeign(ee.Instrument(), ee.Instrument().AdditionalInfo().Sp_PivotRate())

def GetIntrinsicGain(ee):
    ins = acm.FBusinessLogicDecorator.WrapObject(ee.Instrument())
    invertedAcc = ins.AdditionalInfo().Sp_InvertedTarget()
    
    # Target Pivot Forward
    if ins.AdditionalInfo().StructureType() == 'Target Pivot Forward':
        return max(0.0,
                      ((FixingToUseForAccumulation(ee, invertedAcc) - StrikeToUseForAccumulation(ins, invertedAcc))
                        * {True:1.0,False:0.0}.get(PivotUseLower(ee), False))
                    + ((Strike2ToUseForAccumulation(ins, invertedAcc) - FixingToUseForAccumulation(ee, invertedAcc))
                        * {False:1.0,True:0.0}.get(PivotUseLower(ee), False))
                   )
    
    # Target Redemption Forward
    if ins.AdditionalInfo().StructureType() == 'Target Redemption Forward':
        return max(0.0, (FixingToUseForAccumulation(ee, invertedAcc) - StrikeToUseForAccumulation(ins, invertedAcc))
                  * {True:1.0,False:-1.0}.get(ins.OptionTypeIsCall()))
        
    return 0.0

def AccumulateValues(values, maxValue, adjustToMax, barrierValues = []):
    def Accumulate(val, next, max, adjust):
        if (val < max) or (max == 0.0):
            val += next
            if max and val > max and adjust:
                val = max
        return val

    accumulated = []
    
    for v in values:
        accumulated.append(Accumulate(accumulated[-1] if accumulated else 0, v, maxValue, adjustToMax))
    return accumulated

def TrfExpiryEvents(ins):
    return ins.GetExoticEventsOfKind('TRF Expiry')

def TrfExpiryEventsSortedByDate(ins):
    return TrfExpiryEvents(ins).SortByProperty('Date')

def TrfExpiryEvent(ins, date):
    trfExpiries = TrfExpiryEvents(ins)
    for trfExpiry in trfExpiries:
        if trfExpiry.Date() == date:
            return trfExpiry
    return None

def TrfExpiryEventPerPayDate(ins, date):
    trfExpiries = TrfExpiryEvents(ins)
    for trfExpiry in trfExpiries:
        if trfExpiry.EndDate() == date:
            return trfExpiry
    return None

def TrfExpiryEventsIncludeHistorical(instrument, dateToday, includeHistorical):
    events = []
    for event in TrfExpiryEvents(instrument):
        if (acm.Time.DateDifference(event.Date(), dateToday) == 0 or (includeHistorical and acm.Time.DateDifference(event.Date(), dateToday) < 0)):
            if event.EventValue() == -1.0:
                events.append(event)
    return events

def TrfAsianObservationEventsInMonth(instrument, periodDate):
    averagePriceEvents = []
    for averagePrice in instrument.GetExoticEventsOfKind('Average price'):
        averagePriceMonth = acm.Time.FirstDayOfMonth(averagePrice.Date())
        periodMonth = acm.Time.FirstDayOfMonth(periodDate)
        if acm.Time.DateDifference(averagePriceMonth, periodMonth) == 0:
            averagePriceEvents.append(averagePrice)
    return averagePriceEvents

def CalculateAverageFixing(averagePriceEvents, roundingSpec = None):
    def GetRounding(roundingSpec, attr):
        r = None
        rs = roundingSpec
        if rs and type(rs) == type(acm.FRoundingSpec()):
            r = next((r for r in rs.Roundings() if r.Attribute() == attr), None)
        return r
    
    avg = -1.00
    c1 = all(i.EventValue() > 0.0 for i in averagePriceEvents)

    if not c1:
        str = 'Missing daily fixings in period.'
        raise DealPackageUserException(str)
        
    ev = [e.EventValue() for e in averagePriceEvents]
    avg = sum(ev) / float(len(ev))
    
    round = GetRounding(roundingSpec, 'Settled Price')
    Round = acm.GetFunction('round', 3)
    if round:
        avg = Round(avg, round.Decimals(), round.Type())
    else:
        avg = Round(avg, 3, 'Normal')
        
    return avg

def BuySellMappingDictionary():
    return {'FromOptionType':{'Foreign' :{False:"SELL", True:"BUY"},
                              'Domestic':{False:"BUY", True:"SELL"}},
            'ToOptionType'  :{'Foreign' :{"SELL":False, "BUY":True},
                              'Domestic':{"SELL":True, "BUY":False}}}

def BuySellMappingFromOptionTypeDefault(direction):
    return 'SELL' if direction == 'Foreign' else 'BUY'

def BuySellMapping(instrument, direction, value = 'NoValue'):
    if value == 'NoValue':
        return BuySellMappingDictionary()['FromOptionType'][direction].get(instrument.OptionTypeIsCall(), BuySellMappingFromOptionTypeDefault(direction))
    else:
        optionType = BuySellMappingDictionary()['ToOptionType'][direction].get(value, False)
        instrument.SuggestOptionType(optionType)

def TrfHasBarrier(instrument):
    return instrument.Exotic() and instrument.Exotic().BarrierOptionType() in ('Up & In', 'Down & In', 'Double In')

#------------------------------------
# Fixing the FX rate
#------------------------------------
def FixFxRateCalculation(insDecorator, event):
    curr1 = insDecorator.ForeignCurrency()
    curr2 = insDecorator.DomesticCurrency()
    return GetHistoricalFxRate(curr1, curr2, event.Date())

# ----------------------------------------------------------------
# Exotic fixings hook referenced from Custom Instrument Definition
# ----------------------------------------------------------------
def TrfExoticFixingsHook(instrument, dateToday, updateHistorical, updateResult):
    return ['TRF Expiry']

def TrfAsianExoticFixingsHook(instrument, dateToday, updateHistorical, updateResult):
    # Work-around: Class and method definitions below are redundant with FSEQDataMaint. 
    # However, importing FSEQDataMaint cause performance penalty (due to 
    # Selects being assigned to globals)
    class FExoticEventUpdateResult:
        def __init__(self):
            self.nHistoricalSuccess = 0
            self.nHistoricalFailed = 0

        def addResult(self, anotherResult):
            self.nHistoricalSuccess += anotherResult.nHistoricalSuccess
            self.nHistoricalFailed += anotherResult.nHistoricalFailed

        def hasFailedUpdates(self):
            return (self.nHistoricalFailed > 0)

        def logResult(self):
            ael.log_all("Historical updates performed: " + str(self.nHistoricalSuccess))
            ael.log_all("Historical updates failed:    " + str(self.nHistoricalFailed))
            
    def LogEventWritten(derivative, underlying, updatedEvent, oldValue, newValue):
        ael.log_all("\nInstrument:    " + derivative.Name())
        ael.log_all("Underlying:    " + updatedEvent.ComponentInstrument().Name())
        ael.log_all("Event date:    " + str(updatedEvent.Date()))
        ael.log_all("Old Value:     " + str(oldValue))
        ael.log_all("New Value:     " + str(newValue))
        ael.log_all("Event type:    " + str(updatedEvent.Type()))
        ael.log_all("---------------------------------------")
            
    def UpdateExoticEventValue(exoticEvent, eventValue):
        oldValue = exoticEvent.EventValue()
        eClone = exoticEvent.Clone()
        eClone.EventValue = eventValue
        exoticEvent.Apply(eClone)
        try:
            exoticEvent.Commit()
            LogEventWritten(exoticEvent.Instrument(), exoticEvent.Instrument().Underlying(), exoticEvent, oldValue, eventValue)
        except Exception, e:
            ael.log_all("Could not update Exotic Event Value, due to: %s" % str(e))
                
    totalFixingResult = FExoticEventUpdateResult()
    eventsToProcess = TrfExpiryEventsIncludeHistorical(instrument, dateToday, updateHistorical)
    for event in eventsToProcess:
        eventUpdateResult = FExoticEventUpdateResult()
        observations = TrfAsianObservationEventsInMonth(instrument, event.Date())
        try:
            rs = instrument.RoundingSpecification()
            avg = CalculateAverageFixing(observations, rs)
            UpdateExoticEventValue(event, avg)
            eventUpdateResult.nHistoricalSuccess = 1
        except Exception, e:
            eventUpdateResult.nHistoricalFailed = 1
            ael.log_all(instrument.Name() + 
                    ": ERROR: " + str(e) + \
                    " (period ending %s)" % str(event.Date()))
        totalFixingResult.addResult(eventUpdateResult)
    if totalFixingResult.hasFailedUpdates():
        ael.log_all("\n" + instrument.Name() + 
            ": Failed to update exotic events for instrument.")
        totalFixingResult.logResult()
        ael.log_all("---------------------------------------")
    updateResult.addResult(totalFixingResult)
    return []

def MtMPriceFromFixingSource(exoticEvent, currency = None):
    fixingSource = None
    if exoticEvent and exoticEvent.Instrument():
        fixingSource = exoticEvent.Instrument().FixingSource()

    if fixingSource and exoticEvent.ComponentInstrument():
        space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        marketPriceParams = acm.FDictionary()
        marketPriceParams['priceDate'] = exoticEvent.Date()
        marketPriceParams['currency'] = exoticEvent.ComponentInstrument().Currency()
        marketPriceParams['marketPlace'] = fixingSource
        marketPriceParams['useSpecificMarketPlace'] = True
        marketPriceParams['typeOfPrice'] = 'ClosePrice'
        price = exoticEvent.ComponentInstrument().Calculation().MarketPriceParams(space, marketPriceParams).Value().Number()
        if math.isnan(price):
            price = 0.0
        return price, True
    return None, False

#----------------------
# General help methods
#----------------------
def GetPaymentsOfKinds(trade, kinds):
    kindPayments = acm.FArray()
    allPayments = trade.Payments()
    for payment in allPayments:
        if payment.Type() in kinds:
            kindPayments.Add(payment)
    return kindPayments

def GetPaymentsOfKind(trade, kind):
    kinds = acm.FArray()
    kinds.Add(kind)
    return GetPaymentsOfKinds(trade, kinds)

#-------------------------------------
# Custom Methods (Exotic Events)
#-------------------------------------
def TrfFixingDomesticPerForeign(ee):
    return ee.EventValue()

def TrfFixingForeignPerDomestic(ee):
    return GetInverseRate(ee.EventValue())

def TrfAccTarget(ee):
    acc = 0.0
    if ee.EventValue() <= 0.0:
        return None
    allEvents = ee.Instrument().GetExoticEventsOfKind('TRF Expiry').SortByProperty('Date')
    for event in allEvents:
        if event.Date() <= ee.Date() and event.EventValue() > 0.0:
            new_acc = GetIntrinsicGain(event)
            acc += new_acc
            if ee.Instrument().AdditionalInfo().Sp_AdjustedStrike():
                acc = min(acc, ee.Instrument().AdditionalInfo().Sp_TargetLevel())
            if acc >= ee.Instrument().AdditionalInfo().Sp_TargetLevel():
                break
    return acc

#----------------------
# TRF Setup
#----------------------
valuationGroupNameTRF = 'Target Redemption Forward'
mappingContext = 'Global'

add_info_specs = [['Instrument', 'sp_LeverageNotional', 'Double', 'Leveraged Notional', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_TargetLevel', 'Double', 'Target Redemption Level', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_AdjustedStrike', 'Boolean', 'Adjust the strike to cap the gain at the target redemption level', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_BarrierMemory', 'Boolean', 'Barrier will be considered hit if hit at any previous fixing', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_Barrier2Memory', 'Boolean', 'Barrier will be considered hit if hit at any previous fixing', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_RollingPeriod', 'String', 'Frequency of date schedule', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_PayDayMethod', 'BusinessDayMethod', 'Business Day Method for calculating delivery dates', 'Enum', ['Option'], None, False],
                 ['Instrument', 'sp_Strike2', 'Double', 'Second Strike Level', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_PivotRate', 'Double', 'Pivot Rate', 'Standard', ['Option'], None, False],
                 ['Instrument', 'sp_SettleInCurr2', 'Boolean', 'Cash settlement should take place in currency 2', 'Standard', [], None, False],
                 ['Instrument', 'sp_PivotRateStrike', 'ChoiceList', 'sp_PivotRateStrike', 'RecordRef', ['Option'], None, False],
                 ['Instrument', 'sp_BarrierCondition', 'ChoiceList', 'sp_BarrierCondition', 'RecordRef', ['Option'], None, False],
                 ['Instrument', 'sp_Barrier2Cond', 'ChoiceList', 'sp_BarrierCondition', 'RecordRef', ['Option'], None, False],
                 ['Instrument', 'sp_StrikeSettle', 'ChoiceList', 'sp_StrikeSettlement', 'RecordRef', [], None, False],
                 ['Instrument', 'sp_Strike2Settle', 'ChoiceList', 'sp_StrikeSettlement', 'RecordRef', [], None, False],
                 ['Instrument', 'StructureType', 'ChoiceList', 'StructureType', 'RecordRef', [], None, False],
                 ['Instrument', 'sp_InvertedTarget', 'Boolean', 'Targel Level as Curr 1 per Curr 2', 'Standard', ['Option'], None, False]]

choice_list_specs = [('ValGroup', valuationGroupNameTRF, 'TargetRedemptionForward'),
                    ('Valuation Extension', 'udmcTrf', 'Target Redemption Forward'),
                    ('StructureType', 'Target Redemption Forward', 'TargetRedemptionForward'),
                    ('StructureType', 'Target Pivot Forward', 'TargetPivotForward'),
                    ('StructureType', 'Structured Forward', 'StructuredForward'),
                    ('Exotic Event Types', 'TRF Expiry', ''),
                    ('sp_BarrierCondition', 'At or Past', ''),
                    ('sp_BarrierCondition', 'Past', ''),
                    ('sp_PivotRateStrike', 'Upper', ''),
                    ('sp_PivotRateStrike', 'Lower', ''),
                    ('sp_StrikeSettlement', 'None', ''),
                    ('sp_StrikeSettlement', 'Notional 1', ''),
                    ('sp_StrikeSettlement', 'Notional 2', '')                    
                    ]

context_links = [('Valuation Extension', 'udmcTrf', 'Val Group', valuationGroupNameTRF)]

def SetupTrf(definitionSetUp):

    contextName = mappingContext
    if not (contextName and acm.FContext[contextName]):
        raise RuntimeError, 'No valid context for mappings specified in TRF parameters (FParameters)'
    
    from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp, ContextLinkSetUp, CustomMethodSetUp

    for choiceList in choice_list_specs:
        choiceListSetupObject = ChoiceListSetUp( list   = choiceList[0],
                                                 entry  = choiceList[1],
                                                 descr  = choiceList[2]
                                               )
        definitionSetUp.AddSetupItem( choiceListSetupObject )

    for addinfo in add_info_specs:
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

    for contextLink in context_links:
        contextLinkSetUpObject = ContextLinkSetUp(  context     = contextName, 
                                                    type        = contextLink[0], 
                                                    name        = contextLink[1], 
                                                    mappingType = contextLink[2], 
                                                    chlItem     = contextLink[3]
                                                 )
        definitionSetUp.AddSetupItem( contextLinkSetUpObject )

# -------------------------------
# Default values
# to override this behaviour, use module SP_TrfExtension
# -------------------------------
def DefaultSheetDefaultColumns():
    return ['Price Theor', 
            'Portfolio Theoretical Value', 
            'Portfolio Underlying Price', 
            'Portfolio Underlying Forward Price', 
            'Portfolio Volatility', 
            'Portfolio Carry Cost', 
            'Instrument Delta']


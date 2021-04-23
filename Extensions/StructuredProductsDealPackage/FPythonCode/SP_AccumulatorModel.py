
import acm

from DealPackageDevKit import ValGroupChoices, DealPackageException, ReturnDomainDecorator, DealPackageUserException
from SP_DealPackageHelper import SettlementTypeChoices, AddExoticEvent, ExoticEventDates, SafeDivision
from SP_BusinessCalculations import GeneratePeriodEndDates, GenerateExpiryTableDates, AdjustBankingDaysFromMultiCalendars, GenerateFXPeriodDates
from SP_ExerciseUtils import CalculateOpenAmount, AddExerciseCashPayment, BarrierIsCrossedOnDate, CloseDealPackage, CreatePhysicalDeliveryExerciseTrade, TodayIsLastExpiry, IsExercised

# Expiry Date vs. Expiry Table
# Data setting the expiry table
# On Change... (make sure that quotation is always Per Contract(

# Barrier Monitoring Events should be updated from
#     - Monitoring Type
#     - Calendar
#     - Expiry Date
#     - OR last two replaced by a check when generating expiry table

class Sentinel(object): pass
READ = Sentinel()

# ##########################
# Choice List entries
# ##########################

def ChoicesValuation():
    return ValGroupChoices()

def ChoicesAccumulatorType():
    return ['Accumulator', 'Decumulator']

def ChoicesBarrierType():
    return ['Continuous', 'Discrete']

def ChoicesSettlementType(instr):
    return SettlementTypeChoices(instr)

def ChoicesAccumulationFrequency():
    return ['Daily', 'Period End']

# ##########################
# Default values
# ##########################

def DefaultValueValuation():
    return 'AccDec'

def RollingPeriodDefault():
    addinfo = acm.FAdditionalInfoSpec['sp_RollingPeriod']
    if addinfo and addinfo.DefaultValue():
        return addinfo.DefaultValue()
    else:
        return '2W'

def BusinessDayMethodDefault():
    addinfo = acm.FAdditionalInfoSpec['sp_PayDayMethod']
    if addinfo and addinfo.DefaultValue():
        return addinfo.DefaultValue()
    else:
        return 'Following'

def ExpiryPeriodFilter(exerciseEvent):
    return exerciseEvent.Date() == exerciseEvent.NoticeDate()


class AccumulatorInterface:
    
    def __init__(self):
        self._accumulator = None
        self._accumulatorTrade = None
        self._nbrOfPeriods = None
        
    # ######################
    # Private methods
    # ######################

    def _UpdateAllExerciseEventsField(self, field, value):
        for ee in self._accumulator.ExerciseEvents():
            getattr(ee, field)(value)

    def _UpdateBarrierType(self, accumulatorType):
        if accumulatorType == 'Accumulator':
            self._accumulator.Exotic().BarrierOptionType('Up & Out')
        else:
            self._accumulator.Exotic().BarrierOptionType('Down & Out')

    def _UpdatePriceFixingEvents(self):
        #For now, always delete, maybe change this
        allPriceFixings = self._Accumulator().GetExoticEventsOfKind('Price Fixing')
        allPriceFixings.Unsimulate()
        
        for date in self.ObservationDates():
            AddExoticEvent(self._Accumulator().Instrument(), 
                           self._Accumulator().Underlying(), 
                           'Price Fixing', 
                           date,
                           -1.0)

    def _UpdateBarrierMonitoringEvents(self, value):
        # For now, always delete, this should be changed
        allBarrierObservations = self._Accumulator().GetExoticEventsOfKind('Barrier date')
        allBarrierObservations.Unsimulate()

        if value == 'Discrete':
            for date in self.ObservationDates():
                AddExoticEvent(self._Accumulator().Instrument(), 
                               self._Accumulator().Underlying(), 
                               'Barrier date', 
                               date,
                               -1.0)

    def _UpdateExoticEventReferences(self, value):
        allExoticEvents = self._Accumulator().ExoticEvents()
        for ee in allExoticEvents:
            ee.ComponentInstrument(value)

    def _CreateExerciseEvent(self, observation):
        ee = acm.FExerciseEvent()
        ee.Date(observation['observationDate'])
        ee.SettlementDate(observation['settlementDate'])
        ee.NoticeDate(observation['endDate'])
        ee.Strike(self.StrikePrice())
        ee.Type(self._AccumulatorTypeToExericeEventType(self.AccumulatorType()))
        ee.Instrument(self._Accumulator())
        self._Accumulator().ExerciseEvents().Add(ee)
        ee.RegisterInStorage()

    def _GetSettleCalendar(self):
        return self._Accumulator().SettlementCalendar()

    def _GetCurrencyCalendars(self):
        if self._Accumulator().Currency() is not None:
            return [self._Accumulator().Currency().Calendar()]
        else:
            return []

    def GetSettlementCalendars(self):
        if (self._GetSettleCalendar() is None or self._GetSettleCalendar() == '') and self._GetCurrencyCalendars():
            return self._GetCurrencyCalendars()
        return [self._GetSettleCalendar()]
   
    def GetExpiryCalendars(self):
        return self.GetSettlementCalendars()
    
    def _VerifyExpiryTableParameters(self, startDate, endDate, calendars, method, 
                                     rolling, settleDays, frequency, **rest):

        if startDate is None or startDate == '':
            raise DealPackageUserException ('No start date entered')

        if endDate is None or endDate == '':
            raise DealPackageUserException ('No expiry date entered')

        if acm.Time.DateDifference(startDate, endDate) >= 0:
            raise DealPackageUserException ('Start date must be before expiry')
    
        if calendars is None or calendars == []:
            raise DealPackageUserException ('No calendar selected')
        
        if not type(calendars) is type([]):
            raise DealPackageException ('Calendars should be sent as a list')
        
        for cal in calendars:
            if not (type(cal) is type(acm.FCalendar())):
                raise DealPackageUserException ('Invalid calendar')
        
        if method is None or method == '':
            raise DealPackageUserException ('No business day method selected')
        
        if rolling is None or rolling == '':
            raise DealPackageUserException ('No rolling period entered')

        if frequency is None or frequency == '':
            raise DealPackageUserException ('No accumulation frequency entered')

        if frequency not in ChoicesAccumulationFrequency():
            raise DealPackageUserException ('%s is not a valid accumulation frequency' % (frequency))

    def _AccumulatorTypeToExericeEventType(self, accumulatorType):
        return 'Call' if accumulatorType == 'Accumulator' else 'Put'
    
    def _Accumulator(self):
        if self._accumulator:
            return self._accumulator
        else:
            raise DealPackageException ('Accumulator instrument must be created before it is accessed')
    
    def _AccumulatorTrade(self):
        if self._accumulatorTrade:
            return self._accumulatorTrade
        else:
            raise DealPackageException ('Accumulator trade must be created before it is accessed')

    # #####################################
    # Validation Logic
    # #####################################
    def _ValidateNumberOfInstruments(self, instruments, exceptionAccumulator):
        if instruments.Size() != 1:
            exceptionAccumulator ( 'Accumulator Deal Package can only have one instrument' )
        elif instruments[0].InsType() != 'Option':
            exceptionAccumulator ( 'Accumulator Deal Package can only contain an option instrument' )
        return (instruments.Size() == 1 and instruments[0].InsType() == 'Option')
        
    def _ValidateNumberOfTrades(self, trades, exceptionAccumulator):
        if trades.Size() != 1:
            exceptionAccumulator ( 'Accumulator Deal Package can only have one trade' )
        return (trades.Size() == 1)

    def _ValidateBarrierData(self, exceptionAccumulator):
        option = self._Accumulator()
        if  option.OptionTypeIsCall():
            if option.StrikePrice() > option.Barrier():
                exceptionAccumulator ('Barrier level must be above strike for an accumulator')
            
            if option.Exotic().BarrierOptionType() != 'Up & Out':
                exceptionAccumulator ('Barrier type must be "Up & Out" for an accumulator')

        else:
            if option.StrikePrice() < option.Barrier():
                exceptionAccumulator ('Barrier level must be below strike for a decumulator')
            
            if option.Exotic().BarrierOptionType() != 'Down & Out':
                exceptionAccumulator ('Barrier type must be "Down & Out" for an decumulator')
    
    def _ValidateArraySizes(self, array1, array2, msg, exceptionAccumulator):
        if array1.Size() != array2.Size():
            exceptionAccumulator (msg)
    
    def _ValidateEqualDates(self, array1, array2, msg, exceptionAccumulator):
        unionArray = array1.Union(array2)
        self._ValidateArraySizes(unionArray, array1, msg, exceptionAccumulator)

    def _ValidateDatesAgainstObservationDates(self, otherDates, msg, exceptionAccumulator):
            allObservationDates = self.ObservationDates()
            self._ValidateArraySizes(allObservationDates, otherDates, msg, exceptionAccumulator)
            self._ValidateEqualDates(allObservationDates, otherDates, msg, exceptionAccumulator)
    
    def _ValidateObservationAndBarrierDates(self, exceptionAccumulator):
        if self._Accumulator().Exotic().BarrierMonitoring() == 'Discrete':
            msg = 'Mismatch between observation dates and barrier dates'
            self._ValidateDatesAgainstObservationDates(self.BarrierDates(), msg, exceptionAccumulator)
            
    def _ValidateObservationAndPriceFixingDates(self, exceptionAccumulator):
        msg = 'Mismatch between observation dates and price fixing dates'
        self._ValidateDatesAgainstObservationDates(self.PriceFixingDates(), msg, exceptionAccumulator)

    def _ValidateObservationDateStrike(self, ee, exceptionAccumulator):
            if ee.Strike() != self.StrikePrice():
                exceptionAccumulator ( 'Strike price for observation %s is different from accumulator strike price'
                                                        % (str(ee.ExpiryDate())) )

    def _ValidateObservationDateSettlement(self, ee, exceptionAccumulator):
        calendars = self.GetSettlementCalendars()
        
        trueSettleDay = AdjustBankingDaysFromMultiCalendars(ee.NoticeDate(), 
                                                            self._Accumulator().PayDayOffset(), 
                                                            calendars)
        if acm.Time().DateDifference(trueSettleDay, ee.SettlementDate()) != 0:
            exceptionAccumulator ( 'Period end date and settlement date do not agree for observation %s'
                                                    % (str(ee.ExpiryDate())) )

    def _ValidateObservationDateData(self, exceptionAccumulator):
        for ee in self._Accumulator().ExerciseEvents():
            self._ValidateObservationDateStrike(ee, exceptionAccumulator)
            self._ValidateObservationDateSettlement(ee, exceptionAccumulator)

    def _ValidateExerciseType(self, exceptionAccumulator):
        if self._Accumulator().ExerciseType() != 'Bermudan':
            exceptionAccumulator ( 'Exercise type must be equal to Bermudan' )

    def _ValidatePayType(self, exceptionAccumulator):
        if self._Accumulator().PayType() != 'Spot':
            exceptionAccumulator ( 'Pay type must be equal to Spot' )

    def _ValidateQuotation(self, exceptionAccumulator):
        if self._Accumulator().Quotation().Name() != 'Per Contract':
            exceptionAccumulator ( 'Quotation must be equal to Per Contract' )

    def _ValidateDigital(self, exceptionAccumulator):
        if self._Accumulator().Digital():
            exceptionAccumulator ( 'An accumulator cannot be digital' )

    def _ValidateStrikeType(self, exceptionAccumulator):
        if self._Accumulator().StrikeType() != 'Absolute':
            exceptionAccumulator ( 'Strike type must be Absolute' )

    def _HasExoticOtherThanBarrier(self, ins):
        return (   ins.IsAsian()
                or ins.IsChooser()
                or ins.IsCliquet()
                or ins.IsForwardStart()
                or ins.IsLadder()
                or ins.IsLookback()
                or ins.IsRainbow()
                or ins.IsRangeAccrual()
                or (    ins.Exotic()
                    and ins.Exotic().PowerGearing() 
                    and ins.Exotic().PowerExponent() ) )

    def _ValidateExotics(self, exceptionAccumulator):
        if self._HasExoticOtherThanBarrier(self._Accumulator()):
            exceptionAccumulator ( 'Accumulator cannot have other exotic types than Barrier' )

    def _ValidateExerciseTag(self, exceptionAccumulator):
        allExerciseFreeTextStatus = {}
        inconsistencyFound = False
        errorTextFound = False
        for ee in self._Accumulator().ExerciseEvents():
            if ee.FreeText() not in ['', 'Exercised'] and not errorTextFound:
                exceptionAccumulator( 'Free text field on accumulator exercise events can only be used to specify that an event has been exercised.' )
                errorTextFound = True
            if allExerciseFreeTextStatus.has_key(str(ee.NoticeDate())):
                if allExerciseFreeTextStatus.get(str(ee.NoticeDate())) != ee.FreeText() and not inconsistencyFound:
                    exceptionAccumulator( 'Inconsistent exercise specification in accumulator exercise event free text fields.' )
                    inconsistencyFound = True
            else:
                allExerciseFreeTextStatus[str(ee.NoticeDate())] = ee.FreeText()

    def _ValidateCurrencies(self, exceptionAccumulator):
        pass

    def _GetNumberOfPeriods(self):
        return self.ExpiryTable().Size()


    # ##########################
    # Choice List entries
    # ##########################
    def SettlementTypeChoices(self):
        return ChoicesSettlementType(self._Accumulator())
    
    # ###########################
    # Handling the ACM objects
    # ###########################
    
    def CreateAccumulator(self):
        if self._accumulator:
            raise RuntimeError ('Accumulator already created')
        accumulator = acm.DealCapturing().CreateNewInstrument('Accumulator')
        self._accumulator = acm.FBusinessLogicDecorator.WrapObject(accumulator)
        quotation = self._accumulator.Quotation()
        self._accumulator.Generic(False)
        self._accumulator.Quotation(quotation)
        
        accumulatorTrade = acm.DealCapturing().CreateNewTrade(accumulator)
        self._accumulatorTrade = acm.FBusinessLogicDecorator.WrapObject(accumulatorTrade)
        
    def SetAccumulator(self, accumulatorInstruments, accumulatorTrades, exceptionAccumulator = None):
    
        if exceptionAccumulator:
            # We are being called for validation purposes
            validInstruments = self._ValidateNumberOfInstruments(accumulatorInstruments, exceptionAccumulator)
            validTrades = self._ValidateNumberOfTrades(accumulatorTrades, exceptionAccumulator)
            if not (validInstruments and validTrades):
                return False
    
        self._accumulator = accumulatorInstruments[0]
        self._accumulatorTrade = accumulatorTrades[0]

        return True

    def CheckAccumulationFrequency(self):
        allObservationDates = self.ExpiryTableDetail()
        periodEndDates = self.ExpiryTable()
        if (periodEndDates.Size() != 0 and
            allObservationDates.Size() == periodEndDates.Size()):
            return 'Period End'
        else:
            return 'Daily'
       
    def _GeneratePeriodEndDates(self, startDate, endDate, method, rolling, calendars, settleDays, settleCalendars, **rest):
        return GeneratePeriodEndDates(startDate, endDate, method, rolling, calendars, settleDays, settleCalendars)

    def GenerateExpiryTable(self, fixingParams):
    
        # 1) verify parameters or throw exception
        self._VerifyExpiryTableParameters(**fixingParams)

        # 2) Generate dates
        periodEndDates  = self._GeneratePeriodEndDates( **fixingParams )
                                                  
        expiryTableData = GenerateExpiryTableDates( fixingParams['startDate'],
                                                    fixingParams['calendars'],
                                                    periodEndDates,
                                                    fixingParams['frequency'])
        
        # 3) If new dates are different from existing date, update exercise events

        allExerciseEvents = self._Accumulator().ExerciseEvents()

        allExerciseEvents.Unsimulate()
        
        for observation in expiryTableData:
            self._CreateExerciseEvent(observation)
        
        # 4) based on the generated expiry table, generate barrier monitoring if discrete
        self._UpdateBarrierMonitoringEvents(self.BarrierMonitoringType())
        
        # 5) generate price fixing events
        self._UpdatePriceFixingEvents()

    def Accumulator(self):
        return [self._Accumulator()]

    def AccumulatorForAddInfo(self):
        return self._Accumulator()
    
    def AccumulatorTrade(self):
        return self._AccumulatorTrade()

    def AccumulatorCurrency(self):
        return self._Accumulator().Currency()

    def AccumulatorOriginalCurrency(self):
        return self._Accumulator().Originator().Currency()

    def LeadTrade(self):
        return self._AccumulatorTrade()
    
    def IsValid(self, exceptionAccumulator, aspect):

        self._ValidateBarrierData(exceptionAccumulator)
        self._ValidateObservationAndBarrierDates(exceptionAccumulator)
        self._ValidateObservationAndPriceFixingDates(exceptionAccumulator)
        self._ValidateExerciseType(exceptionAccumulator)
        self._ValidateObservationDateData(exceptionAccumulator)
        self._ValidatePayType(exceptionAccumulator)
        self._ValidateQuotation(exceptionAccumulator)
        self._ValidateDigital(exceptionAccumulator)
        self._ValidateStrikeType(exceptionAccumulator)
        self._ValidateExotics(exceptionAccumulator)
        self._ValidateExerciseTag(exceptionAccumulator)
        self._ValidateCurrencies(exceptionAccumulator)

    def InstrumentCurrencyObjects(self):
        return [self._Accumulator()]

    def HasExpiryTable(self):
        return self.ExpiryTable().Size() != 0

    # ###################################
    # Actions
    # ###################################

    def Exercise(self, date):
        returnObjects = acm.FArray()
        exerciseObjects = Exercise(self._AccumulatorTrade(), date)
        if exerciseObjects is not None:
            returnObjects.AddAll(exerciseObjects)
            taggedInstrument = TagInstrumentAsExercised(self._Accumulator(), date)
            if taggedInstrument is not None:
                returnObjects.Add(taggedInstrument)
        return returnObjects

    def Close(self, dealPackage, date):
        close = Close(dealPackage, self._Accumulator(), date)
        return close
    
    def IsExercised(self, date):
        event, dummy = _ExercisableExerciseEventOnDate(self._Accumulator(), date)
        return IsExercised(self._AccumulatorTrade(), event)
    
    def IsClosed(self):
        return IsClosed(self._AccumulatorTrade())
    
    # ###################################
    # Get methods for list objects
    # ###################################

    @ReturnDomainDecorator('FPersistentSet(FExerciseEvent)')
    def ExpiryTable(self):
        # - One event per accumulation period?
        #   (i.e. only events representing the last observation date per period)
        expiryTable = acm.FFilteredSet(self._Accumulator().ExerciseEvents())
        expiryTable.Filter(ExpiryPeriodFilter)
        
        tableAsArray = expiryTable.AsArray()
        tableAsArray.SortByProperty('ExpiryDate')
        return tableAsArray

    @ReturnDomainDecorator('FPersistentSet(FExerciseEvent)')
    def ExpiryTableDetail(self):
        # One event per observation date, i.e. all events
        return  self._Accumulator().ExerciseEvents().SortByProperty('ExpiryDate')

    def ObservationDates(self):
        observationDates = acm.FArray()
        for expiry in self.ExpiryTableDetail():
            observationDates.Add(expiry.ExpiryDate())
        return observationDates

    def BarrierDates(self):
        return ExoticEventDates(self._Accumulator(), 'Barrier date')

    def PriceFixingDates(self):
        return ExoticEventDates(self._Accumulator(), 'Price Fixing')

    @ReturnDomainDecorator('FPersistentSet(FExoticEvent)')
    def HistoricalFixings(self):
        # Should only historical fixings be returned?
        return self._Accumulator().GetExoticEventsOfKind('Price Fixing')

    # ###################################
    # Transform methods
    # ###################################

    def DateFromPeriod(self, period):
        return self._Accumulator().ExpiryDateFromPeriod(period)

    def DateFromPeriodAndStartDate(self, period, startDate, calendars):
        calendars = self.GetExpiryCalendars()
    
        if startDate is None or startDate == '':
            startDate = acm.Time().DateToday()
        unadjustedDate = acm.Time().DateAdjustPeriod(startDate, period)
        if calendars is None or calendars == []:
            return unadjustedDate
        else:
            return AdjustBankingDaysFromMultiCalendars( unadjustedDate, 
                                                        0, 
                                                        calendars)
            

    # ###################################
    # Get Set methods
    # ###################################
    @ReturnDomainDecorator('int')
    def NumberOfPeriods(self, value=READ):
        if value is READ:
            if self._nbrOfPeriods is None:
                self._nbrOfPeriods = self._GetNumberOfPeriods()
            return self._nbrOfPeriods
        else:
            self._nbrOfPeriods = value

    @ReturnDomainDecorator('enum(BusinessDayMethod)')
    def PayDayMethod(self, *value):
        return self._Accumulator().AdditionalInfo().Sp_PayDayMethod(*value)

    @ReturnDomainDecorator('dateperiod')
    def RollingPeriod(self, *value):
        return self._Accumulator().AdditionalInfo().Sp_RollingPeriod(*value)
   
    @ReturnDomainDecorator('double')
    def StrikePrice(self, value=READ):
        if value is READ:
            return self._Accumulator().StrikePrice()
        else:
            self._Accumulator().StrikePrice(value)
            self._UpdateAllExerciseEventsField('Strike', value)
        
    def AccumulatorType(self, value=READ):
        if value is READ:
            return 'Accumulator' if self._Accumulator().OptionTypeIsCall() else 'Decumulator'
        else:
            self._Accumulator().SuggestOptionType(value == 'Accumulator')
            self._UpdateAllExerciseEventsField('Type', self._AccumulatorTypeToExericeEventType(value))
            self._UpdateBarrierType(value)

    @ReturnDomainDecorator('double')
    def Leverage(self, value=READ):
        if value is READ:
            return self._Accumulator().AdditionalInfo().AccumulatorLeverage()
        else:
            self._Accumulator().AdditionalInfo().AccumulatorLeverage(value)

    @ReturnDomainDecorator('FStock')
    def Underlying(self, value=READ):
        if value is READ:
            return self._Accumulator().Underlying()
        else:
            self._Accumulator().Underlying(value)
            self._UpdateExoticEventReferences(value)

    @ReturnDomainDecorator('datetime')
    def Expiry(self, value=READ):
        # How should this map to expiry table?
        # Should expiry date and time be separate fields?
        if value is READ:
            return self._Accumulator().ExpiryDate()
        else:
            self._Accumulator().ExpiryDate(value)

    @ReturnDomainDecorator('date')    
    def StartDate(self, value=READ):
        if value is READ:
            return self._Accumulator().StartDate()
        else:
            self._Accumulator().StartDate(value)
    
    @ReturnDomainDecorator('double')
    def DailyAccumulation(self, value=READ):
        # Map to contact size? Anything else?
        if value is READ:
            return self._Accumulator().ContractSize()
        else:
            self._Accumulator().ContractSize(value)
   
    @ReturnDomainDecorator('enum(BarrierMonitoring)')
    def BarrierMonitoringType(self, value=READ):
        # This should include generating and removing barrier dates
        # Barrier dates should also be afected by changes in observation dates
        if value is READ:
            return self._Accumulator().Exotic().BarrierMonitoring()
        else:
            self._Accumulator().Exotic().BarrierMonitoring(value)
            self._UpdateBarrierMonitoringEvents(value)

    @ReturnDomainDecorator('FChoiceList')
    def ValuationMapping(self, value=READ):
        if value is READ:
            return self._Accumulator().ValuationGrpChlItem().Name()
        else:
            self._Accumulator().ValuationGrpChlItem(value)



class FxAccumulatorInterface(AccumulatorInterface):

    def _CreateExerciseEvent(self, observation):
        #need to use strikeDomesticPerForeign
        ee = acm.FExerciseEvent()
        ee.Date(observation['observationDate'])
        ee.SettlementDate(observation['settlementDate'])
        ee.NoticeDate(observation['endDate'])
        ee.Strike(self.StrikeDomesticPerForeign())
        ee.Type(self._AccumulatorTypeToExericeEventType(self.AccumulatorType()))
        ee.Instrument(self._Accumulator())
        self._Accumulator().ExerciseEvents().Add(ee)
        ee.RegisterInStorage()

    def _GetCurrencyCalendars(self):
        currencyCalendars = []
        if self._Accumulator().ForeignCurrency() is not None:
            currencyCalendars.append(self._Accumulator().ForeignCurrency().Calendar())
        if self._Accumulator().DomesticCurrency() is not None:
            currencyCalendars.append(self._Accumulator().DomesticCurrency().Calendar())
        return currencyCalendars

    def GetExpiryCalendars(self):
        return self._GetCurrencyCalendars()

    def _ValidateBarrierData(self, exceptionAccumulator):
        option = self._Accumulator()
        if  option.OptionTypeIsCall():
            if option.StrikeDomesticPerForeign() > option.Exotic().BarrierDomesticPerForeign():
                exceptionAccumulator ('Barrier level must be above strike for an accumulator')
            
            if option.Exotic().BarrierOptionType() != 'Up & Out':
                exceptionAccumulator ('Barrier type must be "Up & Out" for an accumulator')

        else:
            if option.StrikeDomesticPerForeign() < option.Exotic().BarrierDomesticPerForeign():
                exceptionAccumulator ('Barrier level must be below strike for a decumulator')
            
            if option.Exotic().BarrierOptionType() != 'Down & Out':
                exceptionAccumulator ('Barrier type must be "Down & Out" for an decumulator')

    def _ValidateObservationDateStrike(self, ee, exceptionAccumulator):
            if ee.Strike() != self.StrikeDomesticPerForeign():
                exceptionAccumulator ( 'Strike price for observation %s is different from accumulator strike price'
                                                        % (str(ee.ExpiryDate())) )

    def _ValidateCurrencies(self, exceptionAccumulator):
        if self._AccumulatorTrade().Currency() != self._AccumulatorTrade().FxoPremiumCurr():
            exceptionAccumulator('Premium currency must be equal to trade currency')

    def _GeneratePeriodEndDates(self, startDate, rolling, method, foreignCurrency, domesticCurrency, settleCalendar, settleDays, nbrOfPeriods, **rest):
        currencyPair = foreignCurrency.CurrencyPair(domesticCurrency)
        yesterday = foreignCurrency.Calendar().ModifyDate(domesticCurrency.Calendar(), None, acm.Time.DateAddDelta(startDate, 0, 0, -1), 'Preceding')
        firstPeriodEnd = currencyPair.ExpiryDate(yesterday, rolling)
        datePeriods = GenerateFXPeriodDates(firstPeriodEnd, rolling, method, currencyPair, settleCalendar, nbrOfPeriods, settleDays)
        self.Expiry(datePeriods.Last()['endDate'])
        self.Delivery(datePeriods.Last()['settlementDate'])
        return datePeriods

    def _VerifyExpiryTableParameters(self, startDate, rolling, method, foreignCurrency, domesticCurrency, 
                                     nbrOfPeriods, frequency, **rest):

        if foreignCurrency is None:
            raise DealPackageUserException ('Foreign currency not entered')
        
        if domesticCurrency is None:
            raise DealPackageUserException ('Domestic currency not entered')

        if startDate is None or startDate == '':
            raise DealPackageUserException ('No start date entered')
        
        if method is None or method == '':
            raise DealPackageUserException ('No business day method selected')
        
        if rolling is None or rolling == '':
            raise DealPackageUserException ('No rolling period entered')

        if nbrOfPeriods is None:
            raise DealPackageUserException ('Number of periods not entered')

        if nbrOfPeriods == 0:
            raise DealPackageUserException ('Cannot generate a structure with 0 periods')

        if frequency is None or frequency == '':
            raise DealPackageUserException ('No accumulation frequency entered')

        if frequency not in ChoicesAccumulationFrequency():
            raise DealPackageUserException ('%s is not a valid accumulation frequency' % (frequency))


    # ###########################
    # Handling the ACM objects
    # ###########################
    
    def CreateAccumulator(self):
        if self._accumulator:
            raise RuntimeError ('Accumulator already created')
        accumulator = acm.DealCapturing().CreateNewInstrument('FxAccumulator')
        self._accumulator = acm.FBusinessLogicDecorator.WrapObject(accumulator)
        self._accumulator.Generic(False)
        
        accumulatorTrade = acm.DealCapturing().CreateNewTrade(accumulator)
        self._accumulatorTrade = acm.FBusinessLogicDecorator.WrapObject(accumulatorTrade)

    # ###################################
    # Get Set methods
    # ###################################
    @ReturnDomainDecorator('date')
    def Expiry(self, value=READ):
        # How should this map to expiry table?
        # Should expiry date and time be separate fields?
        if value is READ:
            return self._Accumulator().FxoExpiryDate()
        else:
            self._Accumulator().FxoExpiryDate(value)

    @ReturnDomainDecorator('date')
    def Delivery(self, value=READ):
        if value is READ:
            return self._Accumulator().DeliveryDate()
        else:
            self._Accumulator().DeliveryDate(value)

    @ReturnDomainDecorator('double')
    def StrikeDomesticPerForeign(self, value=READ):
        if value is READ:
            return self._Accumulator().StrikeDomesticPerForeign()
        else:
            self._Accumulator().StrikeDomesticPerForeign(value)
            self._UpdateAllExerciseEventsField('Strike', value)

    @ReturnDomainDecorator('double')
    def StrikeForeignPerDomestic(self, value=READ):
        if value is READ:
            return self._Accumulator().StrikeForeignPerDomestic()
        else:
            self._Accumulator().StrikeForeignPerDomestic(value)
            self._UpdateAllExerciseEventsField('Strike', self.StrikeDomesticPerForeign())

    @ReturnDomainDecorator('double')
    def Notional(self, value=READ):
        # Map to contact size? Anything else?
        if value is READ:
            return self._Accumulator().ContractSize()
        else:
            self._Accumulator().ContractSize(value)
    
    @ReturnDomainDecorator('FQuotation')
    def Quotation(self, value=READ):
        if value is READ:
            if self._Accumulator().Quotation().Name() != 'Per Contract':
                self._Accumulator().Quotation('Per Contract')
            return self._Accumulator().Quotation()
        else:
            self._Accumulator().Quotation('Per Contract')

    @ReturnDomainDecorator('FCurrency')
    def ForeignCurrency(self, value=READ):
        if value is READ:
            return self._Accumulator().ForeignCurrency()
        else:
            self._Accumulator().ForeignCurrency(value)
            self._UpdateExoticEventReferences(value)
            

# Methods for displaying values in grid columns

def SetObservationFixing(ee, value):
    ObservationFixing(ee, value)

def GetObservationFixing(ee):
    return ObservationFixing(ee)

def SetObservationFixingDomesticPerForeign(ee, value):
    ObservationFixing(ee, value)

def GetObservationFixingDomesticPerForeign(ee):
    return ObservationFixing(ee)

def ObservationFixing(ee, value = READ):
    fixings = ee.Instrument().GetExoticEventsOfKind('Price Fixing')
    correspondingFix = None
    for singleFix in fixings:
        if singleFix.Date() == ee.ExpiryDate():
            correspondingFix = singleFix
            break

    if value is READ:
        if correspondingFix:
            return correspondingFix.EventValue()
        return 0.0
    else:
        if correspondingFix:
            correspondingFix.EventValue(value)
        else:
            # PD: Should we create the price fixing event instead?
            raise DealPackageException('Cannot set fixing unless a price fixing event exists')

def SetObservationFixingForeignPerDomestic(ee, value):
    ObservationFixingInverse(ee, value)

def GetObservationFixingForeignPerDomestic(ee):
    return ObservationFixingInverse(ee)

def ObservationFixingInverse(ee, value = READ):
    if value is READ:
        return SafeDivision(1.0, ee.ObservationFixing(), 0.0)
    else:
        ee.ObservationFixing(SafeDivision(1.0, value, 0.0))

def AccumulatorPeriodStartDate(ee):
    periodStart = ee.Date()
    for event in ee.Instrument().ExerciseEvents():
        if (event.NoticeDate() == ee.NoticeDate() and 
            acm.Time.DateDifference(periodStart, event.Date()) > 0 ):
            periodStart = event.Date()
    return periodStart

def LeverageToApply(ee, fixing):
    accDecFactor = 1.0 if ee.Instrument().OptionTypeIsCall() else -1.0
    
    if (StrikeAtDate(ee) - fixing) * accDecFactor > 0:
        return ee.Instrument().AdditionalInfo().AccumulatorLeverage()
    else:
        return 1.0

def StrikeAtDate(ee):
    histStrike = ee.Strike()
    histDividends = ee.Instrument().Underlying().Dividends()
    for div in histDividends:
        if ( acm.Time().DateDifference( div.ExDivDay(), ee.Instrument().StartDate()) >= 0.0 and
             acm.Time().DateDifference( ee.ExpiryDate(), div.ExDivDay() ) >= 0.0 ):
            histStrike -= div.Amount()
    return histStrike


def AccumulatedAmount(ee):
    if acm.Time.DateDifference(ee.Date(), acm.Time.DateToday()) > 0:
        #Future date
        return 0
    fixing      = ee.ObservationFixing()
    instrument  = ee.Instrument()

    if ( instrument.Exotic() and 
         instrument.Exotic().BarrierCrossedStatus() == 'Confirmed' and 
         acm.Time.DateDifference(ee.Date(), instrument.Exotic().BarrierCrossDate()) >= 0 ):
        # Barrier crossed before this observation date
        return 0

    if fixing > 0.0:
        # Fixing is done
        leverage = LeverageToApply(ee, fixing)
        return instrument.ContractSize() * leverage
    
    # Past date (or today) with no fixing
    return 0

def AccumulatedInPeriod(ee):
    accumulatedAmount = 0
    for event in ee.Instrument().ExerciseEvents():
        if event.NoticeDate() == ee.NoticeDate():
            accumulatedAmount += AccumulatedAmount(event)
    return accumulatedAmount

def AccumulatedTotal(ee):
    accumulatedAmount = 0
    for event in ee.Instrument().ExerciseEvents():
        if acm.Time.DateDifference(ee.NoticeDate(), event.NoticeDate()) >= 0:
            accumulatedAmount += AccumulatedAmount(event)
    return accumulatedAmount
    
# ##################################################################
# ------------------   Exercise Logic   ----------------------------
# ##################################################################

def Exercise(trade, date):
    trade = trade.DecoratedObject() if hasattr(trade, 'DecoratedObject') else trade
    ins = trade.Instrument()
    
    ee, settlementDate = _ExercisableExerciseEventOnDate(ins, date)
    if not ee:
        return None

    accumulated = AccumulatedInPeriod(ee) if ins.OptionTypeIsCall() else -AccumulatedInPeriod(ee)
    quantity = accumulated * CalculateOpenAmount(trade, date)
    strike = StrikeAtDate(ee)

    if "Cash" == ins.SettlementType():
        spotAtDate = ObservationFixing(ee)
        amount = quantity * (spotAtDate - strike)
        return AddExerciseCashPayment(trade, ee, amount, settlementDate)
    
    elif "Physical Delivery" == ins.SettlementType():
        return CreatePhysicalDeliveryExerciseTrade(trade, ee, quantity, strike, settlementDate)

def TagInstrumentAsExercised(ins, date):
    updateDone = False
    for ee in ins.ExerciseEvents():
        if (acm.Time().DateDifference(ee.NoticeDate(), date) == 0 and
            ee.FreeText() == ''):
            ee.FreeText('Exercised')
            updateDone = True
    if updateDone:
        return ins
    else:
        return None

def _ExercisableExerciseEventOnDate(ins, date):
    ee = None
    settlementDate = None
    if ins.Exotic().BarrierCrossDate() and ins.Exotic().BarrierCrossedStatus() == "Confirmed":
        if ins.Exotic().BarrierCrossDate() == date:
            ee = next((e for e in ins.ExerciseEvents() if e.Date() == date), None)
            calendar = ins.SettlementCalendar() or ins.Currency().Calendar()
            settlementDate = calendar.AdjustBankingDays(date, ins.PayDayOffset())
    else:
        ee = next((e for e in ins.ExerciseEvents() if e.Date() == date and e.Date() == e.NoticeDate()), None)
        if ee:
            settlementDate = ee.SettlementDate()
    return ee, settlementDate

def IsClosed(trade):
    openAmount = CalculateOpenAmount(trade)
    return abs(openAmount) <= 1e-10

def Close(dealPackage, ins, date):

    if BarrierIsCrossedOnDate(ins, date) or TodayIsLastExpiry(ins, date):
        ee, settlementDate = _ExercisableExerciseEventOnDate(ins, date)
        return CloseDealPackage(dealPackage, date, settlementDate)
    else:
        return None

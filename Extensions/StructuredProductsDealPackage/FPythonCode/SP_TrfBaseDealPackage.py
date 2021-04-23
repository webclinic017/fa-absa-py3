
import acm
import FUxCore
from CompositeAttributesLib import BuySell, PaymentsDialog
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, ValGroupChoices, ReturnDomainDecorator, Box, TradeActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand, NoButtonAttributeDialog, InstrumentPart, DealPart
import SP_TrfUtils
import ChoicesExprInstrument
import math, inspect, string, types
from SP_TrfCompositeAttributes import TrfFxRateComposite, TrfFxStrikeComposite, TrfFxBarrierComposite, TrfFxPivotRateComposite, TrfCommodityStrikeComposite, TrfCommodityBarrierComposite, TrfCommodityPivotRateComposite, TrfFxFixingEditerComposite, TrfCommodityFixingEditerComposite, TrfDailyFixingEditerComposite
from SP_TrfUtils import TransformUsingDecorator, GetInverseRate, ExpiryPeriodToDate, TrfExpiryEventPerPayDate, TrfExpiryEvent, BuySellMapping, TrfHasBarrier, DefaultSheetDefaultColumns, FixFxRateCalculation
from SP_BusinessCalculations import GenerateFXPeriodDates, AdjustBankingDaysFromMultiCalendars, BankingDayPeriodToDateFromStartDate, GetRelevantFixingCalendar, GenerateMonthlyPeriodDates, GenerateAverageDates
from SP_DealPackageHelper import SettlementTypeChoices, DatePeriodToDateTime, StringValueIsInteger, DayMethodOnlyFollowingPreceding, BarrierSingleChoices, GetCurrencyPairPointsDomesticPerForeign, GetCurrencyPairPointsForeignPerDomestic
from SP_TrfExerciseCalculations import CalculateTRFSettlementAmounts, CalculateCommodityTRFSettlementAmounts
from SP_ExerciseUtils import AddExerciseCashPayment, CreatePhysicalDeliveryFxSpotExerciseTrade, CalculateOpenPart, IsExercised, BarrierIsCrossedOnDate, TodayIsLastTrfExpiry, CloseDealPackage
from DealPackageUtil import UnDecorate

epsilon = 0.0000001

@Settings(GraphApplicable=False,
          SheetDefaultColumns=DefaultSheetDefaultColumns(),
          MultiTradingEnabled=True)
class TrfBaseDefinition(DealPackageDefinition):

    name                = Object(   objMapping = InstrumentPart("DealPackage.InstrumentPackage.Name"),
                                    label = "Name",
                                    toolTip = "Name of Instrument Package" )

    notional1           = Object(   objMapping = InstrumentPart("Option.ContractSizeInQuotation"),
                                    label = "Notional 1",
                                    toolTip = "Notional used for in the money fixings" )
    
    notional2           = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_LeverageNotional"),
                                    label = "Notional 2",
                                    toolTip = "Leveraged notional used for out of the money fixings" )

    expiry              = Object(   objMapping = InstrumentPart("ExpiryDate"),
                                    label = "Final Fixing",
                                    editable = False,
                                    toolTip = "Final Fixing Date" )

    delivery            = Object(   objMapping = InstrumentPart("DeliveryDate"),
                                    label = "Final Delivery",
                                    editable = False,
                                    toolTip = "Final Delivery Date" )

    startDate           = Object(   objMapping = InstrumentPart("StartDate"),
                                    label = '@StartDateLabel',
                                    toolTip = "@StartDateTooltip",
                                    validate = "@ValidateStartDate",
                                    transform = "@ExpiryPeriodToDate" )

    valGroup            = Object(   objMapping = InstrumentPart("Option.ValuationGrpChlItem"),
                                    label = "Val Group",
                                    toolTip = "Valuation Group",
                                    choiceListSource = ValGroupChoices() )

    fixingSource        = Object(   objMapping = InstrumentPart("Option.FixingSource"),
                                    label = "Fixing Source" )

    # 'strike2Applicable' not shown in GUI
    strike2Applicable   = Bool(     defaultValue = False,
                                    silent = True)

    # 'pivotApplicable' not shown in GUI
    pivotApplicable     = Bool(     defaultValue = False,
                                    silent = True)

    # 'barrierApplicable' not shown in GUI
    barrierApplicable  = Bool(      defaultValue = False,
                                    silent = True)

    # 'barrier2Applicable' not shown in GUI
    barrier2Applicable  = Bool(     defaultValue = False,
                                    silent = True)

    # 'targetApplicable' not shown in GUI
    targetApplicable    = Bool(     defaultValue = True,
                                    silent = True)

    targetInverseApplicable = Bool( defaultValue = False,
                                    silent = True)
    
    isAsian             = Bool(     defaultValue = False)

    averageMethodType   = Object(   objMapping = InstrumentPart("Option.Exotic.AverageMethodType"),
                                    defaultValue = "None",
                                    visible = False)
    
    averagePriceType    = Object(   objMapping = InstrumentPart("Option.Exotic.AveragePriceType"),
                                    defaultValue = "None",
                                    visible = False)

    
    averageStrikeType   = Object(   objMapping = InstrumentPart("Option.Exotic.AverageStrikeType"),
                                    defaultValue = "None",
                                    visible = False)

    targetLevel         = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_TargetLevel"),
                                    visible = '@VisibleIfTargetApplicable',
                                    formatter = "@FormatTarget",
                                    label = "@LabelTargetLevel" )

    targetLevelInv      = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_InvertedTarget"),
                                    visible = '@VisibleIfTargetInverseApplicable',
                                    label = "Target Level Inverse")

    exactTarget         = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_AdjustedStrike"),
                                    visible = '@VisibleIfTargetApplicable',
                                    toolTip = '@ExactTargetTooltip',
                                    label = "Exact" )

    # Important to store the applicable barrier types for maintenance scripts to work
    barrierType         = Object(   objMapping = InstrumentPart("Option.Exotic.BarrierOptionType"),
                                    visible = False,
                                    recreateCalcSpaceOnChange=True,
                                    label = "Barrier Type",
                                    choiceListSource = BarrierSingleChoices())

    hasEkiBarrier       = Object(   objMapping = InstrumentPart("HasEkiBarrier"),
                                    onChanged = '@SetBarriersToZero',
                                    label = 'EKI barrier',
                                    visible = '@VisibleIfBarrierApplicable')

    settlementType      = Object(   objMapping = InstrumentPart("Option.SettlementType"),
                                    choiceListSource = '@ChoicesSettlementType',
                                    label = "Settlement" )

    datePeriod          = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_RollingPeriod"),
                                    validate = '@ValidateDatePeriod',
                                    visible = '@VisibleIfNotAsian',
                                    label = "Rolling Period" )

    settlementDays      = Object(   objMapping = InstrumentPart("Option.PayDayOffset"),
                                    label = "Settlement Days")

    nbrOfPeriods        = Object(   objMapping = InstrumentPart("NumberOfDatePeriods"),
                                    label = "Number of periods")
    
    dayMethod           = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_PayDayMethod"),
                                    choiceListSource = DayMethodOnlyFollowingPreceding(),
                                    label = "Day Convention" )

    deliveryCalendar    = Object(   objMapping = InstrumentPart("Option.SettlementCalendar"),
                                    label = "Delivery Calendar" )
    
    terminationStatus   = Object(   objMapping = InstrumentPart("Option.Exotic.BarrierCrossedStatus"),
                                    recreateCalcSpaceOnChange=True,
                                    label = "Termination Status",
                                    visible = "@VisibleTerminationStatus" )
    
    terminationDate     = Object(   objMapping = InstrumentPart("Option.Exotic.BarrierCrossDate"),
                                    recreateCalcSpaceOnChange=True,
                                    label = "Termination Date",
                                    visible = "@VisibleTerminationStatus" )
    
    #-----------------------------
    # Trade data
    #-----------------------------
    
    tradeTime           = Object(   objMapping = "Trades.TradeTime",
                                    label = "Trade Time",
                                    transform = '@TradeDayAndTimeFromPeriod' )

    tradeStatus         = Object(   objMapping = "Trades.Status",
                                    choiceListSource = TradeStatusChoices(),
                                    label = "Trade Status" )
    
    tradeValueDay       = Object(   objMapping = "Trades.ValueDay",
                                    label = "Value Day",
                                    transform = '@BankingDayPeriodToDateFromTradeTimePlusSpot' )
    
    tradePortfolio      = Object(   objMapping = "Trades.Portfolio",
                                    choiceListSource = PortfolioChoices(),
                                    label = "Portfolio" )
    
    tradePrice          = Object(   objMapping = "Trades.Price",
                                    label = "Price" )
    
    tradePremium        = Object(   objMapping = "Trades.Premium",
                                    label = "Premium" )
    
    tradeAcquirer       = Object(   objMapping = "Trades.Acquirer",
                                    choiceListSource = AcquirerChoices(),
                                    label = "Acquirer" )
    
    tradeCounterParty   = Object(   objMapping = "Trades.Counterparty",
                                    choiceListSource = CounterpartyChoices(),
                                    label = "Counterparty" )
    
    tradeCurrency       = Object(   objMapping = "Trades.Currency",
                                    label = "Premium Currency" )

    tradeNotional1      = BuySell(  objMapping = "TradeNotional1",
                                    label = "Notional 1" )
    
    tradeNotional2      = BuySell(  objMapping = "TradeNotional2",
                                    label = "Notional 2" )

    tradePayments =       PaymentsDialog( trade = 'LeadTrade' )

    # Non visible trade traits, used for exercise
    tradeType =           Object(   objMapping = "Trades.Type" )
    tradeQuantity =       Object(   objMapping = "Trades.Quantity")

    #-----------------------------
    # Trait building up the expiry table
    #-----------------------------
    
    fixingsGenerate     = Action(   label = "Generate",
                                    enabled = "@EnabledFixingsGenerate",
                                    action = "@ActionFixingsGenerate" )
    
    exoticEvents        = Object(   objMapping = "TrfExpiryEvents",
                                    columns = "@ColumnsExoticEvents",
                                    label = "Expiry Table",
                                    addNewItem=['First', 'Sorted'],
                                    sortIndexCallback='@SortTrfExpiryEvents',
                                    onSelectionChanged = "@SelectionExoticEvents",
                                    dialog = None,
                                    toolTip = "Expiry Table" )

    averageEvents       = Object(   objMapping = "AveragePriceEvents",
                                    label = "Observation Dates",
                                    visible = "@VisibleIfAsian",
                                    onSelectionChanged = "@SelectionAverageEvents",
                                    addNewItem=['First', 'Sorted'],
                                    sortIndexCallback='@SortTrfExpiryEvents',
                                    toolTip = "Observation Dates:\n If a period has been selected in the Expiry table, only observation dates for the selected period will be displayed.",
                                    columns = "@ColumnsAverageEvents")

    #--------------------------
    # B2B parameters
    #--------------------------

    b2bEnabled          = Object( defaultValue=False,
                                  label='B2B Cover',
                                  objMapping='OptionB2B.SalesCoverEnabled',
                                  visible='@IsB2BorDetail')

    b2bMargin           = Object( defaultValue=0.0,
                                  label='Sales Spread',
                                  objMapping='OptionB2B.SalesMargin',
                                  formatter='FullPrecision',
                                  enabled='@IsB2B',
                                  visible='@IsB2BorDetail')
                            
    b2bPrice            = Object( defaultValue=0.0,
                                  label='Trader Price',
                                  objMapping='OptionB2B.TraderPrice',
                                  formatter='FullPrecision',
                                  visible='@IsB2B')
                            
    b2bPortfolio        = Object( label='Trader Portfolio',
                                  objMapping='OptionB2B.TraderPortfolio',
                                  choiceListSource=PortfolioChoices(),
                                  visible='@IsB2B')
             
    b2bAcquirer         = Object( label='Trader Acquirer',
                                  objMapping='OptionB2B.TraderAcquirer',
                                  choiceListSource=AcquirerChoices(),
                                  visible='@IsB2B')

    #-----------------------------
    # Non visible traits
    #-----------------------------
    productType         = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.StructureType"),
                                    defaultValue = 'Target Redemption Forward')
    
    quotation           = Object(   objMapping = InstrumentPart("Option.Quotation"))
    
    exoticType          = Object(   objMapping = InstrumentPart("Option.ExoticType"))
    
    checkTargetLevel    = Action(   action = '@UpdateTerminationStatus',
                                    visible = False )
    
    isCallOption        = Object(   objMapping = InstrumentPart("Option.IsCallOption"),
                                    visible = False )

    #-----------------------------
    # Traits to handle fixing dates
    #-----------------------------
    exercise = Action (action = '@Exercise')
    
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'valGroup': {
                'defaultValue': 'Target Redemption Forward'
            },
            'deliveryCalendar': {
                'defaultValue': None
            },
            'dayMethod': {
                'defaultValue': 'Following'
            },
            'datePeriod': {
                'defaultValue': '1M'
            },
            'barrierType': {
                'defaultValue': 'None'
            },
            'exactTarget': {
                'defaultValue': True
            },
            'startDate': {
                'defaultValue': '1M'
            },
            'nbrOfPeriods': {
                'defaultValue': 12
            },
            'strike_strikeSettlement': {
                'defaultValue': 'None',
                'label': '', 
                'visible': '@VisibleIfPhysicalSettlement'},
            'strike2_strikeSettlement': {
                'defaultValue': 'None',
                'label': '',
                'visible': '@VisibleIfStrike2ApplicableAndPhysicalSettlement'},
            'pivotRate_pivotRateStrike': {
                'defaultValue': 'Upper',
                'label': '',
                'visible': "@VisibleIfPivotApplicable"},
            'barrier_levelInterpretation': {
                'defaultValue': 'At or Past',
                'label': '',
                'visible': '@VisibleIfBarrier'},
            'barrier2_levelInterpretation': {
                'defaultValue': 'At or Past',
                'label': '',
                'visible': '@VisibleIfBarrierAndDoubleBarrierPossible'},
            'barrier_memory': {
                'defaultValue': False,
                'visible': False},
            'barrier2_memory': {
                'defaultValue': False,
                'visible': False}
            # Hide and default the memory on the 
            # barriers as they are not tested and supported
            #'barrier_memory': {
            #    'visible': '@VisibleIfBarrier'},
            #'barrier2_memory': {
            #    'visible': '@VisibleIfBarrierAndDoubleBarrierPossible'}
        })

    def AddExoticEvent(self, type, date, endDate, value, valueSecond, componentInstrument):
        ee = acm.FExoticEvent()
        ee.Instrument(self.Option().Instrument())
        ee.ComponentInstrument(componentInstrument)
        ee.Type(type)
        ee.Date(date)
        ee.EndDate(endDate)
        ee.EventValue(value)
        ee.EventValueSecond(valueSecond)
        self.Option().ExoticEvents().Add(ee)
        ee.RegisterInStorage()

    def GetExoticEventReference(self):
        raise NotImplementedError("Method GetExoticEventReference not implemented")

    def DeleteExoticEventsOfType(self, eeType):
        existingEvents = [event for event in self.Option().GetExoticEventsOfKind(eeType)]
        for ee in existingEvents:
            ee.Unsimulate()

    def DeleteTrfExpiryEvents(self):
        self.DeleteExoticEventsOfType('TRF Expiry')

    def DeleteAveragePriceDates(self):
        self.DeleteExoticEventsOfType('Average price')

    # Method to override for non standard TRFs
    # Return value is for instrument (not for trade), i.e. for trade quantity 1
    def ExerciseAmount(self, date):
        raise NotImplementedError('Method ExerciseAmount not implemented')
        
    def ExerciseObjects(self, date, *rest):
        raise NotImplementedError('Method ExerciseObjects not implemented')
        
    def GeneratePeriodDates(self):
        raise NotImplementedError('Method GeneratePeriodDates not implemented')

    def FieldsSetToGenerate(self):
        raise NotImplementedError('Method FieldsSetToGenerate not implemented')

    def GenerateTrfExpiryEvents(self, dates = None):
        if dates is None:
            dates = self.GeneratePeriodDates()
        for date in dates:
            self.AddExoticEvent('TRF Expiry', date.At('endDate'), date.At('settlementDate'), -1, -1, self.GetExoticEventReference())
        self.expiry = dates.Last().At('endDate')
        self.delivery = dates.Last().At('settlementDate')
        self._generateAttributeUpdated = False

    def GenerateAverageDates(self):
        if self.isAsian:
            averageDates = GenerateAverageDates(self.exoticEvents, GetRelevantFixingCalendar(self.Option()))
            for avgDate in averageDates:
                self.AddExoticEvent("Average price", avgDate, None, -1.0, -1.0, self.GetExoticEventReference())

    @ReturnDomainDecorator('int')
    def NumberOfDatePeriods(self, value = 'NoValue'):
        if value == 'NoValue':
            if self._numberOfPeriods is None:
                self._numberOfPeriods = self.GetNumberOfPeriods()
            return self._numberOfPeriods
        else:
            self._numberOfPeriods = value

    def GetNumberOfPeriods(self):
        return self.Option().GetExoticEventsOfKind('TRF Expiry').Size()

    def SortTrfExpiryEvents(self, attrName, columnNbr, value, formatter, obj):
        if columnNbr < 0:
            return acm.Time.DateTimeToTime(obj.Date())
        elif columnNbr in (0, 1):
            return acm.Time.DateTimeToTime(value)
        else:
            return value

    #-----------------------------
    # Object Mappings
    #-----------------------------
    @ReturnDomainDecorator('date')
    def ExpiryDate(self, value = 'NoVal'):
        if value == 'NoVal':
            return self.OptionNoQuestionGui().ExpiryDate()
        else:
            self.OptionNoQuestionGui().ExpiryDate(value)

    @ReturnDomainDecorator('date')
    def StartDate(self, value = 'NoVal'):
        if value == 'NoVal':
            return self.Option().StartDate()
        else:
            if self.isAsian:
                self.Option().StartDate(self.FirstRelevantDayOfMonth(value))
            else:
                self.Option().StartDate(value)

    @ReturnDomainDecorator('date')
    def DeliveryDate(self, value = 'NoVal'):
        raise NotImplementedError('Method DeliveryDate for object mapping not implemented')

    #-----------------------------
    # Date period logic
    #-----------------------------

    def ExpiryPeriodToDate(self, traitName, value):
        return ExpiryPeriodToDate(self.OptionNoQuestionGui(), value)

    def TradeDayFromPeriod(self, startDate, period):
        tradeDay = acm.Time.DateAdjustPeriod(startDate, period)
        if self.currency and self.currency.Calendar():
            tradeDay = self.currency.Calendar().ModifyDate(None, None, tradeDay)
        return tradeDay

    def TradeDayAndTimeFromPeriod(self, attrName, newDate, *rest):
        dateTime = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            startTime = acm.Time().TimeNow()
            startDate = acm.Time().DateNow()
            currentTime = acm.Time.DateTimeToTime(startTime) - acm.Time.DateTimeToTime(startDate)
            date = self.TradeDayFromPeriod(startDate, newDate)
            dateTime = acm.Time.DateTimeFromTime(acm.Time.DateTimeToTime(date) + currentTime)
        return dateTime

    def BankingDayPeriodToDateFromTradeTimePlusSpot(self, attrName, newDate, *rest):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            tradeDate = acm.Time.AsDate(self.tradeTime)
            try:
                currPair = self.foreignCurrency.CurrencyPair(self.domesticCurrency)
                tradeDatePlusSpot = currPair.SpotDate(tradeDate)
            except RuntimeError:
                tradeDatePlusSpot = self.Option().GetSpotDay(tradeDate, None)
            return BankingDayPeriodToDateFromStartDate(self.GetPairCalendars(), tradeDatePlusSpot, newDate)
        return date

    def FirstRelevantDayOfMonth(self, value):
        return acm.Time.FirstDayOfMonth(value)

    #-----------------------------
    # Enabled Callbacks
    #-----------------------------
    def FieldsUpdatedToGenerate(self):
        return self._generateAttributeUpdated

    def EnabledFixingsGenerate(self, traitName):
        return (self.FieldsSetToGenerate() and
                self.FieldsUpdatedToGenerate() and
                (not self.IsFirstFixingDateFixed()))

    #-----------------------------
    # Action Callbacks
    #-----------------------------

    def ActionFixingsGenerate(self, traitName):
        self.DeleteTrfExpiryEvents()
        self.GenerateTrfExpiryEvents()
        self.DeleteAveragePriceDates()
        self.GenerateAverageDates()

    #-----------------------------
    # Columns callbacks
    #-----------------------------
    def ColumnsExoticEvents(self, traitName):
        raise NotImplementedError('Method ColumnsExoticEvents not implemented')

    def ColumnsAverageEvents(self, traitName):
        return [
                {'methodChain': 'Date',                         'label':'Date',   'formatter':'DateOnly'},
                {'methodChain': 'EventValue',                   'label':'Value',  'formatter':'SP_TrfObservationValue'}
               ]

    #-----------------------------
    # On Selection Changed callacks
    #-----------------------------
    def SelectionExoticEvents(self, traitName, rowObject):
        self.fixingEditer.OnSelectionChanged(rowObject)
        
    def SelectionAverageEvents(self, traitName, rowObject):
        self.dailyFixingEditer.OnSelectionChanged(rowObject)

    #-----------------------------
    # On Changed
    #-----------------------------
    def UpdateBarrierType(self, attrName, *rest):
        if self.hasEkiBarrier is True:
            barrierType = self.GetEkiBarrierType()
            if self.barrierType != barrierType:
                self.barrierType = barrierType

    def SetBarriersToZero(self, attrName, *rest):
        raise NotImplementedError('Method SetBarriersToZero not implemented')

    def RegisterUpdatedAttribute(self, attrName, *args):
        raise NotImplementedError('Method RegisterUpdatedAttribute not implemented')

    #-----------------------------------------
    # Formatters
    #-----------------------------------------
    def FormatTarget(self, traitName):
        raise NotImplementedError('Method FormatTarget not implemented')

    #-----------------------------------------
    # Visibility depending on other fields
    #-----------------------------------------
    def VisibleIfTargetApplicable(self, traitName):
        return self.targetApplicable

    def VisibleIfTargetInverseApplicable(self, attrName):
        return self.VisibleIfTargetApplicable(attrName) and self.targetInverseApplicable

    def VisibleIfStrike2ApplicableAndPhysicalSettlement(self, attrName):
        return self.VisibleIfStrike2Applicable(attrName) and self.VisibleIfPhysicalSettlement(attrName)

    def VisibleIfStrike2Applicable(self, traitName):
        return self.strike2Applicable

    def VisibleIfPivotApplicable(self, traitName):
        return self.pivotApplicable
    
    def VisibleIfBarrier2Applicable(self, attrName):
        return self.barrier2Applicable
    
    def VisibleIfCashSettlement(self, traitName):
        return self.settlementType == "Cash"
    
    def VisibleIfPhysicalSettlement(self, traitName):
        return self.settlementType == "Physical"
            
    def VisibleIfNotCountLoss(self, traitName):
        # For now always true
        # Change if count feature is implemented on other strucutures
        return True

    def VisibleIfBarrier(self, traitName):
        return self.barrierType != "None"
    
    def VisibleIfBarrierAndDoubleBarrierPossible(self, traitName):
        return (self.VisibleIfBarrier(traitName) and self.VisibleIfBarrier2Applicable(traitName))

    def VisibleTerminationStatus(self, traitName):
        return (self.IsShowModeDetail() or self.terminationStatus != "None")

    def VisibleIfBarrierApplicable(self, traitName):
        return self.barrierApplicable

    def VisibleIfAsian(self, attrName):
        return self.isAsian

    def VisibleIfNotAsian(self, attrName):
        return not self.VisibleIfAsian(attrName)

    #-----------------------------------------
    # Validation callbacks
    #-----------------------------------------
    def ValidateDatePeriod(self, attrName, value, *rest):
        if not acm.Time().PeriodSymbolToDate(value):
            raise DealPackageUserException('"%s" is not a valid date period' % value)

    def ValidateBarrierIsNotZero(self, exceptionAccumulator):
        raise NotImplementedError('Method ValidateBarrierIsNotZero not implemented')
        
    def ValidateStartDate(self, attrName, value, *args):
        if not value:
            label = self.GetAttributeMetaData(attrName, 'label')()
            str = 'Expected a %s' % label
            raise DealPackageUserException(str)    
            
    #-----------------------------------------
    # Action callbacks
    #-----------------------------------------
    def Exercise(self, attrName, *rest):
        def CheckAllFixingsDone(event):
            for ee in self.exoticEvents:
                if (acm.Time.DateDifference(ee.Date(), event.Date()) < 0 
                        and ee.EventValue() < epsilon):
                    raise DealPackageUserException('No fixing value for %s' % ee.Date())
            return True
        exerciseObjects = []
        closingPackage = None
        date = rest[0] if len(rest) > 0 else acm.Time().DateToday()
        event = TrfExpiryEvent(self.Option(), date)
        if event:
            openPart = self.tradeQuantity * CalculateOpenPart(self.OptionTrade(), date = event.Date(), tradeType = 'tradeType', status = 'tradeStatus', quantity = 'tradeQuantity', valueDay = 'tradeValueDay', tradeTime = 'tradeTime')
            if abs(openPart) > epsilon:
                if not IsExercised(self.OptionTrade(), event):
                    CheckAllFixingsDone(event)
                    amount = self.ExerciseAmount(date)
                    exerciseObjects = self.ExerciseObjects(amount, event, date, openPart)
                else:
                    raise DealPackageUserException('Trade has already been exercised for %s' % date)
            else:
                raise DealPackageUserException('Position is 0 for %s' % date)

            # Close if last fixing or if early terminated
            if BarrierIsCrossedOnDate(self.Option(), event.Date()) or TodayIsLastTrfExpiry(self.Option(), event.Date()):
                closingPackage = CloseDealPackage(self.DealPackage(), date, event.EndDate(), tradeTimeAttribute='tradeTime')
            
        return exerciseObjects, closingPackage
        
    #-----------------------------------------
    # Choice List values
    #-----------------------------------------
    def ChoicesSettlementType(self, attrName, *rest):
        return SettlementTypeChoices(self.Option())

    #-------------------------------------------------
    # Other methods to be overridden by lower classes
    #-------------------------------------------------

    def GetEkiBarrierType(self):
        if self.barrier2Applicable is True:
            return 'Double In'
        else:
            return 'Down & In'

    #-----------------------------------------
    # Label callbacks
    #-----------------------------------------
    def LabelTargetLevel(self, traitName):
        return "Target"

    def StartDateLabel(self, attrName):
        if self.isAsian:
            return "Start Month"
        else:
            return "First Fixing"

    #-----------------------------------------
    # Tooltip callbacks
    #-----------------------------------------
    def StartDateTooltip(self, attrName):
        if self.isAsian:
            return "First banking day of the first month, used as basis when generating the date schedule"
        else:
            return "First fixing date, used as basis when generating the date schedule"

    def ExactTargetTooltip(self, attrName):
        return "Check this box to adjust strike when the target level is reached in order make the total accumulated target equal to the target level."

    #-----------------------------------------
    # Access components
    #-----------------------------------------
    def Option(self):
        return self.DealPackage().InstrumentAt("Option")

    def OptionNoDecorator(self):
        return self.Option().DecoratedObject()

    def OptionNoQuestionGui(self):
        option = self.OptionNoDecorator()
        gui = acm.FBusinessLogicGUIDefault()
        gui.AskAdjustToFollowingBusinessDay(False)
        return acm.FBusinessLogicDecorator.WrapObject(option, gui)

    def OptionTrade(self):
        return self.DealPackage().TradeAt("Option")
    
    def LeadTrade(self):
        return self.OptionTrade()

    def OptionB2B(self):
        return self.B2BTradeParamsAt("Option")

    #-----------------------------------------
    # Other methods
    #-----------------------------------------
    def UpdateTerminationStatus(self, attrName, *args):
        if self.targetApplicable is True and (self.terminationStatus is None or self.terminationStatus == 'None'):
            accumulation = 0.0
            format = self.GetAttributeMetaData('targetLevel', 'formatter')().NumDecimals()
            for exoticEvent in self.exoticEvents:
                if acm.Time.DateDifference(exoticEvent.Date(), acm.Time.DateToday()) <= 0:
                    if round(self.targetLevel, format) - round(exoticEvent.TrfAccTarget(), format)  < epsilon:
                        self.terminationStatus = 'Confirmed'
                        self.terminationDate =  exoticEvent.Date()
                        return True
        return False

    @ReturnDomainDecorator('bool')
    def HasEkiBarrier(self, value = 'NoValue'):
        if value == 'NoValue':
            return TrfHasBarrier(self.Option())
        else:
            if value is True:
                self.barrierType = self.GetEkiBarrierType()
            else:
                self.barrierType = 'None'

    @ReturnDomainDecorator('FIndexedCollection(FExoticEvent)')
    def TrfExpiryEvents(self, *rest):
        return self.Option().GetExoticEventsOfKind('TRF Expiry')

    @ReturnDomainDecorator('FArray(FExoticEvent)')
    def AveragePriceEvents(self, *rest):
        allEvents = self.Option().GetExoticEventsOfKind('Average price').AsArray()
        if self.fixingEditer.GetFixingEventSelected() is None:
            return acm.FArray()
        else:
            specificEvents = acm.FArray()
            selectedDateAsYMD = acm.Time.DateToYMD(self.fixingEditer.GetFixingEventSelected().Date())
            for event in allEvents:
                eventDateAsYMD = acm.Time.DateToYMD(event.Date())
                if (eventDateAsYMD[0] == selectedDateAsYMD[0] and
                    eventDateAsYMD[1] == selectedDateAsYMD[1]):
                    specificEvents.Add(event)
            return specificEvents

    def TradeNotional(self, value, scaleFactor):
        if value == 'NoValue':
            if scaleFactor:
                return scaleFactor * self.OptionTrade().Quantity()
            else:
                return 0.0
        else:
            if scaleFactor:
                self.OptionTrade().Quantity(value / scaleFactor)

    @ReturnDomainDecorator('float')
    def TradeNotional1(self, value = 'NoValue'):
        return self.TradeNotional(value, self.notional1)
    
    @ReturnDomainDecorator('float')
    def TradeNotional2(self, value = 'NoValue'):
        return self.TradeNotional(value, self.notional2)
    
    def IsFirstFixingDateFixed(self):
        if self.exoticEvents and len(self.exoticEvents) > 0:
            return (self.exoticEvents[0].Date() < acm.Time.DateNow() and \
                   (self.exoticEvents[0].EventValue() > 0.0 or \
                    self.exoticEvents[0].EventValueSecond() > 0.0 ))
        else:
            return False

    def IsB2B(self, attrName):
        return self.b2bEnabled

    def IsB2BorDetail(self, attrName):
        return self.IsB2B(attrName) or self.IsShowModeDetail()

    #-----------------------------------------
    # Interface override
    #-----------------------------------------
    def CustomPanes(self):
        raise NotImplementedError('Method CustomPanes not implemented')

    def OnNew(self):
        if self.InstrumentPackage().IsInfant():

            # Non visible traits
            self.exoticType = "Other"
            
            # Generate TRF Expiry events based on the default values
            self.GenerateTrfExpiryEvents()
            self.GenerateAverageDates()

    def OnSave(self, saveConfig):
        # Check to see if target was reached
        self.checkTargetLevel()
        
        # Make sure that exotic type is set to Other, otherwise
        # Exotic record will be deleted unless a barrier exists
        self.Option().ExoticType('Other')

        super(TrfBaseDefinition, self).OnSave(saveConfig)
        
        return {}

    def IsValid(self, exceptionAccumulator, aspect):
        if self.FieldsUpdatedToGenerate():
            exceptionAccumulator('Fields affecting date periods have been updated, date periods must be re-generated in order to save')
        
        self.ValidateBarrierIsNotZero(exceptionAccumulator)

    def OnInit(self):
        self._formatterTarget = None
        self._standardCalcSpaceCollection = None
        self._numberOfPeriods = None
        self._generateAttributeUpdated = False

        self.RegisterCallbackOnAttributeChanged(self.RegisterUpdatedAttribute)

    def AssemblePackage(self):
        raise NotImplementedError('Method AssemblePackage not implemented')

    @classmethod 
    def SetUp(cls, definitionSetUp):
        SP_TrfUtils.SetupTrf(definitionSetUp)


@TradeActions(
    correct = CorrectCommand(
        statusAttr='tradeStatus', 
        newStatus='Simulated'
    ),
    novate = NovateCommand(
        statusAttr='tradeStatus', 
        nominal='tradeNotional1_value'
    ),
    close = CloseCommand(
        statusAttr='tradeStatus', 
        nominal='tradeNotional1_value'
    ),
    mirror = MirrorCommand(
        statusAttr='tradeStatus', 
        newStatus='Simulated', 
        quantityAttr='tradeNotional1_value'
    )
)
class TrfCommodityBaseDefinition(TrfBaseDefinition):
    
    underlying          = Object(   objMapping = InstrumentPart("Option.Underlying"),
                                    onChanged = '@SetCurrencyEqualToUnderlyingCurrency|UpdateExoticEventReference|UpdateOptionName',
                                    choiceListSource = '@ChoicesUnderlying',
                                    label = "Underlying")

    currency            = Object(   objMapping = InstrumentPart("Option.Currency").DealPart("Trades.Currency"),
                                    editable = False,
                                    label = "Currency")

    strike              = TrfCommodityStrikeComposite(    strikePrice = "Option.StrikePrice",
                                                          strikeSettlement = "Option.AdditionalInfo.Sp_StrikeSettle")

    strike2             = TrfCommodityStrikeComposite(    strikePrice = "Option.AdditionalInfo.Sp_Strike2",
                                                          strikeSettlement = "Option.AdditionalInfo.Sp_Strike2Settle")

    pivotRate           = TrfCommodityPivotRateComposite( pivotRate = "Option.AdditionalInfo.Sp_PivotRate",
                                                          pivotRateStrike = "Option.AdditionalInfo.Sp_PivotRateStrike")
    
    barrier             = TrfCommodityBarrierComposite(   barrierLevel = "Option.Barrier",
                                                          memory = 'Option.AdditionalInfo.Sp_BarrierMemory',
                                                          levelInterpretation = "Option.AdditionalInfo.Sp_BarrierCondition")

    barrier2            = TrfCommodityBarrierComposite(   barrierLevel = "Option.Exotic.DoubleBarrier",
                                                          memory = 'Option.AdditionalInfo.Sp_Barrier2Memory',
                                                          levelInterpretation = "Option.AdditionalInfo.Sp_Barrier2Cond")

    openUnderlying      = Action(   action = '@OpenUnderlying',
                                    enabled = '@UnderlyingIsSet',
                                    label = 'Open')
    
    roundingSpec        = Object(label = 'Rounding',
                                 objMapping = InstrumentPart('Option.RoundingSpecification'),
                                 toolTip = 'Rounding specification affecting the monthly average calculations. If no specification is entered, the average calculations will be rounded to three decimals.')

    #-----------------------------
    # Traits to handle fixing dates
    #-----------------------------
    fixingEditer = TrfCommodityFixingEditerComposite(instrument='Option')
    dailyFixingEditer = TrfDailyFixingEditerComposite(instrument='Option')
    
    #-----------------------------
    # Non visible traits
    #-----------------------------
    notionalQuotation   = Object(    objMapping = InstrumentPart("Option.Underlying.Quotation") )
    optionNameUpdated = Bool(defaultValue = False)
    
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'deliveryCalendar':       dict( label = 'Pay Calendar',
                                            toolTip = 'If a default pay date (generated from the currency calendar) falls on a non banking day according to this optional calendar, it will be adjusted forward.'),
            'delivery':               dict( label = 'Final Payment'),
            'settlementType':         dict( defaultValue = 'Cash',
                                            editable = False),
            'tradeCurrency':          dict( editable = False),
            'tradeNotional1_buySell': dict( label = "@LabelReplaceWithQuotation",
                                            _labelText = "Notional 1 (Quotation)"),
            'tradeNotional2_buySell': dict( label = "@LabelReplaceWithQuotation",
                                            _labelText = "Notional 2 (Quotation)"),
            'notional1':              dict( defaultValue = 100,
                                            label = "@LabelReplaceWithQuotation",
                                            _labelText = "Notional 1 (Quotation)"),
            'notional2':              dict( defaultValue = 200,
                                            label = "@LabelReplaceWithQuotation",
                                            _labelText = "Notional 2 (Quotation)"),
            'strike_strikePrice':     dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Strike (Currency per Quotation)'),
            'strike2_strikePrice':    dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Strike (Currency per Quotation)',
                                            visible="@VisibleIfStrike2Applicable"),
            'pivotRate_pivotRate':    dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Pivot Rate (Currency per Quotation)',
                                            visible="@VisibleIfPivotApplicable"),
            'barrier_barrierLevel':   dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Barrier (Currency per Quotation)',
                                            toolTip='OTM Barrier Level',
                                            validate='@ValidateBarrierLevel',
                                            visible="@VisibleIfBarrier"),
            'barrier2_barrierLevel':  dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Upper Barrier (Currency per Quotation)',
                                            validate='@ValidateBarrierLevel',
                                            recreateCalcSpaceOnChange=True,
                                            visible="@VisibleIfBarrierAndDoubleBarrierPossible"),
            'targetLevel':            dict( defaultValue = 10.0,
                                            label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Target (Currency per Quotation)',
                                            width=9),
            'fixingSource' :          dict( objMapping = InstrumentPart("OptionNoDecorator.FixingSource"),
                                            toolTip = "Fixing Source",
                                            choiceListSource = ChoicesExprInstrument.getFixingSources(False)),
            'isAsian':                dict( defaultValue = True),
            'averageMethodType':      dict( defaultValue = 'Arithmetic'),
            'averagePriceType':       dict( defaultValue = 'Average'),
            'averageStrikeType':      dict( defaultValue = 'Fix'),
            'dayMethod':              dict( visible = False,
                                            defaultValue = 'Following'),
            'isCallOption':           dict( defaultValue = True),
            'valGroup':               dict( visible = '@IsShowModeDetail'),
            'targetLevelInv':         dict( defaultValue = False),
            'exoticEvents' :          dict( dialog = NoButtonAttributeDialog(
                                                label = 'Observations', 
                                                customPanes = self.GetCustomPanes()),
                                            onDoubleClick = '@OnCloseExoticEventsDialog'),
            'fixingEditer_fixingValue': dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                              _labelText = 'Fixing (Currency per Quotation)',
                                              formatter = 'SP_TrfFixingValue'),
            'dailyFixingEditer_fixingValue': dict( label="@LabelReplaceWithCurrencyPerQuotation",
                                            _labelText = 'Value (Currency per Quotation)'),
            'dailyFixingEditer_fixingDate' : dict( label = 'Observation Date:')
            })

    #-----------------------------------------
    # Private methods
    #-----------------------------------------
    def GetCustomPanes(self):
        # Work-around. fixingEditer is not initilized at this stage,
        # causing the call to UniqueLayout to return without the 
        # attributes beeing prefixed with the comp. attr. name
        str = ( 
        '''
            vbox[Fixing;
                hbox(;
                    dailyFixingEditer_fixingDate;
                    dailyFixingEditer_payDate;
                );
                hbox(;   
                    dailyFixingEditer_fixingValue;
                );
                hbox(;
                    dailyFixingEditer_fixingAdd;
                    dailyFixingEditer_fixingUpdate;
                    dailyFixingEditer_fixingRemove;
                    dailyFixingEditer_fixingFixRate;
                );
            ];
        ''')
        set = [{"": 'hbox[;averageEvents;];' + str}]
        return set
    
    def OnCloseExoticEventsDialog(self, *args):
        self.dailyFixingEditer.ResetState()

    #-----------------------------------------
    # Protected methods
    #-----------------------------------------
    def ExerciseAmount(self, date):
        amount = CalculateCommodityTRFSettlementAmounts(
            self.OptionTrade(), date)
        return amount
        
    def ExerciseObjects(self, amount, event, date, openPart):
        if abs(amount) < epsilon:
            raise DealPackageUserException(
                'Exercise amount is 0, no exercise payment booked.')
                
        totAmount = amount * openPart
        settlementDate = event.EndDate()
        exObjs = AddExerciseCashPayment(
            self.OptionTrade(), 
            event, 
            totAmount, 
            settlementDate)
            
        return exObjs
    
    def SetDeliveryDate(self):
        for ee in self.exoticEvents:
            if self._deliveryDate is None or acm.Time.DateDifference(self._deliveryDate, ee.EndDate()) < 0:
                self._deliveryDate = ee.EndDate()

    #-----------------------------
    # Object Mapping
    #-----------------------------
    @ReturnDomainDecorator("date")
    def DeliveryDate(self, value = 'Reading'):
        if value == 'Reading':
            if self._deliveryDate is None:
                self.SetDeliveryDate()
            return self._deliveryDate
        else:
            self._deliveryDate = value
        
    #-----------------------------
    # Columns callbacks
    #-----------------------------
    def ColumnsExoticEvents(self, traitName):
        return [
                {'methodChain': 'Date',                         'label':'Period End',   'formatter':'DateOnly'},
                {'methodChain': 'EndDate',                      'label':'Pay Date',   'formatter':'DateOnly'},
                {'methodChain': 'EventValue',                   'label':'Fixing', 'formatter': 'SP_TrfFixingValue'},
                {'methodChain': 'Instrument.ContractSizeInQuotation', 'label':'Notional 1'},
                {'methodChain': 'Instrument.AdditionalInfo.Sp_LeverageNotional', 'label':'Notional 2'},
                {'methodChain': 'TrfAccTarget',                 'label':'Acc Target',   'formatter':'SP_TrfAccumulated'}
                ]

    #-----------------------------
    # Labels
    #-----------------------------
    def LabelReplaceWithQuotation(self, traitName):
        label = self.GetAttributeMetaData(traitName, '_labelText')()
        if label:
            if label.find('Quotation') > 0:
                if not self.notionalQuotation:
                    return label.split('(')[0].strip()
                quotationName = self.notionalQuotation.Name().replace('Per ', '')
                label = label.replace('Quotation', quotationName)
        return label

    def LabelReplaceWithCurrencyPerQuotation(self, traitName):
        label = self.GetAttributeMetaData(traitName, '_labelText')()
        if label:
            label = self.LabelReplaceWithQuotation(traitName)
            if label.find('Currency') > 0:
                if (not self.underlying) or (not self.underlying.Currency()):
                    return label.split('(')[0].strip()
                ccyName = self.underlying.Currency().Name()
                label = label.replace('Currency', ccyName)            
        return label

    def LabelFixingValue(self, traitName):
        cname = self.underlying.Currency().Name()
        qname = self.underlying.Quotation().Name()
        str = 'Fixing (' + cname + ' per ' + qname + ')'
        return str
        
    #-----------------------------
    # On Changed callbacks
    #-----------------------------

    def UpdateExoticEventReference(self, attrName, *rest):
        if self.underlying:
            for ee in self.Option().ExoticEvents():
                ee.ComponentInstrument(self.GetExoticEventReference())

    def SetCurrencyEqualToUnderlyingCurrency(self, attrName, *rest):
        if self.underlying:
            self.currency = self.underlying.Currency()

    def RegisterUpdatedAttribute(self, attrName, *args):
        if attrName in ('underlying',
                        'startDate',
                        'nbrOfPeriods',
                        'deliveryCalendar',
                        'settlementDays'):
            self._generateAttributeUpdated = True

    def SetBarriersToZero(self, attrName, *rest):
        if attrName != 'hasEkiBarrier' or self.hasEkiBarrier is False:
            self.barrier_barrierLevel = 0.0
            self.barrier2_barrierLevel = 0.0
    
    def UpdateOptionName(self, attrName, *rest):
        if self.Option().Name() != '':
            self.Option().Name(self.Option().SuggestName())
            self.optionNameUpdated = True

    #-----------------------------------------
    # Formatters
    #-----------------------------------------
    def FormatTarget(self, traitName):
        if not self._formatterTarget:
            self._formatterTarget = acm.Get('formats/SP_TrfTargetLevel').Clone()
        self._formatterTarget.NumDecimals(2)
        return self._formatterTarget

    #-----------------------------------------
    # Choice List values
    #-----------------------------------------
    def ChoicesSettlementType(self, attrName, *rest):
        return ['Cash']
    
    def ChoicesUnderlying(self, attrName, *rest):
        return acm.FCommodity.Instances()

    #-----------------------------------------
    # Enabled callbacks
    #-----------------------------------------
    def FieldsSetToGenerate(self):
        return (self.startDate and self.datePeriod and 
                self.dayMethod and self.underlying)

    def UnderlyingIsSet(self, *rest):
        return self.underlying is not None

    #-----------------------------------------
    # Action callbacks
    #-----------------------------------------
    def OpenUnderlying(self, *rest):
        underlying = UnDecorate(self.underlying)
        acm.StartApplication('Instrument Definition', underlying.Originator())

    #-----------------------------------------
    # Date period logic
    #-----------------------------------------
    def GetFixingParams(self):
        if not (self.underlying):
            raise DealPackageUserException(
                'Cannot generate date periods without underlying set')
        if not (self.currency):
            raise DealPackageUserException(
                'Cannot generate date periods without currency set')
        return {
                'startDate'             : self.startDate,
                'fixingCalendar'        : GetRelevantFixingCalendar(self.Option()),
                'settlementCalendar'    : self.currency.Calendar(),
                'deliveryCalendar'      : self.deliveryCalendar,
                'nbrOfPeriods'          : self.nbrOfPeriods,
                'settleDays'            : self.settlementDays,
                'dayMethod'             : 'Following'
                }

    def GeneratePeriodDates(self):
        if self.isAsian:
            return GenerateMonthlyPeriodDates(**self.GetFixingParams())
        else:
            raise DealPackageException("Only monthly Asian style TRF is supported for commodity")

    def GetExoticEventReference(self):
        return self.underlying

    #-----------------------------------------
    # Attribute Validation
    #-----------------------------------------
    def ValidateBarrierLevel(self, attrName, value, *rest):

        if self.hasEkiBarrier is True and value != 0.0:
            if self.barrierType == 'Down & In':
                if value >= self.strike_strikePrice:
                    raise DealPackageUserException('EKI barrier level must be below strike level (%f)' % self.strike_strikePrice)
            elif self.barrierType == 'Double In':
                if attrName == 'barrier_barrierLevel' and value >= self.strike_strikePrice:
                    raise DealPackageUserException('EKI barrier level must be below strike level (%f)' % self.strike_strikePrice)
                if attrName == 'barrier2_barrierLevel' and value <= self.strike2_strikePrice:
                    raise DealPackageUserException('EKI barrier level must be above strike level (%f)' % self.strike2_strikePrice)

    def ValidateBarrierIsNotZero(self, exceptionAccumulator):
        if self.hasEkiBarrier:
            if self.barrierApplicable and self.barrier_barrierLevel < 1e-8:
                exceptionAccumulator('Barrier value cannot be 0')
            if self.barrier2Applicable and self.barrier2_barrierLevel < 1e-8:
                exceptionAccumulator('Barrier value cannot be 0')

    #-----------------------------------------
    # Interface override
    #-----------------------------------------
    def AssemblePackage(self):
        ins = acm.DealCapturing().CreateNewInstrument("Option")
        trade = acm.DealCapturing().CreateNewTrade(ins)
        self.DealPackage().AddTrade(trade, "Option")

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_SP_TrfCommodityDealPackage")

    def OnNew(self):
        if self.InstrumentPackage().IsInfant():
            if ( self.underlying is None or 
                 not self.underlying.IsKindOf(acm.FCommodity)):
                choicListSource = self.GetAttributeMetaData('underlying', 'choiceListSource')()
                if choicListSource.IsKindOf(acm.FArray) and choicListSource.Size() == 0:
                    raise DealPackageUserException('Cannot start the Commodity TRF application because there are no commodities set up in the system')
                choices =choicListSource.GetChoiceListSource()
                if choices.Size() == 0:
                    raise DealPackageUserException('Cannot start the Commodity TRF application because there are no commodities set up in the system')
                self.underlying = choices.At(0)
        super(TrfCommodityBaseDefinition, self).OnNew()

    def OnInit(self):
        self._deliveryDate = None

        super(TrfCommodityBaseDefinition, self).OnInit()

    def OnSave(self, saveConfig):
        if self.optionNameUpdated is True:
            self.Option().Name('')
            self.Option().Name(self.Option().SuggestName())
            self.optionNameUpdated = False
        super(TrfCommodityBaseDefinition, self).OnSave(saveConfig)


@TradeActions( correct = CorrectCommand(statusAttr='tradeStatus', newStatus='Simulated'),
               novate = NovateCommand(statusAttr='tradeStatus', nominal='tradeNotional1_value'),
               close = CloseCommand(statusAttr='tradeStatus', nominal='tradeNotional1_value'),
               mirror = MirrorCommand(statusAttr='tradeStatus', newStatus='Simulated', quantityAttr='tradeNotional1_value'))


class TrfFxBaseDefinition(TrfBaseDefinition):

    foreignPerDomesticVBox = Box( vertical=True,
                                  label='@LabelCurrBox')

    domesticPerForeignVBox = Box( vertical=True,
                                  label='@LabelCurrBox')

    #-----------------------------
    # Visible Traits
    #-----------------------------

    packageType         = SP_TrfUtils.SelectPackageType(label='Type', 
                                            choiceListSource=SP_TrfUtils.GetAllTRFProductTypes(),
                                            definitionPrefix = 'FX ')

    foreignCurrency     = Object(   objMapping = InstrumentPart("Option.ForeignCurrency"),
                                    label = "@BuySellForeignValue",
                                    choiceListSource = "@ChoicesForeignCurrency",
                                    onChanged = "@UpdateCurrencyChoices",
                                    toolTip = "Notional Currency" )

    domesticCurrency    = Object(   objMapping = InstrumentPart("Option.DomesticCurrency"),
                                    label = "@BuySellDomesticValue",
                                    choiceListSource = "@ChoicesDomesticCurrency",
                                    onChanged = "@UpdateCurrencyChoices",
                                    toolTip = "Domestic Currency" )
        
    buySellForeign      = Object(   objMapping = InstrumentPart("BuySellForeign"),
                                    visible = False, # Visible via currency label
                                    label = "",
                                    onChanged = '@UpdateBarrierType|SetBarriersToZero',
                                    choiceListSource = ["BUY", "SELL"],
                                    toolTip = "Is the notional currency bought or sold?" )

    buySellDomestic     = Object(   objMapping = InstrumentPart("BuySellDomestic"),
                                    visible = False, # Visible via currency label
                                    label = "",
                                    onChanged = '@UpdateBarrierType|SetBarriersToZero',
                                    choiceListSource = ["BUY", "SELL"],
                                    toolTip = "Is the second currency bought or sold?" )
    
    strike              = TrfFxStrikeComposite( rateDomPerFor = "Option.StrikeDomesticPerForeign",
                                              rateForPerDom = "Option.StrikeForeignPerDomestic",
                                              strikeSettlement = "Option.AdditionalInfo.Sp_StrikeSettle")

    # Move with override
    strike2             = TrfFxStrikeComposite( rateDomPerFor = "Strike2DomesticPerForeign",
                                              rateForPerDom = "Strike2ForeignPerDomestic",
                                              strikeSettlement = "Option.AdditionalInfo.Sp_Strike2Settle")

    # Move with override
    pivotRate           = TrfFxPivotRateComposite( rateDomPerFor = "PivotRateDomesticPerForeign",
                                                 rateForPerDom = "PivotRateForeignPerDomestic",
                                                 pivotRateStrike = "Option.AdditionalInfo.Sp_PivotRateStrike")

    # Move with override
    barrier             = TrfFxBarrierComposite( rateDomPerFor = "Option.Exotic.BarrierDomesticPerForeign",
                                               rateForPerDom = "Option.Exotic.BarrierForeignPerDomestic",
                                               memory = 'Option.AdditionalInfo.Sp_BarrierMemory',
                                               levelInterpretation = "Option.AdditionalInfo.Sp_BarrierCondition")

    # Move with override
    barrier2            = TrfFxBarrierComposite( rateDomPerFor = "Option.Exotic.DoubleBarrierDomesticPerForeign",
                                               rateForPerDom = "Option.Exotic.DoubleBarrierForeignPerDomestic",
                                               memory = 'Option.AdditionalInfo.Sp_Barrier2Memory',
                                               levelInterpretation = "Option.AdditionalInfo.Sp_Barrier2Cond")

    targetLevelInv      = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_InvertedTarget"),
                                    visible = '@VisibleIfTargetApplicable',
                                    label = "@LabelReplaceWithCurrency",
                                    _labelText = "Inverse Target Level (Foreign per Domestic)" )
    
    settleInCurr2       = Object(   objMapping = InstrumentPart("Option.AdditionalInfo.Sp_SettleInCurr2"),
                                    visible = "@VisibleIfCashSettlement",
                                    defaultValue = True,
                                    label = "Settle in Domestic Currency" )

    #-----------------------------
    # Traits to handle fixing dates
    #-----------------------------
    fixingEditer = TrfFxFixingEditerComposite(instrument='Option')
    
    #-----------------------------
    # Non visible traits
    #-----------------------------
    baseType            = Object(   objMapping = InstrumentPart("Option.Exotic.BaseType") )

    strikeQuotation     = Object(   objMapping = InstrumentPart("Option.StrikeQuotation"),
                                    onChanged = '@SetNonStandardStorageDirection')

    flipBuySell         = Action(   action = "@FlipBuySell")
    
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'notional1':                          dict(defaultValue=1000000),
            'notional2':                          dict(defaultValue=2000000),
            'foreignCurrency':                    dict(defaultValue='EUR'),
            'domesticCurrency':                   dict(defaultValue='USD'),
            'targetLevel':                        dict(defaultValue=0.2),  
            'settlementType':                     dict(defaultValue='Physical'),  
            'settleInCurr2':                      dict(defaultValue=True),  
            'fixingSource' :                      dict(toolTip = "Expiry Cutoff",
                                                       choiceListSource = ChoicesExprInstrument.getFixingSources(True)),
            'strike_rateDomesticPerForeign':      dict(defaultValue= 1.3, 
                                                        label='Strike'),
            'strike_rateForeignPerDomestic':      dict(label='Strike'),
            'strike2_rateDomesticPerForeign':     dict(defaultValue= 1.4, 
                                                        label='Strike',
                                                       visible="@VisibleIfStrike2Applicable"),
            'strike2_rateForeignPerDomestic':     dict(label='Strike',
                                                       visible="@VisibleIfStrike2Applicable"),
            'pivotRate_rateDomesticPerForeign':   dict(defaultValue= 1.35, 
                                                        label='Pivot Rate',
                                                       visible="@VisibleIfPivotApplicable"),
            'pivotRate_rateForeignPerDomestic':   dict(label='Pivot Rate',
                                                       visible="@VisibleIfPivotApplicable"),
            'barrier_rateDomesticPerForeign':     dict(defaultValue= 0.0, 
                                                        label='Barrier',
                                                       toolTip='OTM Barrier Level',
                                                       validate='@ValidateBarrierLevel',
                                                       visible="@VisibleIfBarrier"),
            'barrier_rateForeignPerDomestic':     dict(label='Barrier',
                                                       validate='@ValidateBarrierLevel',
                                                       toolTip='OTM Barrier Level',
                                                       visible="@VisibleIfBarrier"),
            'barrier2_rateDomesticPerForeign':    dict(defaultValue= 0.0, 
                                                        label='Upper Barrier',
                                                       validate='@ValidateBarrierLevel',
                                                       recreateCalcSpaceOnChange=True,
                                                       visible="@VisibleIfBarrierAndDoubleBarrierPossible"),
            'barrier2_rateForeignPerDomestic':    dict(label='Lower Barrier',
                                                       validate='@ValidateBarrierLevel',
                                                       recreateCalcSpaceOnChange=True,
                                                       visible="@VisibleIfBarrierAndDoubleBarrierPossible"),
            'fixingEditer_fixingValue_rateDomesticPerForeign': dict(label="@LabelReplaceWithCurrency",
                                                       _labelText = "Fixing (Domestic per Foreign)"),
            'fixingEditer_fixingValue_rateForeignPerDomestic': dict(label="@LabelReplaceWithCurrency",
                                                       _labelText = "Fixing (Foreign per Domestic)"),
            'tradeNotional1_buySell':             dict(label = "@LabelReplaceWithCurrency",
                                                       _labelText = "Notional 1 (Foreign)"),
            'tradeNotional2_buySell':             dict(label = "@LabelReplaceWithCurrency",
                                                       _labelText = "Notional 2 (Foreign)"),
            'tradeCurrency':                      dict(onChanged = "@OnChangedTradeCurrency"),
            'barrierApplicable':                  dict(defaultValue = True),
            'targetInverseApplicable':            dict(defaultValue = True),
            'barrierType':                        dict(onChanged = "@OnChangedBarrierType"),
            'settlementDays':                     dict(visible = False),
            'targetLevelInv':                     dict(defaultValue = False,
                                                        label = "@LabelReplaceWithCurrency",
                                                       _labelText = "Inverse Target Level (Foreign per Domestic)")
            })

    #-----------------------------
    # Protected methods
    #-----------------------------
    def ExerciseAmount(self, date):
        return CalculateTRFSettlementAmounts(self.OptionTrade(), date)
        
    def ExerciseObjects(self, amount, event, date, openPart):
        if self.settlementType == 'Cash':
            if abs(amount) > epsilon:
                return AddExerciseCashPayment(self.OptionTrade(), event, amount * openPart, event.EndDate(), self.domesticCurrency if self.settleInCurr2 is True else self.foreignCurrency)
            else:
                raise DealPackageUserException('Exercise amount is 0, no exercise payment booked.')
        else:
            if abs(amount[0]) > epsilon and abs(amount[1]) > epsilon:
                amount1 = acm.DenominatedValue(amount[0] * openPart, self.foreignCurrency, date)
                amount2 = acm.DenominatedValue(amount[1] * openPart, self.domesticCurrency, date)
                return CreatePhysicalDeliveryFxSpotExerciseTrade(self.OptionTrade(), amount1, amount2, event.EndDate(), self.OptionB2B())
            else:
                raise DealPackageUserException('Exercise amount is 0, no exercise trade booked.')
        return []
        
    #-----------------------------
    # Object Mappings
    #-----------------------------
    def ExpiryDate(self, value = 'NoVal'):
        if value == 'NoVal':
            return self.OptionNoQuestionGui().FxoExpiryDate()
        else:
            self.OptionNoQuestionGui().FxoExpiryDate(value)

    @ReturnDomainDecorator("date")
    def DeliveryDate(self, value = 'Reading'):
        if value == 'Reading':
            return self.Option().DeliveryDate()
        else:
            self.Option().DeliveryDate(value)

    def GetFixingParams(self):
        if not (self.foreignCurrency and self.domesticCurrency):
            DealPackageUserException(
                'Cannot generate date periods without currencies set'
            )
        currPair = self.foreignCurrency.CurrencyPair(self.domesticCurrency)
        return {
                'startDate'             : self.startDate,
                'rolling'               : self.datePeriod,
                'dayMethod'             : self.dayMethod,
                'currencyPair'          : currPair,
                'deliveryCalendar'      : self.deliveryCalendar,
                'nbrOfPeriods'          : self.nbrOfPeriods
                }

    def GeneratePeriodDates(self):
        return GenerateFXPeriodDates(**self.GetFixingParams())

    #-----------------------------
    # Enabled Callbacks
    #-----------------------------
    def FieldsSetToGenerate(self):
        return (self.startDate and self.datePeriod and 
                self.dayMethod and self.foreignCurrency and self.domesticCurrency)

    #-----------------------------
    # Action Callbacks
    #-----------------------------
    def FlipBuySell(self, attrName = None, *rest):
        self.Option().FxoChangeCallPut()
            
    #-----------------------------
    # Columns callbacks
    #-----------------------------
    def ColumnsExoticEvents(self, traitName):
        return [
                {'methodChain': 'Date',                'label':'Fixing Date',   'formatter':'DateOnly'},
                {'methodChain': 'EndDate',                   'label':'Pay Date',   'formatter':'DateOnly'},
                {'methodChain': 'TrfFixingDomesticPerForeign',  'label':'Fixing',       'formatter':'FXRate'},
                {'methodChain': 'TrfFixingForeignPerDomestic',  'label':'Fixing Inv',   'formatter':'FXRate'},
                {'methodChain': 'Instrument.ContractSize',      'label':'Notional 1'},
                {'methodChain': 'Instrument.AdditionalInfo.Sp_LeverageNotional', 'label':'Notional 2'},
                {'methodChain': 'TrfAccTarget',                 'label':'Acc Target',   'formatter':'SP_TrfAccumulated'}
                ]
    
    #-----------------------------
    # On Changed
    #-----------------------------
    
    def SetBarriersToZero(self, attrName, *rest):
        if attrName != 'hasEkiBarrier' or self.hasEkiBarrier is False:
            if self.strikeQuotation.Name() == 'Per Unit':
                self.barrier_rateDomesticPerForeign = 0.0
                self.barrier2_rateDomesticPerForeign = 0.0
            else:
                self.barrier_rateForeignPerDomestic = 0.0
                self.barrier2_rateForeignPerDomestic = 0.0
    
    def OnChangedTradeCurrency(self, traitName, oldValue, newValue, *rest):
        if newValue and (newValue != oldValue):
            self.Option().Currency(newValue)

    def OnChangedBarrierType(self, traitName, oldValue, newValue, *rest):
        if newValue == "None" and self.baseType != "Vanilla":
            self.ChangeBaseType( "Vanilla" )
        if newValue != "None" and self.baseType != "Barrier":
            self.ChangeBaseType( "Barrier" )

    def RegisterUpdatedAttribute(self, attrName, *args):
        if attrName in ('domesticCurrency',
                        'foreignCurrency',
                        'datePeriod',
                        'startDate',
                        'nbrOfPeriods',
                        'deliveryCalendar',
                        'dayMethod'):
            self._generateAttributeUpdated = True

    #-----------------------------------------
    # FX Rate values
    #-----------------------------------------
    def SetNonStandardStorageDirection(self, attrName, *rest):
        # Set non standard fields if storage deirection is updated by decorator
        if self.strikeQuotation.Name() == 'Per Unit':
            self.pivotRate_rateDomesticPerForeign = GetInverseRate(self.pivotRate_rateDomesticPerForeign)
            self.strike2_rateDomesticPerForeign = GetInverseRate(self.strike2_rateDomesticPerForeign)
        else:
            self.pivotRate_rateForeignPerDomestic = GetInverseRate(self.pivotRate_rateForeignPerDomestic)
            self.strike2_rateForeignPerDomestic = GetInverseRate(self.strike2_rateForeignPerDomestic)
        
    def TriggerFlipOfStorageDirection(self, direction):
        # Tigger decorator driven updates if the storage direction is updated using a non standard field
        if ((direction == 'DomesticPerForeign' and self.strikeQuotation.Name() == 'Per Unit Inverse') or
           (direction == 'ForeignPerDomestic' and self.strikeQuotation.Name() == 'Per Unit')):
            self.GetAttribute('strike_store%s' % direction)()

    @ReturnDomainDecorator('float')
    def PivotRateDomesticPerForeign(self, rate = 'NoValue'):
        if rate == 'NoValue':
            return self.GetNonStandardDomesticPerForeign(self.Option().AdditionalInfo().Sp_PivotRate())
        else:
            self.SetNonStandardDomesticPerForeign(rate, self.Option().AdditionalInfo().Sp_PivotRate)

    @ReturnDomainDecorator('float')
    def PivotRateForeignPerDomestic(self, rate = 'NoValue'):
        if rate == 'NoValue':
            return self.GetNonStandardForeignPerDomestic(self.Option().AdditionalInfo().Sp_PivotRate())
        else:
            self.SetNonStandardForeignPerDomestic(rate, self.Option().AdditionalInfo().Sp_PivotRate)

    @ReturnDomainDecorator('float')
    def Strike2DomesticPerForeign(self, rate = 'NoValue'):
        if rate == 'NoValue':
            return self.GetNonStandardDomesticPerForeign(self.Option().AdditionalInfo().Sp_Strike2())
        else:
            self.SetNonStandardDomesticPerForeign(rate, self.Option().AdditionalInfo().Sp_Strike2)

    @ReturnDomainDecorator('float')
    def Strike2ForeignPerDomestic(self, rate = 'NoValue'):
        if rate == 'NoValue':
            return self.GetNonStandardForeignPerDomestic(self.Option().AdditionalInfo().Sp_Strike2())
        else:
            self.SetNonStandardForeignPerDomestic(rate, self.Option().AdditionalInfo().Sp_Strike2)

    def SetNonStandardDomesticPerForeign(self, value, setMethod):
        self.SetNonStandardRate(value, setMethod, 'DomesticPerForeign')

    def SetNonStandardForeignPerDomestic(self, value, setMethod):
        self.SetNonStandardRate(value, setMethod, 'ForeignPerDomestic')

    def SetNonStandardRate(self, value, setMethod, direction):
        value = TransformUsingDecorator(self.Option(), value, 'Strike%s' % direction)
        # Trigger the decorator flip ahead of setting the value
        self.TriggerFlipOfStorageDirection(direction)
        setMethod(value)

    def GetNonStandardDomesticPerForeign(self, value):
        if self.strikeQuotation is not None and self.strikeQuotation.Name() == 'Per Unit Inverse':
            return GetInverseRate(value)
        return value
    
    def GetNonStandardForeignPerDomestic(self, value):
        if self.strikeQuotation is None or self.strikeQuotation.Name() == 'Per Unit':
            return GetInverseRate(value)
        return value

    #-----------------------------------------
    # Formatters
    #-----------------------------------------
        
    def FormatTarget(self, traitName):
        if not self._formatterTarget:
            self._formatterTarget = acm.Get('formats/SP_TrfTargetLevel').Clone()
        if self.targetLevelInv is True:
            numDecimals = GetCurrencyPairPointsDomesticPerForeign(self.domesticCurrency, self.foreignCurrency)
        else:
            numDecimals = GetCurrencyPairPointsDomesticPerForeign(self.foreignCurrency, self.domesticCurrency)
        self._formatterTarget.NumDecimals(numDecimals)
        return self._formatterTarget

    #-----------------------------------------
    # Choice List values
    #-----------------------------------------
    def ChoicesForeignCurrency(self, traitName):
        self.UpdateCurrencyChoices(traitName)
        return self._foreignCurrencyChoices.Source()
    
    def ChoicesDomesticCurrency(self, traitName):
        self.UpdateCurrencyChoices(traitName)
        return self._domesticCurrencyChoices.Source()

    def UpdateCurrencyChoices(self, traitName, *args):
        self._foreignCurrencyChoices.Clear()
        self._domesticCurrencyChoices.Clear()
        ccy1List = self.Option().DefaultForeignCurrencies()
        ccy2List = self.Option().DefaultDomesticCurrencies()
        self._foreignCurrencyChoices.AddAll(ccy1List)
        self._domesticCurrencyChoices.AddAll(ccy2List)

    #-----------------------------------------
    # Define Labels
    #-----------------------------------------
    def LabelTargetLevel(self, traitName):
        if self.foreignCurrency and self.domesticCurrency:
            if self.targetLevelInv:
                return "Target (%s per %s)" % (self.foreignCurrency.Name(), self.domesticCurrency.Name())
            else:
                return "Target (%s per %s)" % (self.domesticCurrency.Name(), self.foreignCurrency.Name())
        return "Target"

    def LabelReplaceWithCurrency(self, traitName):
        label = self.GetAttributeMetaData(traitName, '_labelText')()
        if label:
            if label.find('Foreign') > 0:
                if not self.foreignCurrency:
                    return label.split('(')[0].strip()
                label = label.replace('Foreign', self.foreignCurrency.Name())
            if label.find('Domestic') > 0:
                if not self.domesticCurrency:
                     return label.split('(')[0].strip()
                label = label.replace('Domestic', self.domesticCurrency.Name())
        return label

    def LabelCurrBox(self, traitName):
        foreign  = self.foreignCurrency.Name() if self.foreignCurrency else 'Foreign'
        domestic = self.domesticCurrency.Name() if self.domesticCurrency else 'Domestic'
        if traitName.startswith('foreign'):
            label = "%s per %s" % (foreign, domestic)
        else:
            label = "%s per %s" % (domestic, foreign)
        return label

    #-------------------------------------------------
    # Other methods to be overridden by lower classes
    #-------------------------------------------------

    def GetEkiBarrierType(self):
        if self.barrier2Applicable is True:
            return 'Double In'
        else:
            if self.buySellForeign == 'SELL':
                return 'Up & In'
            else:
                return 'Down & In'

    #-----------------------------------------
    # Other methods
    #-----------------------------------------
    def SetQuotationPerContract(self, *rest):
        self.quotation = 'Per Contract'

    def GetExoticEventReference(self):
        return self.foreignCurrency

    @ReturnDomainDecorator('string')
    def BuySellDomestic(self, value = 'NoValue'):
        return BuySellMapping(self.Option(), 'Domestic', value)

    @ReturnDomainDecorator('string')
    def BuySellForeign(self, value = 'NoValue'):
        return BuySellMapping(self.Option(), 'Foreign', value)

    def BuySellForeignValue(self, *rest):
        return self.buySellForeign
    
    def BuySellDomesticValue(self, *rest):
        return self.buySellDomestic

    def GetStoredStrikeAndBarriers(self):
        if self.strikeQuotation.Name() == 'Per Unit':
            return (self.strike_rateDomesticPerForeign,
                    self.barrier_rateDomesticPerForeign,
                    self.barrier2_rateDomesticPerForeign)
        else:
            return (self.strike_rateForeignPerDomestic,
                    self.barrier_rateForeignPerDomestic,
                    self.barrier2_rateForeignPerDomestic)
    
    def ResetStoredStrikeAndBarriers(self, strike, barrier, barrier2):
        if self.strikeQuotation.Name() == 'Per Unit':
            self.strike_rateDomesticPerForeign = strike
            self.barrier_rateDomesticPerForeign = barrier
            self.barrier2_rateDomesticPerForeign = barrier2
        else:
            self.strike_rateForeignPerDomestic = strike
            self.barrier_rateForeignPerDomestic = barrier
            self.barrier2_rateForeignPerDomestic = barrier2

    def ChangeBaseType(self, newValue):
        # Store away values that will be reset by the decorator when changing base type
        storeBarrierType        = self.barrierType
        storeStrike1, storeBarrier1, storeBarrier2 = self.GetStoredStrikeAndBarriers()
        storeSettlementType     = self.settlementType
        storeStrikeQuotation    = self.strikeQuotation
    
        # Change the base type
        self.baseType           = newValue

        # Reset the values that were changed by the base type change
        self.barrierType                     = storeBarrierType
        self.strikeQuotation                 = storeStrikeQuotation
        self.ResetStoredStrikeAndBarriers(storeStrike1, storeBarrier1, storeBarrier2)
        self.settlementType                     = storeSettlementType
        self.exoticType                         = 'Other'
        
    def GetPairCalendars(self):
        calendars = []
        if self.foreignCurrency:
            calendars.append(self.foreignCurrency.Calendar())
        if self.domesticCurrency:
            calendars.append(self.domesticCurrency.Calendar())
        return calendars

    def TradeDayFromPeriod(self, startDate, period):
        nonAdjustedDate = acm.Time.DateAdjustPeriod(startDate, period)
        # When entering a period, automatically adjust to a banking day
        date = AdjustBankingDaysFromMultiCalendars(nonAdjustedDate, 0, self.GetPairCalendars())
        return date

    #-----------------------------------------
    # Attribute Validation
    #-----------------------------------------
    def ValidateBarrierLevel(self, attrName, value, *rest):

        if self.hasEkiBarrier is True and value != 0.0:
            if self.barrierType == 'Up & In':
                if attrName == 'barrier_rateDomesticPerForeign' and value <= self.strike_rateDomesticPerForeign:
                    raise DealPackageUserException('EKI barrier level must be above strike level (%f)' % self.strike_rateDomesticPerForeign)
                if attrName == 'barrier_rateForeignPerDomestic' and value >= self.strike_rateForeignPerDomestic:
                    raise DealPackageUserException('EKI barrier level must be below strike level (%f)' % self.strike_rateForeignPerDomestic)
            elif self.barrierType == 'Down & In':
                if attrName == 'barrier_rateDomesticPerForeign' and value >= self.strike_rateDomesticPerForeign:
                    raise DealPackageUserException('EKI barrier level must be below strike level (%f)' % self.strike_rateDomesticPerForeign)
                if attrName == 'barrier_rateForeignPerDomestic' and value <= self.strike_rateForeignPerDomestic:
                    raise DealPackageUserException('EKI barrier level must be above strike level (%f)' % self.strike_rateForeignPerDomestic)
            elif self.barrierType == 'Double In':
                if attrName == 'barrier_rateDomesticPerForeign' and value >= self.strike_rateDomesticPerForeign:
                    raise DealPackageUserException('EKI barrier level must be below strike level (%f)' % self.strike_rateDomesticPerForeign)
                if attrName == 'barrier_rateForeignPerDomestic' and value <= self.strike_rateForeignPerDomestic:
                    raise DealPackageUserException('EKI barrier level must be above strike level (%f)' % self.strike_rateForeignPerDomestic)
                if attrName == 'barrier2_rateDomesticPerForeign' and value <= self.strike2_rateDomesticPerForeign:
                    raise DealPackageUserException('EKI barrier level must be above strike level (%f)' % self.strike2_rateDomesticPerForeign)
                if attrName == 'barrier2_rateForeignPerDomestic' and value >= self.strike2_rateForeignPerDomestic:
                    raise DealPackageUserException('EKI barrier level must be below strike level (%f)' % self.strike2_rateForeignPerDomestic)

    def ValidateBarrierIsNotZero(self, exceptionAccumulator):
        if self.hasEkiBarrier:
            if self.barrierApplicable and self.barrier_rateDomesticPerForeign < 1e-8:
                exceptionAccumulator('Barrier value cannot be 0')
            if self.barrier2Applicable and self.barrier2_rateDomesticPerForeign < 1e-8:
                exceptionAccumulator('Barrier value cannot be 0')

    #-----------------------------------------
    # Interface override
    #-----------------------------------------
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_SP_TrfDealPackage")
        
    def OnNew(self):

        # Non visible traits
        if self.InstrumentPackage().IsInfant():
            self.baseType = "Vanilla"
        super(TrfFxBaseDefinition, self).OnNew()
        # Make sure that quotation has not been changed
        # NOTE: Must be after GenerateTrfExpiryEvents for some reason...
        self.SetQuotationPerContract()

    def OnInit(self):

        self._foreignCurrencyChoices = DealPackageChoiceListSource()
        self._domesticCurrencyChoices = DealPackageChoiceListSource()

        super(TrfFxBaseDefinition, self).OnInit()

    def AssemblePackage(self):
        ins = acm.DealCapturing().CreateNewInstrument("FX Option")
        trade = acm.DealCapturing().CreateNewTrade(ins)
        self.DealPackage().AddTrade(trade, "Option")

    def Refresh(self):
        self.SetQuotationPerContract()

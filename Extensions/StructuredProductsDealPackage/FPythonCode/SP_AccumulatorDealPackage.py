
import acm
from SP_AccumulatorModel import AccumulatorInterface, FxAccumulatorInterface, ChoicesValuation, ChoicesAccumulatorType, ChoicesBarrierType, DefaultValueValuation, ChoicesAccumulationFrequency, RollingPeriodDefault, BusinessDayMethodDefault
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Action, InstrumentPart, DealPart, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, Settings, ValGroupChoices, AttributeDialog, Int, ReturnDomainDecorator, Float, CustomActions, TradeActions, CloseCommand, ParseSuffixedFloat, Str, Label, DealPackageChoiceListSource, Box
from SP_DealPackageHelper import FixingSourceChoices, GetFxFormatter
from StructuredProductBase import ComponentBasedDealPackage
from CompositeTradeComponents import TradeInput
from CompositeAddInfoDefinition import AddInfoDefinition

from SP_CustomTradeActions import AccumulatorExerciseAction

def ValuationProcessDefaultFromAddInfo():
    addinfo = acm.FAdditionalInfoSpec['ValuationProcess']
    if addinfo and addinfo.DefaultValue():
        return addinfo.DefaultValue()
    else:
        return 'LogNorm'


@Settings(MultiTradingEnabled=True)
class AccumulatorBase(ComponentBasedDealPackage):

    # Trade attributes
    tradeInput          = TradeInput ( priceLayout          = "PriceLayout" )
    
    tradePrice          = Object     ( objMapping     = "AccumulatorTrade.Price",
                                       width = 23,
                                       label          = 'Price')
    
    tradePremium        = Object     ( objMapping = "AccumulatorTrade.Premium",
                                       label      = 'Premium' )
    
    # Instrument attributes

    ipName              = Object ( objMapping   = InstrumentPart('InstrumentPackage.Name'),
                                   label        = 'Name' )

    accumulatorType     = Object ( objMapping   = InstrumentPart('AccumulatorInterface.AccumulatorType'),
                                   choiceListSource = ChoicesAccumulatorType(),
                                   label        = 'Type' )

    startDate           = Object ( objMapping   = InstrumentPart('AccumulatorInterface.StartDate'),
                                   transform    = '@TransformPeriodToDate',
                                   label        = 'Start Date',
                                   toolTip      = 'First observation date')
    
    expiry              = Object ( objMapping   = InstrumentPart('AccumulatorInterface.Expiry'),
                                   transform    = '@TransformPeriodToDateFromStartDate',
                                   label        = 'End Date')

    expiryTable         = Object ( objMapping   = InstrumentPart('AccumulatorInterface.ExpiryTable'),
                                   columns      = '@ColumnsExpiryTable',
                                   label        = 'Expiry Table',
                                   onSelectionChanged = '@UpdateSelectedPeriodEndDate' )
        
    expiryTableDetail   = Object ( objMapping   = InstrumentPart('AccumulatorInterface.ExpiryTableDetail'),
                                   columns      = '@ColumnsExpiryTableDetail',
                                   label        = 'Observation Dates',
                                   onSelectionChanged = '@UpdateFixingField',
                                   onDoubleClick = '@UpdatePriceFixing',
                                   dialog       = AttributeDialog( label='Update Fixing', 
                                                                   customPanes=[{"":'fixingValue;'}],
                                                                   btnLabel='Update') 
                                    )

    settlementType      = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.SettlementType'),
                                   choiceListSource = '@SettlementTypeChoices',
                                   label        = 'Settlement',
                                   visible      = '@IsShowModeDetail' )

    leverageFactor      = Object ( objMapping   = InstrumentPart('AccumulatorInterface.Leverage'),
                                   validate     = '@ValidatePositiveValue',
                                   label        = 'Leverage' )

    accumulationFreq    = Str (    label        = '@LabelAccumulationFrequency',
                                   defaultValue = 'Daily',
                                   choiceListSource = ChoicesAccumulationFrequency(),
                                   onChanged    = '@TouchPackage')
    
    barrierStatus       = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.Exotic.BarrierCrossedStatus'),
                                   label        = 'Barrier Status' )
    
    barrierCrossDate    = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.Exotic.BarrierCrossDate'),
                                   label        = 'Cross Date' )
    
    barrierMonitoring   = Object ( objMapping   = InstrumentPart('AccumulatorInterface.BarrierMonitoringType'),
                                   choiceListSource = ChoicesBarrierType(),
                                   label        = 'Monitoring',
                                   recreateCalcSpaceOnChange=True )
    
    priceFixings        = Object ( objMapping   = InstrumentPart('AccumulatorInterface.HistoricalFixings'))
    
    valuationMapping    = Object ( objMapping   = InstrumentPart('AccumulatorInterface.ValuationMapping'),
                                   label        = 'Valuation',
                                   choiceListSource = ChoicesValuation(),
                                   defaultValue = DefaultValueValuation(),
                                   visible      = '@IsShowModeDetail' )
    
    generateExpirytable = Action ( label        = 'Generate Expiry Table',
                                   action       = '@GenerateExpiryTable',
                                   sizeToFit    = True)

    calendar            = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.SettlementCalendar'),
                                   label        = 'Calendar',
                                   visible      = '@IsShowModeDetail' )
    
    businessDayMethod   = Object ( objMapping   = InstrumentPart('AccumulatorInterface.PayDayMethod'),
                                   label        = 'Day Method',
                                   toolTip      = 'Method for adjustment of period end dates',
                                   defaultValue = BusinessDayMethodDefault(),
                                   visible      = '@IsShowModeDetail' )
    
    rollingPeriod       = Object ( objMapping   = InstrumentPart('AccumulatorInterface.RollingPeriod'),
                                   label        = 'Rolling Period',
                                   toolTip      = 'The length of each accumulation period',
                                   defaultValue = RollingPeriodDefault() )
    
    settleDays          = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.PayDayOffset'),
                                   label        = 'Settle Days',
                                   validate     = '@ValidatePositiveValue',
                                   visible      = '@IsShowModeDetail',
                                   toolTip      = 'Number of banking days between each period end date and the corresponding settlment date' )
    
    spotDays            = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.SpotBankingDaysOffset'),
                                   validate     = '@ValidatePositiveValue',
                                   label        = 'Spot Days',
                                   visible      = '@IsShowModeDetail' )

    fixingValue         = Float  ( label        = 'Fixing',
                                   validate     = '@ValidateFixingValue' )
                                  
    insAddInfo          = AddInfoDefinition( obj='AccumulatorAddInfoInstrument' )

    tradeAddInfo        = AddInfoDefinition( obj='LeadTrade' )
    
    selectedEndDate     = Object ( domain = 'date' )

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            { 'tradeInput_status'         : dict(defaultValue = 'Simulated' ),
              'tradeInput_quantity_value' : dict(defaultValue = 1.0 ) } )

    def AccumulatorInterface(self):
        return self._accumulatorInterface

    def AccumulatorInstruments(self):
        return self._accumulatorInterface.Accumulator()

    def AccumulatorAddInfoInstrument(self):
        return self._accumulatorInterface.AccumulatorForAddInfo()

    def AccumulatorTrade(self):
        return self._accumulatorInterface.AccumulatorTrade()

    def LeadTrade(self):
        return self._accumulatorInterface.LeadTrade()
    
    def AssemblePackage(self):
        self._accumulatorInterface.CreateAccumulator()
        self.DealPackage().AddTrade(self._accumulatorInterface.AccumulatorTrade(), 'Accumulator')

    def AsPortfolio(self, *rest):
        return self.DealPackage().AsPortfolio()

    def PriceLayout(self):
        return """
                hbox(;
                    vbox{;
                        tradePrice;
                        };
                    vbox{;
                        tradePremium;
                        };
                    );
                """

    def OnOpen(self):
        self.accumulationFreq = self.AccumulatorInterface().CheckAccumulationFrequency()

    def OnSave(self, saveConfig):
        if self.DealPackage().IsInfant():
            if not self.AccumulatorInterface().HasExpiryTable():
                self.GenerateExpiryTable(None)
        super(AccumulatorBase, self).OnSave(saveConfig)

    def TouchPackage(self, *rest):
        self.DealPackage().Touch()
        self.DealPackage().Changed()

    def LabelAccumulationFrequency(self, *rest):
        if self.accumulatorType == 'Accumulator':
            return 'Accumulation'
        return 'Decumulation'

    def UpdateFixingField(self, attrName, row, *rest):
        if row:
            self.fixingValue = row.ObservationFixing()
        else:
            self.fixingValue = 0.0

    def UpdateSelectedPeriodEndDate(self, attrName, row, *rest):
        if row:
            self.selectedEndDate = row.Date()
        else:
            self.selectedEndDate = None

    def ValidatePositiveValue(self, attrName, newValue, *rest):
        if newValue <= 0:
            raise DealPackageUserException ('%s must be a number greater than 0.' % (self.GetAttributeMetaData(attrName, 'label')()) )

    def ValidateFixingValue(self, attrname, newValue, *rest):
        if newValue < 0.0 and newValue != -1.0:
            raise DealPackageUserException('Invalid fixing value')

    def SettlementTypeChoices(self, *rest):
        return self.AccumulatorInterface().SettlementTypeChoices()

    def UpdatePriceFixing(self, attrName, doubleClickedItem, dialogReturnValue):
        if dialogReturnValue:
            doubleClickedItem.ObservationFixing(self.fixingValue)

    def GetAccumulationFrequency(self):
        # Other accumulation fequencies than Daily ha only been tested for FX ACcumulators.
        return 'Daily'

    def ColumnsExpiryTableDetail(self, attrName, *rest):
        return [{'methodChain' : 'ExpiryDate',        'label' : 'Obervation Date'},
                {'methodChain' : 'NoticeDate',        'label' : 'Valuation Date'},
                {'methodChain' : 'SettlementDate',    'label' : 'Settlement Date'},
                {'methodChain' : 'ObservationFixing', 'label' : 'Fixing'},
                {'methodChain' : 'AccumulatedAmount', 'label' : 'Accumulation'}]

    def ColumnsExpiryTable(self, attrName, *rest):
        return [{'methodChain' : 'AccumulatorPeriodStartDate', 'label' : 'Period Start'},
                {'methodChain' : 'Date',                       'label' : 'Period End'},
                {'methodChain' : 'SettlementDate',             'label' : 'Settlement'},
                {'methodChain' : 'AccumulatedInPeriod',        'label' : 'Period Accumulation'},
                {'methodChain' : 'AccumulatedTotal',           'label' : 'Total Accumulation'}]
    
    def TransformPeriodToDate(self, name, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = self.AccumulatorInterface().DateFromPeriod(newDate)
        return date
    
    def TransformPeriodToDateFromStartDate(self, name, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = self.AccumulatorInterface().DateFromPeriodAndStartDate(newDate, self.startDate, 
                                                                          self.AccumulatorInterface().GetExpiryCalendars())
        return date

    @classmethod
    def SetUp(cls, definitionSetUp):
        import SP_AccumulatorSetup
        SP_AccumulatorSetup.Setup(definitionSetUp)

    
@TradeActions(exercise = AccumulatorExerciseAction(),
              close    = CloseCommand(nominal = 'tradeInput_quantity_value',
                                      statusAttr  = 'tradeInput_status',
                                      newStatus   = 'FO Confirmed' ) )
class Accumulator(AccumulatorBase):


    # Update Deal Part reference once the trades are also handled via the accumulator interface
    currency            = Object ( objMapping   = InstrumentPart('AccumulatorInterface.InstrumentCurrencyObjects.Currency').
                                                  DealPart('Trades.Currency'),
                                   domain       = 'FCurrency',
                                   label        = 'Currency')

    underlying          = Object ( objMapping   = InstrumentPart('AccumulatorInterface.Underlying'),
                                   onChanged    = '@SetCurrencyEqualUnderlyingCurrency|SetStrikeBasedOnUnderlyingPrice|SetBarrierBasedOnUnderlyingPrice',
                                   label        = 'Underlying',
                                   validate     = '@ValidateUnderlying' )
    
    strike              = Object ( objMapping      = InstrumentPart('AccumulatorInterface.StrikePrice'),
                                   validate        = '@ValidatePositiveValue',
                                   label           = 'Initial Strike',
                                   solverParameter = '@SolverParametersStrike',
                                   backgroundColor = '@SolverColor',
                                   transform       = '@TransformStrike' )

    valuationProcess    = Object ( objMapping   = InstrumentPart('AccumulatorInstruments.AdditionalInfo.ValuationProcess'),
                                   label        = 'Valuation Process',
                                   defaultValue = ValuationProcessDefaultFromAddInfo(),
                                   visible      = '@IsShowModeDetail' )

    currentStrike       = CalcVal( calcMapping  = 'AccumulatorInstruments:FDealSheet:AccDec Current Strike',
                                   label        = 'Current Strike',
                                   enabled      = False )
    
    dailyAccumulation   = Object ( objMapping   = InstrumentPart('AccumulatorInterface.DailyAccumulation'),
                                   validate     = '@ValidatePositiveValue',
                                   label        = 'Daily Accumulation' )
    
    barrierLevel        = Object ( objMapping      = InstrumentPart('AccumulatorInstruments.Barrier'),
                                   validate        = '@ValidatePositiveValue',
                                   label           = 'Initial Barrier' )

    currentBarrier      = CalcVal( calcMapping  = 'AccumulatorInstruments:FDealSheet:AccDec Current Barrier',
                                   label        = 'Current Barrier',
                                   enabled      = False )

    exercise            = Action ( action       = '@Exercise')
    


    # Calc values that can be solved for
    theorValue          = CalcVal ( calcMapping = 'AsPortfolio:FPortfolioSheet:Portfolio Theoretical Value No Trade Payments',
                                    label = '',
                                    solverTopValue = True)

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'expiry':      dict(validate = "@ValidateEndDate"),
            'startDate':   dict(validate = "@ValidateStartDate")})

    # #########################
    # Methods needed for solver

    def TransformStrike(self, attrName, value):
        goalValue = None
        f = self.GetFormatter('theorValue')
        # First check if we are solving for theoretical value
        goalValue = ParseSuffixedFloat(value, suffix=['pv', 'theorval', 'val'], formatter=f)

        if goalValue is None:
            # if solving for price still use theor value as there os no theor price for package level.
            # We always use quotation Per Contract so there is always a linear 
            # relationship between theor price and theor val
            theorGoalValue = ParseSuffixedFloat(value, suffix=['p', 'theor', 'price'], formatter=f)
            if theorGoalValue is not None:
                goalValue = theorGoalValue * self.tradeInput_quantity_value

        if goalValue is not None:
            return self.Solve('theorValue', attrName, goalValue)
        else:
            return value

    def SolverParametersStrike(self, *rest):
        return [{'minValue':0.01,'maxValue':1e10,'precision':1}]
    
    # End methods needed for solver
    # #########################

    def GraphYValues(self, xValues):
        yValues = []
        if xValues:
            accDecFactor = 1 if self.accumulatorType == 'Accumulator' else -1
            strike = self.currentStrike.Value()
            barrier = self.currentBarrier.Value()
            size = self.dailyAccumulation * self.tradeInput_quantity_value
            
            for x in xValues:
                if (x - barrier) * accDecFactor >= 0:
                    yValues.append(0)
                    continue
                
                iv = (x - strike) * accDecFactor
                leverage = self.leverageFactor if iv < 0 else 1.0
                yValues.append(iv * leverage * size)
                
        return yValues
        
    def GraphXValues(self):
        try:
            strike = self.currentStrike.Value()
            barrier = self.currentBarrier.Value()
            tailSize = max(abs(strike - barrier), 0.2 * strike)
            if barrier > strike:
                return [ max(strike - tailSize, 0),
                         strike,
                         barrier - 0.1,
                         barrier,
                         barrier + tailSize]
            elif barrier == strike:
                return [ max(strike - tailSize, 0),
                         strike,
                         strike + tailSize]
            else:
                return [ max(0, barrier - tailSize),
                         barrier,
                         barrier + 0.1,
                         strike,
                         strike + tailSize]
        except:
            return []
    
    def Exercise(self, attrName, *rest):

        date = rest[0] if len(rest) > 0 else acm.Time().DateToday()
        exerciseTrades = []
        closingDP = None

        if not self.AccumulatorInterface().IsExercised(date):
            exerciseTrades = self.AccumulatorInterface().Exercise(date)
        else:
            acm.Log ('Accumulator %i has already been exercised for %s'
                 % (self.DealPackage().Originator().Oid(), str(date)) )


        if not self.AccumulatorInterface().IsClosed():
            closingDP = self.AccumulatorInterface().Close(self.DealPackage(), date)
        else:
            acm.Log ('Accumulator %i has already been closed'
                 % (self.DealPackage().Originator().Oid()) )

        return exerciseTrades, closingDP

    def GenerateExpiryTable(self, attrName):
        try:
            self.AccumulatorInterface().GenerateExpiryTable(
                {'startDate' : self.startDate,
                 'endDate' : self.expiry,
                 'calendars' : self.AccumulatorInterface().GetExpiryCalendars(),
                 'method' : self.businessDayMethod,
                 'rolling' : self.rollingPeriod,
                 'settleDays' : self.settleDays,
                 'settleCalendars' : self.AccumulatorInterface().GetSettlementCalendars(),
                 'frequency' : self.GetAccumulationFrequency()} )
        except DealPackageUserException as e:
            msg = "Failed on generation of expiry table: %s"
            raise DealPackageUserException(msg%str(e))

    def ValidateUnderlying(self, attrName, newValue, *rest):
        if newValue is None:
            raise DealPackageUserException ( "No underlying selected" )

    def ValidateStartDateBeforeEndDate(self, startDate, endDate, msg):
        if acm.Time().DateDifference(startDate, endDate) >= 0:
            raise DealPackageUserException (msg)
    
    def ValidateStartDate(self, attrName, newValue, *rest):
        self.ValidateStartDateBeforeEndDate(newValue, self.expiry, 'Start Date must be before End Date')
    
    def ValidateEndDate(self, attrName, newValue, *rest):
        self.ValidateStartDateBeforeEndDate(self.startDate, newValue, 'End Date must be after Start Date')
    
    def SetCurrencyEqualUnderlyingCurrency(self, attrName, *rest):
        self.currency = self.underlying.Currency()
    
    def SetStrikeBasedOnUnderlyingPrice(self, attrName, *rest):
        price = self.underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value()
        if (price and price.Number() > 0.0):
            self.strike = price.Number()

    def SetBarrierBasedOnUnderlyingPrice(self, attrName, *rest):
        price = self.underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value()
        if (price and price.Number() > 0.0):
            self.barrierLevel = price.Number()
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_Accumulator')

    def OnInit(self):
        self.selectedEndDate = None

        self._accumulatorInterface = AccumulatorInterface()
        
        if self.Instruments():
            self.AccumulatorInterface().SetAccumulator(self.Instruments(), self.Trades())

    def IsValid(self, exceptionAccumulator, aspect):
        # If we enter from FValidation, OnInit has been run with the persisted
        # instruments / trades so we need to create a new instance of the
        # accumulator interface.

        validationInterface = AccumulatorInterface()
        validParts = validationInterface.SetAccumulator(self.Instruments(), self.Trades(), exceptionAccumulator)

        if validParts:
            validationInterface.IsValid(exceptionAccumulator, aspect)


        
class FxAccumulator(AccumulatorBase):

    foreignPerDomesticVBox = Box( vertical=True,
                                  label='@LabelCurrBox')

    domesticPerForeignVBox = Box( vertical=True,
                                  label='@LabelCurrBox')

    # Trade attributes
    
    tradeCurrency       = Object     ( objMapping = "AccumulatorTrade.FxoPremiumCurr",
                                       label      = "Premium Curr",
                                       enabled    = "@OnlyOneDealPackageExists",
                                       onChanged  = '@SetTradeCurrency',
                                       choiceListSource = "@PremiumCurrencyCurrencies" )

    # Instrument attributes

    # Update Deal Part reference once the trades are also handled via the accumulator interface
    foreignCurrency     = Object ( objMapping      = InstrumentPart('AccumulatorInterface.ForeignCurrency'),
                                   onChanged       = '@SetStrikeBasedOnCurrencyPair|SetBarrierBasedOnCurrencyPair|UpdatePremiumCurrencyChoices',
                                   label           = 'Foreign')

    domesticCurrency    = Object ( objMapping      = InstrumentPart('AccumulatorInstruments.DomesticCurrency'),
                                   onChanged       = '@SetStrikeBasedOnCurrencyPair|SetBarrierBasedOnCurrencyPair|UpdatePremiumCurrencyChoices',
                                   label           = 'Domestic' )

    fixingSource        = Object ( objMapping      = InstrumentPart('AccumulatorInstruments.FixingSource'),
                                   label           = 'Fixing',
                                   choiceListSource= FixingSourceChoices() )

    expiryTableDetail   = Object ( objMapping      = InstrumentPart('AccumulatorInterface.ExpiryTableDetail'),
                                   columns         = '@ColumnsExpiryTableDetail',
                                   label           = 'Observation Dates',
                                   onSelectionChanged = '@UpdateFixingField',
                                   onDoubleClick   = '@UpdatePriceFixing',
                                   dialog          = AttributeDialog( label='Update Fixing', 
                                                                customPanes=[{"Fixing":'unfixValue;fixingValue;fixingValueInverse'}],
                                                                btnLabel='Update')
                                    )

    delivery            = Object ( objMapping      = InstrumentPart('AccumulatorInterface.Delivery'),
                                   label           = 'Final Settlement',
                                   editable        = False )

    nbrOfPeriods        = Object ( objMapping      = InstrumentPart('AccumulatorInterface.NumberOfPeriods'),
                                   label           = "Number of periods",
                                   validate        = "@ValidatePositiveValue")

    fixingValueInverse  = Float  ( label           = '@LabelFixingInverse',
                                   formatter       = '@FXRateInverseFormatter',
                                   onChanged       = '@UpdateFixingFromInverse',
                                   validate        = '@ValidateFixingValue' )

    fixingValue         = Float  ( label           = '@LabelFixing',
                                   formatter       = '@FXRateFormatter',
                                   onChanged       = '@UpdateFixingInverseFromFixing',
                                   validate        = '@ValidateFixingValue' )

    unfixValue          = Action ( label           = 'Unfix',
                                   visible         = '@IsShowModeDetail',
                                   action          = '@UnfixFixing')

    strikeDomPerFor     = Object ( objMapping      = InstrumentPart('AccumulatorInterface.StrikeDomesticPerForeign'),
                                   validate        = '@ValidatePositiveValue',
                                   formatter       = '@FXRateInverseFormatter',
                                   label           = 'Strike')

    strikeForPerDom     = Object ( objMapping      = InstrumentPart('AccumulatorInterface.StrikeForeignPerDomestic'),
                                   formatter       = '@FXRateFormatter',
                                   label           = 'Strike')
        
    notional            = Object ( objMapping      = InstrumentPart('AccumulatorInterface.Notional'),
                                   validate        = '@ValidatePositiveValue',
                                   label           = '@LabelNotional' )
    
    barrierDomPerFor    = Object ( objMapping      = InstrumentPart('AccumulatorInstruments.Exotic.BarrierDomesticPerForeign'),
                                   validate        = '@ValidatePositiveValue',
                                   formatter       = '@FXRateInverseFormatter',
                                   recreateCalcSpaceOnChange = True,
                                   label           = 'Barrier' )

    barrierForPerDom    = Object ( objMapping      = InstrumentPart('AccumulatorInstruments.Exotic.BarrierForeignPerDomestic'),
                                   validate        = '@ValidatePositiveValue',
                                   formatter       = '@FXRateFormatter',
                                   label           = 'Barrier' )
    
    quotation           = Object ( objMapping      = InstrumentPart('AccumulatorInterface.Quotation'),
                                   onChanged       = 'QuotationChanged')

    # Calc values that can be solved for
    theorValue          = CalcVal ( calcMapping    = 'AsPortfolio:FPortfolioSheet:Portfolio Theoretical Value No Trade Payments',
                                    label          = '')

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'expiry':      dict(editable = False,
                                label    = 'Final Fixing')})
        
    def OnlyOneDealPackageExists(self, *rest):
        return self.InstrumentPackage().Originator().DealPackages().Size() == 1
    
    def UpdatePremiumCurrencyChoices(self, *rest):
        self._premiumCurrChoices.Clear()
        if self.domesticCurrency:
            self._premiumCurrChoices.Add(self.domesticCurrency)
        if self.foreignCurrency:
            self._premiumCurrChoices.Add(self.foreignCurrency)
    
    def PremiumCurrencyCurrencies(self, *rest):
        if self._premiumCurrChoices.IsEmpty():
            self.UpdatePremiumCurrencyChoices()
        return  self._premiumCurrChoices

    def SetTradeCurrency(self, *rest):
        # Reason for onChanged mapping on trade currency instead of
        # double object mapping is that the trade decorator will upadte 
        # FxoPremiumCurr but not Trade Currency when Domestic Currency
        # is updated causing a mismatch in the object mapping.
        if self.tradeCurrency is not None:
            self.AccumulatorTrade().Currency(self.tradeCurrency)

    def GenerateExpiryTable(self, attrName):
        try:
            self.AccumulatorInterface().GenerateExpiryTable(
                {'startDate' : self.startDate,
                 'method' : self.businessDayMethod,
                 'rolling' : self.rollingPeriod,
                 'calendars' : self.AccumulatorInterface().GetExpiryCalendars(),
                 'settleCalendar' : self.calendar,
                 'settleDays': self.settleDays,
                 'foreignCurrency':self.foreignCurrency,
                 'domesticCurrency':self.domesticCurrency,
                 'nbrOfPeriods' : self.nbrOfPeriods,
                 'frequency' : self.GetAccumulationFrequency()} )
        except DealPackageUserException as e:
            msg = "Failed on generation of expiry table: %s"
            raise DealPackageUserException(msg%str(e))

    # New Methods
    def SetStrikeBasedOnCurrencyPair(self, attrName, *rest):
        if self.domesticCurrency and self.foreignCurrency:
            price = self.foreignCurrency.Calculation().FXRate(self._GetStdCalcSpace(), self.domesticCurrency).Value()
            if (price and price.Number() > 0.0):
                self.strikeDomPerFor = price.Number()

    def SetBarrierBasedOnCurrencyPair(self, attrName, *rest):
        if self.domesticCurrency and self.foreignCurrency:
            price = self.foreignCurrency.Calculation().FXRate(self._GetStdCalcSpace(), self.domesticCurrency).Value()
            if (price and price.Number() > 0.0):
                self.barrierDomPerFor = price.Number()

    def InverseFxRateFixing(self, value):
        if value <= 0.0:
            return value
        return 1.0 / value

    def UpdateFixingFromInverse(self, *rest):
        inverse = self.InverseFxRateFixing(self.fixingValueInverse)
        if abs(self.fixingValue - inverse) > 1e-6:
            self.fixingValue = inverse
    
    def UpdateFixingInverseFromFixing(self, *rest):
        inverse = self.InverseFxRateFixing(self.fixingValue)
        if abs(self.fixingValueInverse - inverse) > 1e-6:
            self.fixingValueInverse = inverse
            
    def QuotationChanged(self, attributeName, oldValue, newValue, *args):
        if newValue != 'Per Contract':
            self.AccumulatorInterface().Quotation('Per Contract')

    def LabelNotional(self, *rest):
        return 'Notional%s' % ((' (%s)' % self.foreignCurrency.Name()) if self.foreignCurrency is not None else '')
    
    def LabelFixingInverse(self, *rest):
        return "%s per %s" % (self.foreignCurrency.Name(), self.domesticCurrency.Name())
    
    def LabelFixing(self, *rest):
        return "%s per %s" % (self.domesticCurrency.Name(), self.foreignCurrency.Name())

    def LabelCurrBox(self, traitName):
        foreign  = self.foreignCurrency.Name() if self.foreignCurrency else 'Foreign'
        domestic = self.domesticCurrency.Name() if self.domesticCurrency else 'Domestic'
        if traitName.startswith('foreign'):
            label = "%s per %s" % (foreign, domestic)
        else:
            label = "%s per %s" % (domestic, foreign)
        return label

    def ColumnsExpiryTableDetail(self, attrName, *rest):
        return [{'methodChain' : 'ExpiryDate',        'label' : 'Obervation Date'},
                {'methodChain' : 'NoticeDate',        'label' : 'Valuation Date'},
                {'methodChain' : 'SettlementDate',    'label' : 'Settlement Date'},
                {'methodChain' : 'ObservationFixingDomesticPerForeign', 'label' : 'Fixing'},
                {'methodChain' : 'ObservationFixingForeignPerDomestic', 'label' : 'Fixing Inverse'},
                {'methodChain' : 'AccumulatedAmount', 'label' : 'Accumulation'}]

    def GraphYValues(self, xValues):
        yValues = []
        if xValues:
            accDecFactor = 1 if self.accumulatorType == 'Accumulator' else -1
            strike = self.strikeDomPerFor
            barrier = self.barrierDomPerFor
            size = self.notional * self.tradeInput_quantity_value
            for x in xValues:
                if (x - barrier) * accDecFactor >= 0:
                    yValues.append(0)
                    continue

                iv = (x - strike) * accDecFactor
                leverage = self.leverageFactor if iv < 0 else 1.0
                yValues.append(iv * leverage * size)

        return yValues
        
    def GraphXValues(self):
        try:
            strike = self.strikeDomPerFor
            barrier = self.barrierDomPerFor
            increment = 0.0001 * strike
            tailSize = max(abs(strike - barrier), 0.2 * strike)
            if barrier > strike:
                return [ strike - tailSize,
                         strike,
                         barrier - increment,
                         barrier,
                         barrier + tailSize]
            elif barrier == strike:
                return [ strike - tailSize,
                         strike,
                         strike + tailSize]
            else:
                return [ barrier - tailSize,
                         barrier,
                         barrier + increment,
                         strike,
                         strike + tailSize]
        except:
            return []

    def PriceLayout(self):
        return """
                hbox(;
                    vbox{;
                        tradePrice;
                        };
                    vbox{;
                        tradePremium;
                        tradeCurrency;
                        };
                    );
                """

    def OnInit(self):
        self.selectedEndDate = None
        self._premiumCurrChoices = DealPackageChoiceListSource()

        self._accumulatorInterface = FxAccumulatorInterface()
        
        if self.Instruments():
            self.AccumulatorInterface().SetAccumulator(self.Instruments(), self.Trades())

    def OnCopy(self, originalPackage, aspect):
        self.nbrOfPeriods = originalPackage.GetAttribute('nbrOfPeriods')

    def IsValid(self, exceptionAccumulator, aspect):
        # If we enter from FValidation, OnInit has been run with the persisted
        # instruments / trades so we need to create a new instance of the
        # accumulator interface.

        validationInterface = FxAccumulatorInterface()
        validParts = validationInterface.SetAccumulator(self.Instruments(), self.Trades(), exceptionAccumulator)

        if validParts:
            validationInterface.IsValid(exceptionAccumulator, aspect)

        # Validation below is independent of instrument and trade modelling
        dpOrig = self.DealPackage().Originator()
        allDpOrig = self.InstrumentPackage().Originator().DealPackages()
        
        if not self.DealPackage().IsStorageImage() and allDpOrig and dpOrig not in allDpOrig:
            # We are doing a save new of only the deal package
            if allDpOrig.At(0).Edit().GetAttribute('tradeCurrency') != self.tradeCurrency:
                exceptionAccumulator('Cannot change trade currency if another deal already exists')        

    def GetAccumulationFrequency(self):
        return self.accumulationFreq

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_FxAccumulator')

    def UnfixFixing(self, *args):
        self.fixingValue = -1

    def FXRateInverseFormatter(self, *args):
        return GetFxFormatter(self.foreignCurrency, self.domesticCurrency)
        
    def FXRateFormatter(self, *args):
        return GetFxFormatter(self.domesticCurrency, self.foreignCurrency)

    
def StartAccumulator(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Accumulator')
    return  


def StartFxAccumulator(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'FX Accumulator')
    return  

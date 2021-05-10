
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, ParseSuffixedFloat, Settings, ReturnDomainDecorator

from StructuredProductBase import ComponentBasedDealPackage
from CompositeTradeComponents import TradeInput
from CompositeBasketOptionComponents import BasketAsianOption, BasketOption
from CompositeCashFlowComponents import ZeroBond
from SP_DealPackageHelper import MergeDictionaries, AddHalfPeriod, SuggestInstrumentName, FirstDate, LastDate


def RollingPeriodDefaultFromAddInfo():
    addinfo = acm.FAdditionalInfoSpec['sp_RollingPeriod']
    if addinfo and addinfo.DefaultValue():
        return addinfo.DefaultValue()
    else:
        return '1Y'

# Default values that will be shared by a number of attribtues
defaultValueContractSize = 1000
defaultValueStrike = 1000
defaultValueProtection = 0.7

@Settings(GraphApplicable=False,
          MultiTradingEnabled=True)
class CapitalProtectedCertificate(ComponentBasedDealPackage):

    ipName            = Object( objMapping     = InstrumentPart('InstrumentPackage.Name'),
                                label          = 'Name',
                                onChanged      = '@SetInstrumentName') 
    
    upsideOption      = BasketAsianOption ( optionName          = 'UpsideOption',
                                            basketName          = 'Underlying',
                                            basketUpdateAction  = 'BasketUpdateAction',
                                            totalBasketValue    = 'zero_contractSize',
                                            eventTypes          = ['Average price'],
                                            eventLabel          = 'Average Price Dates',
                                            showEventsAsButton  = False,
                                            eventColumns        = [{'methodChain' : 'Date',                            'label' : 'Date'},
                                                                   {'methodChain' : 'ComponentInstrument.VerboseName', 'label' : 'Underlying'},
                                                                   {'methodChain' : 'EventValue',                      'label' : 'Price Fixing'}
                                                                   ],
                                            eventUpdateAction   = 'EventUpdateAction' )
            
    downsideOption      = BasketOption (    optionName          = 'DownsideOption',
                                            basketName          = 'Underlying',
                                            basketUpdateAction  = 'BasketUpdateAction' )

    stopLossOption      = BasketOption (    optionName          = 'StopLossOption',
                                            basketName          = 'Underlying',
                                            basketUpdateAction  = 'BasketUpdateAction' )

    zero                = ZeroBond (        zeroName            = 'Zero',
                                            zeroLegName         = 'ZeroLeg' )

    asianRolling        = Object ( objMapping      = InstrumentPart('RollingPeriod'),
                                   label           = 'Average Rolling',
                                   defaultValue    = RollingPeriodDefaultFromAddInfo(),
                                   onChanged       = '@SetAverageDates' )

    asianStartDate      = Date   ( objMapping      = InstrumentPart('AsianStartDate'),
                                   label           = 'Average Start Date',
                                   transform       = '@TransformAsianStartDate' )

    privateAsianStartDate = Date ( onChanged       = '@SetAverageDates' )

    currency            = Object ( objMapping      = InstrumentPart('Combination.Currency|UpsideOption.Currency|UpsideOption.StrikeCurrency|DownsideOption.Currency|DownsideOption.StrikeCurrency|StopLossOption.Currency|StopLossOption.StrikeCurrency|Underlying.Currency|Zero.Currency|ZeroLeg.Currency').DealPart('CombinationTrade.Currency'),
                                   onChanged       = '@UpdateQuantoType',
                                   label           = 'Currency' )
        
    protection          = Object ( objMapping      = InstrumentPart('Protection'),
                                   label           = 'Protection (%)',
                                   backgroundColor = '@SolverColor',
                                   transform       = '@TransformSolver',
                                   solverParameter = '@ProtectionSolverParameters',
                                   formatter       = 'PercentShowZero',
                                   onChanged       =  '@ValidateProtectionChange')

    quotation           = Object ( objMapping      = InstrumentPart('Combination.Quotation'),
                                   defaultValue    = 'Per Unit',
                                   label           = 'Quotation' )

    contractSize        = Object ( objMapping      = InstrumentPart('Combination.ContractSize') )

    # Combination fields
    participation       = Object ( objMapping      = InstrumentPart('UpsideOptionCombinationMap.Weight'),
                                   label           = 'Participation (%)',
                                   backgroundColor = '@SolverColor',
                                   transform       = '@TransformSolver',
                                   solverParameter = '@ParticipationSolverParameters',
                                   formatter       = 'PercentShowZero' )

    tradeInput          = TradeInput( priceLayout = 'PriceLayout')

    combinationPrice    = Object  ( objMapping = "CombinationTrade.Price",
                                    label = 'Price',
                                    width = 22)
    
    combinationPremium  = Object  ( objMapping = "CombinationTrade.Premium",
                                    label = 'Premium' )
    
    pv          = CalcVal ( calcMapping = 'CombinationTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                            solverTopValue = True )

    # Solver functionality

    def ProtectionSolverParameters(self, attrName):
        return {'minValue':0.000, 'maxValue':1.0}
    
    def ParticipationSolverParameters(self, attrName):
        return {'minValue':0.0, 'maxValue':10.0}

    def TransformSolver(self, attrName, value, *rest):
        return self.upsideOption.TransformSolver(attrName, value)

    def TopValueFields(self):
        return {'PV':'pv'}

    def PriceLayout(self):
        return """
                hbox(;
                    vbox{;
                        combinationPrice;
                        };
                    vbox{;
                        combinationPremium;
                        };
                    );
                """

    def TransformAsianStartDate(self, attrName, value):
        value = self._PeriodToDateTransform(value)
        value = self._ValidateDate(value, 'Start')
        return value

    # On changed
    def SetAverageDates(self, attrName, *rest):
        self.upsideOption.asian.averageDates.GenerateExoticEvents(
                                'Average price',
                                FirstDate( self.privateAsianStartDate,
                                           self.upsideOption_expiry ),
                                self.upsideOption_expiry,
                                self.asianRolling,
                                AddHalfPeriod( self.privateAsianStartDate, 
                                               self.asianRolling),
                                includeStartDate = True,
                                regenerate = True,
                                generatePerUnderlying = True )

    def UpdateQuantoType(self, attrName, *rest):
        for combLink in self.upsideOption_underlying_instruments:
            if combLink.Instrument().Currency() != self.currency:
                self.upsideOption_quantoType = 'Quanto'
                return
        self.upsideOption_quantoType = 'None'
    
    def ValidateProtectionChange(self, attrName, old, new, changedAttribute):
        if changedAttribute == "downsideOption_strikePrice" :
            self.SetAttribute(attrName, old)

    def SetOptionContractSize(self, attrName, *rest):
        if self.upsideOption_strikePrice:
            self.upsideOption_contractSize = self.zero_contractSize / self.upsideOption_strikePrice
        else:
            self.upsideOption_contractSize = self.zero_contractSize

    def SetCombinationContractSize(self, attrName, *rest):
        self.contractSize = self.zero_contractSize
    
    def SetUpsideStrike(self, attrName, *rest):
        gui = self.DealPackage().GUI()
        enabled = self.GetAttributeMetaData('upsideOption_underlying_updateWeights', 'enabled')()
        if gui and enabled and gui.GenericYesNoQuestion("Do you wan't to rebalance your basket?"):
            self.upsideOption_underlying_updateWeights()
        self.upsideOption_strikePrice = self.zero_contractSize

    def SetZeroEndDate(self, *rest):
        baseForEnd = LastDate(self.upsideOption_expiry, self.zero_startDate)
        self.zero_endDate = self.UpsideOption().SpotDate(baseForEnd)
    
    def EventUpdateAction(self, *rest):
        pass
        
    def BasketUpdateAction(self, attrName, actionInstruments = None):
        if attrName in ('upsideOption_underlying_addInstrument', 'upsideOption_underlying_removeInstrument'):
            self.UpdateQuantoType(attrName)
            self.SetAverageDates(attrName)

    def SetInstrumentName(self, *rest):
        suggestName = SuggestInstrumentName(self.ipName)
        self.Combination().Name(suggestName)
        
    def OnSave(self, saveConfig):
        super(CapitalProtectedCertificate, self).OnSave(saveConfig)
        self.SetInstrumentName()

    # Object mappings

    @ReturnDomainDecorator('date')
    def AsianStartDate(self, value = '*READING*'):
        if value == '*READING*':
            return self.privateAsianStartDate
        else:
            self.privateAsianStartDate = value


    @ReturnDomainDecorator('double')
    def Protection(self, value = '*READING*'):
        if value == '*READING*':
            if self.stopLossOption_strikePrice and self.downsideOption_strikePrice:
                return self.stopLossOption_strikePrice / self.downsideOption_strikePrice
            else:
                return 1.0
        else:
            self.stopLossOption_strikePrice = self.downsideOption_strikePrice * value

    @ReturnDomainDecorator('dateperiod')
    def RollingPeriod(self, value = '*READING*'):
        mappedMethod = self.UpsideOption().AdditionalInfo().Sp_RollingPeriod
        if value == '*READING*':
            return mappedMethod()
        else:
            mappedMethod(value)
    
    # Dev kit overrides
    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Combination', 'Combination')
        self.DealPackage().AddCombinationMap(self.upsideOption.CreateInstrument(), 1.0, 'UpsideOption', 'Combination')
        self.DealPackage().AddCombinationMap(self.downsideOption.CreateInstrument(existingBasket = self.UpsideOption().Underlying()), 
                                             -1.0, 'DownsideOption', 'Combination')
        self.DealPackage().AddCombinationMap(self.stopLossOption.CreateInstrument(existingBasket = self.UpsideOption().Underlying()), 
                                             1.0, 'StopLossOption', 'Combination')
        self.DealPackage().AddCombinationMap(self.zero.CreateInstrument(), 1.0, 'Zero', 'Combination')

        self.UpsideOption().Quotation('Per Contract')
        self.DownsideOption().Quotation('Per Contract')
        self.StopLossOption().Quotation('Per Contract')

        self.UpsideOption().StrikeType('Absolute')
        self.DownsideOption().StrikeType('Absolute')
        self.StopLossOption().StrikeType('Absolute')
        
        self.Combination().ContractSize(1.0)
        
    def IsValid(self, exceptionAccumulator, aspect):
        # protection < 100
        # expiry before or equal end date
        pass

    def AttributeOverrides(self, overrideAccumulator):
    
        attrs = {}
        
        attrs['upsideOption'] = {
                    'expiry'         : dict ( onChanged = '@SetAverageDates|SetZeroEndDate'),
                    'strikePrice'    : dict ( solverParameter = None,
                                              onChanged = '@SetOptionContractSize',
                                              label = 'Initial Fixing' ),
                    'settlementType' : dict ( visible = '@IsShowModeDetail',
                                              defaultValue = 'Cash'),
                    'optionType'     : dict ( defaultValue = 'Call' )
                    }
        
        attrs['upsideOption_asian'] = {
                    'averageMethodType' : dict ( defaultValue = 'Arithmetic',
                                                 visible = '@IsShowModeDetail'),
                    'averagePriceType'  : dict ( defaultValue = 'Average',
                                                 visible = '@IsShowModeDetail'),
                    'averageStrikeType' : dict ( defaultValue = 'Fix',
                                                 visible = '@IsShowModeDetail')
                    }
    
        attrs['downsideOption'] = {
                    'settlementType' : dict ( defaultValue = 'Cash' ),
                    'valuationGroup' : dict ( visible = True,
                                              label = 'Basket Val Group' ),
                    'optionType'     : dict ( defaultValue = 'Put' )
                    }

        attrs['stopLossOption'] = {
                    'settlementType' : dict ( defaultValue = 'Cash'),
                    'optionType'     : dict ( defaultValue = 'Put' )
                    }
        
        attrs['zero'] = {
                    'contractSize' : dict ( onChanged = '@SetUpsideStrike|SetOptionContractSize',
                                            label = 'Notional' ),
                                            #objMapping = 'Combination.ContractSize',
                    'startDate'    : dict ( visible = '@IsShowModeDetail',
                                            width = 1,
                                            label = 'Bond Start Date' ),
                    'endDate'      : dict ( label = 'Bond End Date' )
                    }
    
        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })

    def OnNew(self):
        # When called though FValidation, a new Deal Package
        # is created but not a new instrument package.
        if self.InstrumentPackage().IsInfant():
            self.currency = self.Zero().Currency()
            self.upsideOption_strikePrice = defaultValueStrike
            self.protection = defaultValueProtection
            self.zero_contractSize = defaultValueContractSize
            try:
                self.SetZeroEndDate()
            except:
                pass
            self.zero_RegenerateCashFlows()
            self.privateAsianStartDate = acm.Time.DateNow()

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_CapitalProtectedCertificate')


    def OnInit(self):

        self.RegisterAlignmentAcrossComponents(['upsideOption_strikePrice',
                                                'downsideOption_strikePrice'])

        self.RegisterAlignmentAcrossComponents(['upsideOption_expiry',
                                                'downsideOption_expiry',
                                                'stopLossOption_expiry'])

        self.RegisterAlignmentAcrossComponents(['upsideOption_contractSize',
                                                'downsideOption_contractSize',
                                                'stopLossOption_contractSize'])

        self.RegisterAlignmentAcrossComponents(['upsideOption_settlementType',
                                                'downsideOption_settlementType',
                                                'stopLossOption_settlementType'])

        self.RegisterAlignmentAcrossComponents(['upsideOption_settleDays',
                                                'downsideOption_settleDays',
                                                'stopLossOption_settleDays'])

        self.RegisterAlignmentAcrossComponents(['upsideOption_quantoType',
                                                'downsideOption_quantoType',
                                                'stopLossOption_quantoType'])

        self.RegisterAlignmentAcrossComponents(['upsideOption_quantoType',
                                                'downsideOption_quantoType',
                                                'stopLossOption_quantoType'])

        self.RegisterAlignmentAcrossComponents(['downsideOption_valuationGroup',
                                                'stopLossOption_valuationGroup'])

    def OnOpen(self):

        priceEvents = self.UpsideOption().GetExoticEventsOfKind('Average price')
        _startDate = acm.Time.DateNow()
        if len(priceEvents) != 0:
            _startDate = acm.Time.BigDate()
            for event in priceEvents:
                if acm.Time.DateDifference(_startDate, event.Date()) > 0:
                    _startDate = event.Date()

        self.SetAttribute('privateAsianStartDate', _startDate, silent = True)

    # Component access
    def Combination(self):
        return self.InstrumentAt('Combination')
    
    def UpsideOption(self):
        return self.InstrumentAt('UpsideOption')
    
    def DownsideOption(self):
        return self.InstrumentAt('DownsideOption')
    
    def StopLossOption(self):
        return self.InstrumentAt('StopLossOption')
    
    def Zero(self):
        return self.InstrumentAt('Zero')
    
    def ZeroLeg(self):
        return self.Zero().FirstFixedLeg()

    def UpsideOptionCombinationMap(self):
        return self.CombinationMapAt('UpsideOption', 'Combination')

    def DownsideOptionCombinationMap(self):
        return self.CombinationMapAt('DownsideOption', 'Combination')
    
    def StopLossOptionCombinationMap(self):
        return self.CombinationMapAt('StopLossOption', 'Combination')
    
    def ZeroCombinationMap(self):
        return self.CombinationMapAt('Zero', 'Combination')

    def CombinationTrade(self):
        return self.TradeAt('Combination')

    def LeadTrade(self):
        return self.CombinationTrade()

    def Underlying(self):
        return self.UpsideOption().Underlying()

    def AveragePriceEvents(self):
        return self.upsideOption_asian_averageDates_events


    # Methods for handling a generic date field
    
    def _PeriodToDateTransform(self, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = acm.Time().PeriodSymbolToDate(newDate)
        return date

    def _GetInstrumentCurrency(self):
        currency = self.currency
        if not currency:
            mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
            currency = mappedValuationParameter().Parameter().AccountingCurrency()
        return currency

    def _GetInstrumentCalendar(self):
        return self._GetInstrumentCurrency().Calendar()

    def _ValidateDate(self, date, dateName):
        adjustedDate = date
        calendar = self._GetInstrumentCalendar()
        if date and calendar and calendar.IsNonBankingDay(None, None, date):
            if self._ShowAdjustDateDialog(dateName, calendar, date):
                adjustedDate = calendar.ModifyDate(None, None, date, "Following")
        return adjustedDate
    
    def _ShowAdjustDateDialog(self, name, calendar, date):
        return self.DealPackage().GUI().AskAdjustDate(name, calendar, date)
        
    @classmethod
    def SetUp(cls, definitionSetUp):
        from DealPackageSetUp import AddInfoSetUp
        definitionSetUp.AddSetupItems(
                            AddInfoSetUp( 
                                recordType='Instrument',
                                fieldName='sp_RollingPeriod',
                                dataType='String',
                                description='Frequency of date schedule',
                                dataTypeGroup='Standard',
                                subTypes=['Option'],
                                defaultValue=None,
                                mandatory=False
                                ) )


def StartCapitalProtectedCertificate(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'SP_CapitalProtectedCertificate')
    return  


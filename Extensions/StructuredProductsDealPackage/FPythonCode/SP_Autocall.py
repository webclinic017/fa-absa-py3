
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, ParseSuffixedFloat, Settings, ReturnDomainDecorator

from StructuredProductBase import ComponentBasedDealPackage
from CompositeTradeComponents import TradeInput
from CompositeBasketOptionComponents import BasketBarrierOption
from CompositeOptionAdditionComponents import InitialFixingMulti
from CompositeExoticEventComponents import ExoticEvent
from SP_DealPackageHelper import AddExoticEvent, MergeDictionaries, AddHalfPeriod, SuggestInstrumentName


def RollingPeriodDefaultFromAddInfo():
    addinfo = acm.FAdditionalInfoSpec['sp_RollingPeriod']
    if addinfo and addinfo.DefaultValue():
        return addinfo.DefaultValue()
    else:
        return '1Y'

def UdmcProcessDefaultFromAddInfo():
    addinfo = acm.FAdditionalInfoSpec['ValuationProcess']
    if addinfo and addinfo.DefaultValue():
        return addinfo.DefaultValue()
    else:
        return 'LogNorm'

@Settings(GraphApplicable=False,
          MultiTradingEnabled=True)
class AutocallBasket(ComponentBasedDealPackage):

    ipName      = Object( label          = 'Name',
                          width          = 80,
                          objMapping     = InstrumentPart('InstrumentPackage.Name'),
                          onChanged      = '@SetInstrumentName') 
    
    option      = BasketBarrierOption ( optionName     = 'Option',
                                        basketName     = 'Underlying',
                                        basketUpdateAction = 'BasketUpdateAction',
                                        basketColumns  = [ {'methodChain': 'Instrument.VerboseName', 'label': 'Instrument'},
                                                           {'methodChain': 'Instrument.InsType',     'label': 'Type'},
                                                           {'methodChain': 'Instrument.Currency',    'label': 'Currency'},
                                                           {'methodChain': 'Weight',                 'label': 'Weight'},
                                                           {'methodChain': 'FixFxRate',              'label': 'Fix Fx Rate'},
                                                           {'methodChain': 'InitialFixing',          'label': 'Initial Fixing'},
                                                           {'methodChain': 'PerformanceSinceInitialFixing', 'label': 'Performance (%)', 'formatter':'PercentShowZero'}
                                                         ])

    initialFixing = InitialFixingMulti ( optionName = 'Option' ) 

    autocallRolling = Object ( objMapping   = InstrumentPart('RollingPeriod'),
                               label        = 'Autocall Rolling',
                               defaultValue = RollingPeriodDefaultFromAddInfo(),
                               onChanged    = '@SetAutocallDates' )
    
    payoffType      = Object ( objMapping   = InstrumentPart('Option.AdditionalInfo.PayoffType'),
                               label        = 'Payoff Type' )
    
    currency    = Object( objMapping = InstrumentPart('Option.Currency').DealPart('OptionTrade.Currency'),
                          onChanged  = '@UpdateQuantoType|UpdateBasketCurrency',
                          label = 'Currency' )
    
    basketCurrency = Object( objMapping = InstrumentPart('Option.StrikeCurrency|Underlying.Currency'),
                             label      = 'Basket Currency',
                             onChanged  = '@SetFixFxRate',
                             visible    = '@IsShowModeDetail' )

    monitoring  = Object( objMapping = InstrumentPart('Monitoring'),
                          label      = 'Monitoing',
                          choiceListSource = '@ChoicesMonitoring',
                          defaultValue = 'LastLook' )

    processType = Object( objMapping   = InstrumentPart('Option.AdditionalInfo.ValuationProcess'),
                          label        = 'MC Process',
                          defaultValue = UdmcProcessDefaultFromAddInfo() )

    tradeInput  = TradeInput( priceLayout = 'PriceLayout')

    optionPrice = Object  ( objMapping = "OptionTrade.Price",
                            label = 'Price',
                            width = 22)
    
    optionPremium = Object  ( objMapping = "OptionTrade.Premium",
                              label = 'Premium' )
    
    pv          = CalcVal ( calcMapping = 'OptionTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                            solverTopValue = True )

    autocallDates = ExoticEvent ( optionName     = 'Option', 
                                  underlyingName = 'Underlying',
                                  eventTypes     = ['Price Fixing'],
                                  eventLabel     = 'Autocall Dates',
                                  showAsButton   = False,
                                  displayColumns = [{'methodChain' : 'Date',                            'label' : 'Date'},
                                                    {'methodChain' : 'ComponentInstrument.VerboseName', 'label' : 'Underlying'},
                                                    {'methodChain' : 'EventValue',                      'label' : 'Fixing'}
                                                    ] )


    @ReturnDomainDecorator('dateperiod')
    def RollingPeriod(self, value = '*READING*'):
        mappedMethod = self.Option().AdditionalInfo().Sp_RollingPeriod
        if value == '*READING*':
            return mappedMethod()
        else:
            mappedMethod(value)

    def AttributeOverrides(self, overrideAccumulator):
    
        attrs = {}
        
        attrs['option'] = {
                        'expiry'        : dict ( onChanged = '@SetAutocallDates|UpdateBarrierMonitoringEvents' ),
                        'quotation'     : dict ( visible = '@IsShowModeDetail' ),
                        'strikePrice'   : dict ( visible = '@IsShowModeDetail',
                                                 solverParameter = '@SolverParametersACStrike',
                                                 label = 'Strike Price (%)' ),
                        'quantoType'    : dict ( enabled = False ),
                        'optionType'    : dict ( visible = '@IsShowModeDetail' )
                        }
        
        attrs['option_barrier'] = {
                        'barrierLevel'       : dict ( solverParameter = '@SolverParametersACLevel',
                                                      label = 'Autocall Level (%)' ),
                        'doubleBarrierLevel' : dict ( solverParameter = '@SolverParametersACBarrier',
                                                      label = 'Protection (%)' ),
                        'barrierType'        : dict ( choiceListSource = '@ChoicesBarrierType',
                                                      visible = '@IsShowModeDetail' ),
                        'barrierMonitoring'  : dict ( choiceListSource = '@ChoicesBarrierMonitoring' ),
                        'crossDate'          : dict ( visible = '@IsShowModeDetail' ),
                        'barrierStatus'      : dict ( visible = '@IsShowModeDetail' ),
                        'rebate'             : dict ( backgroundColor = '@SolverColor',
                                                      solverParameter = '@SolverParameterCoupon',
                                                      transform = '@TransformCoupon',
                                                      toolTip = 'Coupon (%)',
                                                      label = 'Coupon (%)')
                        }
        
        attrs['initialFixing'] = {
                        'initialFixingDate'  : dict ( enabled   = '@BasketHasComponents',
                                                      onChanged = '@SetAutocallDates' )
                            }
        
        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })

    def PriceLayout(self):
        return """
                hbox(;
                    vbox{;
                        optionPrice;
                        };
                    vbox{;
                        optionPremium;
                        };
                    );
                """

    def BasketHasComponents(self, attrName, *rest):
        return self.option_underlying_instruments.Size() > 0

    def SetInstrumentName(self, *rest):
        suggestName = SuggestInstrumentName(self.ipName)
        self.Option().Name(suggestName)

    def SetAutocallDates(self, attrName, *rest):
        self.autocallDates.GenerateExoticEvents( 
                            'Price Fixing',
                            self.initialFixing_initialFixingDate,
                            self.option_expiry,
                            self.autocallRolling,
                            AddHalfPeriod( self.initialFixing_initialFixingDate, 
                                           self.autocallRolling),
                            includeStartDate = False,
                            regenerate = True,
                            generatePerUnderlying = True )

    def BasketUpdateAction(self, attrName, actionInstruments = None):
        if attrName in ('option_underlying_addInstrument', 'option_underlying_removeInstrument'):
            self.UpdateBarrierMonitoringEvents(attrName)
            self.SetAutocallDates(attrName)
            self.UpdateQuantoType(attrName)

        # handle initial fixing events
        if attrName == 'option_underlying_addInstrument':
            for ins in actionInstruments:
                self.initialFixing.AddInitialFixing(ins)
        
        if attrName == 'option_underlying_removeInstrument':
            self.initialFixing.RemoveInitialFixing(actionInstruments)

    def UpdateQuantoType(self, attrName, *rest):
        for combLink in self.option_underlying_instruments:
            if combLink.Instrument().Currency() != self.currency:
                self.option_quantoType = 'Quanto'
                return
        self.option_quantoType = 'None'

    def UpdateBasketCurrency(self, attrName, *rest):
        self.basketCurrency = self.currency

    def SetFixFxRate(self, attrName, *rest):
        if self.Option().FixFxRate() == 0.0 and self.currency != self.basketCurrency:
            self.Option().FixFxRate(1.0)
    
    def UpdateBarrierMonitoringEvents(self, attrName, *rest):
        # For now, always delete, this should be changed
        allBarrierObservations = self.Option().GetExoticEventsOfKind('Barrier date')
        allBarrierObservations.Unsimulate()

        if self.monitoring == 'LastLook':
            for combMap in self.option_underlying_instruments:
                AddExoticEvent(self.Option(), 
                               combMap.Instrument(), 
                               'Barrier date', 
                               self.option_expiry,
                               -1.0)

    def ChoicesBarrierType(self, *rest):
        return ['Custom']
    
    def ChoicesBarrierMonitoring(self, *rest):
        return ['Continuous', 'Discrete']
    
    def ChoicesMonitoring(self, *rest):
        return ['Continuous', 'LastLook']

    def Monitoring(self, value = '*READ*'):
        if value == '*READ*':
            return {'Continuous':'Continuous', 'Discrete':'LastLook'}.get(self.option_barrier_barrierMonitoring)
        else:
            self.option_barrier_barrierMonitoring = {
                                        'Continuous':'Continuous', 
                                        'LastLook':'Discrete'}.get(value)
            self.UpdateBarrierMonitoringEvents('monitoring')

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_AutocallBasket')

    def OnNew(self):
        # When called though FValidation, a new Deal Package
        # is created but not a new instrument package.
        if self.InstrumentPackage().IsInfant():
            self.currency = self.Option().Currency()
            self.basketCurrency = self.currency

    def AssemblePackage(self):
        ins = self.option.CreateInstrument('BasketAutocall')
        trade = acm.DealCapturing().CreateNewTrade(ins)
        self.DealPackage().AddTrade(trade, 'Option')
        self.DealPackage().AddInstrument(ins.Underlying(), 'Basket')

    def PriceFixingEvents(self):
        return self.Option().GetExoticEventsOfKind('Price Fixing')
    
    def Option(self):
        return self.InstrumentAt('Option')

    def Underlying(self):
        return self.InstrumentAt('Basket')
        #return self.Option().Underlying()
    
    def OptionTrade(self):
        return self.TradeAt('Option')

    def LeadTrade(self):
        return self.OptionTrade()

    @classmethod
    def SetUp(cls, definitionSetUp):
        AutocallSetup(definitionSetUp)
        InitialFixingMulti.SetUp(definitionSetUp)

    # Solver functionality

    def MonteCarloPVSolverParameters(self):
        return {'precision':1, 'maxIterations':10}

    def SolverParameterCoupon(self, attrName, *rest):
        return MergeDictionaries({'minValue':0.00, 'maxValue':100}, 
                                 self.MonteCarloPVSolverParameters())

    def SolverParametersACStrike(self, attrName, *rest):
        return MergeDictionaries({'minValue':0.01, 'maxValue':200}, 
                                 self.MonteCarloPVSolverParameters())

    def SolverParametersACBarrier(self, attrName, *rest):
        return MergeDictionaries({'minValue':20, 'maxValue':100}, 
                                 self.MonteCarloPVSolverParameters())
    
    def SolverParametersACLevel(self, attrName, *rest):
        return MergeDictionaries({'minValue':50, 'maxValue':150},
                                 self.MonteCarloPVSolverParameters())

    def TopValueFields(self):
        return {'PV':'pv'}

    def TransformCoupon(self, attrName, value, *rest):
        return self.option.TransformSolver(attrName, value)



def BasketAutocallInstrumentDefaultHook(ins):

    ins.AdditionalInfo().StructureType('BasketAutocall')

    if ins.Underlying() is None or ins.Underlying().InsType() != 'EquityIndex':
        allEis = acm.FEquityIndex.Select('')
        if len(allEis) > 0:
            ins.Underlying(allEis[0])

    ins.StrikeType('Rel Spot Pct 100')

    defaultPayoff = acm.FAdditionalInfoSpec['PayoffType'].DefaultValue()
    ins.AdditionalInfo().PayoffType(defaultPayoff if defaultPayoff else 'Basket')

    ins.CreateExotic()

    ins.Exotic().BarrierMonitoring('Discrete')
    
    ins.Exotic().BarrierOptionType('Custom')
    
    ins.OptionType('Put')

    ins.FixFxRate(1.0)
    
    if ins.ContractSize() == 0.0:
        ins.ContractSize(1000)
    
    if ins.StrikePrice() == 0.0:
        ins.StrikePrice(100)
    
    if ins.Barrier() == 0.0:
        ins.Barrier(100)
    
    if ins.Exotic().DoubleBarrier() == 0.0:
        ins.Exotic().DoubleBarrier(80)

    if ins.ValuationGrpChlItem() is None:
        ins.ValuationGrpChlItem('AutoCallableBasket')

    if ins.Generic() is True:
        quotation = ins.Quotation()
        ins.Generic(False)
        ins.Quotation(quotation)

    return ins

def AutocallSetup(definitionSetUp):
    # Accumulator specific setup
    from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp, ContextLinkSetUp
    definitionSetUp.AddSetupItems(
                        ChoiceListSetUp(
                            list        = 'StructureType', 
                            entry       = 'BasketAutocall', 
                            descr       = 'BasketAutocall'
                            ),
                        ChoiceListSetUp(
                            list        = 'PayoffType', 
                            entry       = 'Rainbow', 
                            descr       = 'Rainbow'
                            ),
                        ChoiceListSetUp(
                            list        = 'PayoffType', 
                            entry       = 'Basket', 
                            descr       = 'Basket'
                            ),
                        ChoiceListSetUp(
                            list        = 'Exotic Event Types',
                            entry       = 'Initial Fixing',
                            descr       = 'Initial Fixing'
                            ),
                        ChoiceListSetUp(
                            list        = 'Valuation Extension',
                            entry       = 'udmcAutocallableBasket',
                            descr       = 'udmcAutocallableBasket'
                            ),
                        ChoiceListSetUp(
                            list        = 'ValGroup',
                            entry       = 'AutoCallableBasket',
                            descr       = 'AutoCallableBasket'
                            ),
                        ChoiceListSetUp(
                            list        = 'ValuationProcess',
                            entry       = 'LogNorm',
                            descr       = 'LogNorm'
                            ),
                        ChoiceListSetUp(
                            list        = 'ValuationProcess',
                            entry       = 'LocalVolatility',
                            descr       = 'LocalVolatility'
                            ),
                        ContextLinkSetUp(
                            context='Global',
                            type='Valuation Extension',
                            name='udmcAutocallableBasket',
                            mappingType='Val Group',
                            chlItem='AutoCallableBasket'
                            ),
                        AddInfoSetUp( 
                            recordType='Instrument',
                            fieldName='sp_RollingPeriod',
                            dataType='String',
                            description='Frequency of date schedule',
                            dataTypeGroup='Standard',
                            subTypes=['Option'],
                            defaultValue=None,
                            mandatory=False
                            ),
                        AddInfoSetUp( 
                            recordType    = 'Instrument',
                            fieldName     = 'StructureType',
                            dataType      = 'ChoiceList',
                            description   = 'StructureType',
                            dataTypeGroup = 'RecordRef',
                            subTypes      = [],
                            defaultValue  = None,
                            mandatory     = False
                            ),
                        AddInfoSetUp(
                            recordType      = 'Instrument',
                            fieldName       = 'PayoffType',
                            dataType        = 'ChoiceList',
                            description     = 'PayoffType',
                            dataTypeGroup   = 'RecordRef',
                            subTypes        = ['Option'],
                            defaultValue    = 'Basket',
                            mandatory       = False
                            ),
                        AddInfoSetUp(
                            recordType      = 'Instrument',
                            fieldName       = 'ValuationProcess',
                            dataType        = 'ChoiceList',
                            description     = 'ValuationProcess',
                            dataTypeGroup   = 'RecordRef',
                            subTypes        = ['Option'],
                            defaultValue    = 'LogNorm',
                            mandatory       = False
                            )
                        )


def ExoticFixingsHook(instrument, dateToday, updateHistorical, updateResult):
    return ['Price Fixing', 'Initial Fixing']

def StartAutocallBasket(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'SP_AutocallBasket')
    return  


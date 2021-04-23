
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, ParseSuffixedFloat

from CompositeCashFlowComponents import ZeroBond
from CompositeOptionComponents import OptionPctStrike

from StructuredProductBase import ProductBase

from SP_DealPackageHelper import SafeDivision

@Settings(GraphApplicable=True)
class CapitalProtectedNoteBase(ProductBase):
    
    option      = OptionPctStrike ( optionName = 'Option',
                                    undType    = acm.FStock )
    
    zero        = ZeroBond ( zeroName       = 'Zero', 
                             zeroLegName    = 'ZeroLeg' )

    participation = Object ( objMapping     = 'InstrumentPackage.AdditionalInfo.Participation',
                             formatter      = "PercentShowZero",
                             defaultValue   = 1.0,
                             onChanged      = "@ChangeWeightFromParticipation",
                             label          = 'Participation (%)',
                             transform      = '@TransformSolver',
                             solverParameter = '@SolverParameterParticipation',
                             backgroundColor = '@SolverColor')
    
    protection    = Object ( objMapping     = 'InstrumentPackage.AdditionalInfo.CapitalProtection',
                             formatter      = "PercentShowZero",
                             defaultValue   = 1.0,
                             onChanged      = "@ChangeWeightFromProtection",
                             label          = 'Protection (%)',
                             transform      = '@TransformSolver',
                             solverParameter = '@SolverParameterProtection',
                             backgroundColor = '@SolverColor')

    def AttributeOverrides(self, overrideAccumulator):
        attrs = {}

        attrs['option'] = {
                    'expiry'            : dict ( validate = '@ValidateExpiry',
                                                 defaultValue = '3Y',
                                                 label = 'Final Fixing Date' ),
                    'optionType'        : dict ( defaultValue = 'Call' ),
                    'pctStrike_initialFixing_initialFixingDate' : dict ( defaultValue = '1W' ),
                    'pctStrike_strikePricePct' : dict ( label = 'Strike Price' ),
                    'strikePrice'       : dict ( label = '' )
                    }
        
        attrs['zero'] = {
                    'endDate'     : dict ( validate = '@ValidateEndDate',
                                           defaultValue = '3Y' ),
                    'payCalendar' : dict ( validate = '@ValidatePayCalendar' ),
                    'startDate'   : dict ( defaultValue = '1W' )
                    }

        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })

    def TransformSolver(self, attrName, value):
        goalValue = None

        if self.TopValueFields().has_key('PV'):
            f = self.GetFormatter(self.TopValueFields().get('PV'))
            goalValue = ParseSuffixedFloat(value, suffix=['pv'], formatter=f)
            if goalValue != None:
                topValue = self.TopValueFields().get('PV')
        
        if self.TopValueFields().has_key('Price') and (goalValue == None):
            f = self.GetFormatter(self.TopValueFields().get('Price'))
            goalValue = ParseSuffixedFloat(value, suffix=['price', 'p'], formatter=f)
            if goalValue != None:
                topValue = self.TopValueFields().get('Price')
        
        if goalValue != None:
            return self.Solve(topValue, attrName, goalValue)
        else:
            return value

    def Notional(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Zero().ContractSize()
        else:
            value = float(value)
            self.UpdateOptionContractPrice(value)
            self.SetContractSizesFromNotional(value)
            self.UpdatePremiums()

    def UpdateOptionContractPrice(self, value):
        # This is only needed if there is a separate
        # trade in the option.
        pass

    def SetContractSizesFromNotional(self, value):
        self.zero_contractSize = value
        self.option_contractSize = SafeDivision( value, self.option_pctStrike_initialFixing_initialFixing, value )        

    def VerifyOptionQuotation(self, *rest):
        # Then the underlying is changed, the quotation of the option
        # is changed by the decorator. It needs to be Per Contract to be able
        # to view it as a % price of the nominal amount
        self.Option().Quotation('Per Contract')

    def ChangeCurrency(self, attrName, oldValue, newValue, *rest):
        self.currency = self.option_underlying.Currency()

    def ChangeOptionContractSize(self, attrName, oldFixing, newFixing, *rest):
        self.option_contractSize = SafeDivision( self.notional, newFixing, self.notional )

    def UpdateSettleDays(self, attrName, oldValue, newValue, *rest):
        # Make sure that both expiry and maturity are valid datetime values.
        # As it is possible to enter date periods in those fields
        # can we end up here before a transformation has been done on both
        # fields when a new package is created.
        if not (acm.Time().PeriodSymbolToDate(self.option_expiry) or acm.Time().PeriodSymbolToDate(self.zero_endDate)):
            if self.currency:
                cal = self.currency.Calendar()
            else:
                cal = self.Zero().Currency().Calendar()
            self.option_settleDays = cal.BankingDaysBetween(self.option_expiry, self.zero_endDate)


    # ### Validation callbacks for attributes defeind in this class

    def ValidateSpotDays(self, attrName, newValue):
        self.ValidateDaysBetweenFinalFixingAndMaturity(attrName, newValue)

    def ValidateDaysBetweenFinalFixingAndMaturity(self, attrName, newValue):
        spot            = newValue if attrName == 'spotDays' else self.spotDays
        calendar        = newValue if attrName == 'zero_payCalendar' else self.zero_payCalendar
        finalFixing     = newValue if attrName == 'option_expiry' else self.option.TransformExpiry('option_expiry', self.option_expiry)
        maturity        = newValue if attrName == 'zero_endDate' else self.zero.TransformPeriodToEndDate('zero_endDate', self.zero_endDate)
        if spot and calendar and finalFixing and maturity:
            if calendar.BankingDaysBetween(finalFixing, maturity) <= spot:
                raise DealPackageUserException( 'Number of spot days must be smaller than number of days between final fixing and maturity.' )

    def ValidateExpiryBeforeEndDate(self, attrName, newValue):
        finalFixing     = newValue if attrName == 'option_expiry' else self.option.TransformExpiry('option_expiry', self.option_expiry)
        maturity        = newValue if attrName == 'zero_endDate' else self.zero.TransformPeriodToEndDate('zero_endDate', self.zero_endDate)
        if acm.Time().DateDifference(finalFixing, maturity) >= 0:
            raise DealPackageUserException( 'Final fixing must be before end date' )

    # ### Validation callbacks for attributes defined 
    # ### in composite attributes

    def ValidateExpiry(self, attrName, newValue):
        self.ValidateDaysBetweenFinalFixingAndMaturity(attrName, newValue)
        self.ValidateExpiryBeforeEndDate(attrName, newValue)
    
    def ValidateEndDate(self, attrName, newValue):
        self.ValidateDaysBetweenFinalFixingAndMaturity(attrName, newValue)
        self.ValidateExpiryBeforeEndDate(attrName, newValue)

    def ValidatePayCalendar(self, attrName, newValue):
        self.ValidateDaysBetweenFinalFixingAndMaturity(attrName, newValue)

    # ### Define solver paramters avaiable in the PV field

    def SolverParameterProtection(self, *rest):
        return {'minValue':0.01, 'maxValue':1.0}
    
    def SolverParameterParticipation(self, *rest):
        return {'minValue':0.01, 'maxValue':2.0}

    def TransformPV(self, attrName, value):
        goalVal = None
        f = self.GetFormatter(attrName)

        goalValue = ParseSuffixedFloat(value, suffix=['C', 'CP', 'PROTECTION'], formatter=f)
        if goalValue != None:
            self.solverParameter = 'protection'
        
        else:
            goalValue = ParseSuffixedFloat(value, suffix=['P', 'PART', 'PARTICIPATION'], formatter=f)
            if goalValue != None:
                self.solverParameter = 'participation'
        
        return goalVal if goalVal != None else self.MapSolverTopValueToComponent(value, attrName, {'strikePricePct':'option_pctStrike'})
    
    # ### Component access methods

    def Zero(self):
        return self.InstrumentAt('Zero')
    
    def ZeroLeg(self):
        return self.Zero().FirstFixedLeg()

    def Option(self):
        return self.InstrumentAt('Option')

    def InstrumentPartCurrencies(self):
        ccyObj = acm.FArray()
        ccyObj.Add(self.Option())
        ccyObj.Add(self.Zero())
        ccyObj.Add(self.ZeroLeg())
        return ccyObj
        
    def DealPartCurrencies(self):
        ccyObj = acm.FArray()
        ccyObj.AddAll(self.DealPackage().Trades())
        return ccyObj

    def OnInit(self):
        self._tradeQuantityMapping = []
        self.RegisterCallbackOnAttributeChanged(self.UpdateSettleDays, ['option_expiry',
                                                                        'zero_endDate'] )
        self.RegisterCallbackOnAttributeChanged(self.ChangeOptionContractSize, 'option_pctStrike_initialFixing_initialFixing')
        self.RegisterCallbackOnAttributeChanged(self.ChangeCurrency, 'option_underlying')
        self.RegisterCallbackOnAttributeChanged(self.VerifyOptionQuotation)
    
    def OnNew(self):
        # When called though FValidation, a new Deal Package
        # is created but not a new instrument package.
        if self.InstrumentPackage().IsInfant():
            self.currency = self.Zero().Currency()
            self.spotDays = self.Zero().SpotBankingDaysOffset()
            self.zero_RegenerateCashFlows()
    
    def AssemblePackage(self):
        self._option = self.option.CreateInstrument()
        self._zero = self.zero.CreateInstrument()

    def CustomPanes(self):
        layout = self.GetCustomPanesFromExtValue('CustomPanes_SP_CapitalProtectedNoteSingle')
        layout[0]['General'] = layout[0]['General'].replace('priceLayout', self.PriceLayout())
        return layout

    @classmethod
    def SetUp(cls, definitionSetUp):
        super(CapitalProtectedNoteBase, cls).SetUp(definitionSetUp)
        from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp, ContextLinkSetUp, CustomMethodSetUp

        definitionSetUp.AddSetupItems(
                            AddInfoSetUp(
                                recordType      = 'InstrumentPackage',
                                fieldName       = 'Participation',
                                dataType        = 'Double',
                                description     = 'Participation Level',
                                dataTypeGroup   = 'Standard',
                                subTypes        = [],
                                defaultValue    = 1.0,
                                mandatory       = False
                                ),
                            AddInfoSetUp(
                                recordType      = 'InstrumentPackage',
                                fieldName       = 'CapitalProtection',
                                dataType        = 'Double',
                                description     = 'Capital Protection Level',
                                dataTypeGroup   = 'Standard',
                                subTypes        = [],
                                defaultValue    = 1.0,
                                mandatory       = False
                                ))


class CapitalProtectedNoteCombination(CapitalProtectedNoteBase):

    combinationPrice            = Object  ( objMapping = "CombinationTrade.Price",
                                            label = 'Price' )
    
    combinationPremium          = Object  ( objMapping = "CombinationTrade.Premium",
                                            label = 'Premium' )

    combinationContractSize     = Object  ( objMapping = "Combination.ContractSize")
    
    combinationPV               = CalcVal ( calcMapping = 'CombinationTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                                            label = 'PV',
                                            solverTopValue = True,
                                            transform = '@TransformPV' )

    def TopValueFields(self):
        return {'PV':'combinationPV'}

    def ChangeWeightFromParticipation(self, *rest):
        self.OptionCombinationMap().Weight(self.participation * 100.0)
    
    def ChangeWeightFromProtection(self, *rest):
        self.ZeroCombinationMap().Weight(self.protection * 100.0)

    def SetContractSizesFromNotional(self, value):
        super(CapitalProtectedNoteCombination, self).SetContractSizesFromNotional(value)
        self.combinationContractSize = value

    def Combination(self):
        return self.InstrumentAt('Combination')
    
    def CombinationTrade(self):
        return self.TradeAt('Combination')

    def OptionCombinationMap(self):
        return self.CombinationMapAt('Option', 'Combination')
    
    def ZeroCombinationMap(self):
        return self.CombinationMapAt('Zero', 'Combination')

    def InstrumentPartCurrencies(self):
        currencies = super(CapitalProtectedNoteCombination, self).InstrumentPartCurrencies()
        currencies.Add(self.Combination())
        return currencies
    
    def OnInit(self):
        super(CapitalProtectedNoteCombination, self).OnInit()

        comboTradeMapping = acm.FDictionary()
        comboTradeMapping.AtPut('trade', 'CombinationTrade')
        comboTradeMapping.AtPut('quantityFactor', lambda *args : 1.0)
        self._tradeQuantityMapping.append(comboTradeMapping)

    def LeadTrade(self):
        return self.CombinationTrade()
    
    def AssemblePackage(self):
        super(CapitalProtectedNoteCombination, self).AssemblePackage()
        tradeCombination = self.DealPackage().CreateTrade('Combination', 'Combination')
        self.Combination().Quotation('Clean')
        self.Combination().Factor(100)
        self.DealPackage().AddCombinationMap(self._option, 100.0, 'Option', 'Combination')
        self.DealPackage().AddCombinationMap(self._zero, 100.0, 'Zero', 'Combination')

    def PriceLayout(self):
        return """
                hbox(;
                    vbox{;
                        combinationPrice;
                        };
                    vbox{;
                        combinationPremium;
                        };
                    vbox{;
                        combinationPV;
                        };
                    );
                """

class CapitalProtectedNoteTrades(CapitalProtectedNoteBase):

    optionPrice         = Object ( objMapping = 'OptionTradePrice',
                                   label = 'Option',
                                   formatter = "PercentShowZero",
                                   domain = 'double', 
                                   defaultValue = 0.0 )
    
    optionPremium       = Object ( objMapping = 'OptionTrade.Premium',
                                   label = '' )
    
    zeroPrice           = Object ( objMapping = 'ZeroTrade.Price',
                                   #domain = 'float',
                                   label = 'Zero' )
    
    zeroPremium         = Object ( objMapping = 'ZeroTrade.Premium',
                                   label = '' )
    
    totalPrice          = Object ( objMapping = 'TotalPrice',
                                   domain = 'double',
                                   label = 'Total',
                                   enabled = False )
    
    totalPremium        = Object ( objMapping = 'TotalPremium',
                                   domain = 'double',
                                   label = '',
                                   enabled = False )

    optionPV            = CalcVal ( calcMapping = 'OptionTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                                    label = '' )
    
    zeroPV              = CalcVal ( calcMapping = 'ZeroTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                                    label = '' )

    totalPV             = CalcVal ( calcMapping = 'AsPortfolio:FPortfolioSheet:Portfolio Theoretical Value No Trade Payments',
                                    label = '',
                                    solverTopValue = True,
                                    transform = '@TransformPV' )

    # ############################################################################
    # Non visible attributes that should be 
    # removed and logic accessing them replaced
    # when SPR XYZ has been fixed.
    # ############################################################################
    
    optionTradeQuantity = Object ( objMapping = 'OptionTrade.Quantity' )
    
    zeroTradeQuantity   = Object ( objMapping = 'ZeroTrade.Quantity' )

    # ############################################################################

    def TopValueFields(self):
        return {'PV':'totalPV'}

    def OptionTradePrice(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.OptionTrade().Price() / self.notional
        else:
            self.OptionTrade().Price( value * self.notional )
    
    def TotalPrice(self, value = '*Reading*'):
        if value == '*Reading*':
            if self.tradeInput_quantity_value:
                return ( 
                        (   self.OptionTradePrice() * 100.0 * self.OptionTrade().Quantity()
                           + self.ZeroTrade().Price() * self.ZeroTrade().Quantity() 
                         )
                          / self.tradeInput_quantity_value
                       )

    def TotalPremium(self, value = '*Reading*'):
        if value == '*Reading*':
            return (   
                       self.OptionTrade().Premium()
                     + self.ZeroTrade().Premium()
                   )

    def UpdateOptionContractPrice(self, value):
        oldPrice = self.OptionTrade().Price()
        oldNotional = self.Zero().ContractSize()
        pctPrice = oldPrice / oldNotional
        newPrice = pctPrice * value
        self.OptionTrade().Price(newPrice)

    def OptionTrade(self):
        return self.TradeAt("Option")
    
    def ZeroTrade(self):
        return self.TradeAt("Zero")

    def LeadTrade(self):
        return self.ZeroTrade()
    
    def OnInit(self):
        super(CapitalProtectedNoteTrades, self).OnInit()

        zeroTradeMapping = acm.FDictionary()
        zeroTradeMapping.AtPut('trade', 'ZeroTrade')
        zeroTradeMapping.AtPut('quantityFactor', self.ZeroTradeQuantityFactor)
        self._tradeQuantityMapping.append(zeroTradeMapping)

        optTradeMapping = acm.FDictionary()
        optTradeMapping.AtPut('trade', 'OptionTrade')
        optTradeMapping.AtPut('quantityFactor', self.OptionTradeQuantityFactor)
        self._tradeQuantityMapping.append(optTradeMapping)
    
    def AssemblePackage(self):
        super(CapitalProtectedNoteTrades, self).AssemblePackage()
        tradeOption = acm.DealCapturing().CreateNewTrade(self._option)
        tradeZero = acm.DealCapturing().CreateNewTrade(self._zero)
        self.DealPackage().AddTrade(tradeZero, "Zero")
        self.DealPackage().AddTrade(tradeOption, "Option")

    def OptionTradeQuantityFactor(self):
        return self.participation
    
    def ZeroTradeQuantityFactor(self):
        return self.protection

    def ChangeWeightFromParticipation(self, *rest):
        self.optionTradeQuantity = self.tradeInput_quantity_value * self.participation
    
    def ChangeWeightFromProtection(self, *rest):
        self.zeroTradeQuantity  = self.tradeInput_quantity_value * self.protection

    def PriceLayout(self):
        return """
                hbox(;
                    vbox[Price;
                        optionPrice;
                        zeroPrice;
                        totalPrice;
                        ];
                    vbox[Premium;
                        optionPremium;
                        zeroPremium;
                        totalPremium;
                        ];
                    vbox[PV;
                        optionPV;
                        zeroPV;
                        totalPV;
                        ];
                    );
                    """



def StartCPNCombination(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Capital Protected Note (Combination)')
    return  

def StartCPNTrades(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Capital Protected Note (Trades)')
    return  

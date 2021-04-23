
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, SalesTradingInteraction, ReturnDomainDecorator

from StructuredProductBase import ProductBase
from CompositeTradeComponents import TradeB2B   

from CompositeCashFlowComponents import Bond
from CompositeOptionComponents import BarrierOptionPctStrike
import Validation_BarrierReverseConvertible

from SP_DealPackageHelper import SafeDivision

# ######################################
# Base Deal Package, same regardless of using combination or not
# ######################################
@Settings(GraphApplicable=True)
class BarrierReverseConvertibleBase(ProductBase):

    option              = BarrierOptionPctStrike ( optionName    = "Option",
                                                   undType       = acm.FStock )

    bond                = Bond ( bondName       = "Bond",
                                 bondLegName    = "BondLeg" )

    def AttributeOverrides(self, overrideAccumulator):
    
        attrs = {}
        
        attrs['option'] = {
                    'expiry'                    : dict ( validate = '@ValidateExpiry',
                                                         defaultValue = '1Y',
                                                         label = 'Final Fixing Date' ),
                    'barrier_barrierType'       : dict ( choiceListSource = ['Down & In', 'Up & In'],
                                                         defaultValue = 'Down & In',
                                                         label = '' ),
                    'barrier_barrierLevel'      : dict ( label = '' ),
                    'barrier_barrierMonitoring' : dict ( defaultValue = 'Continuous'),
                    'optionType'                : dict ( defaultValue = 'Put' ),
                    'strikePrice'               : dict ( label = '' ),
                    'pctBarrier_strikePricePct' : dict ( label = 'Strike Price' ),
                    'pctBarrier_barrierLevelPct': dict ( label = 'Barrier' ),
                    'pctBarrier_initialFixing_initialFixingDate' : dict ( defaultValue = '1W' )
                    }
        
        attrs['bond'] = {
                   'endDate'     : dict ( validate = '@ValidateEndDate',
                                          defaultValue = '1Y'),
                   'payCalendar' : dict ( validate = '@ValidatePayCalendar'),
                   'startDate'   : dict ( defaultValue = '1W' )
                   }
                    
        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })

    # ###########################
    # # Object mappings         #
    # ###########################
    
    def Notional(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Bond().ContractSize()
        else:
            value = float(value)
            self.UpdateOptionContractPrice(value)
            self.SetContractSizesFromNotional(value)
            self.UpdatePremiums()

    def SetContractSizesFromNotional(self, value):
        self.bond_contractSize = value
        self.option_contractSize = SafeDivision( value, self.option_pctBarrier_initialFixing_initialFixing, value )

    def UpdateOptionContractPrice(self, value):
        # This is only needed if there is a separate
        # trade in the option.
        pass

    # #################################################
    # # On Changed methods on attributes implemented  #
    # # in the various composit attribute classes     #
    # #################################################
    
    def ChangeCurrency(self, attrName, oldValue, newValue, *rest):
        self.currency = self.option_underlying.Currency()

    def ChangeOptionContractSize(self, attrName, oldFixing, newFixing, *rest):
        self.option_contractSize = SafeDivision( self.notional, newFixing, self.notional )

    def UpdateSettleDays(self, attrName, oldValue, newValue, *rest):
        # Make sure that both expiry and maturity are valid datetime values.
        # As it is possible to enter date periods in those fields
        # can we end up here before a transformation has been done on both
        # fields when a new package is created.
        if not (acm.Time().PeriodSymbolToDate(self.option_expiry) or acm.Time().PeriodSymbolToDate(self.bond_endDate)):
            if self.currency:
                cal = self.currency.Calendar()
            else:
                cal = self.Bond().Currency().Calendar()
            self.option_settleDays = cal.BankingDaysBetween(self.option_expiry, self.bond_endDate)

    def VerifyOptionQuotation(self, *rest):
        # Then the underlying is changed, the quotation of the option
        # is changed by the decorator. It needs to be Per Contract to be able
        # to view it as a % price of the nominal amount
        self.Option().Quotation('Per Contract')

    # ### Validation callbacks for attributes defeind in this class

    def ValidateSpotDays(self, attrName, newValue):
        self.ValidateDaysBetweenFinalFixingAndMaturity(attrName, newValue)

    def ValidateDaysBetweenFinalFixingAndMaturity(self, attrName, newValue):
        spot            = newValue if attrName == 'spotDays' else self.spotDays
        calendar        = newValue if attrName == 'bond_payCalendar' else self.bond_payCalendar
        finalFixing     = newValue if attrName == 'option_expiry' else self.option.TransformExpiry('option_expiry', self.option_expiry)
        maturity        = newValue if attrName == 'bond_endDate' else self.bond.TransformPeriodToEndDate('bond_endDate', self.bond_endDate)
        if spot and calendar and finalFixing and maturity:
            if calendar.BankingDaysBetween(finalFixing, maturity) <= spot:
                raise DealPackageUserException( 'Number of spot days must be smaller than number of days between final fixing and maturity.' )

    def ValidateExpiryBeforeEndDate(self, attrName, newValue):
        finalFixing     = newValue if attrName == 'option_expiry' else self.option.TransformExpiry('option_expiry', self.option_expiry)
        maturity        = newValue if attrName == 'bond_endDate' else self.bond.TransformPeriodToEndDate('bond_endDate', self.bond_endDate)
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
    def TransformPV(self, attrName, value):
        return self.MapSolverTopValueToComponent(value, attrName, {'coupon'          : 'bond',
                                                                   'barrierLevelPct' : 'option_pctBarrier',
                                                                   'strikePricePct'  : 'option_pctBarrier' })

    # ### Component access methods
    
    def InstrumentPartCurrencies(self):
        ccyObj = acm.FArray()
        ccyObj.Add(self.Option())
        ccyObj.Add(self.Bond())
        ccyObj.Add(self.BondLeg())
        return ccyObj
        
    def DealPartCurrencies(self):
        ccyObj = acm.FArray()
        ccyObj.AddAll(self.DealPackage().Trades())
        return ccyObj
        
    def Option(self):
        return self.InstrumentAt("Option")
    
    def Bond(self):
        return self.InstrumentAt("Bond")
    
    def BondLeg(self):
        return self.Bond().FirstFixedLeg()

    def OnInit(self):
        self._tradeQuantityMapping = []
        self.RegisterCallbackOnAttributeChanged(self.UpdateSettleDays, ['option_expiry',
                                                                        'bond_endDate'] )
        self.RegisterCallbackOnAttributeChanged(self.ChangeOptionContractSize, 'option_pctBarrier_initialFixing_initialFixing')
        self.RegisterCallbackOnAttributeChanged(self.ChangeCurrency, 'option_underlying')
        self.RegisterCallbackOnAttributeChanged(self.VerifyOptionQuotation)
        
    def OnNew(self):
        # When called though FValidation, a new Deal Package
        # is created but not a new instrument package.
        if self.InstrumentPackage().IsInfant():
            self.currency = self.Bond().Currency()
            self.spotDays = self.Bond().SpotBankingDaysOffset()
            self.bond_RegenerateCashFlows()

    def AssemblePackage(self):
        self._option = self.option.CreateInstrument()
        self._bond = self.bond.CreateInstrument()
    
    def IsValid(self, exceptionAccumulator, aspect):
        # First, call super to ensure that component validation is executed
        super(BarrierReverseConvertibleBase, self).IsValid(exceptionAccumulator, aspect)
        
        Validation_BarrierReverseConvertible.GeneralValidate(self, exceptionAccumulator)
        
        if aspect == 'DealPackage':
            Validation_BarrierReverseConvertible.GeneralValidateTradeParts(self, exceptionAccumulator)


# ######################################
# ### Deal Package based on two trades
# ######################################


class BarrierReverseConvertibleSTI(SalesTradingInteraction):
    createTradesOnRequest=True
    statusAttr='tradeInput_status'
    status='FO Confirmed'
    amountInfo = {'name' : 'Quantity',
                  'amountAttr' : 'tradeInput_quantity_value'} 
    tradeTimeAttr='tradeInput_tradeTime'
    clientAttr='tradeInput_counterparty' 
    acquirerAttr='tradeInput_acquirer'
    portfolioAttr='tradeInput_portfolio' 
    salesCustomPane='CustomPanes_SP_BarrierReverseConvertibleSingle_RFQ'
    tradingCustomPane='CustomPanes_SP_BarrierReverseConvertibleSingle_RFQ'
    allInPriceAttr='allInPrice',
    componentAttrs={
                    'Option'   : {'priceAttr' : 'optionPriceUnscaled', 'traderPrfAttr' : 'optionB2B_b2bPrf', 'traderAcqAttr' : 'optionB2B_b2bAcq'},
                    'Bond'     : {'priceAttr' : 'bondPrice',           'traderPrfAttr' : 'bondB2B_b2bPrf',   'traderAcqAttr' : 'bondB2B_b2bAcq'}
                   }
    
    def QuoteRequestComponents(self, mainTrade, dealPackage):
        components = acm.FDictionary()
        components.AtPut('Option', dealPackage.TradeAt('Option'))
        components.AtPut('Bond', dealPackage.TradeAt('Bond'))
        return components
    
    def QuantityFactor(self, dealPackage, componentName):
        quantityFactor = 0.0
        trade = dealPackage.TradeAt(componentName)
        dpQuantity = dealPackage.GetAttribute(self.amountInfo['amountAttr'])
        if abs(dpQuantity) > 1e-10:
            quantityFactor = trade.Quantity() / dpQuantity
        return quantityFactor
    
    def TraderPrice(self, dealPackage, prices):
        return dealPackage.GetAttribute('calculateTotalPrice')(prices)
    
    def TraderQuantity(self, dealPackage, quantities):
        return abs(dealPackage.GetAttribute('calculateTotalQuantity')(quantities))

@BarrierReverseConvertibleSTI()
class BarrierReverseConvertibleTrades(BarrierReverseConvertibleBase):

    optionPrice         = Object ( objMapping = 'OptionTradePrice',
                                   label = 'Option',
                                   formatter = "PercentShowZero",
                                   domain = 'double', 
                                   defaultValue = 0.0 )
    
    optionPriceUnscaled = Object(  objMapping = 'OptionTrade.Price')
    
    optionPremium       = Object ( objMapping = 'OptionTrade.Premium',
                                   label = '' )
    
    bondPrice           = Object ( objMapping = 'BondTrade.Price',
                                   #domain = 'float',
                                   label = 'Bond' )
    
    bondPremium         = Object ( objMapping = 'BondTrade.Premium',
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
    
    bondPV              = CalcVal ( calcMapping = 'BondTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                                    label = '' )

    totalPV             = CalcVal ( calcMapping = 'AsPortfolio:FPortfolioSheet:Portfolio Theoretical Value No Trade Payments',
                                    label = '',
                                    solverTopValue = True,
                                    transform = '@TransformPV' )
                                    
    # B2B Trades
    # ----------
    
    optionB2B           = TradeB2B ( uiLabel            = 'Option',
                                     b2bTradeParamsName = 'OptionB2BParams' )

    bondB2B             = TradeB2B ( uiLabel            = 'Bond',
                                     b2bTradeParamsName = 'BondB2BParams' )
                                     
    allInPrice          = Object   ( objMapping    = "AllInPrice")
    
    calculateTotalPrice     = Action ( action        = '@CalculateTotalPrice')
    
    calculateTotalQuantity  = Action ( action        = '@CalculateTotalQuantity')

    def TopValueFields(self):
        return {'PV':'totalPV'}

    def OptionTradePrice(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.OptionTrade().Price() / self.notional
        else:
            self.OptionTrade().Price( value * self.notional )

    def SumOfPrices(self, optionPrice, bondPrice):
        sum = 0
        if self.tradeInput_quantity_value:
            sum = (( optionPrice * 100.0 * self.OptionTrade().Quantity()
                     + bondPrice * self.BondTrade().Quantity() 
                    )
                   / self.tradeInput_quantity_value)     
        return sum
        
    def TotalPrice(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.SumOfPrices(self.OptionTradePrice(), self.BondTrade().Price())
               
    def TotalPremium(self, value = '*Reading*'):
        if value == '*Reading*':
            return (   
                       self.OptionTrade().Premium()
                     + self.BondTrade().Premium()
                   )

    def UpdateOptionContractPrice(self, value):
        oldPrice = self.OptionTrade().Price()
        oldNotional = self.Bond().ContractSize()
        pctPrice = oldPrice / oldNotional
        newPrice = pctPrice * value
        self.OptionTrade().Price(newPrice)

    def OptionTrade(self):
        return self.TradeAt("Option")
    
    def BondTrade(self):
        return self.TradeAt("Bond")
    
    def OptionB2BParams(self):
        return self.B2BTradeParamsAt('Option')
        
    def BondB2BParams(self):
        return self.B2BTradeParamsAt('Bond')
    
    def AssemblePackage(self):
        super(BarrierReverseConvertibleTrades, self).AssemblePackage()
        tradeOption = acm.DealCapturing().CreateNewTrade(self._option)
        tradeBond = acm.DealCapturing().CreateNewTrade(self._bond)
        self.DealPackage().AddTrade(tradeBond, "Bond")
        self.DealPackage().AddTrade(tradeOption, "Option")

    def OnInit(self):
        super(BarrierReverseConvertibleTrades, self).OnInit()
        self._allInPrice = 0.0

        bondTradeMapping = acm.FDictionary()
        bondTradeMapping.AtPut('trade', 'BondTrade')
        bondTradeMapping.AtPut('quantityFactor', lambda *args : 1.0)
        self._tradeQuantityMapping.append(bondTradeMapping)

        optTradeMapping = acm.FDictionary()
        optTradeMapping.AtPut('trade', 'OptionTrade')
        optTradeMapping.AtPut('quantityFactor', lambda *args : -1.0)
        self._tradeQuantityMapping.append(optTradeMapping)

    def LeadTrade(self):
        return self.BondTrade()
    
    def PriceLayout(self):
        return """
                hbox(;
                    vbox[Price;
                        optionPrice;
                        bondPrice;
                        totalPrice;
                        ];
                    vbox[Premium;
                        optionPremium;
                        bondPremium;
                        totalPremium;
                        ];
                    vbox[PV;
                        optionPV;
                        bondPV;
                        totalPV;
                        ];
                    );
                    """
                        

    def IsValid(self, exceptionAccumulator, aspect):
        # First, call super to ensure that BRC non trade validation is carried out
        super(BarrierReverseConvertibleTrades, self).IsValid(exceptionAccumulator, aspect)
        
        Validation_BarrierReverseConvertible.IndividualTradesValidate(self, exceptionAccumulator)
        
        if aspect == 'DealPackage':
            Validation_BarrierReverseConvertible.IndividualTradesValidateTradeParts(self, exceptionAccumulator)

    @ReturnDomainDecorator('double')
    def AllInPrice(self, value = '*Reading*'):
        if value =='*Reading*':
            return self._allInPrice
        else:
            self._allInPrice = value
            totalPrice = self.TotalPrice()
            totalMargin = value - totalPrice
            shouldSubtractSpread = -1 if self.tradeInput_quantity_value > 0.0 else 1
            self.SetAttribute('bondB2B_b2bEnabled', True)
            self.SetAttribute('bondB2B_b2bMargin', shouldSubtractSpread * totalMargin / 2.0)
            self.SetAttribute('optionB2B_b2bEnabled', True)
            self.SetAttribute('optionB2B_b2bMargin', shouldSubtractSpread * totalMargin / 2.0)

    def CalculateTotalPrice(self, attrName, prices):
        pctNomOptPrice = prices.At('Option') / self.notional
        return self.SumOfPrices(pctNomOptPrice, prices.At('Bond'))
    
    def CalculateTotalQuantity(self, attrName, quantities):
        return quantities.At('Bond')

    def CustomPanes(self):
        layout = self.GetCustomPanesFromExtValue('CustomPanes_SP_BarrierReverseConvertibleSingle')
        layout[0]['General'] = layout[0]['General'].replace('priceLayout', self.PriceLayout())
        return layout

# ######################################
# ### Deal Package based on combination
# ######################################
class BarrierReverseConvertibleCombination(BarrierReverseConvertibleBase):

    combinationPrice            = Object  ( objMapping = "CombinationTrade.Price",
                                            label = 'Price' )
    
    combinationPremium          = Object  ( objMapping = "CombinationTrade.Premium",
                                            label = 'Premium' )

    combinationContractSize     = Object  ( objMapping = "Combination.ContractSize")
    
    combinationPV               = CalcVal ( calcMapping = 'CombinationTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments',
                                            label = 'PV',
                                            solverTopValue = True,
                                            transform = '@TransformPV')


    def TopValueFields(self):
        return {'PV':'combinationPV'}
    
    def Combination(self):
        return self.InstrumentAt('Combination')

    def InstrumentPartCurrencies(self):
        currencies = super(BarrierReverseConvertibleCombination, self).InstrumentPartCurrencies()
        currencies.Add(self.Combination())
        return currencies
    
    def CombinationTrade(self):
        return self.TradeAt('Combination')
    
    def AssemblePackage(self):
        super(BarrierReverseConvertibleCombination, self).AssemblePackage()
        tradeCombination = self.DealPackage().CreateTrade('Combination', 'Combination')
        self.Combination().Quotation('Clean')
        self.DealPackage().AddCombinationMap(self._option, -1.0, 'Option', 'Combination')
        self.DealPackage().AddCombinationMap(self._bond, 1.0, 'Bond', 'Combination')
        
    def OnInit(self):
        super(BarrierReverseConvertibleCombination, self).OnInit()

        comboTradeMapping = acm.FDictionary()
        comboTradeMapping.AtPut('trade', 'CombinationTrade')
        comboTradeMapping.AtPut('quantityFactor', lambda *args : 1.0)
        self._tradeQuantityMapping.append(comboTradeMapping)

    def SetContractSizesFromNotional(self, value):
        super(BarrierReverseConvertibleCombination, self).SetContractSizesFromNotional(value)
        self.combinationContractSize = value

    def LeadTrade(self):
        return self.CombinationTrade()

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

    def IsValid(self, exceptionAccumulator, aspect):
        # First, call super to ensure that BRC non trade validation is carried out
        super(BarrierReverseConvertibleCombination, self).IsValid(exceptionAccumulator, aspect)

        Validation_BarrierReverseConvertible.CombinationValidate(self, exceptionAccumulator)

        if aspect == 'DealPackage':
            Validation_BarrierReverseConvertible.CombinationValidateTradeParts(self, exceptionAccumulator)

    def CustomPanes(self):
        layout = self.GetCustomPanesFromExtValue('CustomPanes_SP_BarrierReverseConvertibleSingleCombination')
        layout[0]['General'] = layout[0]['General'].replace('priceLayout', self.PriceLayout())
        return layout

def StartBRCCombination(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Barrier Reverse Convertible (Combination)')
    return  

def StartBRCTrades(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Barrier Reverse Convertible (Trades)')
    return  

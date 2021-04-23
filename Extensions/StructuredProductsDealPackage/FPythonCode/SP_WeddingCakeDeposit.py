

import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, ParseSuffixedFloat

from CompositeOptionComponents import BarrierOption
from CompositeCashFlowComponents import CD
from CompositeTradeComponents import StructuredTradeInput, TradeB2B
from StructuredProductBase import ProductBase

class WeddingCakeDepositTrades(StructuredTradeInput):
    
    _buySellLabels = ["Deposit", "Loan", "-"]
    _buySellChoiceListWidth = 10


class WeddingCakeDeposit(ProductBase):

    primaryRange         = BarrierOption ( optionName = "PrimaryRange",
                                           undType    = acm.FCommodity )
    
    secondaryRange       = BarrierOption ( optionName = "SecondaryRange",
                                           undType    = acm.FCommodity )
    
    deposit              = CD               ( cdName        = "Deposit",
                                              cdLegName     = "DepositLeg" )

    tradeInput          = WeddingCakeDepositTrades ( quantityMappingName  = "TradeQuantitySpecification",
                                                      priceLayout         = "PriceLayout" )

    primaryRangeB2B      = TradeB2B ( uiLabel            = 'Options',
                                      b2bTradeParamsName = 'PrimaryRangeB2BParams' )
    
    secondaryRangeB2B    = TradeB2B ( uiLabel            = 'Secondary Range',
                                      b2bTradeParamsName = 'SecondaryRangeB2BParams' )
    
    depositB2B           = TradeB2B ( uiLabel            = 'Deposit',
                                      b2bTradeParamsName = 'DepositB2BParams' )

    primaryRangeReturn   = Float ( label                 = 'Return',
                                   defaultValue          = 4.0,
                                   solverParameter       = '@SolverParameterPrimaryReturn',
                                   backgroundColor       = '@SolverColor',
                                   transform             = '@TransformSolver' )
    
    secondaryRangeReturn = Float ( label                 = 'Return',
                                   defaultValue          = 2.0,
                                   solverParameter       = '@SolverParameterSecondaryReturn',
                                   backgroundColor       = '@SolverColor',
                                   transform             = '@TransformSolver' )


    # Attributes only used as solver paramters
    primaryRangeSize     = Float ( label                 = 'Primary Range',
                                   solverParameter       = '@SolverParameterPrimaryRangeSize',
                                   backgroundColor       = '@SolverColor',
                                   onChanged             = '@SetPrimaryRangeFromSize' )
    
    secondaryRangeSize   = Float ( label                 = 'Secondary Range',
                                   solverParameter       = '@SolverParameterSecondaryRangeSize',
                                   backgroundColor       = '@SolverColor',
                                   onChanged             = '@SetSecondaryRangeFromSize' )

    # Calc values to be used for solving
    
    PV                   = CalcVal ( calcMapping = 'AsPortfolio:FPortfolioSheet:Portfolio Theoretical Value',
                                     label = 'Theor Val',
                                     solverTopValue = True )
    
    undSpot                = CalcVal( label="Underlying Spot",
                                      calcMapping="PrimaryRange:FDealSheet:Portfolio Underlying Price" )

    # ############################################################################
    # Non visible attributes that should be 
    # removed and logic accessing them replaced
    # when SPR XYZ has been fixed.
    # ############################################################################
    
    primaryRangeTradeQuantity     = Object ( objMapping = 'PrimaryRangeTrade.Quantity',
                                             visible    = False )
    
    secondaryRangeTradeQuantity   = Object ( objMapping = 'SecondaryRangeTrade.Quantity',
                                             visible    = False )

    depositTradeQuantity          = Object ( objMapping = 'DepositTrade.Quantity',
                                             visible    = False )

    def AttributeOverrides(self, overrideAccumulator):
    
        attrs = {}
        
        attrs['primaryRange'] = {
                    'strikePrice'        : dict ( solverParameter = False ),
                    'optionType'         : dict ( defaultValue = "Call" ),
                    'settlementType'     : dict ( defaultValue = "Cash" )
                    }
        
        attrs['primaryRange_barrier'] = {
                    'barrierLevel'       : dict ( solverParameter = False,
                                                  label = 'Lower' ),
                    'doubleBarrierLevel' : dict ( solverParameter = False,
                                                  label = 'Upper' ),
                    'barrierType'        : dict ( defaultValue = "Double Out" ),
                    'barrierMonitoring'  : dict ( defaultValue = "Continuous" )
                    }
        
        attrs['secondaryRange'] = {
                    'strikePrice'        : dict ( solverParameter = False ),
                    'optionType'         : dict ( defaultValue = "Call" ),
                    'settlementType'     : dict ( defaultValue = "Cash" )
                    }

        attrs['secondaryRange_barrier'] = {
                    'barrierLevel'       : dict ( solverParameter = False,
                                                  label = 'Lower' ),
                    'doubleBarrierLevel' : dict ( solverParameter = False,
                                                  label = 'Upper' ),
                    'barrierType'        : dict ( defaultValue = "Double Out" ),
                    'barrierMonitoring'  : dict ( defaultValue = "Continuous" )
                    }

        attrs['deposit'] = {
                    'coupon'    : dict ( solverParameter = False ),
                    'startDate' : dict ( defaultValue = '0d',
                                         width = 26 ), # to compensate the layout for the fix width in the buy sell control
                    'endDate'   : dict ( defaultValue = '1Y',
                                         label = 'Maturity' )
                    }

        attrs['depositB2B'] = {
                    'b2bPrice' : dict ( enabled = False )
                    }

        attrs['primaryRangeB2B'] = {
                    'b2bPrice' : dict ( enabled = False )
                    }

        attrs['secondaryRangeB2B'] = {
                    'b2bPrice' : dict ( enabled = False )
                    }

        attrs['tradeInput'] = {
                    'status'         : dict ( defaultValue = 'Simulated' ),
                    'quantity_value' : dict ( defaultValue = 1000000 ),
                    'quantity_buySell' : dict ( label = 'Cash Amount' )
                    }

        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })
                    
    def UpdatePrimaryRangeQuantity(self, *rest):
        self.primaryRangeTradeQuantity = self.SetPrimaryRangeNominal() * self.tradeInput_quantity_value

    def UpdateSecondaryRangeQuantity(self, *rest):
        self.secondaryRangeTradeQuantity = self.SetSecondaryRangeNominal() * self.tradeInput_quantity_value

    def UpdateDepositQuantity(self, *rest):
        self.depositTradeQuantity = self.SetDepositQuantity() * self.tradeInput_quantity_value

    # ############################################################################


    # ############################################################################
    # SOLVER FUNCTIONS
    # ############################################################################

    def SolverParameterPrimaryReturn(self, *rest):
        return {'minValue':self.secondaryRangeReturn, 'maxValue':100}

    def SolverParameterSecondaryReturn(self, *rest):
        return {'minValue':0.00001, 'maxValue':self.primaryRangeReturn}

    def GetMidPrice(self, range = 'primary'):
        mid = (getattr(self, '%sRange_barrier_doubleBarrierLevel' % range) + getattr(self, '%sRange_barrier_barrierLevel' % range)) / 2.0
        return mid or getattr(self, '%sRange_barrier_doubleBarrierLevel' % range) or self.primaryRange_underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value().Number()

    def SolverParameterPrimaryRangeSize(self, *rest):
        max = self.GetMidPrice('secondary') * 2 * 0.99
        return {'minValue':0.00001, 'maxValue':max}

    def SolverParameterSecondaryRangeSize(self, *rest):
        max = self.GetMidPrice('primary') * 2 * 0.99
        return {'minValue':self.primaryRange_barrier_doubleBarrierLevel - self.primaryRange_barrier_barrierLevel, 'maxValue':max}

    def TopValueFields(self):
        return {'PV':'PV'}
    
    def SetPrimaryRangeFromSize(self, *rest):
        mid = self.GetMidPrice('secondary')
        
        self.primaryRange_barrier_barrierLevel       = mid - self.primaryRangeSize / 2.0
        self.primaryRange_barrier_doubleBarrierLevel = mid + self.primaryRangeSize / 2.0

    def SetSecondaryRangeFromSize(self, *rest):
        mid = self.GetMidPrice('primary')
        self.secondaryRange_barrier_barrierLevel       = mid - self.secondaryRangeSize / 2.0
        self.secondaryRange_barrier_doubleBarrierLevel = mid + self.secondaryRangeSize / 2.0

    def TransformSolver(self, attrName, value):
        goalValue = None

        f = self.GetFormatter(self.TopValueFields().get('PV'))
        goalValue = ParseSuffixedFloat(value, suffix=['pv'], formatter=f)
        if goalValue != None:        
            return self.Solve(self.TopValueFields().get('PV'), attrName, goalValue)
        else:
            return value



    # END SOLVER #################################################################

    # #################################
    # Overrides of class ProductBase
    # #################################

    def DealPartCurrencies(self):
        dealPartCurrencies = acm.FArray()
        dealPartCurrencies.Add(self.PrimaryRangeTrade())
        dealPartCurrencies.Add(self.SecondaryRangeTrade())
        dealPartCurrencies.Add(self.DepositTrade())
        return dealPartCurrencies
    
    def InstrumentPartCurrencies(self):
        instrumentPartCurrencies = acm.FArray()
        instrumentPartCurrencies.Add(self.PrimaryRange())
        instrumentPartCurrencies.Add(self.SecondaryRange())
        instrumentPartCurrencies.Add(self.Deposit())
        instrumentPartCurrencies.Add(self.DepositLeg())
        return instrumentPartCurrencies
    
    def Notional(self, value = '*READ*'):
        if value == '*READ*':
            return self.deposit_contractSize
        else:
            self.deposit_contractSize = value

    # ##############################
    # Quantity mapping methods 
    # ##############################
 
    def SetPrimaryRangeNominal(self, *rest):
        return -(self.primaryRangeReturn - self.secondaryRangeReturn) * 0.01 * self.YearsToMaturity()
    
    def SetSecondaryRangeNominal(self, *rest):
        return -self.secondaryRangeReturn * 0.01 * self.YearsToMaturity()

    def SetDepositQuantity(self, *rest):
        return -1 / self.notional

    # ##############################
    # Component access
    # ##############################

    def PrimaryRange(self):
        return self.InstrumentAt("PrimaryRange")

    def PrimaryRangeTrade(self):
        return self.TradeAt("PrimaryRange")
    
    def SecondaryRange(self):
        return self.InstrumentAt("SecondaryRange")

    def SecondaryRangeTrade(self):
        return self.TradeAt("SecondaryRange")
    
    def Deposit(self):
        return self.InstrumentAt("Deposit")
    
    def DepositLeg(self):
        return self.Deposit().FirstFixedLeg()

    def DepositTrade(self):
        return self.TradeAt("Deposit")

    def PrimaryRangeB2BParams(self):
        return self.B2BTradeParamsAt("PrimaryRange")
    
    def SecondaryRangeB2BParams(self):
        return self.B2BTradeParamsAt("SecondaryRange")
    
    def DepositB2BParams(self):
        return self.B2BTradeParamsAt("Deposit")

    # ##############################
    # Dev Kit methods
    # ##############################

    def LeadTrade(self):
        return self.DepositTrade()

    def GraphYValues(self, xValues):
        return [-y for y in DealPackageDefinition.GraphYValues(self, xValues)]

    def OnOpen(self):
        self.SetRangeReturnsOnOpen()

    def OnNew(self):
    
        if self.InstrumentPackage().IsInfant():
        
            if (   self.primaryRange_underlying is None 
                or not self.primaryRange_underlying.IsKindOf(acm.FCommodity) 
                or not self.primaryRange_underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value().Number()
                or (self.primaryRange_underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value().Number() != self.primaryRange_underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value().Number())):
                # Ensure that application started with commodity underlying as default
                for und in [acm.FCommodity['Silver']] + [acm.FCommodity['AG']] + list(acm.FCommodity.Select("")):
                    if und:
                        undPrice = und.Calculation().MarketPrice(self._GetStdCalcSpace()).Value().Number()
                        if undPrice and undPrice == undPrice:
                            self.primaryRange_underlying = und
                            break
                else:
                    DealPackageException("ERROR - Can't find a commodity with a price to set as underlying")
            else:
                self.SetCurrencyToUnderlyingCurrency()
                self.UpdateExpiry()
                self.UpdateStrikeQuotations()
                self.UpdateRanges()

            # Set notional default value for new instrument packages
            if self.InstrumentPackage().IsInfant():
                self.notional = 1000000
        
        else:
            self.SetRangeReturnsOnOpen()

    def OnInit(self):

        self._tradeQuantityMapping = [
            {'trade':'PrimaryRangeTrade', 'quantityFactor':self.SetPrimaryRangeNominal},
            {'trade':'SecondaryRangeTrade', 'quantityFactor':self.SetSecondaryRangeNominal},
            {'trade':'DepositTrade', 'quantityFactor':self.SetDepositQuantity}]
        
        self.RegisterCallbackOnAttributeChanged(self.UpdatePrimaryRangeQuantity, ['primaryRangeReturn',
                                                                                  'secondaryRangeReturn', 
                                                                                  'deposit_startDate', 
                                                                                  'deposit_endDate', 
                                                                                  'currency'] )
        self.RegisterCallbackOnAttributeChanged(self.UpdateSecondaryRangeQuantity, ['secondaryRangeReturn', 
                                                                                    'deposit_startDate', 
                                                                                    'deposit_endDate', 
                                                                                    'currency'] )
        self.RegisterCallbackOnAttributeChanged(self.UpdateDepositQuantity, ['notional'])
        self.RegisterCallbackOnAttributeChanged(self.SetCurrencyToUnderlyingCurrency, ['primaryRange_underlying'])
        self.RegisterCallbackOnAttributeChanged(self.UpdateExpiry, ['primaryRange_underlying', 
                                                                    'deposit_endDate'])
        self.RegisterCallbackOnAttributeChanged(self.UpdateStrikeQuotations, ['primaryRange_underlying'])
        self.RegisterCallbackOnAttributeChanged(self.UpdateRanges, ['primaryRange_underlying'])
        self.RegisterCallbackOnAttributeChanged(self.SetOptionTradePriceFromTheor)

    
        optionFieldsToAlign = ['_optionType',
                               '_settlementType',
                               '_quotation',
                               '_valuationGroup',
                               '_settleDays',
                               '_underlying',
                               '_contractSize',
                               '_expiry',
                               '_barrier_barrierType',
                               '_barrier_barrierMonitoring',
                               'B2B_b2bEnabled',
                               'B2B_b2bPrf',
                               'B2B_b2bAcq' ]

        for field in optionFieldsToAlign:
            field1 = 'primaryRange%s' % (field)
            field2 = 'secondaryRange%s' % (field)
            self.RegisterAlignmentAcrossComponents([field1,
                                                    field2])


    def AssemblePackage(self):

        # Check if there are certain values that should be set

        _primaryRange = self.primaryRange.CreateInstrument()
        _secondaryRange = self.secondaryRange.CreateInstrument()
        _primaryRange.PayType("Spot")
        _secondaryRange.PayType("Spot")
        _primaryRange.Digital(True)
        _secondaryRange.Digital(True)
        _primaryRange.Rebate(1.0)
        _secondaryRange.Rebate(1.0)
        _primaryRange.Exotic().DigitalBarrierType('Barrier')
        _secondaryRange.Exotic().DigitalBarrierType('Barrier')
        
        _tradePrimaryRange = acm.DealCapturing().CreateNewTrade(_primaryRange)
        _tradeSecondaryRange = acm.DealCapturing().CreateNewTrade(_secondaryRange)
        _deposit = self.deposit.CreateInstrument()
        _tradeDeposit = acm.DealCapturing().CreateNewTrade(_deposit)
        self.DealPackage().AddTrade(_tradePrimaryRange, "PrimaryRange")
        self.DealPackage().AddTrade(_tradeSecondaryRange, "SecondaryRange")
        self.DealPackage().AddTrade(_tradeDeposit, "Deposit")


    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_WeddingCakeDeposit')

    def ValidateRange(self, exceptionAccumulator):
        if self.primaryRange_barrier_barrierLevel < self.secondaryRange_barrier_barrierLevel or self.primaryRange_barrier_doubleBarrierLevel > self.secondaryRange_barrier_doubleBarrierLevel:
            exceptionAccumulator( 'Primary Range has to be in Secondary Range' )
        if self.primaryRangeReturn < self.secondaryRangeReturn:
            exceptionAccumulator( 'Primary Range Return has to be greater than Secondary Range Return' )
        if self.primaryRange_barrier_barrierLevel > self.primaryRange_barrier_doubleBarrierLevel or self.secondaryRange_barrier_barrierLevel > self.secondaryRange_barrier_doubleBarrierLevel:
            exceptionAccumulator( 'Upper range has to be grater than Lower Range' )

    def IsValid(self, exceptionAccumulator, aspect):
        
        super(WeddingCakeDeposit, self).IsValid(exceptionAccumulator, aspect)
        
        self.ValidateRange(exceptionAccumulator)

        if not (self.PrimaryRange() and self.SecondaryRange() and self.Deposit() and self.DealPackage().Instruments().Size() == 3):
            exceptionAccumulator( 'Wedding Cake deposit should consist of two options and one deposit' )
            
        if not (self.PrimaryRangeTrade() and self.SecondaryRangeTrade() and self.DepositTrade() and self.DealPackage().Trades().Size() == 3):
            exceptionAccumulator( 'Wedding Cake Deposit should consist of one Deposit Trade and two Option Trades' )

    # ###################################
    # On Changed callbacks
    # ###################################

    def SetOptionTradePriceFromTheor(self, name, *args):
    
        if self._MinorChange(name):
            return
        if not (self.primaryRange_barrier_barrierLevel and self.secondaryRange_barrier_barrierLevel and self.primaryRange_barrier_doubleBarrierLevel and self.secondaryRange_barrier_doubleBarrierLevel):
            return
        try:
            self.DepositTrade().Price(self.DepositTrade().Calculation().TheoreticalPrice(self._GetStdCalcSpace()))
        except Exception as e:
            print ('Failed to calculate theoretical price for deposit', e)
        try:
            self.PrimaryRangeTrade().Price(self.PrimaryRangeTrade().Calculation().TheoreticalPrice(self._GetStdCalcSpace()))
        except Exception as e:
            print ('Failed to calculate theoretical price for primary range', e, name)
        try:
            self.SecondaryRangeTrade().Price(self.SecondaryRangeTrade().Calculation().TheoreticalPrice(self._GetStdCalcSpace()))
        except Exception as e:
            print ('Failed to calculate theoretical price for secondary range', e, name)
        optionPrice = -self.tradeInput_quantity_value + self.DepositTrade().Premium()
        theorPrice = -self.PrimaryRangeTrade().Premium() - self.SecondaryRangeTrade().Premium()
        if theorPrice:
            priceFactor = optionPrice / theorPrice
            self.PrimaryRangeTrade().Price = self.PrimaryRangeTrade().Price() * priceFactor
            self.SecondaryRangeTrade().Price = self.SecondaryRangeTrade().Price() * priceFactor
        else:
            self.PrimaryRangeTrade().Price = optionPrice / 2.0 / self.PrimaryRangeTrade().Quantity()
            self.SecondaryRangeTrade().Price = optionPrice / 2.0 / self.SecondaryRangeTrade().Quantity()
        #Added to avoid rounding errors, the total premium should always sum up to the nominal
        self.SecondaryRangeTrade().Premium = -optionPrice - self.PrimaryRangeTrade().Premium()
        self.spotDays = 2

    def UpdateExpiry(self, *rest):
        if self.primaryRange_underlying and self.deposit_endDate:
            self.primaryRange_expiry = self.primaryRange_underlying.Currency().Calendar().AdjustBankingDays(self.deposit_endDate, 
                                                                                                    -self.primaryRange_underlying.SpotBankingDaysOffset())
        else:
            self.primaryRange_expiry = self.deposit_endDate

    def UpdateStrikeQuotations(self, *rest):
        self.PrimaryRange().StrikeQuotation(self.PrimaryRange().Quotation())
        self.SecondaryRange().StrikeQuotation(self.SecondaryRange().Quotation())
    
    def UpdateRanges(self, *rest):
        undPrice = self.primaryRange_underlying.Calculation().MarketPrice(self._GetStdCalcSpace()).Value().Number()
        self.secondaryRange_barrier_doubleBarrierLevel = round(undPrice * 1.2, 1)
        self.primaryRange_barrier_doubleBarrierLevel = round(undPrice * 1.1, 1)
        self.primaryRange_barrier_barrierLevel = round(undPrice * 0.9, 1)
        self.secondaryRange_barrier_barrierLevel = round(undPrice * 0.8, 1)

    def SetCurrencyToUnderlyingCurrency(self, *rest):
        self.currency = self.primaryRange_underlying.Currency()

    def YearsToMaturity(self):
        return self.currency.Calendar().CalendarInformation().YearsBetween(self.deposit_startDate, self.deposit_endDate, self.currency.DayCountMethod())

    # #####################
    # Utility methods
    # #####################

    def SetRangeReturnsOnOpen(self):
        primaryRangeQuantity      = self.primaryRangeTradeQuantity
        secondaryRangeQuantity    = self.secondaryRangeTradeQuantity
        tradeInputQuantity        = self.tradeInput_quantity_value
        
        self.secondaryRangeReturn = secondaryRangeQuantity / -tradeInputQuantity * 100 / self.YearsToMaturity()
        self.primaryRangeReturn   = primaryRangeQuantity / -tradeInputQuantity * 100 / self.YearsToMaturity() + self.secondaryRangeReturn


    
def StartWCD(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'SP_WeddingCakeDeposit')
    return  


import acm
import decimal, math
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart

from SP_DealPackageHelper import IsDateTime
from CompositeOptionComponents import FxOption
from CompositeCashFlowComponents import Deposit
from CompositeTradeComponents import TradeInput, TradeB2B
from StructuredProductBase import ComponentBasedDealPackage

class DualCurrencyDepositTrades(TradeInput):
    
    _quantityMapping = 'DepositTrade.CashAmount|FxoTrade.AmountForeign'
    _buySellLabels = ["Deposit", "Loan", "-"]
    _buySellChoiceListWidth = 10

class DualCurrencyDeposit(ComponentBasedDealPackage):

    ipName              = Object  ( objMapping  = 'InstrumentPackage.Name',
                                    label       = 'Name' )


    currency            = Object ( label        = 'Currency',
                                   toolTip      = "The leading currency",
                                   defaultValue = "EUR",
                                   objMapping   = (InstrumentPart("Deposit.ChangeCurrency|FXO.Currency|FXO.FxoPremiumCurr").
                                                   DealPart("DealPartCurrencies.Currency" ) ) )

    # Composite components (FXO, Deposit, trades and 2 B2B)

    fxo                 = FxOption        ( optionName     = "FXO" )

    deposit             = Deposit         ( depositName    = "Deposit",
                                            depositLegName = "DepositLeg" )

    tradeInput          = DualCurrencyDepositTrades ( priceLayout         = "PriceLayout" )

    fxoB2B              = TradeB2B ( uiLabel            = 'FX Option',
                                     b2bTradeParamsName = 'FxoB2BParams' )
    
    depositB2B          = TradeB2B ( uiLabel            = 'Deposit',
                                     b2bTradeParamsName = 'DepositB2BParams' )


    # Additional trade fields

    nominalCurr2        = Object( objMapping    = "FxoTrade.AmountDomestic",
                                  label         = "@NominalCurr2Label",
                                  enabled       = False )

    # Risk factors to be displayed in the UI and possible to simulate
    irCurr1         = CalcVal( label="@IntRateCurr1Label",
                               calcMapping="FxoTrade:FDealSheet:Foreign Repo Rate" )
       
    irCurr2         = CalcVal( label="@IntRateCurr2Label",
                               calcMapping="FxoTrade:FDealSheet:Domestic Repo Rate" )
    
    volatility      = CalcVal( label="Volatility",
                               calcMapping="FxoTrade:FDealSheet:Portfolio Volatility" )
    
    undVal          = CalcVal( label="Und. Spot",
                               calcMapping="FxoTrade:FDealSheet:Underlying Value")
                            
    undFwd          = CalcVal( label="Und. Fwd",
                               calcMapping="FxoTrade:FDealSheet:Portfolio Underlying Forward Value From Spot" )

    # Calculated values
    maxYield        = Float(   label="Max Yield",
                               enabled=False )

    
    customerYield   = Float(   label="Customer Yield",
                               onChanged="@SetSalesCommission")

    endIntCurr1     = Float(   label="@EndInterestCurr1Label",
                               enabled=False )

    salesCommission = Float(   label="Sales Commission",
                               onChanged="@PerformTouch")


    def AttributeOverrides(self, overrideAccumulator):
        attrs = {}
        
        attrs['deposit'] = {
                'endDate'   : dict ( transform = '@TransformPeriodToEndDate',
                                     defaultValue = '1m',
                                     toolTip = "The Maturity Date of the Dual Currency Deposit" ),
                'startDate' : dict ( onChanged = '@SetEndDateAfterStartDate',
                                     defaultValue = '0d',
                                     toolTip = "The start day of the Deposit",
                                     width = 26 )  # to compensate the layout for the fix width in the buy sell control
                }
        
        attrs['fxo'] = {
                'expiryDate'       : dict ( enabled = False,
                                            defaultValue = '1m',
                                            label = 'Notify Date',
                                            toolTip = "The Expiry Date of the FX Option" ),
                'optionType'       : dict ( defaultValue = 'Call' ),
                'foreignCurrency'  : dict ( defaultValue = 'EUR',
                                            label = 'Currency',
                                            toolTip = "The leading currency" ),
                'domesticCurrency' : dict ( defaultValue = 'USD',
                                            label = 'Alt Currency',
                                            toolTip = 'The alternative currency' ),
                'strikeDomesticPerForeign' : dict ( label = 'Conversion Rate' )
                }

        attrs['tradeInput'] = {
                'status'         : dict ( defaultValue = 'Simulated' ),
                'quantity_value' : dict ( defaultValue = 1000000 ),
                'quantity_buySell' : dict ( label = 'Cash Amount' )
                }

        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })

    # ### _default callbacks, would be nice to replace these if possible ###############
    '''** Customer DCD Yield **'''
    def _customerYield_default(self):
        return self.GetDCDYield(self.GetEndInterestCurrency1())
    
    def _salesCommission_default(self):
        return self.GetTheorFXOInterest() - self.GetFXOInterest()
    
    # ###################################################################

    def PriceLayout(self):
        return ''

    # ###############################################
    # ### Calculations, methods for handling values in float attributes

    def SetEndInterestCurrency1(self):
        self.endIntCurr1 = self.GetEndInterestCurrency1()

    def GetTotalInterest(self):
        return self.tradeInput_quantity_value * 0.01 * self.YearsBetween() * self.customerYield

    def GetEndInterestCurrency1(self):
        return self.GetEndMaxInterestCurrency1() - self.salesCommission

    def GetFXOInterest(self):
        return -self.FxoTrade().ForwardPremium()

    def SetFXOInterest(self):
        fwdPremium = -(self.GetTheorFXOInterest()-self.salesCommission)
        self.FxoTrade().ForwardPremium(fwdPremium)
    
    def SetMaxYield(self):
        maxInterest = self.GetEndMaxInterestCurrency1()
        self.maxYield = self.GetDCDYield(maxInterest)    
    
    def GetEndMaxInterestCurrency1(self):
        return self.GetDepositInterest() + self.GetTheorFXOInterest()

    def GetDepositInterest(self):
        return self.tradeInput_quantity_value * 0.01 * self.YearsBetween() * self.deposit_coupon

    def YearsBetween(self):
        startDate = self.deposit_startDate
        endDate = self.deposit_endDate
        #calendarInfo = self.deposit_payCalendar.CalendarInformation()
        calendarInfo = self.DepositLeg().PayCalendar().CalendarInformation()
        return calendarInfo.YearsBetween(startDate, endDate, self.DepositLeg().DayCountMethod())   

    def GetTheorFXOInterest(self):
        return -self.GetFXOTradeForwardPremiumFromTheor()

    def GetFXOTradeForwardPremiumFromTheor(self):
        fxoTrade = self.FxoTrade().Trade().Clone()
        fxoTrade.RegisterInStorage()
        fxoTrade.Price = self.CalculateFxoTheorPrice()
        fxoTradeDec = acm.FBusinessLogicDecorator.WrapObject(fxoTrade)
        return fxoTradeDec.ForwardPremium()

    def CalculateFxoTheorPrice(self):
        premiumCurrency = self.FxoTrade().Currency()
        quotation = self.FXO().Quotation()
        definition = {'Quotation':quotation, 'Currency':premiumCurrency}
        configuration = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(definition)
        calc = self._GetCalcSpace('FDealSheet').CreateCalculation(self.FXO().Instrument(), "Price Theor Parameters", configuration)
        theorPrice = calc.Value().Number()
        return theorPrice

    def GetDCDYield(self, interest):
        return self.YieldFromCoupon(interest, self.tradeInput_quantity_value)

    def SetDCDYield(self):
        customerInterest = self.GetEndInterestCurrency1()
        self.customerYield = self.GetDCDYield(customerInterest)

    def YieldFromCoupon(self, interest, nominal):
        years = self.YearsBetween()
        if nominal and years:
            return ( interest / nominal ) * ( 1 / years ) * 100
        return 0.0
    
    #
    # ### End calculations
    # ###############################################


    # ### Label Callbacks ### #

    def EndInterestCurr1Label(self, *args):
        if self.fxo_foreignCurrency:
            return "End Int. " + self.fxo_foreignCurrency.Name()
        else:
            return "End Int."

    def NominalCurr2Label(self, *rest):
        if self.fxo_domesticCurrency:
            return "Nominal " + self.fxo_domesticCurrency.Name()
        else:
            return "Nominal"

    def IntRateCurr1Label(self, *args):
        if self.fxo_foreignCurrency:
            return "Int. Rate " + self.fxo_foreignCurrency.Name()
        else:
            return "Int. Rate"

    def IntRateCurr2Label(self, *args):
        if self.fxo_domesticCurrency:
            return "Int. Rate " + self.fxo_domesticCurrency.Name()
        else:
            return "Int. Rate"

    # Utility methods - TODO: Move to general calculations and remove rounding
    def CalculateConversionRate(self):
        currency = self.fxo_foreignCurrency
        altCurrency = self.fxo_domesticCurrency
        maturityDate = self.TransformPeriodToEndDate(None, self.deposit_endDate)
        fxRate = 1
        if currency and altCurrency:
            try:
                fxRate = currency.Calculation().FXRate(self._GetStdCalcSpace(), altCurrency, maturityDate).Value().Number()
                fxRate = round(decimal.Decimal(str(fxRate)), 4)
            except Exception as e:
                raise DealPackageException("No exchange rate for chosen currency pair, " + str(e))
        return fxRate

    # ### On Changed Callbacks ### #
            
    def SetConversionRate(self, *rest):
        self.fxo_strikeDomesticPerForeign = self.CalculateConversionRate()
    
    def SetDepositCoupon(self, *rest):
        self.deposit.SetParRate()
    
    def SetConversionRateIfZero(self, *rest):
        if self.fxo_strikeDomesticPerForeign == 0.0:
            self.SetConversionRate()

    def SetNotifyDate(self, name, oldDate, newDate, *args):
        currPair = self.FxoTrade().CurrencyPair(True)
        if currPair:
            self.fxo_expiryDate = self.FXO().SpotDateInverted(newDate)

    def SetSalesCommission(self, *args):
        totalInterest = self.GetTotalInterest()
        depoInterest = self.GetDepositInterest()
        fxoInterest = self.GetTheorFXOInterest()
        salesCommission = fxoInterest + depoInterest - totalInterest
        if math.isnan(salesCommission):
            salesCommission = 0.0
        self.salesCommission = salesCommission
        # Check, whay a second touch, this is already a registered on change callback on salesCommisson
        #self.PerformTouch()


    # ########################################
    # ### Intercept behaviour from composite components ### #
    # ########################################

    def TransformPeriodToEndDate(self, attrName, value):
        deliveryDate = value
        startDate = self.deposit.TransformPeriodToStartDate(None, self.deposit_startDate)
        if acm.Time().PeriodSymbolToDate(value) and startDate:
            currPair = self.FxoTrade().CurrencyPair(True)
            if currPair:
                invertedSpot = self.FXO().SpotDateInverted(startDate)
                deliveryDate = currPair.ForwardDate(invertedSpot, value)
            else:
                deliveryDate = self.Deposit().LegEndDateFromPeriod(value)
        return deliveryDate

    def SetEndDateAfterStartDate(self, *rest):
        if IsDateTime(self.deposit_startDate) and IsDateTime(self.deposit_endDate):
            if acm.Time.DateDifference(self.deposit_startDate, self.deposit_endDate) >= 0:            
                currPair = self.FxoTrade().CurrencyPair(True)
                if currPair:
                    deliveryDate = currPair.ForwardDate(self.deposit_startDate, '1d')
                else:
                    deliveryDate = self.Deposit().LegEndDateFromPeriod('1d')
                self.SetAttribute('deposit_endDate', deliveryDate, silent=True)

    # ########################################
    # ### Dev kit overrides
    # ########################################

    def GraphXValues(self):
        strike = self.fxo_strikeDomesticPerForeign
        return [strike * 0.95, strike * 0.975, strike, strike * 1.025, strike * 1.05]

    def GraphYValues(self, xValues):
        depoInt = self.GetDepositInterest()
        trade = self.FxoTrade()
        
        volAndTimeDim = self.CreateVolAndTimeDimension(trade.Instrument())
        priceAttributes = acm.GetDefaultContext().MemberNames("FExtensionAttribute", "risk factors", "market price")
        priceDim = self.CreateXValueDimension(priceAttributes, xValues)
        config = self.CreateScenarioConfig([volAndTimeDim, priceDim])
        
        calc = self._GetCalcSpace().CreateCalculation(trade, "Portfolio Theoretical Value", config)
        yValues = []
        for x in calc.Value():
            yValues.append(depoInt-x.Number()) 
        return yValues

    def Refresh(self):
        # As the calculated values updated by the methods below should change
        # when the market date changes as well as when input data changes
        # the decision was made to use the Refresh method rather than having 
        # onCahnged callbacks on all market data calcVals.
        self.SetFXOInterest()
        self.SetEndInterestCurrency1()
        self.SetDCDYield()
        self.SetMaxYield()
    
    def DealPartCurrencies(self, *rest):
        return self.Trades()

    def OnOpen(self):
        #Set values on transient attributes
        self.SetEndInterestCurrency1()
        self.SetMaxYield()

    def OnInit(self):
        
        # Register callbacks on fields defined on the composite components
        self.RegisterCallbackOnAttributeChanged(self.SetConversionRate, ['fxo_foreignCurrency',
                                                                         'fxo_domesticCurrency'])
        self.RegisterCallbackOnAttributeChanged(self.SetConversionRateIfZero, 'deposit_endDate')
        self.RegisterCallbackOnAttributeChanged(self.SetNotifyDate, 'deposit_endDate')
        self.RegisterCallbackOnAttributeChanged(self.SetDepositCoupon, ['deposit_endDate',
                                                                        'deposit_startDate',
                                                                        'currency'] )
        
        # Register alignment accross the different components
        self.RegisterAlignmentAcrossComponents(['currency',
                                                'fxo_foreignCurrency'])

        self.RegisterAlignmentAcrossComponents(['tradeInput_valueDay',
                                                'deposit_startDate'])




    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_DualCurrencyDeposit')

    def OnNew(self):
        if not self.InstrumentPackage().IsInfant():
            self.tradeInput_valueday = self.deposit_startDate
        
        #self.salesCommission = self.GetTheorFXOInterest() - self.GetFXOInterest()
        #self.customerYield = self.GetDCDYield(self.GetEndInterestCurrency1())
        #self.salesCommission = self.GetTheorFXOInterest() - self.GetFXOInterest()
    
        self.SetConversionRate(None, None, None, None)
        self.SetConversionRateIfZero(None, None, None, None)
        self.SetDepositCoupon(None, None, None, None)
        self.SetNotifyDate(None, None, self.deposit_endDate, None)
        
    def AssemblePackage(self):
        _option = self.fxo.CreateInstrument()
        _option.PayType("Forward")
        _tradeOption = acm.DealCapturing().CreateNewTrade(_option)
        _deposit = self.deposit.CreateInstrument()
        _tradeDeposit = acm.DealCapturing().CreateNewTrade(_deposit)
        self.DealPackage().AddTrade(_tradeOption, "FXO")
        self.DealPackage().AddTrade(_tradeDeposit, "Deposit")
    
    def FXO(self):
        return self.InstrumentAt("FXO")
    
    def FXOBase(self):
        return self.FXO().DecoratedObject()

    def Deposit(self):
        return self.InstrumentAt("Deposit")
    
    def DepositBase(self):
        return self.Deposit().DecoratedObject()
    
    def DepositLeg(self):
        return self.Deposit().FirstFixedLeg()
    
    def FxoTrade(self):
        return self.TradeAt("FXO")

    def DepositTrade(self):
        return self.TradeAt("Deposit")

    def LeadTrade(self):
        return self.DepositTrade()

    def FxoB2BParams(self):
        return self.B2BTradeParamsAt("FXO")

    def DepositB2BParams(self):
        return self.B2BTradeParamsAt("Deposit")

    # Convenience methods

    def PerformTouch(self, *rest):
        self.DealPackage().Touch()
        self.DealPackage().Changed()

    # Note: The three methods below are the same methods that are used in module
    #       DealPackagePayoffGraphCalculations by the standard graph coordinates methods
    #       However, they are not published on the DealPackageDefinition class
    #       and we need them for the calculation of our Y values.
    def CreateScenarioConfig(self, dimensions):
        scenario = acm.FExplicitScenario()
        for d in dimensions:
            scenario.AddDimension(d)
        config = acm.Sheet().Column().ConfigurationFromScenario(scenario, None)
        return config
    
    def CreateXValueDimension(self, extAttr, xValues):
        dim = acm.FDirectScenarioDimension()
        scm = acm.CreateScenarioMember(acm.GetFunction("replaceNumericValue", 2), extAttr, acm.FObject, xValues)
        dim.AddScenarioMember( scm )
        return dim
    
    def CreateVolAndTimeDimension(self, instrument):
        def GetValuationOffset(instrument):
            valuationOffset = 0
            timeToExpiry = self._GetCalcSpace().CreateCalculation(instrument, "Time to Expiry")
            if timeToExpiry.Value():
                spotDateInverted = instrument.SpotDateInverted(instrument.ExpiryDateOnly())
                holidayAdjustedSpot = acm.Time().DateDifference(acm.Time.AsDate(instrument.ExpiryDateOnly()), spotDateInverted)
                valuationOffset = timeToExpiry.Value() - holidayAdjustedSpot - 1
            return valuationOffset
        
        dim = acm.FDirectScenarioDimension()
        valuationOffset = GetValuationOffset(instrument)
        volaScm = acm.CreateScenarioMember(acm.GetFunction("*", 2), "volatility", acm.FObject, [0])
        timeScm = acm.CreateScenarioMember(acm.GetFunction("fixedvalue", 2), "valuationBaseDateTimeOffsetInput", acm.FObject, [valuationOffset])
        dim.AddScenarioMember( volaScm )
        dim.AddScenarioMember( timeScm )
        return dim


def StartDCD(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Dual Currency Deposit')
    return  

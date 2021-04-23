
import acm
from DealPackageDevKit import Object, CalcVal, ReturnDomainDecorator, Action, CustomActions, TradeActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand, Settings, SalesTradingInteraction
from StructuredProductBase import ProductBase
from CompositeOptionComponents import Option
from SP_CustomTradeActions import UpdatePriceAction
from CompositeTradeComponents import TradeB2B   
    
class CallPutSpreadSTI(SalesTradingInteraction):
    createTradesOnRequest=True
    statusAttr='tradeInput_status'
    status='FO Confirmed'
    amountInfo = {'name' : 'Quantity',
                  'amountAttr' : 'tradeInput_quantity_value'} 
    tradeTimeAttr='tradeInput_tradeTime'
    clientAttr='tradeInput_counterparty' 
    acquirerAttr='tradeInput_acquirer'
    portfolioAttr='tradeInput_portfolio' 
    salesCustomPane='CustomPanes_SP_CallPutSpreadRFQ'
    allInPriceAttr='allInPrice',
    componentAttrs={
                    'Low'   : {'priceAttr' : 'lowPrice', 'traderPrfAttr' : 'lowB2B_b2bPrf', 'traderAcqAttr' : 'lowB2B_b2bAcq'},
                    'High'  : {'priceAttr' : 'highPrice', 'traderPrfAttr' : 'highB2B_b2bPrf', 'traderAcqAttr' : 'highB2B_b2bAcq'}
                   }
    
    def QuoteRequestComponents(self, mainTrade, dealPackage):
        components = acm.FDictionary()
        components.AtPut('Low', dealPackage.TradeAt('Low'))
        components.AtPut('High', dealPackage.TradeAt('High'))
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

@CallPutSpreadSTI()
@CustomActions(updatePrices = UpdatePriceAction(FieldMapping = [{'FromField':'highTheor',  'ToField':'highPrice'},
                                                                {'FromField':'lowTheor', 'ToField':'lowPrice'}]))
@TradeActions( correct = CorrectCommand(statusAttr='tradeInput_status', newStatus='FO Confirmed'),
               novate = NovateCommand(statusAttr='tradeInput_status', nominal='tradeInput_quantity_value'),
               close  = CloseCommand(statusAttr='tradeInput_status', nominal='tradeInput_quantity_value'),
               mirror = MirrorCommand(statusAttr='tradeInput_status', newStatus='Simulated', quantityAttr='tradeInput_quantity_value'))
@Settings(MultiTradingEnabled=True)
class CallPutSpread(ProductBase):
    
    # Components
    # ----------
    highOption           = Option( optionName="HighOption",
                                   undType=acm.FStock )
                                                    
    lowOption            = Option( optionName="LowOption",
                                   undType=acm.FStock )
    
    # B2B Trades
    # ----------
    
    highB2B                 = TradeB2B ( uiLabel            = 'High Option',
                                         b2bTradeParamsName = 'HighOptionB2BParams' )


    lowB2B                  = TradeB2B ( uiLabel            = 'Low Option',
                                         b2bTradeParamsName = 'LowOptionB2BParams' )
    
    # Pricing fields
    # --------------

    lowPrice                = Object   ( objMapping    = "LowOptionTrade.Price",
                                         label         = '' )
    
    highPrice               = Object   ( objMapping    = "HighOptionTrade.Price",
                                         label         = '' )
    
    allInPrice              = Object   ( objMapping    = "AllInPrice")
    
    lowPremium              = Object   ( objMapping    = "LowOptionTrade.Premium",
                                         label         = '' )
    
    highPremium             = Object   ( objMapping    = "HighOptionTrade.Premium",
                                         label         = '' )
    
    totalPrice              = Object   ( objMapping    = "TotalPrice",
                                         label         = '',
                                         enabled       = False )
    
    totalPremium            = Object   ( objMapping    = "SumOfPremiums",
                                         label         = '',
                                         enabled       = False )

    lowTheor                = CalcVal  ( calcMapping   = 'LowOption:FDealSheet:Price Theor',
                                         label         = 'Low Option')

    highTheor               = CalcVal  ( calcMapping   = 'HighOption:FDealSheet:Price Theor',
                                         label         = 'High Option' )
    
    totalTheor              = Object   ( objMapping    = 'TotalTheorPrice',
                                         label         = 'Total' )

    updatePrices            = Action   ( label         = 'Update prices',
                                         action        = '@UpdatePrices' )
    
    calculateTotalPrice     = Action   ( action        = '@CalculateTotalPrice')
    
    calculateTotalQuantity  = Action   ( action        = '@CalculateTotalQuantity')

    def AttributeOverrides(self, overrideAccumulator):
    
        attrs = {}
        
        attrs['highOption'] = {
                    'expiry'            : dict ( defaultValue = '1M' ),
                    'optionType'        : dict ( defaultValue = 'Call' ),
                    'strikePrice'       : dict ( label = 'High Strike' )
                    }
        
        attrs['lowOption'] = {
                    'expiry'            : dict ( defaultValue = '1M' ),
                    'optionType'        : dict ( defaultValue = 'Call' ),
                    'strikePrice'       : dict ( label = 'Low Strike' )
                    }
                    
        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })


    def OnInit(self):
        self._allInPrice = 0.0
        self._tradeQuantityMapping = [
            {'trade':'LowOptionTrade', 'quantityFactor':self.LowFactor},
            {'trade':'HighOptionTrade', 'quantityFactor':self.HighFactor}]
        
        toBeSame = ['underlying', 'contractSize', 'expiry', 'valuationGroup', 
            'settleDays', 'settlementType', 'optionType', 'quotation']
        for attr in toBeSame:
            self.RegisterAlignmentAcrossComponents(['highOption_'+attr, 'lowOption_'+attr])
        self.RegisterCallbackOnAttributeChanged(self.ChangeCurrency, 'highOption_underlying')
        self.RegisterCallbackOnAttributeChanged(self.UpdateQuantity, 'highOption_optionType')

    def AssemblePackage(self, *args):
        highOption = self.highOption.CreateInstrument()
        lowOption = self.lowOption.CreateInstrument()
        trdHigh = acm.DealCapturing().CreateNewTrade(highOption)
        trdLow = acm.DealCapturing().CreateNewTrade(lowOption)
        self.DealPackage().AddTrade(trdHigh, "High")
        self.DealPackage().AddTrade(trdLow, "Low")

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SP_CallPutSpread')

    def PriceLayout(self):
        return """
                hbox(;
                    vbox[Theor;
                        lowTheor;
                        highTheor;
                        totalTheor;
                        ];
                    vbox[Price;
                        lowPrice;
                        highPrice;
                        totalPrice;
                        updatePrices;
                        ];
                    vbox[Premium;
                        lowPremium;
                        highPremium;
                        totalPremium;
                        tradeInput_payments;
                        ];
                    );
                """

    def IsValid(self, exceptionAccumulator, aspect):
        super(CallPutSpread, self).IsValid(exceptionAccumulator, aspect)
        
        if self.lowOption_strikePrice > self.highOption_strikePrice:
            msg = 'Cannot have lower strike price (%s) higher than the high strike price (%s)' %(
                self.lowOption_strikePrice,
                self.highOption_strikePrice)
            exceptionAccumulator(msg)

    def GraphXValues(self):
        low = self.lowOption_strikePrice
        high = self.highOption_strikePrice
        spread = high - low
        xValues = acm.FArray()
        if spread == 0.0:
            xValues.Add(0.0)
            xValues.Add(10.0)
        else:
            xValues.Add(max(0, low - spread*0.5))
            xValues.Add(low)
            xValues.Add(high)
            xValues.Add(high + spread*0.5)
        return xValues

    # ############################
    # Component access
    # ############################
    def HighOption(self):
        return self.InstrumentAt('High')
        
    def HighOptionTrade(self):
        return self.TradeAt('High')

    def LowOption(self):
        return self.InstrumentAt('Low')
        
    def LowOptionTrade(self):
        return self.TradeAt('Low')

    def LeadTrade(self):
        return self.HighOptionTrade()

    def HighOptionB2BParams(self):
        return self.B2BTradeParamsAt('High')
    
    def LowOptionB2BParams(self):
        return self.B2BTradeParamsAt('Low')

    def InstrumentPartCurrencies(self, *rest):
        return self.Instruments()
    
    def DealPartCurrencies(self, *rest):
        return self.Trades()

    # ############################
    # Mapping methods
    # ############################
    @ReturnDomainDecorator('double')
    def AllInPrice(self, value = '*Reading*'):
        if value =='*Reading*':
            return self._allInPrice
        else:
            self._allInPrice = value
            totalPrice = self.TotalPrice()
            totalMargin = value - totalPrice
            shouldSubtractSpread = self.tradeInput_quantity_value > 0.0 # If we are buying from customer, customer price should be lower than trader price
            signCorrection = -1 if shouldSubtractSpread else 1
            self.SetAttribute('lowB2B_b2bEnabled', True)
            self.SetAttribute('lowB2B_b2bMargin', signCorrection * totalMargin / 2.0)
            self.SetAttribute('highB2B_b2bEnabled', True)
            self.SetAttribute('highB2B_b2bMargin', signCorrection * totalMargin / 2.0)
        
    @ReturnDomainDecorator('double')
    def TotalTheorPrice(self, value = '*Reading*'):
        if value == '*Reading*':
            if self.highTheor and self.lowTheor:
                return self.SumOfPrices(self.highTheor.Value().Number(), self.lowTheor.Value().Number())

    @ReturnDomainDecorator('double')
    def TotalPrice(self, value='*Reading*'):
        if value == '*Reading*':
            return self.SumOfPrices(self.highPrice, self.lowPrice)
    
    # ############################
    # Actions 
    # ############################
    def CalculateTotalPrice(self, attrName, prices):
        return self.SumOfPrices(prices.At('High'), prices.At('Low'))
    
    def CalculateTotalQuantity(self, attrName, quantities):
        return quantities.At('High') / self.HighFactor()

    # ############################
    # Attribute callbacks
    # ############################
    def UpdatePrices(self, attrName, *rest):
        self.DealPackage().CustomActionAt('updatePrices').Invoke()

    def ChangeCurrency(self, attrName, oldValue, newValue, *rest):
        self.currency = self.highOption_underlying.Currency()

    def UpdateQuantity(self, *args):
        quantity = self.tradeInput_quantity_value
        self.tradeInput_quantity_value = quantity + 0.1
        self.tradeInput_quantity_value = quantity

    def LowFactor(self):
        return 1.0 if self.lowOption_optionType == "Call" else -1.0
        
    def HighFactor(self):
        return -1.0 if self.highOption_optionType == "Call" else 1.0

    def VisibleSpotDays(self, *args):
        return self.IsShowModeDetail()

    def Notional(self, value = '*Reading*'):
        return 0.0 #Todo: Remove
    
    def SumOfPrices(self, highPrice, lowPrice):
        return self.HighFactor()*highPrice + self.LowFactor()*lowPrice


def StartCallPutSpread(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Call/Put Spread')
    return  

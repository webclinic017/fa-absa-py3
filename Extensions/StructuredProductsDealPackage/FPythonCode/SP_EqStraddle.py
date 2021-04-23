
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, Delegate, ReturnDomainDecorator, CustomActions
from SP_DealPackageHelper import SafeDivision
from CompositeTradeComponents import TradeB2B
from StructuredProductBase import ProductBase
from CompositeOptionComponents import Option
from SP_CustomTradeActions import UpdatePriceAction

@Settings(GraphApplicable=True,
          MultiTradingEnabled=True)
@CustomActions(updatePrices = UpdatePriceAction(FieldMapping = [{'FromField':'putTheor',  'ToField':'putPrice'},
                                                                {'FromField':'callTheor', 'ToField':'callPrice'}]))
@TradeActions( correct = CorrectCommand(statusAttr='tradeInput_status', newStatus='FO Confirmed'),
               novate = NovateCommand(statusAttr='tradeInput_status', nominal='tradeInput_quantity_value'),
               close  = CloseCommand(statusAttr='tradeInput_status', nominal='tradeInput_quantity_value'),
               mirror = MirrorCommand(statusAttr='tradeInput_status', newStatus='Simulated', quantityAttr='tradeInput_quantity_value'))
class EqStraddle(ProductBase):

    # Components
    # ----------

    callOption              = Option ( optionName    = "CallOption",
                                       undType       = acm.FStock )

    putOption               = Option ( optionName    = "PutOption",
                                       undType       = acm.FStock )

    # B2B Trades
    # ----------
    
    callB2B                 = TradeB2B ( uiLabel            = 'Call Option',
                                         b2bTradeParamsName = 'CallOptionB2BParams' )


    putB2B                  = TradeB2B ( uiLabel            = 'Put Option',
                                         b2bTradeParamsName = 'PutOptionB2BParams' )


    # Pricing fields
    # --------------

    putPrice                = Object   ( objMapping    = "PutOptionTrade.Price",
                                         label         = '' )
    
    callPrice               = Object   ( objMapping    = "CallOptionTrade.Price",
                                         label         = '' )
    
    putPremium              = Object   ( objMapping    = "PutOptionTrade.Premium",
                                         label         = '' )
    
    callPremium             = Object   ( objMapping    = "CallOptionTrade.Premium",
                                         label         = '' )
    
    totalPrice              = Object   ( objMapping    = "SumOfTradePrices",
                                         label         = '',
                                         enabled       = False )
    
    totalPremium            = Object   ( objMapping    = "SumOfPremiums",
                                         label         = '',
                                         enabled       = False )


    putTheor                = CalcVal  ( calcMapping   = 'PutOption:FDealSheet:Price Theor',
                                         label         = 'Put Option' )


    callTheor               = CalcVal  ( calcMapping   = 'CallOption:FDealSheet:Price Theor',
                                         label         = 'Call Option' )
    
    totalTheor              = Object   ( objMapping    = 'TotalTheorPrice',
                                         label         = 'Total' )

    updatePrices            = Action   ( label         = 'Update prices',
                                         action        = '@UpdatePrices' )

    # ############################
    # Devkit override
    # ############################
    def AttributeOverrides(self, overrideAccumulator):
        attrs = {}
        
        attrs['callOption'] = {
                'expiry'     : dict ( defaultValue = '1M' ),
                'optionType' : dict ( defaultValue = 'Call' )
                }
        
        attrs['putOption'] = {
                'expiry'     : dict ( defaultValue = '1M' ),
                'optionType' : dict ( defaultValue = 'Put' )
                }

        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })
    
    def OnInit(self):
        self._tradeQuantityMapping = []
        putTradeMapping = acm.FDictionary()
        putTradeMapping.AtPut('trade', 'PutOptionTrade')
        putTradeMapping.AtPut('quantityFactor', lambda *args : 1.0)
        self._tradeQuantityMapping.append(putTradeMapping)

        callTradeMapping = acm.FDictionary()
        callTradeMapping.AtPut('trade', 'CallOptionTrade')
        callTradeMapping.AtPut('quantityFactor', lambda *args : 1.0)
        self._tradeQuantityMapping.append(callTradeMapping)


        self.RegisterAlignmentAcrossComponents(['putOption_strikePrice',
                                                'callOption_strikePrice'])

        self.RegisterAlignmentAcrossComponents(['putOption_underlying',
                                                'callOption_underlying'])

        self.RegisterAlignmentAcrossComponents(['putOption_contractSize',
                                                'callOption_contractSize'])

        self.RegisterAlignmentAcrossComponents(['putOption_expiry',
                                                'callOption_expiry'])

        self.RegisterAlignmentAcrossComponents(['putOption_valuationGroup',
                                                'callOption_valuationGroup'])

        self.RegisterAlignmentAcrossComponents(['putOption_settleDays',
                                                'callOption_settleDays'])

        self.RegisterAlignmentAcrossComponents(['putOption_settlementType',
                                                'callOption_settlementType'])

        self.RegisterCallbackOnAttributeChanged(self.ChangeCurrency, 'callOption_underlying')

    def AssemblePackage(self):
        putOption  = self.putOption.CreateInstrument()
        callOption = self.callOption.CreateInstrument()
        tradePutOption = acm.DealCapturing().CreateNewTrade(putOption)
        tradeCallOption = acm.DealCapturing().CreateNewTrade(callOption)
        self.DealPackage().AddTrade(tradePutOption, "PutOption")
        self.DealPackage().AddTrade(tradeCallOption, "CallOption")
    
        self.callOption_contractSize = 1
        
    def LeadTrade(self):
        return self.CallOptionTrade()

    def IsValid(self, exceptionAccumulator, aspect):

        super(EqStraddle, self).IsValid(exceptionAccumulator, aspect)
    
        if self.PutOption().OptionType() != 'Put':
            exceptionAccumulator('Cannot set option type on a straddle put option to %s' 
                                            % self.PutOption().OptionType() )

        if self.CallOption().OptionType() != 'Call':
            exceptionAccumulator('Cannot set option type on a straddle call option to %s' 
                                            % self.CallOption().OptionType() )


    # ############################
    # Layout & UI
    # ############################
    def CustomPanes(self):
        layout = self.GetCustomPanesFromExtValue('CustomPanes_SP_EqStraddle')
        return layout

    def PriceLayout(self):
        return """
                hbox(;
                    vbox[Theor;
                        putTheor;
                        callTheor;
                        totalTheor;
                        ];
                    vbox[Price;
                        putPrice;
                        callPrice;
                        totalPrice;
                        updatePrices;
                        ];
                    vbox[Premium;
                        putPremium;
                        callPremium;
                        totalPremium;
                        tradeInput_payments;
                        ];
                    );
                """

    def GraphXValues(self):
        strike = self.DealPackage().GetAttribute("callOption_strikePrice")
        xValues = acm.FArray()
        if strike == 0.0:
            xValues.Add(0.0)
            xValues.Add(10.0)
        else:
            for i in range(95, 106, 1):
                xValues.Add( strike * i / 100 )
        return xValues

    def UpdatePrices(self, attrName, *rest):
        self.DealPackage().CustomActionAt('updatePrices').Invoke()
        
    # ############################
    # Component access
    # ############################
    def PutOption(self):
        return self.InstrumentAt("PutOption")

    def CallOption(self):
        return self.InstrumentAt("CallOption")

    def PutOptionTrade(self):
        return self.TradeAt("PutOption")

    def CallOptionTrade(self):
        return self.TradeAt("CallOption")

    def CallOptionB2BParams(self):
        return self.B2BTradeParamsAt('CallOption')
    
    def PutOptionB2BParams(self):
        return self.B2BTradeParamsAt('PutOption')

    def InstrumentPartCurrencies(self):
        ccyObj = acm.FArray()
        ccyObj.Add(self.CallOption())
        ccyObj.Add(self.PutOption())
        return ccyObj
        
    def DealPartCurrencies(self):
        ccyObj = acm.FArray()
        ccyObj.AddAll(self.DealPackage().Trades())
        return ccyObj

    # ############################
    # Mapping methods
    # ############################
    def Notional(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.callOption_strikePrice * self.callOption_contractSize
        else:
            value = float(value)
            if value != 0.0:
                self.callOption_contractSize = SafeDivision(value, self.callOption_strikePrice, self.callOption_contractSize)
                self.UpdatePremiums()

    @ReturnDomainDecorator('double')
    def TotalTheorPrice(self, value = '*Reading*'):
        if value == '*Reading*':
            if self.callTheor and self.putTheor:
                return self.callTheor.Value().Number() + self.putTheor.Value().Number()

    # ############################
    # Attribute callbacks
    # ############################
    def VisibleSpotDays(self, *rest):
        return self.IsShowModeDetail()

    def ChangeCurrency(self, attrName, oldValue, newValue, *rest):
        self.currency = self.callOption_underlying.Currency()
        


def StartEqStraddle(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Equity Straddle')
    return 


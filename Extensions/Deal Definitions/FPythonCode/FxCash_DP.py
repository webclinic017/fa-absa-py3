import acm
from DealDevKit import DealDefinition, Settings, Action, Object, CalcVal, Str, Label, ReturnDomainDecorator
from CompositeAttributesLib import TradeDefinition, TradeBODefinition, AddInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition, BuySell
from DealPackageDevKit import CompositeAttributeDefinition

class FxCashLeg(CompositeAttributeDefinition):

    def OnInit(self, trade, **kwargs):
        self._trade = trade
        self._stdCalcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    
    def Attributes(self):
        attributes = { 
                         'quantity'             : BuySell(label=self.UniqueCallback('@QuantityLabel'),
                                                          objMapping=self.UniqueCallback('Quantity'),
                                                          showBuySell=False,
                                                          visible=self.UniqueCallback('@IsNearLegOrSwap')),
                         'valueDay'             : Object( label='Value Day',
                                                          objMapping=self.UniqueCallback('ValueDay'),
                                                          recreateCalcSpaceOnChange=True,
                                                          transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                          visible=self.UniqueCallback('@IsNearLegOrSwap')),    
                         'spotPrice'            : Object( label='Spot Price',
                                                          objMapping=self.UniqueCallback('SpotPrice'),
                                                          formatter='InstrumentDefinitionFxPrice',
                                                          visible=self.UniqueCallback('@IsNearLegForwardOrSwapFarLeg')),
                         'spotPriceEmpty'       : Label(  label=' ',
                                                          visible=self.UniqueCallback('@IsFarLegAndSwap')), 
                         'price'                : Object( label='Price',
                                                          objMapping=self._trade+'.Price',
                                                          formatter='InstrumentDefinitionFxPrice',
                                                          visible=self.UniqueCallback('@IsNearLegOrSwap')),
                         'points'               : Object( label='Points',
                                                          objMapping=self.UniqueCallback('Points'),
                                                          enabled=self.UniqueCallback('@IsForward'),
                                                          visible=self.UniqueCallback('@IsNearLegForwardOrSwap')),
                         'premium'              : BuySell(label=self.UniqueCallback('@PremiumLabel'),
                                                          objMapping=self.UniqueCallback('Premium'),
                                                          showBuySell=False,
                                                          visible=self.UniqueCallback('@IsNearLegOrSwap')),
                         'currentSpot'          : Object( label='Current Spot',
                                                          objMapping=self.UniqueCallback('CurrentSpot'),
                                                          formatter='InstrumentDefinitionFxPrice',
                                                          enabled=self.UniqueCallback('@IsNotFarLeg'),
                                                          editable=False,
                                                          visible=self.UniqueCallback('@IsNearLeg')),
                         'currentSpotEmpty'     : Label(  label=' ',
                                                          visible=self.UniqueCallback('@IsFarLegAndSwap')), 
                         'pv'                   : CalcVal(label='PV',
                                                          calcMapping=self._trade + ':FTradeSheet:Portfolio Total Profit and Loss',
                                                          editable=False,
                                                          visible=self.UniqueCallback('@IsNearLegOrSwap')),
                         'empty'                : Label(  label=' ',
                                                          visible=self.UniqueCallback('@IsFarLegNotSwap')), 
                         'suggestPrices'        : Action(action=self.UniqueCallback('@SuggestPrices')),

                         'lastAmountUpdate'     : Str(defaultValue='quantity')
                    }
        return attributes
        
    # Labels
    def PremiumLabel(self, attributeName, *args):
        label = self.Trade().Currency().Name() if self.Trade().Currency() else 'Amount'
        return self.AmountPrefix(attributeName) + label
        
    def QuantityLabel(self, attributeName, *args):
        label = self.Trade().Instrument().Name()
        return self.AmountPrefix(attributeName) + label
        
    # Visible
    def IsSwap(self, *args):
        return self.Trade().FxSwapNearLeg() or self.Trade().FxSwapFarLeg()
            
    def IsForward(self, *args):
        return self.IsNearLegOrSwap() and not self.Trade().IsFxSpot()

    def IsNearLegForwardOrSwap(self, *args):
        return (self.IsForward() and self.IsNotFarLeg()) or self.IsSwap()

    def IsNearLegForwardOrSwapFarLeg(self, *args):
        return self.IsNotFarLeg() and (self.IsForward() or self.IsSwap())

    def IsForwardOrSwapNearLeg(self, *args):
        return self.IsForward() or self.Trade().IsFxSwapNearLeg()
        
    def IsNotFarLeg(self, *args):
        return not self.Trade().IsFxSwapFarLeg()
    
    def IsNearLeg(self, *args):
        return not self.Trade().IsFxSwapFarLeg()

    def IsNearLegOrSwap(self, *args):
        return (not self.Trade().IsFxSwapFarLeg()) or self.Trade().FxSwapNearLeg() or self.Trade().FxSwapFarLeg()
    
    def IsFarLegNotSwap(self, *args):
        return self.Trade().IsFxSwapFarLeg() and not self.Trade().FxSwapNearLeg() 
    
    def IsFarLegAndSwap(self, *args):
        return self.Trade().IsFxSwapFarLeg() and self.Trade().FxSwapNearLeg() 
    
    # Transform
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToRebasedDate(date, self.Trade().SpotDate())
        if period:
            date = self.Trade().AdjustToBusinessDay(period)
        return date   
    
    # Action
    def SuggestPrice(self, *args):
        forwardPrice = self.Trade().Instrument().Calculation().FXRate(self.StdCalcSpace(), self.Trade().Currency(), self.Trade().ValueDay()).Value().Number()
        self.price = forwardPrice * self.spotPrice/ self.CurrentSpot()
        
    def SuggestSpotPrice(self, *args):
        self.spotPrice = self.CurrentSpot()
        
    def SuggestPrices(self, *args):
        self.SuggestSpotPrice()
        self.SuggestPrice()
    
    def SetTradeProcesses(self, *args):
        self.Trade().IsFxSpot(self.Trade().IsFxSpotDated())
        
    # Configuration
    def ForwardDateConfiguration(self, forwardDate):
        scenario = acm.FExplicitScenario()
        scm = acm.CreateScenarioMember( acm.GetFunction('fixedVariant', 2), ['fxForwardDate'], acm.FObject, forwardDate)
        dim = acm.FDirectScenarioDimension()
        dim.AddScenarioMember(scm)
        scenario.AddDimension(dim)
        config = acm.Sheet().Column().ConfigurationFromScenario(scenario, None)
        return config
    
    def ForwardRateConfiguration(self, attributeName):
        return self.ForwardDateConfiguration(self.Trade().ValueDay())
        
    def SpotRateConfiguration(self, attributeName):
        return self.ForwardDateConfiguration(self.Trade().SpotDate())
        
    # Decorators
    @ReturnDomainDecorator('double')
    def SpotPrice(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Trade().ReferencePrice()
        else:
            self.Trade().ReferencePrice = value
            self.price = value + self.points/self.Trade().PipsFactor()
                                                      
    @ReturnDomainDecorator('double')
    def Points(self, value = '*Reading*'):
        if value == '*Reading*':
            return (self.Trade().Price() - self.Trade().ReferencePrice()) * self.Trade().PipsFactor()
        else:
            self.price = self.spotPrice + value/self.Trade().PipsFactor()

    @ReturnDomainDecorator('double')
    def Quantity(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Trade().Quantity()
        else:
            self.Trade().Quantity(value)
            self.lastAmountUpdate = 'quantity'

    @ReturnDomainDecorator('date')
    def ValueDay(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Trade().ValueDay()
        else:
            self.Trade().ValueDay(value)
            self.SetTradeProcesses()
            self.SuggestPrice()
            
    @ReturnDomainDecorator('double')
    def Premium(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Trade().Premium()
        else:
            self.Trade().Premium(value)
            self.lastAmountUpdate = 'premium'

    @ReturnDomainDecorator('double')
    def CurrentSpot(self, value = '*Reading*'):
        if value == '*Reading*':
            currentSpot = self.Trade().Instrument().Calculation().FXRate(self.StdCalcSpace(), self.Trade().Currency(), self.Trade().SpotDate()).Value().Number()
            return currentSpot
            
    # Util 
    def Trade(self):
        return self.GetMethod(self._trade)()     

    def StdCalcSpace(self):
        return self._stdCalcSpace

    def AmountPrefix(self, attributeName):
        return '* ' if self.lastAmountUpdate in attributeName else ''
        
    def GetLayout(self):
        return self.UniqueLayout(
                    """
                    vbox(;
                        quantity;
                        valueDay;
                        currentSpot;
                        hbox(;
                            currentSpotEmpty;
                            fill;
                        );
                        spotPrice;
                        hbox(;
                            spotPriceEmpty;
                            fill;
                        );
                        points;
                        price;
                        premium;
                        pv;
                        hbox(;
                            empty;
                            fill;
                        );
                    );
                    """
                )

@Settings(SheetApplicable=False)
class FxCashDefinition(DealDefinition):

    trades              = TradeDefinition( trade='FxTrades', 
                                           included=['currency', 
                                                     'portfolio', 
                                                     'counterparty', 
                                                     'tradeTime', 
                                                     'acquirer', 
                                                     'trader',
                                                     'status'] )
    
    trade               = TradeDefinition( trade='Trade', 
                                           included=['trdnbr',
                                                     'boTrdnbr',
                                                     'payments'] )

    nearLeg             = FxCashLeg( trade='Trade' )
    farLeg              = FxCashLeg( trade='FarTrade' )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")    

    instrument          = Object(objMapping='CashInstrument',
                                 label='',
                                 choiceListSource='@InstrumentChoices',
                                 onChanged='@CurrencyPairChanged')
                                 
    isFxSwap            = Object(objMapping='IsFxSwap',
                                 label='Swap',
                                 onChanged='@SetDefaultValuesFromCurrencyPair')
                                 
    farTrade            = Object(defaultValue=None,
                                 domain=acm.FTrade)
    
                                 
                                 
     # Attribute overrides
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {
                'trades_currency': dict(label='',
                                                               visible=True, 
                                                               onChanged='@CurrencyPairChanged'),
                'trades_tradeTime': dict(onChanged='@TradeTimeChanged'),
                'nearLeg_quantity_value': dict(onChanged='@NearQuantityChanged'),
                'nearLeg_premium_value': dict(onChanged='@NearPremiumChanged'),
                'nearLeg_spotPrice': dict(onChanged='@NearSpotPriceChanged'),
                'nearLeg_valueDay': dict(onChanged='@SetDefaultValuesFromCurrencyPair'),
                'farLeg_valueDay': dict(onChanged='@SetTradeTime'),
            }
        )  
        
    def OnNew(self, *args):
        if self.Trade().IsInfant():
            self.instrument = 'EUR'
            self.trades_currency = 'USD'
            self.nearLeg_quantity_value = 1.0
            self.farLeg_quantity_value = -self.nearLeg_quantity_value
            self.CurrencyPairChanged()
        else:
             self.InitSwap() # should be in OnOpen?
        
    def OnCopy(self, original, *args):
        self.InitSwap(original.GetAttribute('farTrade'))
            
    def UpdateTradeOnSave(self, trade):
        trade.SuggestBaseCurrencyEquivalent()
        trade.ReferencePrice(trade.Price())
        
    def OnSave(self, saveConfig):
        saveConfig.InstrumentPackage('Exclude')
        super(FxCashDefinition, self).OnSave(saveConfig) 
        if saveConfig.DealPackage() == 'SaveNew' and self.FarTrade().IsStorageImage():
            self.FarTrade().StorageSetNew()
            
        self.UpdateTradeOnSave(self.Trade())
        self.UpdateTradeOnSave(self.FarTrade())
            
        self.FarTrade().TradeTime = self.Trade().TradeTime()
        if self.isFxSwap:
            return {'commit':[self.farTrade],
                    'delete':[]}
        elif saveConfig.DealPackage() == 'Save':
            originalFarLeg = self.Trade().Originator().FxSwapFarLeg()
            if originalFarLeg and not originalFarLeg.IsInfant():
                return {'commit':[],
                        'delete':[self.farTrade]}
                    
    def OnOpen(self, *args):
        self.InitSwap()

    def IsValid(self, exceptionAccumulator, aspect):
        if self.Trade().GroupTrdnbr():
            exceptionAccumulator('Not supported to save trade that belongs to a group.')
        if self.Trade().IsFxSwapFarLeg():
            exceptionAccumulator('Not supported to save a swap far leg.')
        if self.Trade().MirrorTrade():
            exceptionAccumulator('Not supported to save a trade with a mirror.')
        if self.Trade().MirrorPortfolio():
            exceptionAccumulator('Not supported to save a trade with mirror portfolio.')
        if self.Trade().IsB2BSalesCover():
            exceptionAccumulator('Not supported to save a trade with B2B.')
                    
    # Choices
    def InstrumentChoices(self, *args):
        return acm.FCurrency.Instances()
        
    # OnChanged 
    def SetDefaultValuesFromCurrencyPair(self, *args):
        def SetAcquirerFromPortfolio(portfolio):
            if portfolio and portfolio.PortfolioOwner():
                self.trades_acquirer = portfolio.PortfolioOwner()

        pair = self.InstrumentPair()
        if pair:
            if self.Trade().IsFxSpot() and not self.isFxSwap:
                self.trades_portfolio = pair.SpotPortfolio()
                SetAcquirerFromPortfolio(pair.SpotPortfolio())
            else:
                self.trades_portfolio = pair.ForwardPortfolio()
                SetAcquirerFromPortfolio(pair.ForwardPortfolio())

    def CurrencyPairChanged(self, *args):
        spotDate = self.Trade().SpotDate()
        self.nearLeg_valueDay = spotDate
        self.farLeg_valueDay = spotDate
        self.SetDefaultValuesFromCurrencyPair()
        self.nearLeg_suggestPrices()
        self.farLeg_suggestPrices()
        
    def NearQuantityChanged(self, name, oldValue, newValue, aspect):
        if aspect == None:
            self.farLeg_quantity_value = -newValue
        
    def NearPremiumChanged(self, name, oldValue, newValue, aspect):
        if aspect == None:
            self.farLeg_premium_value = -newValue

    def NearSpotPriceChanged(self, name, oldValue, newValue, *args):
        self.farLeg_spotPrice = newValue

    def TradeTimeChanged(self, name, oldValue, newValue, aspect):
        if self.Trade().IsFxSpot():
            self.nearLeg_valueDay = '0d'

    def SetTradeTime(self, *args):
        self.tradeTime = self.Trade().TradeTime()

    # Decorators
    @ReturnDomainDecorator('FCurrency')
    def CashInstrument(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Instrument()
        else:
            self.DealPackage().ReplaceInstrumentAt('Trade', value)
            self.FarTrade().Instrument = self.Instrument()
            
    @ReturnDomainDecorator('bool')
    def IsFxSwap(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.Trade().IsFxSwapNearLeg()
        else:
            self.ConnectFxSwap(value)
            self.SetDefaultSwapValues(value)
            
    # Util 
    def FxTrades(self):
        return [self.Trade(), self.FarTrade()]
        
    def FarTrade(self):
        if not self.farTrade:
            self.InitSwap()
        return self.farTrade
        
    def WrapAndSetFarTrade(self, farTrade):
        if farTrade:
            nearTrade = self.Trade()
            farTrade.Instrument = nearTrade.Instrument()
            self.farTrade = acm.FBusinessLogicDecorator.WrapObject(farTrade, nearTrade.GUI())
            
    def ConnectFxSwap(self, isFxSwap):
        self.Trade().IsFxSwapNearLeg(isFxSwap)
        if isFxSwap:
            self.Trade().ConnectedTrade(self.Trade())
            self.FarTrade().ConnectedTrade(self.Trade())
            if not self.Trade().FxSwapFarLeg():
                acm.FX().RegisterFxSwap(self.Trade(), self.FarTrade())
        else:
            self.Trade().ConnectedTrade(None)
            self.FarTrade().ConnectedTrade(None)

    def SetDefaultSwapValues(self, isFxSwap):
        if isFxSwap:
            wrongWay = self.farLeg_valueDay < self.nearLeg_valueDay
            if wrongWay:
                farValueDay = self.nearLeg_valueDay
                farPoints = self.nearLeg_points
            else:
                farValueDay = self.farLeg_valueDay
                farPoints = self.farLeg_points
                
            self.nearLeg_valueDay = '0d'
            self.farLeg_valueDay = farValueDay
            self.farLeg_points = farPoints
            self.nearLeg_quantity_value = -self.nearLeg_quantity_value

        else:
            self.nearLeg_valueDay = self.farLeg_valueDay
            self.nearLeg_points = self.farLeg_points
            self.nearLeg_quantity_value = -self.nearLeg_quantity_value
            
    def InitSwap(self, farTrade=None):
        near = self.Trade()
        
        if not farTrade:
            farTrade = near.FxSwapFarLeg()
        
        if not farTrade:
            farTrade = near.Originator().FxSwapFarLeg()
        
        if near.ConnectedTrade():
            near.ConnectedTrade = near  
            
        if farTrade:
            if farTrade.IsInfant():
                newFarTrade = farTrade.Clone()
                newFarTrade.RegisterInStorage()
            else:
                newFarTrade = farTrade.StorageImage()
                
            self.WrapAndSetFarTrade(newFarTrade)
            self.ConnectFxSwap(near.IsFxSwap())
        else:
            farTrade = near.Clone()
            farTrade.ConnectedTrade(None)
            farTrade.RegisterInStorage()
            self.WrapAndSetFarTrade(farTrade)
            self.farTrade.IsFxSwapFarLeg = True

    def InstrumentPair(self):
        return self.Trade().InstrumentPair(True)
            
    def TradePanes(self):
        return 'CustomPanes_FxCashTrade'

   

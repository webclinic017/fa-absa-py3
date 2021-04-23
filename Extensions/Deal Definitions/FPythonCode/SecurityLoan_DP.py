import acm
from DealDevKit import DealDefinition, Settings, Object, Bool, Label, CalcVal, NoOverride, ReturnDomainDecorator, NoOverride
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition, BuySell
from DealSTI import DealSTI

 
class SecurityLoanLeg(LegDefinition):
        
    def Attributes(self):
        attributes = super(SecurityLoanLeg, self).Attributes()
        attributes['initialFX']                 = Object(  label='FX',
                                                           objMapping=self.UniqueCallback('InitialFX'),
                                                           formatter='InstrumentDefinitionFxPrice',
                                                           visible=self.UniqueCallback('@InitialFXVisible'))
                                                           
        attributes['initialIndexValueDomestic'] = Object(  label=self.UniqueCallback('@InitialIndexValueDomesticLabel'),
                                                           objMapping=self.UniqueCallback('InitialIndexValueDomestic'),
                                                           formatter='InstrumentDefinitionPrice',
                                                           visible=self.UniqueCallback('@InitialFXVisible'))
                                                            
        attributes['fixedPrice']                = Bool(    label='Fixed Price',
                                                           objMapping=self.UniqueCallback('FixedPrice'))

        attributes['indexRefFixingDateRule']    = Object(    label='Fixing Rule',
                                                            visible = self.UniqueCallback('@IndexRefFixingDateRuleVisible'),
                                                            toolTip = 'Select a Fixing Date Rule in order to override the default logic' 
                                                        ' used for generating the fixing Date for nominal scaling resets linked to the Index Reference.',
                                                           objMapping=self._leg+'.IndexRefFixingDateRule')
                                                           
        attributes['nominal']                   = BuySell( label='Nominal',
                                                           objMapping=self.UniqueCallback('Nominal'),
                                                           editable=self.UniqueCallback('@HasUnderlying'),
                                                           showBuySell=False)                                 
                                                            
        attributes['initialMargin']             = Object(  label='Initial Margin',
                                                           formatter='PercentShowZero',
                                                           objMapping=self._leg+'.NominalFactor')
                                                           
                                                           
        self.Owner().RegisterCallbackOnAttributeChanged(self.AttributeChanged, last=True)
        return attributes
        
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'nominalScaling': dict(choiceListSource=self.UniqueCallback('@NominalScalingChoices'),
                                                        onChanged=self.UniqueCallback('@NominalScalingChanged')),
             'indexRef': dict(choiceListSource=self.UniqueCallback('@UnderlyingChoices'),
                                                        onChanged=self.UniqueCallback('@UpdateIntialIndex')),
             'indexRefFXFixingType': dict(visible=self.UniqueCallback('@IndexRefFXFixingTypeVisible'),
                                                        onChanged=self.UniqueCallback('@UpdateIntialIndex')),
             'initialIndexValue': dict(label=self.UniqueCallback('@InitialIndexValueLabel'),
                                                        formatter='InstrumentDefinitionPrice'),
             'nominalScalingPeriod': dict(visible=self.UniqueCallback('@IndexRefFXFixingTypeVisible')),
             'currency': dict(label='',
                                                        onChanged=self.UniqueCallback('@UpdateIntialIndex'),
                                                        visible='@IsShowModeInstrumentDetail',
                                                        width=10,
                                                        maxWidth=10),
             'fixedRate': dict(label='Fee'),
            }
        )
        
    def OnInit(self, leg, trade, **kwargs):
        super(SecurityLoanLeg, self).OnInit(leg, trade, **kwargs)
        self._lastInitialFX = 0.0
        
    def Trade(self):
        return self.GetMethod(self._trade)()
       
    def NominalScalingChoices(self, *args):
        return acm.FIndexedPopulator(['None', 'Initial Price', 'Price'])
        
    def UpdateIntialIndex(self, *args):
        self.initialIndexValue = self.Leg().SuggestInitialIndexValue()
        self._lastInitialFX = 0.0
        
    def NominalScalingChanged(self, attributeName, oldValue, newValue, *args):
        if oldValue == 'None':
            self.indexRef = self.Owner().GetAttribute('ins_underlying')
        
        if newValue != oldValue:
            if newValue == 'Price':
                if self.IsCrossCurrency():
                    self.indexRefFXFixingType = 'Explicit'
                else:
                    self.indexRefFXFixingType = 'None'
            if newValue == 'Initial Price':
                self.indexRefFXFixingType = 'None'
        self.UpdateIntialIndex()

    def IsCrossCurrency(self, *args):
        leg = self.Leg()
        return leg.IndexRef() and leg.IndexRef().Currency() != leg.Currency()
        
    def UnderlyingChoices(self, *args):
        return self.Owner().GetAttributeMetaData('ins_underlying', 'choiceListSource')()
        
    def IndexRefFXFixingTypeVisible(self, *args):
        leg = self.Leg()
        return self.IsCrossCurrency() and leg.NominalScaling() == 'Price'
        
    def InitialFXVisible(self, *args):
        leg = self.Leg()
        return self.IsCrossCurrency() and self.indexRefFXFixingType == 'Explicit'
        
    def IndexRefFixingDateRuleVisible(self, *args):
        return self.nominalScaling == 'Price'
        
    @ReturnDomainDecorator('double')
    def InitialFX(self, value = 'NoValue', **kwargs):
        leg = self.Leg()
        if leg.IndexRef() and leg.IndexRef().Currency() != leg.Currency():
            if value == 'NoValue':
                return self.GetInitialFX()
            else:
                self.SetInitialFX(value)
        else:
            return 1.0
    
    def SetInitialFX(self, value):
        if self.indexRefFXFixingType == 'Explicit':
            first = self.InitialFXFixing()
            if first:
                first.FixFixingValue(value)
    
    def GetInitialFX(self):
        if self.indexRefFXFixingType == 'Explicit':
            first = self.InitialFXFixing()
            initialFX = 0.0
            if first:
                if first.IsFixed():
                    initialFX = first.FixingValue()
                    self._lastInitialFX = initialFX
                else:
                    initialFX = self.CalculateInitialFxFromFixing(first)
                return initialFX
        return self.CalculateInitialFxEstimate()

         
    def CalculateInitialFxFromFixing(self, fixing):
        try:
            calcSpaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
            calcSpace = calcSpaceCollection.GetSpace('FMoneyFlowSheet', acm.GetDefaultContext())
            calculation = calcSpace.CreateCalculation(fixing, 'Cash Analysis Fixing Estimate', None)
            return calculation.Value().Number()
        except:
            pass
   
    def CalculateInitialFxEstimate(self):
        try:
            leg = self.Leg()
            calcSpaceCollection = acm.Calculations().CreateStandardCalculationsSpaceCollection()
            return leg.IndexRef().Currency().Calculation().FXRate(calcSpaceCollection, leg.Currency(), leg.StartDate()).Number()
        except:
            pass
   
    @ReturnDomainDecorator('double')
    def Nominal(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            space = acm.FStandardCalculationsSpaceCollection()
            payFactor = 1.0 if self.Leg().PayLeg() else -1.0
            if self.Instrument().Underlying():
                contractSize = self.Instrument().Underlying().ContractSize()
                return self.Leg().Calculation().Nominal(space, self.Trade()).Number() * payFactor * contractSize
            else:
                return 0.0
        else:
            self.Trade().Quantity = self.Trade().Quantity() * value / self.Nominal()

    def HasUnderlying(self, *args):
        return True if self.Instrument().Underlying() else False

    def InitialFXFixing(self):
        first = None
        for cf in self.Leg().CashFlows():
            for reset in cf.Resets():
                if reset.ResetType() == 'Index Reference FX' and (not first or reset.Day() < first.Day()):
                    first = reset
        return first
        
    def InitialIndexValueDomesticLabel(self, *args):
        return self.Leg().Instrument().Currency().StringKey() + ' Price'
        
    def InitialIndexValueLabel(self, *args):
        label = 'Price'
        if self.indexRef and self.indexRef.Currency() != self.Leg().Instrument().Currency():
            if self.nominalScaling == 'Price':
                label = self.indexRef.Currency().StringKey() + ' Price'
            elif self.nominalScaling == 'Initial Price':
                label = self.Leg().Instrument().Currency().StringKey() + ' Price'
        return label
        
    @ReturnDomainDecorator('double')
    def InitialIndexValueDomestic(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            if self.initialFX:
                return self.initialIndexValue * self.initialFX
        else:
            if self.initialFX:
                self.SetAttribute('initialIndexValue', value / self.initialFX)
        
    def AttributeChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        if self._lastInitialFX and self.initialFX != self._lastInitialFX:
            self.initialFX = self._lastInitialFX
            
    def FixedPrice(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            return self.nominalScaling == 'Initial Price'
        else:
            self.nominalScaling = 'Initial Price' if value else 'Price'
        

@DealSTI('SecurityLoan')    
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Market Price YTM', 'Price Theor', 'Portfolio Theoretical Value', 'Portfolio Delta Yield'])   
class SecurityLoanDefinition(DealDefinition):

    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")
    
    payLeg              = SecurityLoanLeg( leg='PayLeg', trade='Trade' )
    
    receiveLeg          = SecurityLoanLeg( leg='ReceiveOrDummyLeg', trade='Trade' )
    
    payCashFlows        = CashFlowDefinition( leg='PayLeg', trade='Trade')
    
    recCashFlows        = CashFlowDefinition( leg='ReceiveOrDummyLeg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade', buySellLabels=['Borrow', 'Lend', '-'])      
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")   
                                  
    secLoanPaymentType  = Object( label='Payment',
                                  choiceListSource=['No Collateral', 'Collateral'],
                                  objMapping='SecurityLoanPaymentType')
                                  
    empty               = Label( label=' ',
                                 visible='@ReceiveLegNotVisible')
                                  
    _indexRef           = Object( objMapping='Instrument.Legs.IndexRef',
                                  validateMapping=False)
                            
    def OnInit(self):
        ins = acm.DealCapturing().CreateNewInstrument('SecurityLoan')
        acm.FBusinessLogicDecorator.WrapObject(ins.Legs().First())
        dummyLeg = ins.CreateLeg('Float', 'Receive')
        self._dummyLeg = acm.FBusinessLogicDecorator.WrapObject(dummyLeg)
        
    def OnNew(self):
        self.Instrument().ContractSize = 1
        self.Instrument().RefPrice = 1
                
    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_name': dict(visible='@IsShowModeInstrumentDetail'),
             'ins_startDate': dict(onChanged='@OnInstrumentStartDateChanged'),
             'ins_underlyingType': dict(label='Sec Type',
                                                               maxWidth=500),
             'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_underlying': dict(label='Security', onChanged='@OnUnderlyingChanged'),
             'ins_dividendFactor': dict(visible=True, label = 'Div Factor', formatter = 'Percent'),
             'ins_openEnd': dict(width=13),
             'ins_noticePeriod': dict(width=9),
             'receiveLeg_legType': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_spread': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_fixedRate': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_floatRateReference': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_rollingPeriod': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_floatRateReference': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_initialRate': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_spread': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_resets_resets': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_nominal_value': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_nominal_buySell': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_nominalScaling': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_indexRefFXFixingType': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_nominalScalingPeriod': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_rollingPeriodBase': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_dayCountMethod': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_payCalendar': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_pay2Calendar': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_pay3Calendar': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_pay4Calendar': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_pay5Calendar': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_currency': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_indexRef': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_indexRefFixingDateRule': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_initialIndexValue': dict(visible='@ReceiveLegVisible'),
             'receiveLeg_initialMargin': dict(visible='@ReceiveLegVisible'),
             'trade_acquireDay': dict(visible='@IsShowModeTradeDetail'),
             'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
             'trade_yourRef': dict(visible=True),
             'trade_collateralAgreement': dict(visible=True),
             'trade_quantity_value': dict(editable='@HasUnderlying'),
            }
        ) 

    
    # Util     
        
    def InstrumentPanes(self):
       return 'CustomPanes_SecurityLoan'
       
    def TradePanes(self):
       return 'CustomPanes_SecurityLoanTrade'
    
    @ReturnDomainDecorator('string')
    def SecurityLoanPaymentType(self, value = 'NoValue', **kwargs):
        if value == 'NoValue':
            return self.GetPaymentType()
        else:
            self.SetPaymentType(value)
    
    def GetPaymentType(self):
        return 'Collateral' if len(self.Instrument().Legs()) == 2 else 'No Collateral'
        
    def SetPaymentType(self, value):
        if value == 'Collateral' and len(self.Instrument().Legs()) < 2:
            leg = self.Instrument().CreateLeg('Float', 'Receive')
            leg.NominalScaling = 'Price'
            leg.NominalScalingPeriod = self.PayLeg().NominalScalingPeriod()
            leg.IndexRefFXFixingType = self.PayLeg().IndexRefFXFixingType()
            leg.IndexRef = self.PayLeg().IndexRef()
            leg.InitialIndexValue = self.PayLeg().InitialIndexValue()
            leg.StartPeriod = self.PayLeg().StartPeriod()
            leg.StartDate = self.PayLeg().StartDate()
            leg.EndPeriod = self.PayLeg().EndPeriod()
            leg.EndDate = self.PayLeg().EndDate()
            leg.RollingPeriod = self.PayLeg().RollingPeriod()
            leg.RollingPeriodBase = self.PayLeg().RollingPeriodBase()
            leg.IndexRefFixingDateRule = self.PayLeg().IndexRefFixingDateRule()
            leg.GenerateCashFlows(0.0)
        elif value == self.GetPaymentType():
            pass
        else:
            self.Instrument().FirstReceiveLeg().Unsimulate()

    def OnInstrumentCurrencyChanged(self, attributeName, oldValue, newValue, *args):
        if self.payLeg.IsCrossCurrency() and self.PayLeg().NominalScaling() == 'Price':
            self.PayLeg().IndexRefFXFixingType = 'Explicit'

    def OnUnderlyingChanged(self, attributeName, oldValue, newValue, *args):
        self.SetAttribute('_indexRef', newValue, True)
        if newValue is not None:
            self.SetAttribute('ins_currency', newValue.Currency(), True)

    def HasUnderlying(self, *args):
        return True if self.Instrument().Underlying() else False

    def ReceiveOrDummyLeg(self):
        receiveLeg = self.ReceiveLeg()
        return receiveLeg if receiveLeg else self._dummyLeg
        
    def ReceiveLegVisible(self, *args):
        return NoOverride if self.SecurityLoanPaymentType() == 'Collateral' else False
        
    def ReceiveLegNotVisible(self, *args):
        return not self.ReceiveLegVisible()

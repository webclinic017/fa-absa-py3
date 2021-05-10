import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Action, Settings, DealPackageChoiceListSource, AcquirerChoices, PortfolioChoices
from inspect import cleandoc

@Settings(GraphApplicable=False)
class DealPackageExampleDeltaHedge(DealPackageDefinition):
    """
    Example showing the controls needed to make a 
    Delta hedge for an fx-trade
    """
    
    ipName            = Object( label='Name',
                                objMapping='InstrumentPackage.Name') 

    type              = Object( label='Hedge Type',
                                objMapping='DeltaHedge.HedgeType')
                                                
    useLivePrice      = Object( label='Use Live Price',
                                objMapping='DeltaHedge.UseLivePrice',
                                visible='@IsDeltaHedgeApplicable')
                                    
    useLiveDelta      = Object( label='Use Live Delta',
                                objMapping='DeltaHedge.UseLiveDelta',
                                visible='@IsDeltaHedgeApplicable')
                                                
    useSurfaceDelta   = Object( label='Use Surface Delta',
                                objMapping='DeltaHedge.UseSurfaceDelta',
                                visible='@IsDeltaHedgeApplicable')
    
    updatePrice       = Action( label='Update Price',
                                action='@DeltaHedgeUpdatePrice',
                                visible='@IsDeltaHedgeApplicable')
                                                
    updateDelta       = Action( label='Update Delta',
                                action='@DeltaHedgeUpdateDelta',
                                visible='@IsDeltaHedgeApplicable')
                                                
    valueDay          = Object( defaultValue='3m',
                                label='Value Day',
                                objMapping='DeltaHedge.ValueDay',
                                visible='@IsDeltaHedgeApplicable',
                                transform='@TransformExpPeriodToDate')
                                                
    counterparty      = Object( label='Counterparty',
                                objMapping='DeltaHedge.Counterparty',
                                visible='@IsDeltaHedgeApplicable',
                                choiceListSource='@Counterparties',
                                onChanged="@UpdateCounterpartyPortfolioChoices|ResetCounterpartyPortfolio")
                                                
    cpPortfolio       = Object( label='CP Portfolio',
                                objMapping='DeltaHedge.CounterpartyPortfolio',
                                visible='@IsDeltaHedgeApplicable',
                                enabled='@IsInternalCounterparty',
                                choiceListSource='@CounterpartyPortfolios')
                                                
    price             = Object( label='Price',
                                objMapping='DeltaHedge.Price',
                                enabled='@NotUseLivePrice',
                                visible='@IsDeltaHedgeApplicable')
                                                
    delta             = Object( label='Delta',
                                objMapping='DeltaHedge.Delta',
                                enabled='@NotUseLiveDelta',
                                visible='@IsDeltaHedgeApplicable')
                                    
    amountForeign     = Object( label='Amount Foreign',
                                objMapping='DeltaHedge.AmountCurr1',
                                enabled='@NotUseLiveDelta',
                                visible='@IsDeltaHedgeApplicable')
                                
    amountDomestic    = Object( label='Amount Domestic',
                                objMapping='DeltaHedge.AmountCurr2',
                                enabled='@NotUseLiveDelta',
                                visible='@IsDeltaHedgeApplicable')
                                
    portfolio         = Object( label='Portfolio',
                                objMapping='OptionTrade.Portfolio',
                                mandatory=True)

    acquirer          = Object( label='Acquirer',
                                objMapping='OptionTrade.Acquirer',
                                choiceListSource=AcquirerChoices(),
                                mandatory=True)
    
    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=80)
                                
    # ######################## #
    #    Interface Overrides   #
    # ######################## #      

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_DeltaHedge_DPE')
    
    def OnInit(self):
        self._underlyingChoices = DealPackageChoiceListSource()
    
    def AssemblePackage(self):
        optTradeDeco = self.DealPackage().CreateTrade('FX Option', 'Option')
        optDeco = optTradeDeco.Instrument()

        currPair = acm.FCurrencyPair['EUR/USD']
        if not currPair:
            raise DealPackageException('Failed to get currency pair')
        #Make sure the option has default quotation setup
        optDeco.Currency = currPair.Currency2()
        optTradeDeco.Currency = currPair.Currency2()
        optDeco.StrikeCurrency = currPair.Currency2()
        optDeco.Underlying = currPair.Currency1()
        optDeco.Quotation('Points of UndCurr')
        
        calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        fx_rate = currPair.Currency1().Calculation().FXRate(calcSpace, currPair.Currency2()).Value().Number()
        optDeco.StrikePrice(fx_rate)

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def DeltaHedgeUpdateDelta(self, attributeName):
        self.DeltaHedge().UpdateDelta()
        
    def DeltaHedgeUpdatePrice(self, attributeName):
        self.DeltaHedge().UpdatePrice()

    def IsDeltaHedgeApplicable(self, attributeName):
        return self.DeltaHedge().HedgeType() != 'None'
    
    def NotUseLiveDelta(self, attributeName):
        return not self.useLiveDelta
    
    def NotUseLivePrice(self, attributeName):
        return not self.useLivePrice
    
    def TransformExpPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Option().FxoExpiryDateFromPeriod(newDate)
        return newDate
    
    def Counterparties(self, attributeName):
        return acm.FParty.Select('type <> "Issuer" and type <> "MtM Market"')
    
    def CounterpartyPortfolios(self, attributeName):
        if self._underlyingChoices.IsEmpty():
            self.UpdateCounterpartyPortfolioChoices()
        return self._underlyingChoices

    def IsInternalCounterparty(self, attributeName):
        return self.counterparty and 'Intern Dept' == self.counterparty.Type()

    def ResetCounterpartyPortfolio(self, attributeName, oldValue, newValue, userInputAttributeName):
        self.cpPortfolio = None
    
    def UpdateCounterpartyPortfolioChoices(self, *args):
        self._underlyingChoices.Clear()
        portfolios = acm.FPhysicalPortfolio.Select('compound=0').SortByProperty('StringKey', True)#.AsList()
        choices = [p for p in portfolios if p.PortfolioOwner() == self.counterparty]
        self._underlyingChoices.AddAll(choices)
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def DeltaHedge(self):
        return self.DeltaHedgeParamsAt('Option')
        
    def OptionTrade(self):
        return self.TradeAt('Option')
    
    def Option(self):
        return self.InstrumentAt('Option')

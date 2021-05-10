import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, AcquirerChoices, ReturnDomainDecorator                     

class PremiumTranslation(CompositeAttributeDefinition):

    def OnInit(self, trade, showMode=None):
        self._trade = trade
        self._showMode = showMode
        self._tradeKey = None
        self._fxPortfolioChoices = acm.FChoiceListPopulator()
        
    def Attributes(self):
        return {
                
                'fxAcquirer'                   : Object( label='FX Acquirer',
                                                         choiceListSource=AcquirerChoices(),
                                                         objMapping=self.UniqueCallback('PremiumTransParams') + '.FxAcquirer',
                                                         visible=self.UniqueCallback('@FxPortfolioFxAcquirerVisible'),
                                                         enabled=self.UniqueCallback('@PremiumTranslationFieldsEnabled'),
                                                         width=15),
                                                         
                'fxPortfolio'                  : Object( label='FX Portfolio',
                                                         objMapping=self.UniqueCallback('PremiumTransParams') + '.FxPortfolio',
                                                         choiceListSource=self.UniqueCallback('@FxPortfolioChoices'),
                                                         visible=self.UniqueCallback('@FxPortfolioFxAcquirerVisible'),
                                                         enabled=self.UniqueCallback('@PremiumTranslationFieldsEnabled'),
                                                         width=15),
                                                         
                'fxPrice'                      : Object( label='FX Price',
                                                         objMapping=self.UniqueCallback('PremiumTransParams') + '.FxPrice',
                                                         formatter='InstrumentDefinitionFxPrice',
                                                         visible=self.UniqueCallback('@PremiumTranslationFieldsVisible'),
                                                         enabled=self.UniqueCallback('@PremiumTranslationFieldsEnabled'),
                                                         width=11),
                                                         
                'fxRate'                       : Object( label=self.UniqueCallback('@FxRateLabel'),
                                                         objMapping=self.UniqueCallback('PremiumTransParams') + '.FxRate',
                                                         formatter='InstrumentDefinitionPrice',
                                                         visible=self.UniqueCallback('@PremiumTranslationFieldsVisible'),
                                                         enabled=self.UniqueCallback('@PremiumTranslationFieldsEnabled'),
                                                         width=11),
                                                         
                'settleCurrency'               : Object( label='Settle Curr',
                                                         objMapping=self.UniqueCallback('PremiumTransParams') + '.SettleCurrency',
                                                         onChanged=self.UniqueCallback('@UpdateFxPortfolioChoices'),
                                                         visible=self.UniqueCallback('@PremiumTranslationFieldsVisible'),
                                                         enabled=self.UniqueCallback('@PremiumTranslationFieldsEnabled'),
                                                         width=11)
        }
    
    def GetLayout(self):
        return self.UniqueLayout("""
                                    hbox{;
                                        vbox(;
                                            hbox(;
                                                fxRate;
                                            );
                                            fxPortfolio;
                                        );
                                        vbox(;
                                            settleCurrency;
                                            fxAcquirer;
                                        );
                                        vbox(;
                                            fxPrice;
                                        );
                                    };
                                """)
    
    def PremiumTransParams(self):
        return self.GetMethod('PremiumTranslationParamsAt')(self.TradeKey())

    def Trade(self):
        return self.GetMethod(self._trade)()
        
    def TradeKey(self):
        if not self._tradeKey:
            dp = self.GetMethod('DealPackage')()
            for link in dp.TradeLinks():
                if link.Trade().Oid() == self.Trade().Oid():
                    self._tradeKey = link.Name()
        return self._tradeKey
    
    def IsValid(self, exceptionAccumulator, aspect):
        if aspect == 'DealPackage':
            params = self.PremiumTransParams()
            if params and params.IsActive() and params.UseTrades():
                if not self.Trade().Portfolio():
                    exceptionAccumulator('Trade portfolio must be specified for premium translation')
                if not self.Trade().Acquirer():
                    exceptionAccumulator('Trade acquirer must be specified for premium translation')
                if self.fxPortfolio == self.Trade().Portfolio() and self.fxAcquirer == self.Trade().Acquirer():
                    exceptionAccumulator('FxAcquirer and FxPortfolio cannot be the same as the acquirer and portfolio of the main trade.')
    
    def UpdateFxPortfolioChoices(self, *args):
        params = self.PremiumTransParams()
        currencyPair = None
        if params and params.UseTrades():
            currencyPair = self.PremiumTransParams().CurrencyPair()
            if currencyPair:
                self._fxPortfolioChoices = currencyPair.CurrencyPairPortfolioPopulator()
    
    def FxPortfolioChoices(self, attributeName):
        params = self.PremiumTransParams()
        source = self._fxPortfolioChoices.GetChoiceListSource()
        if params and params.UseTrades():
            if source and source.IsEmpty():
                self.UpdateFxPortfolioChoices()
        return self._fxPortfolioChoices
            

    # Visibility callbacks
    
    def PremiumTranslationFieldsVisible(self, attributeName):
        visible = False
        params = self.PremiumTransParams()
        if params:
            if params.IsActive():
                visible = True
            elif self.Trade().IsPremiumTranslationEligible() and params.IsOn():
                visible = True if not self._showMode else self.GetMethod(self._showMode)()
        return visible
    
    def FxPortfolioFxAcquirerVisible(self, attributeName):
        visible = self.PremiumTranslationFieldsVisible(attributeName)
        params = self.PremiumTransParams()
        if params:
            visible = visible if params.UseTrades() else False
        return visible
    
    # Enabled callbacks
    
    def PremiumTranslationFieldsEnabled(self, attributeName):
        enabled = False
        if not self.Trade().Instrument().Generic():
            params = self.PremiumTransParams()
            if params:
                if params.UseTrades():
                    enabled = True if self.Trade().Premium() != 0.0 else False
                elif params.UsePayments():
                    enabled = True if self.Trade().Premium() != 0.0 or self.Trade().Fee() != 0.0 else False
        return enabled
    
    # Label callbacks
    
    def FxRateLabel(self, attributeName):
        label = ""
        premiumCurr = self.Trade().Currency()
        params = self.PremiumTransParams()
        settleCurr = None
        if params:
            if not params.IsActive():
                label = 'per'
                if premiumCurr:
                    label += premiumCurr.Name()
            else:
                settleCurr = params.SettleCurrency()
                if settleCurr:
                    label += settleCurr.Name()
                label += 'per'
                if premiumCurr:
                    label += premiumCurr.Name()
        return label

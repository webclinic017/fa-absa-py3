import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, CalcVal, ParseSuffixedFloat
from CompositeAttributes import BuySell
from CompositeTradeDefinition import TradeDefinition

class FxForwardTradeDefinition(TradeDefinition):

    def OnInit(self, trade, showBuySell=True, **kwargs):
        super(FxForwardTradeDefinition, self).OnInit(trade, showBuySell, **kwargs)
        self._profitLossCurrencyChoices = DealPackageChoiceListSource()
        self._fxForwardCurrencyTwoChoices = DealPackageChoiceListSource()

    def Attributes(self):
        
        attributes = super(FxForwardTradeDefinition, self).Attributes()
        

        attributes['fxForwardAmount1']            = BuySell( label=self.UniqueCallback('@FxForwardAmounts1Label'),
                                                         buySellLabels=["B", "S", "-"],
                                                         objMapping=self._trade+'.FxForwardAmount1',
                                                         enabled=self.UniqueCallback('@FxForwardAmountsEnabled'),
                                                         showBuySell=False)
        attributes['fxForwardAmount2']            = BuySell( label=self.UniqueCallback('@FxForwardAmounts2Label'),
                                                         buySellLabels=["B", "S", "-"],
                                                         objMapping=self._trade+'.FxForwardAmount2',
                                                         enabled= self.UniqueCallback('@FxForwardAmountsEnabled'),
                                                         showBuySell=False)
        attributes['fxForwardCurrencyOne']        = Object( label='Curr Pair',
                                                         objMapping=self._trade+'.FxForwardCurrencyOne',
                                                         choiceListSource=self.UniqueCallback('@FxForwardCurrencyOneChoices'),
                                                         onChanged=self.UniqueCallback('@UpdateProfitLossCurrencyChoices|@UpdateFxForwardCurrencyTwoChoices'))
        attributes['fxForwardCurrencyTwo']        = Object( label='',
                                                         objMapping=self._trade+'.FxForwardCurrencyTwo',
                                                         choiceListSource=self.UniqueCallback('@FxForwardCurrencyTwoChoices'),
                                                         onChanged=self.UniqueCallback('@UpdateProfitLossCurrencyChoices'))
        attributes['fxForwardSettlementDate']     = Object( label='Settle Date',
                                                         objMapping=self._trade+'.FxForwardSettlementDate',
                                                         transform=self.UniqueCallback('@TransformSettlementPeriodToDate'))
        attributes['fxForwardPoints']             = Object( label='Points',
                                                         objMapping=self._trade+'.FxForwardPoints',
                                                         enabled=self.UniqueCallback('@FxForwardAmountsEnabled'))                                                         
        attributes['profitLossCurrency']          = Object( label='P/L Curr',
                                                         objMapping=self._trade+'.SettlementCurrency',
                                                         choiceListSource=self.UniqueCallback('@ProfitLossCurrencyChoices'))
        attributes['quotingMethod']               = Action( label=self.UniqueCallback('@QuotingMethodLabel'),
                                                         sizeToFit=True,
                                                         action=self.UniqueCallback('@QuotingMethod'))                                                
        
        return attributes
     
    # Enabled callbacks
    def FxForwardAmountsEnabled(self, attributeName):
        return self.Trade().FxForwardCurrencyOne() and self.Trade().FxForwardCurrencyTwo()
        
    # Visible callbacks
        
    # ChoiceListSource callbacks
    def ProfitLossCurrencyChoices(self, attributeName):
        if self._profitLossCurrencyChoices.IsEmpty():
            self.UpdateProfitLossCurrencyChoices()
        return self._profitLossCurrencyChoices
        
    def FxForwardCurrencyOneChoices(self, attributeName):
        return self.Trade().Instrument().DefaultOneCurrencies()
        
    def FxForwardCurrencyTwoChoices(self, attributeName):
        if self._fxForwardCurrencyTwoChoices.IsEmpty():
            self.UpdateFxForwardCurrencyTwoChoices()
        return self._fxForwardCurrencyTwoChoices      
       
    # Label callbacks
    def FxForwardAmounts1Label(self, attributeName):
        if self.FxForwardAmountsEnabled(attributeName):
            return 'Amount '+self.Trade().FxForwardCurrencyOne().Name()
        else:
            return 'Amount 1'
            
    def FxForwardAmounts2Label(self, attributeName):
        if self.FxForwardAmountsEnabled(attributeName):
            return 'Amount '+self.Trade().FxForwardCurrencyTwo().Name()
        else:
            return 'Amount 2'

    def QuotingMethodLabel(self, attributeName):
        if self.FxForwardIsNormalQuoted():
            return 'N'
        else:
            return 'I'
            
    # Transform callbacks
    def TransformSettlementPeriodToDate(self, name, date, *args):
        try:            
            date = self.Trade().FxForwardSettlementDateFromPeriod(date)
            return date
        except:
            return date
             
    # OnChanged callbacks
    def UpdateMirrorPortfolioChoices(self, *args):
        self._mirrorPortfolioChoices.Clear()
        counterparty = self.Trade().Counterparty()
        if counterparty:
            self._mirrorPortfolioChoices.AddAll(counterparty.OwnedPortfolios())
            
    def UpdateCollateralAgreementChoices(self, *args):
        self._collateralAgreementChoices.Clear()
        collateralAgreements = acm.Risk().CollateralAgreements(self.Trade().Counterparty(), self.Trade().Acquirer())
        self._collateralAgreementChoices.AddAll(collateralAgreements)
        
    def UpdateProfitLossCurrencyChoices(self, *args):
        self._profitLossCurrencyChoices.Clear()
        self._profitLossCurrencyChoices.AddAll(self.Trade().Instrument().DefaultDealtCurrencies())
    
    def UpdateFxForwardCurrencyTwoChoices(self, *args):
        self._fxForwardCurrencyTwoChoices.Clear()
        self._fxForwardCurrencyTwoChoices.AddAll(self.Trade().Instrument().DefaultTwoCurrencies())
   
    def QuotingMethod(self, *args):
        self.Trade().FxForwardQuotingMethod()
        
    # Util
    def FxForwardIsNormalQuoted(self):
        quotationType = self.Trade().Instrument().Quotation().QuotationType()
        underlyingCurrency = self.Trade().Instrument().Underlying()
        currencyPair = self.Trade().CurrencyPair()
        if currencyPair:
            return ( (quotationType != 'Per Unit Inverse' and underlyingCurrency == currencyPair.Currency1()) or
                     (quotationType == 'Per Unit Inverse' and underlyingCurrency == currencyPair.Currency2()) )
        else:
            return True

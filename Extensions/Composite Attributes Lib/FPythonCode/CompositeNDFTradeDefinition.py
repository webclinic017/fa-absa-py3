import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, CalcVal, ParseSuffixedFloat
from CompositeAttributes import BuySell  
from CompositeTradeDefinition import TradeDefinition

class NDFTradeDefinition(TradeDefinition):

    def OnInit(self, trade, showBuySell=True, **kwargs):
        super(NDFTradeDefinition, self).OnInit(trade, showBuySell, **kwargs)
        self._settlementCurrencyChoices = DealPackageChoiceListSource()
        self._ndfCurrencyTwoChoices = DealPackageChoiceListSource()

    def Attributes(self):
        
        attributes = super(NDFTradeDefinition, self).Attributes()
        

        attributes['fxNDFAmount1']            = BuySell( label=self.UniqueCallback('@NDFAmounts1Label'),
                                                         buySellLabels=["B", "S", "-"],
                                                         objMapping=self._trade+'.FxForwardAmount1',
                                                         enabled=self.UniqueCallback('@NDFAmountsEnabled'),
                                                         showBuySell=False)
        attributes['fxNDFAmount2']            = BuySell( label=self.UniqueCallback('@NDFAmounts2Label'),
                                                         buySellLabels=["B", "S", "-"],
                                                         objMapping=self._trade+'.FxForwardAmount2',
                                                         enabled= self.UniqueCallback('@NDFAmountsEnabled'),
                                                         showBuySell=False)
        attributes['fxNDFCurrencyOne']        = Object( label='Curr Pair',
                                                         objMapping=self._trade+'.FxForwardCurrencyOne',
                                                         choiceListSource=self.UniqueCallback('@NDFCurrencyOneChoices'),
                                                         onChanged=self.UniqueCallback('@UpdateSettlementCurrencyChoices|@UpdateNDFCurrencyTwoChoices'))
        attributes['fxNDFCurrencyTwo']        = Object( label='',
                                                         objMapping=self._trade+'.FxForwardCurrencyTwo',
                                                         choiceListSource=self.UniqueCallback('@NDFCurrencyTwoChoices'),
                                                         onChanged=self.UniqueCallback('@UpdateSettlementCurrencyChoices'))
        attributes['fxNDFSettlementDate']     = Object( label='Settle Date',
                                                         objMapping=self._trade+'.FxForwardSettlementDate',
                                                         transform=self.UniqueCallback('@TransformSettlementPeriodToDate'))
        attributes['fxNDFPoints']             = Object( label='Points',
                                                         objMapping=self._trade+'.FxForwardPoints',
                                                         enabled=self.UniqueCallback('@NDFAmountsEnabled'))                                                         
        attributes['settlementCurrency']      = Object( label='Settle Curr',
                                                         objMapping=self._trade+'.SettlementCurrency',
                                                         choiceListSource=self.UniqueCallback('@SettlementCurrencyChoices'))
        attributes['quotingMethod']           = Action( label=self.UniqueCallback('@QuotingMethodLabel'),
                                                         sizeToFit=True,
                                                         action=self.UniqueCallback('@QuotingMethod'))
                                                        
        
        return attributes
     
    # Enabled callbacks
    def NDFAmountsEnabled(self, attributeName):
        return self.Trade().FxForwardCurrencyOne() and self.Trade().FxForwardCurrencyTwo()
        
    # Visible callbacks
        
    # ChoiceListSource callbacks
    def SettlementCurrencyChoices(self, attributeName):
        if self._settlementCurrencyChoices.IsEmpty():
            self.UpdateSettlementCurrencyChoices()
        return self._settlementCurrencyChoices
        
    def NDFCurrencyOneChoices(self, attributeName):
        return self.Trade().Instrument().DefaultOneCurrencies()
        
    def NDFCurrencyTwoChoices(self, attributeName):
        if self._ndfCurrencyTwoChoices.IsEmpty():
            self.UpdateNDFCurrencyTwoChoices()
        return self._ndfCurrencyTwoChoices      
       
    # Label callbacks
    def NDFAmounts1Label(self, attributeName):
        if self.NDFAmountsEnabled(attributeName):
            return 'Amount '+self.Trade().FxForwardCurrencyOne().Name()
        else:
            return 'Amount 1'
            
    def NDFAmounts2Label(self, attributeName):
        if self.NDFAmountsEnabled(attributeName):
            return 'Amount '+self.Trade().FxForwardCurrencyTwo().Name()
        else:
            return 'Amount 2'
            
    def QuotingMethodLabel(self, attributeName):
        if self.NDFIsNormalQuoted():
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
        
    def UpdateSettlementCurrencyChoices(self, *args):
        self._settlementCurrencyChoices.Clear()
        self._settlementCurrencyChoices.AddAll(self.Trade().Instrument().DefaultDealtCurrencies())
    
    def UpdateNDFCurrencyTwoChoices(self, *args):
        self._ndfCurrencyTwoChoices.Clear()
        self._ndfCurrencyTwoChoices.AddAll(self.Trade().Instrument().DefaultTwoCurrencies())
    
    def QuotingMethod(self, *args):
        self.Trade().FxForwardQuotingMethod()

    # Util
    def NDFIsNormalQuoted(self):
        quotationType = self.Trade().Instrument().Quotation().QuotationType()
        underlyingCurrency = self.Trade().Instrument().Underlying()
        currencyPair = self.Trade().CurrencyPair()
        if currencyPair:
            return ( (quotationType != 'Per Unit Inverse' and underlyingCurrency == currencyPair.Currency1()) or
                     (quotationType == 'Per Unit Inverse' and underlyingCurrency == currencyPair.Currency2()) )
        else:
            return True

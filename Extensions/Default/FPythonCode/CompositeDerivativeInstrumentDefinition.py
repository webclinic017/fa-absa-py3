import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool
from CompositeInstrumentDefinition import InstrumentDefinition

class DerivativeInstrumentDefinition(InstrumentDefinition):

    def OnInit(self, instrument, **kwargs):
        super(DerivativeInstrumentDefinition, self).OnInit(instrument, **kwargs)

    def Attributes(self):
        
        attributes = super(DerivativeInstrumentDefinition, self).Attributes()
        
        attributes['dividendAdjustment']      = Object( label='Dividend Adjustment',
                                                        objMapping=self._instrument+'.DividendAdjustment')
        
        attributes['expiryDateTime']          = Object( label='Expiry',
                                                        objMapping=self._instrument+'.ExpiryDateTime',
                                                        visible=self.UniqueCallback('@ExpiryDateTimeVisible'),
                                                        enabled=self.UniqueCallback('@ExpiryDateTimeEnabled'),
                                                        width=22)
                                                        
        attributes['expiryPeriod']            = Object( label='',
                                                        objMapping=self._instrument+'.ExpiryPeriod',
                                                        enabled=self.UniqueCallback('@ExpiryPeriodEnabled'),
                                                        width=8,
                                                        maxWidth=8)
                                                        
        attributes['firstNoticeDate']         = Object( label='1st Notice',
                                                        objMapping=self._instrument+'.FirstNoticeDate',
                                                        visible=self.UniqueCallback('@FirstNoticeDateVisible')) 
                                                        
        attributes['fixingSourceExpiryDate']  = Object( label='Expiry',
                                                        objMapping=self._instrument+'.FixingSourceExpiryDate',
                                                        transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                        visible=self.UniqueCallback('@FixingSourceExpiryDateVisible'),
                                                        enabled=self.UniqueCallback('@FixingSourceExpiryDateEnabled'),
                                                        width=22)
                                                        
        attributes['fxForwardFixingDate']     = Object( label='Fixing Date',
                                                        objMapping=self._instrument+'.FxForwardFixingDate',
                                                        transform=self.UniqueCallback('@TransformPeriodToDate'))
        
        attributes['quantoOptionType']        = Object( label='Quanto',
                                                        objMapping=self._instrument+'.QuantoOptionType',
                                                        visible=self.UniqueCallback('@QuantoOptionTypeVisible'))
        
        attributes['fixFxRate']               = Object( label='Fix FX Rate',
                                                        objMapping=self._instrument+'.FixFxRate',
                                                        visible=self.UniqueCallback('@FixFXRateVisible'))
        
        attributes['strikeCurrency']          = Object( label='Strike Curr',
                                                        objMapping=self._instrument+'.StrikeCurrency',
                                                        enabled=self.UniqueCallback('@StrikeCurrencyEnabled'),
                                                        visible=self.UniqueCallback('@StrikeCurrencyVisible'))
        
        return attributes
    
    # Enabled callbacks
    def ExpiryDateTimeEnabled(self, attributeName):
        return self.Instrument().IsEnabled('ExpiryDateTime')
        
    def ExpiryPeriodEnabled(self, attributeName):
        return self.Instrument().Generic()
    
    def FixingSourceExpiryDateEnabled(self, attributeName):
        return self.Instrument().IsEnabled('FixingSourceExpiryDate')
    
    def StrikeCurrencyEnabled(self, attributeName):
        return self.Instrument().IsEnabled('StrikeCurrency')
    
    # Visible callbacks
    def ExpiryDateTimeVisible(self, attributeName):
        return self.Instrument().IsVisible('ExpiryDateTime', self.IsShowModeDetail())
        
    def FixingSourceExpiryDateVisible(self, attributeName):
        return self.Instrument().IsVisible('FixingSourceExpiryDate', self.IsShowModeDetail())
        
    def FirstNoticeDateVisible(self, attributeName):
        if self.settlementType == 'Physical':
            return (self.Instrument().IsCommodityDerivative() or self.IsShowModeDetail())
        else:
            return False
    
    def QuantoOptionTypeVisible(self, attributeName):
        if self.ExoticNeverShow(self.underlyingType):
            return False
        elif self.Instrument().InsType() in ['VarianceSwap', 'VolatilitySwap']:
            return (self.IsShowModeDetail() or self.Instrument().QuantoOptionType() == 'Quanto')
        elif self.Instrument().IsFuture():
            return self.IsCurrFutureOrDetail()
        elif self.underlyingType in ['Average Future/Forward', 'Bill', 'Bond', 'CFD', 'CLN', 'Commodity Index', 'CreditDefaultSwap', 'CurrSwap', 'Deposit', 'FreeDefCF', 'FRA', 'FRN', 'IndexLinkedSwap', 'PromisLoan', 'RateIndex', 'Swap', 'TotalReturnSwap', 'VarianceSwap', 'Zero']:
            return (self.IsShowModeDetail() or self.Instrument().QuantoOptionType() in ['Quanto', 'Custom'])
        else:
            return True
    
    def FixFXRateVisible(self, attributeName):
        if self.ExoticNeverShow(self.underlyingType):
            return False
        elif not self.Instrument().IsFuture() and self.underlyingType in ['Average Future/Forward', 'Bill', 'Bond', 'CFD', 'CLN', 'Commodity Index', 'CreditDefaultSwap', 'CurrSwap', 'Deposit', 'FreeDefCF', 'FRA', 'FRN', 'IndexLinkedSwap', 'PromisLoan', 'RateIndex', 'Swap', 'TotalReturnSwap', 'VarianceSwap', 'Zero']:
            return (self.IsShowModeDetail() or self.Instrument().QuantoOptionType() in ['Quanto', 'Custom'])
        else:
            return self.Instrument().QuantoOptionType() in ['Custom', 'Quanto']
    
    def StrikeCurrencyVisible(self, attributeName):
        return self.Instrument().IsVisible('StrikeCurrency', self.IsShowModeDetail())
    
    # Transform callbacks
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date 

        
    # Action


    # OnChanged callbacks
    def ExoticNeverShow(self, undType):
        return undType in ['Option', 'Warrant', 'Cap', 'Floor', 'Collar', 'Convertible']
        
    # Util
    def IsCurrFutureOrDetail(self):
        isQuanto = 'Quanto' == str(self.Instrument().QuantoOptionType())
        isFuture = 'Future' == str(self.Instrument().PayType())
        isUndCurr = 'Curr' == str(self.Instrument().UnderlyingType())
        return (isQuanto or (isFuture and (self.IsShowModeDetail() or isUndCurr)))

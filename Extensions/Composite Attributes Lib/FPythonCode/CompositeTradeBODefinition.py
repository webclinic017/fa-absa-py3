import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, ReturnDomainDecorator, DealPackageException

class TradeBODefinition(CompositeAttributeDefinition):
    def OnInit(self, trade, **kwargs):
        self._trade = trade
        
    def Attributes(self):
        return { 
                 'baseCurrencyPerCurrency1': Object( label=self.UniqueCallback('@BaseCurrencyPerCurrency1Label'),
                                                         objMapping=self._trade+'.BaseCurrencyPerCurrency1',                                                         formatter='SixDecimalDetailedShowZero'),
                 'baseCurrencyPerCurrency2': Object( label=self.UniqueCallback('@BaseCurrencyPerCurrency2Label'),
                                                         objMapping=self._trade+'.BaseCurrencyPerCurrency2',
                                                         formatter='SixDecimalDetailedShowZero'),
                 'baseCurrencyEquivalent': Object( label=self.UniqueCallback('@BaseCurrencyEquivalentLabel'),
                                                         objMapping=self._trade+'.BaseCurrencyEquivalent',
                                                         enabled=False),                                                         
                 'boFXRate': Object( label='BO FX Rate',
                                                         objMapping=self._trade+'.BoFxRate',
                                                         visible='@IsShowModeTradeDetail'), 
                 'calcAgent': Object( label='Calc Agent',
                                                         objMapping=self._trade+'.Calcagent'),  
                 'contractTrdnbr': Object( label='Contract Ref',
                                                         objMapping=self.UniqueCallback('ContractTrade')), 
                 'connectedTrdnbr': Object( label='Connect Ref',
                                                         objMapping=self.UniqueCallback('ConnectedTrade'),
                                                         editable=False,
                                                         enabled=True), 
                 'correctionTrade': Object( label='CorrectRef',
                                                         objMapping=self.UniqueCallback('CorrectionTrade'),
                                                         editable=False,
                                                         enabled=True), 
                 'documentType': Object( label='Document',
                                                         objMapping=self._trade+'.DocumentType',
                                                         choiceListSource=acm.GetDomain("FChoiceList('Standard Document')").Instances()),
                 'executionTime': Object( label='Exec Time',
                                                         objMapping=self.UniqueCallback('ExecTime'),
                                                         editable=False,
                                                         enabled=True), 
                 'groupTrdnbr': Object( label='Group Ref',
                                                         objMapping=self.UniqueCallback('GroupTrade'),
                                                         editable=False,
                                                         enabled=True),  
                 'hedgeRef': Object( label='Hedge Ref',
                                                         objMapping=self.UniqueCallback('HedgeTrade'),
                                                         visible='@IsShowModeTradeDetail'), 
                 'interestRateAtTradeTime': Object( label='Gap Rate',
                                                         objMapping=self._trade+'.InterestRateAtTradeTime',
                                                         formatter='VeryDetailedPercentShowZeroClearToZero'),
                 'mirrorTrade': Object( label='Mirror Ref',
                                                         objMapping=self.UniqueCallback('MirrorTrade'),
                                                         editable=False,
                                                         enabled=True), 
                 'openingBoTrade': Object( label='BO Ref',
                                                         objMapping=self.UniqueCallback('OpeningBoTrade')),
                 'optionalKey': Object( label='External ID',
                                                         objMapping=self._trade+'.OptionalKey'),
                 'dealPackage': Object( label='Deal Pkg',
                                                         objMapping=self.UniqueCallback('DealPkg'),
                                                         editable=False,
                                                         enabled=True), 
                 'tradePackage': Object( label='Trade Pkg',
                                                         objMapping=self.UniqueCallback('TradePkg'),
                                                         editable=False,
                                                         enabled=True, 
                                                         visible='@IsShowModeTradeDetail'),
                 'primaryIssuance': Object( label='Primary Issuance',
                                                         objMapping=self._trade+'.PrimaryIssuance'), 
                 'suggestIntRateAtTradeTime': Action( label='Suggest',
                                                         sizeToFit=True,
                                                         action=self.UniqueCallback('@SuggestInterestRateAtTradeTime')),   
                 'text1': Object( label='Free Text 1',
                                                         objMapping=self._trade+'.Text1'),             
                 'text2': Object( label='Free Text 2',
                                                         objMapping=self._trade+'.Text2'),  
                 'tradeProcesses': Object( label='Trd Process',
                                                         objMapping=self._trade+'.TradeProcesses',
                                                         editable=False,
                                                         enabled=True), 
                 'trxTrade': Object( label='Trans Ref',
                                                         objMapping=self.UniqueCallback('TrxTrade')),  
                 'type': Object( label='Trade Type',
                                                         objMapping=self._trade+'.Type'),
                 'uniqueTradeIdentifier': Object( label='UTI',
                                                         objMapping=self._trade+'.UniqueTradeIdentifier'),

 }
  
    def IsShowModeDetail(self, *args):
        return self.Owner().GetAttribute('uiViewModeIsSlim').At("DetailedMode2") == False
           
    # Actions
    def SuggestInterestRateAtTradeTime(self, *args):
        self.Trade().SuggestInterestRateAtTradeTime()
        
    # Label
    def BaseCurrencyPerCurrency1Label(self, attributeName):
        label = ''
        baseCurrency = self.BaseCurrency()
        if self.Trade().InstrumentPair():
            otherCurrency = self.Trade().InstrumentPair().Instrument1()
            pair = baseCurrency.InstrumentPair(otherCurrency)
            label = pair.Name() if pair else str(otherCurrency.Name() + '/' + baseCurrency.Name())
        else:
            label = baseCurrency.Name() + '/Curr2'
        return label
        
    def BaseCurrencyPerCurrency2Label(self, attributeName):
        label = ''
        baseCurrency = self.BaseCurrency()
        if self.Trade().InstrumentPair():
            otherCurrency = self.Trade().InstrumentPair().Instrument2()
            pair = baseCurrency.InstrumentPair(otherCurrency)
            label = pair.Name() if pair else str(otherCurrency.Name() + '/' + baseCurrency.Name())
        else:
            label = baseCurrency.Name() + '/Curr1'
        return label
        
    def BaseCurrencyEquivalentLabel(self, attributeName):
        return self.BaseCurrency().Name()+' Eqv'
    
    def BaseCurrency(self):
        mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
        currency = mappedValuationParameter().Parameter().FxHolidayObservanceBaseCurrency()
        return currency
        
    # Choices
        
    # Changed
        
    # Transform
        
    # Color callbacks
        
    # Util
    def Trade(self):
        return self.GetMethod(self._trade)()
        
    @ReturnDomainDecorator('string')
    def DealPkg(self, value = '*Reading*'):
        if value == '*Reading*':
            oid = self.Trade().OriginalDealPackageNumber()
            return str(oid) if oid > 0 else ''
            
    @ReturnDomainDecorator('string')
    def TradePkg(self, value = '*Reading*'):
        if value == '*Reading*':
            oid = self.Trade().OriginalTradePackageNumber()
            return str(oid) if oid > 0 else ''
              
    @ReturnDomainDecorator('string')
    def ExecTime(self, value = '*Reading*'):
        if value == '*Reading*':
            exectime = self.Trade().ExecutionTime()
            return exectime if acm.Time().DateDifference(acm.Time().AsDate(exectime), acm.Time().SmallDate()) > 0 else ''
            
    @ReturnDomainDecorator('string')
    def HedgeTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            hedgeTrade = self.Trade().HedgeTrade()
            return hedgeTrade.Oid() if hedgeTrade else ''
        else:
            value = int(acm.GetDomain('int').DefaultFormatter().Parse(value))
            hedgeTrade = acm.FTrade[value] if value else None
            if not hedgeTrade and value:
                raise DealPackageException('No Trade')
            self.Trade().HedgeTrade(hedgeTrade)
            
    @ReturnDomainDecorator('string')
    def TrxTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            trxTrade = self.Trade().TrxTrade()
            return trxTrade.Oid() if trxTrade else ''
        else:
            value = int(acm.GetDomain('int').DefaultFormatter().Parse(value))
            trxTrade = acm.FTrade[value] if value else None
            if not trxTrade and value:
                raise DealPackageException('No Trade')
            self.Trade().TrxTrade(trxTrade)

    @ReturnDomainDecorator('string')
    def ContractTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            contractTrdnbr = self.Trade().ContractTrdnbr()
            return contractTrdnbr if contractTrdnbr else ''
        else:
            value = int(acm.GetDomain('int').DefaultFormatter().Parse(value))
            contractTrade = acm.FTrade[value] if value else None
            if not contractTrade and value:
                raise DealPackageException('No Trade')
            self.Trade().ContractTrdnbr(value)
                
    @ReturnDomainDecorator('string')
    def OpeningBoTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            boNbr = self.Trade().OpeningBoTrade()
            return boNbr if boNbr else ''
        else:
            self.Trade().OpeningBoTrade(value)
            
    @ReturnDomainDecorator('string')
    def ConnectedTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            connTrade = self.Trade().ConnectedTrade()
            return connTrade.Oid() if connTrade else ''  

    @ReturnDomainDecorator('string')
    def CorrectionTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            corrTrade = self.Trade().CorrectionTrade()
            return corrTrade.Oid() if corrTrade else ''            
            
    @ReturnDomainDecorator('string')
    def MirrorTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            mirror = self.Trade().MirrorTrade()
            return mirror.Oid() if mirror else ''
            
    @ReturnDomainDecorator('string')
    def GroupTrade(self, value = '*Reading*'):
        if value == '*Reading*':
            groupTrade = self.Trade().GroupTrdnbr()
            return groupTrade.Oid() if groupTrade else ''              
        

    def GetLayout(self):
        return self.UniqueLayout(
                    """
                    """
                )

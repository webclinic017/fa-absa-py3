import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool
from ChoicesExprInstrument import getFixingSources, getSeniorityChoices, getYTMChoices, getPayTypeChoices, getSettlementTypeChoices, getUnderlyingChoices, getOptionTypeChoices
from ChoicesExprParty import getRating1Choices, getRating2Choices, getRating3Choices

class InstrumentDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, instrument, **kwargs):
        self._instrument = instrument 
        self._optionTypeChoices = DealPackageChoiceListSource()
        self._underlyingChoices = DealPackageChoiceListSource()
        self._quotationChoices = DealPackageChoiceListSource()
        
    def Attributes(self):
        return { 
                'accruedArrear': Object( label='In Arrear',
                                                        objMapping=self._instrument+'.AccruedArrear',
                                                        visible=self.UniqueCallback('@AccruedArrearVisible')),
                 'contractSize': Object( label='Contr Size',
                                                        objMapping=self._instrument+'.ContractSize',
                                                        visible=self.UniqueCallback('@ContractSizeVisible'),
                                                        formatter='InstrumentDefintionContrSize'),
                 'contractSizeInQuotation': Object( label='Quot Size',
                                                        objMapping=self._instrument+'.ContractSizeInQuotation',
                                                        visible=self.UniqueCallback('@ContractSizeInQuotationVisible'),
                                                        formatter='InstrumentDefintionContrSize'),
                 'conversionRatio': Object( label='Conv Ratio',
                                                        objMapping=self._instrument+'.ConversionRatio',
                                                        formatter='SixDecimalDetailedShowZero'),                                
                 'currency': Object( label='Currency',
                                                        objMapping=self._instrument+'.Currency'),
                 'digital': Object( label='Digital',
                                                        objMapping=self._instrument+'.Digital',
                                                        visible=self.UniqueCallback('@DigitalVisible')),
                 'discountingType': Object( label='Disc Type',
                                                        objMapping=self._instrument+'.DiscountingType',
                                                        choiceListSource=acm.GetDomain("FChoiceList('DiscType')").Instances(),
                                                        width=12),
                 'dividendFactor': Object( label='Factor',
                                                        objMapping=self._instrument+'.DividendFactor',
                                                        visible='@IsShowModeInstrumentDetail'),
                 'fixingSource': Object( label='FX Source',
                                                        objMapping=self._instrument+'.FixingSource',
                                                        choiceListSource=self.UniqueCallback('@FixingSourceChoices'),
                                                        visible=self.UniqueCallback('@FixingSourceVisible')),
                 'issuer': Object( label='Issuer',
                                                        objMapping=self._instrument+'.Issuer',            
                                                        choiceListSource=self.UniqueCallback('@IssuerChoices')),
                 'name': Object( label='Name',
                                                        objMapping=self._instrument+'.Name'),
                 'nominal': Object( label='Nominal',
                                                        objMapping=self._instrument+'.Nominal',
                                                        visible='@IsShowModeInstrumentDetail'),
                 'notional': Object( label='Notional',
                                                        objMapping=self._instrument+'.Notional',
                                                        visible='@IsShowModeInstrumentDetail'),
                 'openEnd': Object( label='Open End',
                                                        objMapping=self._instrument+'.OpenEnd'),
                 'optionType': Object( label='',
                                                        objMapping=self._instrument+'.OptionType',
                                                        choiceListSource=self.UniqueCallback('@OptionTypeChoices')),
                 'otc': Object( label='OTC',
                                                        objMapping=self._instrument+'.Otc'),
                 'payDayOffset': Object( label='Settle Days',
                                                        objMapping=self._instrument+'.PayDayOffset',
                                                        width=13),
                 'payType': Object( label='Pay Type',
                                                        objMapping=self._instrument+'.PayType',
                                                        choiceListSource=self.UniqueCallback('@PayTypeChoices'),
                                                        width=18),
                 'quotation': Object( label='Quotation',
                                                        objMapping=self._instrument+'.Quotation',
                                                        choiceListSource=self.UniqueCallback('@QuotationChoices'),
                                                        width=18),
                 'rating1ChlItem': Object( label=self.UniqueCallback('@Rating1Label'),
                                                        objMapping=self._instrument+'.Rating1ChlItem',
                                                        choiceListSource=getRating1Choices(),
                                                        visible=self.UniqueCallback('@Rating1Visible')),
                 'rating2ChlItem': Object( label=self.UniqueCallback('@Rating2Label'),
                                                        objMapping=self._instrument+'.Rating2ChlItem',
                                                        choiceListSource=getRating2Choices(),
                                                        visible=self.UniqueCallback('@Rating2Visible')),
                 'rating3ChlItem': Object( label=self.UniqueCallback('@Rating3Label'),
                                                        objMapping=self._instrument+'.Rating3ChlItem',
                                                        choiceListSource=getRating3Choices(),
                                                        visible=self.UniqueCallback('@Rating3Visible')),
                 'refPrice': Object( label='Ref Price',
                                                        objMapping=self._instrument+'.RefPrice',
                                                        visible='@IsShowModeInstrumentDetail'),
                 'seniorityChlItem': Object( label='Seniority',
                                                        objMapping=self._instrument+'.SeniorityChlItem',
                                                        choiceListSource=getSeniorityChoices(),
                                                        visible=self.UniqueCallback('@SeniorityVisible')),
                 'settlementType': Object( label='',
                                                        objMapping=self._instrument+'.SettlementType',
                                                        choiceListSource=self.UniqueCallback('@SettlementTypeChoices')),
                 'shortDividendFactor': Object( label='Short Factor',
                                                        objMapping=self._instrument+'.ShortDividendFactor',
                                                        visible='@IsShowModeInstrumentDetail'), 
                 'underlying': Object( label='Underlying',
                                                        objMapping=self._instrument+'.Underlying',
                                                        choiceListSource=self.UniqueCallback('@UnderlyingChoices')),                                                        
                 'underlyingType': Object( label='',
                                                        objMapping=self._instrument+'.UnderlyingType',
                                                        choiceListSource=self.UniqueCallback('@ValidUnderlyingTypes'),
                                                        onChanged=self.UniqueCallback('@UpdateUnderlyingChoices|@UpdateOptionTypeChoices|@UpdateExerciseTypeChoices|@UpdateQuotationChoices'),
                                                        maxWidth=20),                                                    
        
                 'valuationGrpChlItem': Object( label='Val Group',
                                                        objMapping=self._instrument+'.ValuationGrpChlItem',
                                                        choiceListSource=acm.GetDomain("FChoiceList('ValGroup')").Instances(),
                                                        visible='@IsShowModeInstrumentDetail'),
                 'ytmMethod': Object( label='YTM Meth',
                                                        objMapping=self._instrument+'.YTMMethod',
                                                        choiceListSource=self.UniqueCallback('@YTMChoices'),
                                                        visible='@IsShowModeInstrumentDetail'),
                                                        
                 'dividendSettlementType': Object( label='Div Settle',
                                                        objMapping=self._instrument+'.DividendSettlementType',
                                                        visible=self.UniqueCallback('@DividendSettlementTypeVisible')), 
        
               }
    # Enabled callbacks


    # Label callbacks
    def Rating1Label(self, attributeName):
        label = ''
        if acm.ChoiceList.Rating1ChoiceList():
            label = acm.ChoiceList.Rating1ChoiceList().Name()
        return label
        
    def Rating2Label(self, attributeName):
        label = ''
        if acm.ChoiceList.Rating2ChoiceList():
            label = acm.ChoiceList.Rating2ChoiceList().Name()
        return label
        
    def Rating3Label(self, attributeName):
        label = ''
        if acm.ChoiceList.Rating3ChoiceList():
            label = acm.ChoiceList.Rating3ChoiceList().Name()
        return label
        
    # ChoiceListSource callbacks
    def QuotationChoices(self, attributeName):
        if self._quotationChoices.IsEmpty():
            self.UpdateQuotationChoices()
        return self._quotationChoices    
    
    def FixingSourceChoices(self, attributeName):
        unFilteredListInsTypes=['Cap', 'Floor', 'CurrencySwap', 'Average Future/Forward', 'Swap']
        filter=self.Instrument().InsType() not in unFilteredListInsTypes
        return getFixingSources(filter)

    def IssuerChoices(self, attributeName):
        return acm.FParty.Select('issuer=true')
        
    def OptionTypeChoices(self, attributeName):
        if self._optionTypeChoices.IsEmpty():
            self.UpdateOptionTypeChoices()
        return self._optionTypeChoices

    def PayTypeChoices(self, attributeName):
        return getPayTypeChoices(self.Instrument())
        
    def SettlementTypeChoices(self, attributeName):
        return getSettlementTypeChoices(self.Instrument())
        
    def UnderlyingChoices(self, attributeName):
        if self._underlyingChoices.IsEmpty():
            self.UpdateUnderlyingChoices()
        return self._underlyingChoices 

    def ValidUnderlyingTypes(self, attributeName):
        return self.Instrument().ValidUnderlyingTypes()   
 
    def YTMChoices(self, attributeName):
        return getYTMChoices(self.Instrument())
        
    
    # OnChanged callbacks
    def UpdateUnderlyingChoices(self, *args):
        self._underlyingChoices.Populate(getUnderlyingChoices(self.Instrument()))
        
    def UpdateOptionTypeChoices(self, *args):
        self._optionTypeChoices.Populate(getOptionTypeChoices(self.underlyingType))
        
    def UpdateExerciseTypeChoices(self, *args):
        pass
        
    def UpdateQuotationChoices(self, *args):
        self._quotationChoices.Populate(self.Instrument().DefaultQuotations())
        
    # Visible callbacks
    def Rating1Visible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().Rating1ChlItem()
        
    def Rating2Visible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().Rating2ChlItem()
        
    def Rating3Visible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().Rating3ChlItem()
        
    def SeniorityVisible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().SeniorityChlItem()
        
    def AccruedArrearVisible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().AccruedArrear()
    
    def ContractSizeVisible(self, attributeName):
        if self.Instrument().IsCommodityDerivative():
            if self.Instrument().Underlying():
                return self.IsShowModeDetail()
            else:
                return True
        else:
            return True
        
    def ContractSizeInQuotationVisible(self, attributeName):
        if (self.Instrument().IsCommodityDerivative() and self.Instrument().Underlying()):
            return True

    def DigitalVisible(self, attributeName):
        return True
        
    def DividendSettlementTypeVisible(self, attributeName):
        return self.underlyingType in ("EquityIndex", "Stock", "Depositary Receipt")
        
    def FixingSourceVisible(self, attributeName):
        return self.Instrument().IsVisible('FixingSource', self.IsShowModeDetail())
        
    # Util        
    def Instrument(self):
        return self.GetMethod(self._instrument)()
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                   """
               )

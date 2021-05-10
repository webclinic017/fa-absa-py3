
import acm
from DealPackageDevKit import CompositeAttributeDefinition, Action, Date, DatePeriod, Delegate
from DealPackageDevKit import AttributeDialog, DealPackageChoiceListSource, DealPackageUserException, CounterpartyChoices
from PairOptionsFormatters import GetFXSpotForwardFormatter, AmountFormatter

class GenerateStripLegs(CompositeAttributeDefinition):
    def OnInit(self, templatePackage, **kwargs):
        self._templatePackageName = templatePackage
        self._subTypeChoices = DealPackageChoiceListSource()

    def Attributes(self):
        attr =  {
                'instrumentPair'  : Delegate(   label='Curr Pair',
                                                attributeMapping='TemplatePackage.instrumentPair',
                                                enabled=self.UniqueCallback('@AllowChangeCurrency')),
                                
                'premiumCurrency' : Delegate(   label='Premium',
                                                attributeMapping='TemplatePackage.premiumCurrency',
                                                enabled=self.UniqueCallback('@AllowChangeCurrency')),
                
                'rolling'         : DatePeriod( defaultValue='3m',
                                                label='Rolling'),

                'startDate'       : Date(       defaultValue=self.TransformDate(self.PrefixedName('startDate'), '3m'),
                                                label='Start Date',
                                                transform=self.UniqueCallback('@TransformDate')),
                
                'endDate'         : Date(       defaultValue=self.TransformDate(self.PrefixedName('endDate'), '12m'),
                                                label='End Date',
                                                transform=self.UniqueCallback('@TransformDate')),
                                                
                'strikeForeignPerDomestic': Delegate(   label='Strike',
                                                        attributeMapping='TemplatePackage.strikeForeignPerDomestic',
                                                        visible=self.UniqueCallback('@EnabledIfFlipped')),
                                                        
                'strikeDomesticPerForeign': Delegate(   label='Strike',
                                                        attributeMapping='TemplatePackage.strikeDomesticPerForeign',
                                                        visible=self.UniqueCallback('@EnabledIfNotFlipped')),

                'amountForeign'     : Delegate(   attributeMapping='TemplatePackage.amountForeign',
                                                enabled=self.UniqueCallback('@EnabledIfNotFlipped'),
                                                formatter='NumDefault',
                                                transform=self.UniqueCallback('@TransformAmount')),
                                         
                'amountDomestic'    : Delegate(   attributeMapping='TemplatePackage.amountDomestic',
                                                enabled=self.UniqueCallback('@EnabledIfFlipped'),
                                                formatter='NumDefault',
                                                transform=self.UniqueCallback('@TransformAmount')),
                                         
                'optionType'        : Delegate(   attributeMapping='TemplatePackage.optionType'),
                
                'baseType'          : Delegate(   attributeMapping='TemplatePackage.baseType'),
                
                'subtypeForeign'    : Delegate(   attributeMapping='TemplatePackage.subtypeForeign',
                                                    visible=self.UniqueCallback('@EnabledIfNotFlipped'),
                                                    choiceListSource = self.UniqueCallback('@SubtypeForeignChoices')),
                
                'subtypeDomestic'   : Delegate(   attributeMapping='TemplatePackage.subtypeDomestic',
                                                  visible=self.UniqueCallback('@EnabledIfFlipped')  ),

                'generateDialog'    : Action(     dialog=AttributeDialog( 
                                                  label='Generate Strip', 
                                                  customPanes=self.UniqueCallback('@GetGenerateStripPanes'),
                                                  btnLabel='Generate'),
                                                action=self.UniqueCallback('@OnApply'))
                }
                
        self.Owner().RegisterCallbackOnAttributeChanged(self.AttributeChanged, last=True)
        
        return attr
        
    def AttributeChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        if attributeName == 'generateStripLegs_baseType':
            self.UpdateSubtypeForeignChoices()
    
    def UpdateSubtypeForeignChoices(self, *args):
        choices = self.TemplatePackage().GetAttributeMetaData('subtypeForeign', 'choiceListSource')()
        self._subTypeChoices.Populate(choices.GetChoiceListSource())
        
    def SubtypeForeignChoices(self, *args):
        if self._subTypeChoices.IsEmpty():
            self.UpdateSubtypeForeignChoices()
        return self._subTypeChoices        
        
    '''*******************************************************
    * Transform Methods
    *******************************************************'''            
    def TransformDate(self, attrName, value):
        fxo = self.TemplatePackage().Instruments().First()
        return fxo.FxoExpiryDateTimeFromString(value)
        
    def TransformAmount(self, fullAttrName, value):
        if isinstance(value, str) and not value.startswith( ('+', '-') ):
            value = '+' + value
        return value
    
    '''*******************************************************
    * Enabled Methods
    *******************************************************'''            
    def AllowChangeCurrency(self, *args):
        return self.GetMethod('OpeningDealPackages')().Size() == 0

    def EnabledIfFlipped(self, *args):
        return self.IsFlipped()
    
    def EnabledIfNotFlipped(self, *args):
        return not self.IsFlipped()
        
    def IsFlipped(self):
        return self.TemplatePackage().GetAttribute('saveIsFlippedSide')
        
    '''*******************************************************
    * Object Mapping Methods
    *******************************************************'''     
    def TemplatePackage(self):
        return self.GetMethod(self._templatePackageName)()

 
    '''*******************************************************
    * Generate Strip
    *******************************************************'''             
    def DateAdjustmentOption(self, curr1, curr2):
        opt = acm.DealCapturing().CreateNewInstrument('FX Option')
        opt = acm.FBusinessLogicDecorator.WrapObject(opt)
        opt.ForeignCurrency(curr1)
        opt.DomesticCurrency(curr2)
        opt.FixingSource(None)
        return opt

    def StripDates(self, curr1, curr2, startDate, endDate, rolling, rollingBase, longStub):
        dates = acm.DealCapturing().GenerateStripOfOptionDates(startDate, endDate, rolling, rollingBase, "Mod. Following", acm.FArray(), longStub)
        opt = self.DateAdjustmentOption(curr1, curr2)
        newDates = acm.FArray()
        for date in dates:
            opt.FxoExpiryDate(date)
            if not opt.FxoExpiryDate() in newDates:
                newDates.Add(opt.FxoExpiryDate())
        return newDates
    
    def GenerateLeg(self, expiry):      
        newLeg = self.TemplatePackage().Copy()
        newLeg.SetAttribute('expiryDate', expiry)
        return newLeg
        
    def AddLegToParentPackage(self, newLeg):
        addChildDealPackage = self.GetMethod('AddChildDealPackage')
        addChildDealPackage(newLeg)
        
    def GenerateLegsFromExpiryDates(self, expiryDates):
        for expiry in expiryDates:
            newLeg = self.GenerateLeg(expiry)
            self.AddLegToParentPackage(newLeg)
        
    def GenerateChildDealPackages(self):
        foreign = self.TemplatePackage().GetAttribute('foreignInstrument')
        domestic = self.TemplatePackage().GetAttribute('domesticCurrency')
        expiryDates = self.StripDates(foreign, domestic, self.startDate, self.endDate, self.rolling, self.startDate, False)
        self.GenerateLegsFromExpiryDates(expiryDates)
        
    def OnApply(self, attrName, doGenerate = True):
        if doGenerate:
            self.GenerateChildDealPackages()
        self._subTypeChoices = DealPackageChoiceListSource()
        
    '''*******************************************************
    * Ux
    *******************************************************'''     
    def GetGenerateStripPanes(self, *args):
        return [{'Generate': self.GetGenerateStripLayout()}]
    
    def GetGenerateStripLayout(self):
        return self.UniqueLayout('''
                    vbox(;
                        instrumentPair;
                        premiumCurrency;
                        optionType;
                        baseType;
                        subtypeForeign;
                        subtypeDomestic;
                        startDate;
                        rolling;
                        endDate;
                        strikeForeignPerDomestic;
                        strikeDomesticPerForeign;
                        amountForeign;
                        amountDomestic;
                    );
                    ''')

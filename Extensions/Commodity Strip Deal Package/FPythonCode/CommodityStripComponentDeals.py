
import acm
import types
from CommodityStripUtils import LastDayOfMonth, GetBulletExpiryDate, UpdateTradeInstrument, GetStrip, TransformToDateInMonth, GetSettlementCalendar, ValidateDateInMonth
from CommodityStripInstrumentSearch import FindExistingInstrument
from DealPackageDevKit import ReturnDomainDecorator, Object, Action, DealPackageException, Bool, Delegate, CalcVal, Str, InstrumentPart
from DealDevKit import DealDefinition, Settings
from CommodityStripExtensionPoints import CustomDealAttributeOverrides, CustomDealAttributes, CustomDealBulletAttributes, CustomDealAsianAttributes, OnInstrumentsUpdated
from CompositeAttributesLib import BuySell


@Settings(GraphApplicable=False,
          SheetApplicable=False,  
          LogMode='Verbose')
class CommodityStripDealBase(DealDefinition):
    ONCHANGED_MODE = 2

    customDealAttributes =      CustomDealAttributes( tradeMethod = 'Trade',
                                                      instrumentMethod = 'Instrument')

    baseUnderlying =            Object( objMapping = InstrumentPart('BaseUnderlying'))

    quotation =                 Object( objMapping = InstrumentPart('Instrument.Quotation'),
                                        _queryMapping = ['Quotation.Name', 'RE_LIKE_NOCASE'])
    
    currency =                  Object( objMapping = InstrumentPart('Instrument.Currency'),
                                        _queryMapping = ['Currency.Name', 'RE_LIKE_NOCASE'])


    otc =                       Object( objMapping = InstrumentPart('Instrument.Otc'),
                                         _queryMapping = ['Otc', 'EQUAL'])

    payDayOffset =              Object( objMapping = InstrumentPart('Instrument.PayDayOffset'),
                                        _queryMapping = ['PayDayOffset', 'EQUAL'],
                                        visible = '@IsOtc',
                                        label = 'Settle Days')

    payOffsetMethod =           Object( objMapping = InstrumentPart('Instrument.PayOffsetMethod'),
                                        choiceListSource = ['Business Days', 'Calendar Days'],
                                        visible = '@IsOtc',
                                        _queryMapping = ['PayOffsetMethod', 'EQUAL'])
                                         
    theorPrice =                CalcVal( calcMapping = 'Trade:FDealSheet:Price Theor')    

    useCurrentFuture =          Bool(False)

    endDateIsCustom =           Bool(False)

    choiceListsDirty =          Bool( defaultValue=False,
                                      silent=True)

    # Trade attributes
    quantity =                  BuySell(label = 'Quantity',
                                        objMapping = 'Trade.Quantity',
                                        choiceListWidth=None)
                                        
                                        
    nominalInQuotation =        BuySell(label = 'Nominal In Quotation',
                                        objMapping = 'Trade.NominalInQuotation')
                                        
    price =                     Object( objMapping = 'Trade.Price',
                                        formatter='InstrumentDefinitionPrice',
                                        label = 'Price')
    uti =                       Object( label='UTI',
                                        objMapping = 'Trade.UniqueTradeIdentifier')

    # B2B parameters
    b2bEnabled =                Object( objMapping = 'B2BEnabled')

    b2bMargin =                 Object( label      = 'Margin',
                                        formatter  = 'InstrumentDefinitionPrice',
                                        visible    = '@IsB2B',
                                        objMapping = 'TradeB2B.SalesMargin')
                            
    b2bPrice =                  Object( label      = 'Trader Price',
                                        formatter  = 'InstrumentDefinitionPrice',
                                        visible    = '@IsB2B',
                                        objMapping = 'TradeB2B.TraderPrice')
                            
    b2bPrf =                    Object( objMapping = 'TradeB2B.TraderPortfolio',
                                        visible    = '@IsB2B')
             
    b2bAcq =                    Object( objMapping = 'TradeB2B.TraderAcquirer',
                                        visible    = '@IsB2B')

    # Attributes that have to be re-defined on child class level
    # These mappings will result in an exception
    underlying = Object(objMapping = InstrumentPart('UnderlyingDefault'))
    startDate = Object(objMapping = InstrumentPart('StartDateDefault'))
    endDate = Object(objMapping = InstrumentPart('EndDateDefault'))

   # Needed for the layout to make the web work correctly. Web does not support dynamic layouts in dialogs.
    customExpiry = Str(visible=False, enabled=False)

    def AttributeOverrides(self, overrideAccelerator):
        overrideAccelerator({'underlying': dict(onChanged='@FindOrCreateNeeded'),
                             'currency': dict(onChanged='@FindOrCreateNeeded'),
                             'startDate': dict(onChanged='@FindOrCreateNeeded'),
                             'endDate': dict(onChanged='@FindOrCreateNeeded'),
                             'quotation': dict(onChanged='@FindOrCreateNeeded'),
                             'otc': dict(onChanged='@FindOrCreateNeeded'),
                             'payDayOffset': dict(onChanged='@FindOrCreateNeeded'),
                             'payOffsetMethod': dict(onChanged='@FindOrCreateNeeded'),
                            })
        
        CustomDealAttributeOverrides(self, overrideAccelerator)

    def OnInit(self):
        self._baseUnderlying = None
        self._findOrCreateNeeded = False
        self._initialAttributeValues = {}
        self._disableTransform = False
        
    def SetInitialValues(self):
        def VerifyValue(attribute, value):
            domain = self.GetAttributeMetaData(attribute, 'domain')()
            attributeValue = self.GetAttribute(attribute)
            if domain.IsKindOf('FDateTimeDomain') or domain.IsKindOf('FDateDomain'):
                if acm.Time.DateDifference(value, attributeValue) == 0:
                    return True
                transform = self.GetAttributeMetaData(attribute, 'transform')
                if not transform.IsDefault() and acm.Time.DateDifference(transform(value), attributeValue) == 0:
                     return True
                return False
            if hasattr(attributeValue, 'Originator') and hasattr(value, 'Originator'):
                return value.Originator() == attributeValue.Originator()
            return value == attributeValue

        def SetValues():
            valueSet = False
            for attribute, value in self._initialAttributeValues.items():
                try:
                    if not VerifyValue(attribute, value):
                        self.SetAttribute(attribute, value)
                    valueSet = True
                except Exception as e:
                    self.Log().Verbose('Failed to set attribute %s in copy. %s' % (attribute, e))
            return valueSet
            
        for attr in self._initialAttributeValues.keys():
            if not attr in self.DealPackage().GetAttributes() or not self.ShouldCopy(self, attr):
                del self._initialAttributeValues[attr]

        if self._initialAttributeValues:
            for i in self._initialAttributeValues:
                if not SetValues():
                    break
            else:
                failedAttrs = sorted(attr for attr, value in self._initialAttributeValues.items() if not VerifyValue(attr, value))
                if failedAttrs:
                    pass # Uncomment if debugging
                    #self.Log().Error('FAILED TO COPY PACKAGE. Failed attribute(s): %s' % failedAttrs)
            self._initialAttributeValues.clear()
    
    def ShouldCopy(self, dp, attr):
        ignoreAttributeTypes = ('action', 'calcval')
        try:
            return dp.GetAttributeMetaData(attr, 'enabled')() and dp.GetAttributeMetaData(attr, 'editable')() and dp.GetAttributeMetaData(attr, 'type')() not in ignoreAttributeTypes and not dp.GetAttributeMetaData(attr, 'calcMapping')()
        except:
            return True    
    
    def OnNew(self):
        self._disableTransform = True
        self.SetInitialValues()
        self._disableTransform = False
        # Adding component to strip, underlying will be automatically set, but not base underlying
        if self.underlying and self.baseUnderlying is None:
            self.SetAttribute('baseUnderlying', self.underlying.UnderlyingOrSelf(), True)
        # Starting the application new, If there is a base Underlying defualt value, this should also be underlying default
        elif self.baseUnderlying and self.underlying is None:
            self.SetAttribute('underlying', self.baseUnderlying, True)
        
    def AssemblePackage(self, optArg=None):
        if optArg and hasattr(optArg, 'IsKindOf') and optArg.IsKindOf(acm.FDictionary):
            contents = optArg['contents']
            if contents and contents.IsKindOf(acm.FDealPackage):
                self._initialAttributeValues = dict((a, contents.GetAttribute(a)) for a in contents.GetAttributes() if self.ShouldCopy(contents, a))
                trade = contents.Trades().First()
                contents.Dismantle()
                UpdateTradeInstrument(trade, acm.DealCapturing().CreateNewInstrument(optArg['type']))
                optArg['contents'] = trade

        super(CommodityStripDealBase, self).AssemblePackage(optArg)

    def FindOrCreateNeeded(self, *args):
        self._findOrCreateNeeded = True
        self.choiceListsDirty = True
        
    def Refresh(self):
        if self._findOrCreateNeeded and not self._registeringAllObjMappingsOnNew:
            try:
                self.FindOrCreate()
            except Exception as e:
                self._findOrCreateNeeded = False
                raise Exception('FindOrCreate failed: (%s)' % str(e))
            self._findOrCreateNeeded = False
        return False
        
    def FindOrCreate(self):
        # Field and value is what has changed, the rest of the data should stay the same
        if not self.Trade().Instrument().IsInfant():
            #A stored instrument should never be modified
            newInstrument = self.Trade().Instrument().StorageNew()
            newInstrument.InitializeUniqueIdentifiers()
            UpdateTradeInstrument(self.Trade(), newInstrument)
        self.FindOrUseInstrument()
        OnInstrumentsUpdated(self.StripDealPackage(), self.DealPackage())
        
    def FindOrUseInstrument(self, *rest):
        if not self._initialAttributeValues:
            #Don't try to find the instrument while setting initial values
            existingInstrument = self.FindInstrument()
            if existingInstrument:
                UpdateTradeInstrument(self.Trade(), existingInstrument)
            else:
                ins = self.Instrument()
                if ins.IsCashFlowInstrument():
                    ins.Legs().First().GenerateCashFlowsFromDate(0)
        
    def FindInstrument(self):
        return FindExistingInstrument(self.DealPackage())

    # Methods that can be used to display attibute date in the UI grid
    def AttrEndDate(self):
        return self.endDate
    
    def AttrStartDate(self):
        return self.startDate
    
    def AttrUnderlying(self):
        return self.underlying

    # Object mappings
    @ReturnDomainDecorator('FInstrument')
    def BaseUnderlying(self, value = 'NoValue'):
        if value == 'NoValue':
            if self._baseUnderlying is None and self.underlying is not None:
                self._baseUnderlying = self.underlying.UnderlyingOrSelf()
            return self._baseUnderlying
        else:
            if type(value) == types.StringType:
                value = acm.FInstrument[value]
            self._baseUnderlying = value

    
    # Attribute mappings that have to be implemented each time

    @ReturnDomainDecorator('FInstrument')
    def UnderlyingDefault(self, value = 'NoValue'):
        raise DealPackageException('Attribute underlying not specified')
    
    @ReturnDomainDecorator('DateTime')
    def StartDateDefault(self, value = 'NoValue'):
        raise DealPackageException('Attribute startDate not specified')

    @ReturnDomainDecorator('DateTime')
    def EndDateDefault(self, value = 'NoValue'):
        raise DealPackageException('Attribute endDate not specified')
        
    def CustomPanes(self):
        return [{'General' : """quantity;
                                b2bPrice;
                                b2bMargin;
                                price;
                 """}]

    @ReturnDomainDecorator('FB2BSalesCoverConstellationParameters')
    def TradeB2B(self):
        return self.B2BTradeParamsAt('Trade')

    @ReturnDomainDecorator('bool')
    def B2BEnabled(self, value = 'NoValue'):
        if value == 'NoValue':
            return self.TradeB2B().SalesCoverEnabled()
        else:
            if not value and self.b2bEnabled:
                self.b2bMargin = 0
                self.price = self.b2bPrice
            self.TradeB2B().SalesCoverEnabled(value)
                 
    def StripDealPackage(self):
        return GetStrip(self)
        
    def IsB2B(self, attrName, *rest):
        return self.b2bEnabled

    def IsOtc(self, *args):
        return self.otc
        
    def Calendar(self):
        if self.underlying:
            return GetSettlementCalendar(self.underlying)
        else:
            return self.currency.Calendar() if self.currency else None

class CommodityStripDealAsian(CommodityStripDealBase):

    customDealAttributes = CustomDealAsianAttributes( tradeMethod = 'Trade',
                                                      instrumentMethod = 'Instrument')

    currency =                  Object( objMapping = InstrumentPart('Instrument.Currency|Instrument.Legs.Currency'),
                                        _queryMapping = ['Legs.Currency.Name', 'RE_LIKE_NOCASE'])

    underlying =        Object( objMapping = InstrumentPart('Instrument.FirstFloatLeg.FloatRateReference'),
                                _queryMapping = ['Legs.FloatRateReference.Name',
                                                 'RE_LIKE_NOCASE'])

    resetCalendar =     Object( objMapping = InstrumentPart('Instrument.FirstFloatLeg.ResetCalendar'),
                                _queryMapping = ['Legs.ResetCalendar.Name',
                                                 'RE_LIKE_NOCASE'])
    
    startDate =         Object( objMapping = InstrumentPart('Instrument.LegStartDate'),
                                transform = '@TransformStartDate',
                                _queryMapping = ['Legs.StartDate', 'EQUAL'])

    endDate =           Object( objMapping = InstrumentPart('Instrument.LegEndDate'),
                                transform = '@TransformEndDate',
                                _queryMapping = ['Legs.EndDate', 'EQUAL'])

    fixingSource =      Object( label='Source',
                                objMapping = InstrumentPart('Instrument.FirstFloatLeg.FloatRefFixingSource'),
                                _queryMapping = ['Legs.FloatRefFixingSource.Name', 'RE_LIKE_NOCASE'])

    fxSource =          Object( label='FX Source',
                                objMapping = InstrumentPart('Instrument.FixingSource'),
                                visible='@IsCurrencyDifferent',
                                _queryMapping = ['FixingSource.Name', 'RE_LIKE_NOCASE'])
                                
    convType =          Object( label='Conv Type',
                                visible='@IsCurrencyDifferent',
                                objMapping = InstrumentPart('Instrument.CrossCurrencyCalculation'))
                            
    convTypeForQuery =  Object( objMapping = InstrumentPart('Instrument.Legs.FloatRefFXScalingType'),
                                visible=False,
                                onChanged='@UpdateFxFixingRule',
                                _queryMapping = ['Legs.FloatRefFXScalingType', 'EQUAL'])
    
    fxFixRule =         Object( label = 'FX Fix Rule',
                                objMapping = InstrumentPart('Instrument.FirstFloatLeg.FloatRefFXFixingDateRule'),
                                visible='@IsAverageThenConvert',
                                _queryMapping = ['Legs.FloatRefFXFixingDateRule.Name', 'RE_LIKE_NOCASE'])
    
    payDayOffset =      Object( objMapping = InstrumentPart('Instrument.FirstFloatLeg.PayOffsetCount'),
                                visible = '@IsOtc',
                                _queryMapping =['Legs.PayOffsetCount', 'EQUAL'],
                                label = 'Pay Offset')
                                
    payDayMethod =      Object( objMapping = InstrumentPart('Instrument.FirstFloatLeg.PayDayMethod'),
                                visible = '@IsOtc',
                                _queryMapping =['Legs.PayDayMethod', 'EQUAL'],
                                onChanged='@FindOrCreateNeeded')
                                
    def AttributeOverrides(self, overrideAccelerator):
        overrideAccelerator({'payOffsetMethod':dict(visible=False, enabled=False, _queryMapping = None),
                             'fixingSource':dict(onChanged='@FindOrCreateNeeded'),
                             'fxSource':dict(onChanged='@FindOrCreateNeeded'),
                             'convType':dict(onChanged='@FindOrCreateNeeded'),
                             'fxFixRule':dict(onChanged='@FindOrCreateNeeded')})
        # Do not call CustomDealAttributeOverrides(self, overrideAccelerator)
                            
    def IsCurrencyDifferent(self, attributeName):
        return bool(self.underlying) and self.currency != self.underlying.Currency()

    def IsAverageThenConvert(self, attributeName):
        return self.IsCurrencyDifferent(attributeName) and self.convType == 'Average then convert' 

    def UpdateFxFixingRule(self, attributeName, *rest):
        if self.convTypeForQuery == 'After Aggregating':
            if self.fxFixRule is None:
                currPair = self.currency.CurrencyPair(self.underlying.Currency())
                if currPair:
                    default = currPair.FloatRefFXFixingDateRule()
                    if default:
                        self.fxFixRule = default
        else:
            self.fxFixRule = None

    def TransformStartDate(self, attribute, value):
        if isinstance(value, str):
            if value.startswith('!'):
                value = value[1:]
            else:
                value = acm.Time.FirstDayOfMonth(value)
        return value

    def TransformEndDate(self, attribute, value):
        if isinstance(value, str):
            if value.startswith('!'):
                value = value[1:]
            else:
                value = LastDayOfMonth(value)
        return value

class CommodityStripDealBullet(CommodityStripDealBase):

    customDealAttributes = CustomDealBulletAttributes( tradeMethod = 'Trade',
                                                       instrumentMethod = 'Instrument')

    underlying =        Object( objMapping = InstrumentPart('Instrument.Underlying'),
                                onChanged='@AdjustEndDate',
                                _queryMapping = ['Underlying.Name', 'RE_LIKE_NOCASE'])

    startDate =         Object( objMapping = InstrumentPart('StartDate'),
                                transform = '@TransformEndDate', #needed to get a valid datetime
                                enabled = False)

    endDate =           Object( objMapping = InstrumentPart('Instrument.ExpiryDate'),
                                transform = '@TransformEndDate',
                                _queryMapping = ['ExpiryDate', 'EQUAL'])
    
    customExpiry =      Object(objMapping = InstrumentPart('Instrument.ExpiryDate'),
                               label = 'Expiry',
                               validate='@ValidateCustomExpiry',
                               transform = '@TransformToCustomExpiry')

    @ReturnDomainDecorator('datetime')
    def StartDate(self, value = 'NoValue'):
        return acm.Time.FirstDayOfMonth(self.endDate)
        
    def AdjustEndDate(self, attribute, *rest):
        if not self.endDateIsCustom:
            self.endDate = self.TransformEndDate(attribute, self.endDate)
    
    def TransformEndDate(self, attribute, value):
        if isinstance(value, str) and value.startswith('!'):
            value = value[1:]
        if self.underlying:
            year, month, day = acm.Time.DateToYMD(value)
            return GetBulletExpiryDate(self.underlying, month, year, self.useCurrentFuture)
        else:
            return value
    
    def ValidateCustomExpiry(self, attrname, value, *rest):
        if not self._disableTransform:
            ValidateDateInMonth(value, self.Instrument().ExpiryDate(), self.Calendar())
    
    def TransformToCustomExpiry(self, name, input, *args):
        if not self._disableTransform:
            expiryDate = self.Instrument().ExpiryDate()
            return TransformToDateInMonth(input, expiryDate)
            
    def CustomPanes(self):
        customPanes = super( CommodityStripDealBullet, self).CustomPanes()
        customPanes[0]['General'] += 'vbox[Optional;customExpiry;];'
        return customPanes
        

class CommodityStripDealBulletOption(CommodityStripDealBullet):
    strikePrice =               Object(     objMapping = InstrumentPart('Instrument.StrikePrice'),
                                            label = 'Strike',
                                            onChanged='@FindOrCreateNeeded',
                                            _queryMapping = ['StrikePrice', 'EQUAL'])
    
    optionType =                Object(     objMapping = InstrumentPart('Instrument.OptionType'),
                                            label = 'C/P',
                                            onChanged='@FindOrCreateNeeded',
                                            choiceListSource = ['Call', 'Put'])

    optionTypeForQuery =        Object(     objMapping = InstrumentPart('Instrument.IsCallOption'),
                                            visible = False,
                                            _queryMapping = ['IsCallOption', 'EQUAL'])

    settlementType =            Object(     objMapping = InstrumentPart('Instrument.SettlementType'),
                                            onChanged='@FindOrCreateNeeded')

    # The decorator uses enum(settlementTypeShortName) but the query needs enum(settlementType)
    settlementTypeForQuary =    Object(     objMapping = InstrumentPart('Instrument.Instrument.SettlementType'),
                                            _queryMapping = ['SettlementType', 'EQUAL'])

    payType =                   Object(     objMapping = InstrumentPart('Instrument.PayType'),
                                            visible='@IsOtc',
                                            onChanged='@FindOrCreateNeeded',
                                            label = '',
                                            _queryMapping = ['PayType', 'EQUAL'])

    exerciseType =              Object(     objMapping = InstrumentPart('Instrument.ExerciseType'),
                                            choiceListSource = ['American', 'European'],
                                            onChanged='@FindOrCreateNeeded',
                                            label = 'Exercise',
                                            _queryMapping = ['ExerciseType', 'EQUAL'])

    spotDaysOffset =            Object(     objMapping = InstrumentPart('Instrument.SpotBankingDaysOffset'),
                                            visible='@IsOtc',
                                            onChanged='@FindOrCreateNeeded',
                                            label = 'Spot Days',
                                            _queryMapping = ['SpotBankingDaysOffset', 'EQUAL'])

    def OnNew(self):
        super(CommodityStripDealBulletOption, self).OnNew()
        # When adding more options to each period there is no attribute onChanged triggering
        # FindOrCreateNeeded.
        self.FindOrCreateNeeded()

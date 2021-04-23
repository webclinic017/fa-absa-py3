
import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object, Action, InstrumentPart, ReturnDomainDecorator, Date, DealPackageUserException, Float
from SP_DealPackageHelper import GetCurrencyPairPointsDomesticPerForeign, GetCurrencyPairPointsForeignPerDomestic, StringValueIsInteger
from SP_BusinessCalculations import GenerateFXPeriodDates, AdjustBankingDaysFromMultiCalendars, BankingDayPeriodToDateFromStartDate
from SP_TrfUtils import TrfExpiryEvent, TrfExpiryEventPerPayDate, FixFxRateCalculation, GetInverseRate, CalculateAverageFixing, MtMPriceFromFixingSource
from sys import float_info

class TrfFxRateComposite(CompositeAttributeDefinition):

    def Attributes(self):
        
        return {

                'rateDomesticPerForeign' :    Object( objMapping = InstrumentPart(self.UniqueCallback('ObjectMappingDomesticPerForeign')),
                                                      formatter = self.UniqueCallback('@FormatFXDomesticPerForeign')),
                
                'rateForeignPerDomestic' :    Object( objMapping = InstrumentPart(self.UniqueCallback('ObjectMappingForeignPerDomestic')),
                                                      formatter = self.UniqueCallback('@FormatFXForeignPerDomestic')),
                
                'storeDomesticPerForeign' :   Action( action = self.UniqueCallback('@SetStorageDomesticPerForeign')),

                'storeForeignPerDomestic' :   Action( action = self.UniqueCallback('@SetStorageForeignPerDomestic')),
                
                'reEvaluateObjectMappings' :  Action( action = self.UniqueCallback('@ReEvaluateObjectMappings'))
                }
                          
    def OnInit(self, rateDomPerFor, rateForPerDom, foreignCurrency = 'foreignCurrency', domesticCurrency = 'domesticCurrency'):
        self._rateDomPerFor = rateDomPerFor
        self._rateForPerDom = rateForPerDom
        self._formatterFxDomesticPerForeign = None
        self._formatterFxForeignPerDomestic = None
        self._foreignCurrency = foreignCurrency
        self._domesticCurrency = domesticCurrency

    def ReadMapping(self, mapping):
        parts = mapping.split('.')
        value = self.GetMethod(parts[0])()
        for part in range(1, len(parts)):
            value = getattr(value, parts[part])()
        return value
    
    def WriteMapping(self, mapping, value):
        parts = mapping.split('.')
        writeMethod = self.GetMethod(parts[0])
        for part in range(1, len(parts)):
            writeMethod = getattr(writeMethod(), parts[part])
        writeMethod(value)

    def ObjectMappingRates(self, mapping, value = 'NoValue'):
        if value == 'NoValue':
            return self.ReadMapping(mapping)
        else:
            self.WriteMapping(mapping, value)
            self.GetAttribute('reEvaluateObjectMappings')()

    @ReturnDomainDecorator('double')
    def ObjectMappingDomesticPerForeign(self, value = 'NoValue'):
        return self.ObjectMappingRates(self._rateDomPerFor, value)

    @ReturnDomainDecorator('double')
    def ObjectMappingForeignPerDomestic(self, value = 'NoValue'):
        return self.ObjectMappingRates(self._rateForPerDom, value)

    # Action to trigger re-draw of UI
    def ReEvaluateObjectMappings(self, *rest):
        pass

    def SetStorageDomesticPerForeign(self, attrName, *rest):
        silent = rest[0] if len(rest) > 0 else False
        self.SetStorageDirection('rateDomesticPerForeign', silent)
    
    def SetStorageForeignPerDomestic(self, attrName, *rest):
        silent = rest[0] if len(rest) > 0 else False
        self.SetStorageDirection('rateForeignPerDomestic', silent)
    
    def SetStorageDirection(self, attrName, silent):
        storageAttr = attrName.replace('store', 'rate')
        currentValue = self.GetAttribute(storageAttr)
        self.SetAttribute(storageAttr, currentValue + 0.00000001, silent)
        self.SetAttribute(storageAttr, currentValue, silent)

    def FormatFXDomesticPerForeign(self, traitName):
        if not self._formatterFxDomesticPerForeign:
            self._formatterFxDomesticPerForeign = acm.Get('formats/SP_TrfFXRate').Clone()
        numDecimals = GetCurrencyPairPointsDomesticPerForeign(self.Owner().GetAttribute(self._foreignCurrency), self.Owner().GetAttribute(self._domesticCurrency))
        self._formatterFxDomesticPerForeign.NumDecimals(numDecimals)
        return self._formatterFxDomesticPerForeign
    
    def FormatFXForeignPerDomestic(self, traitName):
        if not self._formatterFxForeignPerDomestic:
            self._formatterFxForeignPerDomestic = acm.Get('formats/SP_TrfFXRate').Clone()
        numDecimals = GetCurrencyPairPointsForeignPerDomestic(self.Owner().GetAttribute(self._foreignCurrency), self.Owner().GetAttribute(self._domesticCurrency))
        self._formatterFxForeignPerDomestic.NumDecimals(numDecimals)
        return self._formatterFxForeignPerDomestic

class TrfFxStrikeComposite(TrfFxRateComposite):

    def Attributes(self):
        attributes = super(TrfFxStrikeComposite, self).Attributes()

        attributes['strikeSettlement'] =    Object ( objMapping = InstrumentPart(self._strikeSettlement),
                                                     choiceListSource = acm.FChoiceList.Select("list = 'sp_StrikeSettlement'"),
                                                     toolTip = "Notional amount to use for physical settlement when fixing equals strike")

        return attributes

    def OnInit(self, rateDomPerFor, rateForPerDom, strikeSettlement, foreignCurrency = 'foreignCurrency', domesticCurrency = 'domesticCurrency'):
        super(TrfFxStrikeComposite, self).OnInit(rateDomPerFor, rateForPerDom, foreignCurrency, domesticCurrency)
        self._strikeSettlement = strikeSettlement

class TrfCommodityStrikeComposite(CompositeAttributeDefinition):

    def Attributes(self):
        return {
                'strikePrice' :         Object ( objMapping = InstrumentPart(self._strikePrice),
                                                 validate = self.UniqueCallback('@ValidateStrikePrice')),
                
                'strikeSettlement' :    Object ( objMapping = InstrumentPart(self._strikeSettlement),
                                                 choiceListSource = acm.FChoiceList.Select("list = 'sp_StrikeSettlement'"),
                                                 toolTip = "Notional amount to use for physical settlement when fixing equals strike")
                }
    
    def OnInit(self, strikePrice, strikeSettlement):
        self._strikePrice = strikePrice
        self._strikeSettlement = strikeSettlement
        
    def ValidateStrikePrice(self, traitName, newStrike):
        if newStrike and newStrike < float_info.epsilon:
            Md = self.GetMethod('GetAttributeMetaData')
            label = Md(traitName, 'label')()
            str = 'Expected positive %s' % label
            raise DealPackageUserException(str)    

class TrfFxBarrierComposite(TrfFxRateComposite):

    def Attributes(self):
        attributes = super(TrfFxBarrierComposite, self).Attributes()

        attributes['memory'] =              Object ( objMapping = InstrumentPart(self._memory),
                                                     label = "Memory",
                                                     toolTip = "Once the barrier is breached it will be considered breached for all remaining fixing dates")

        attributes['levelInterpretation'] = Object ( objMapping = InstrumentPart(self._levelInterpretation),
                                                     choiceListSource = acm.FChoiceList.Select("list = 'sp_BarrierCondition'"),
                                                     toolTip = 'Specify when the barrier should be considered crossed' )

        return attributes

    def OnInit(self, rateDomPerFor, rateForPerDom, memory, levelInterpretation, foreignCurrency = 'foreignCurrency', domesticCurrency = 'domesticCurrency'):
        super(TrfFxBarrierComposite, self).OnInit(rateDomPerFor, rateForPerDom, foreignCurrency, domesticCurrency)
        self._memory = memory
        self._levelInterpretation = levelInterpretation

class TrfCommodityBarrierComposite(CompositeAttributeDefinition):

    def Attributes(self):
        return {
                'barrierLevel' :         Object ( objMapping = InstrumentPart(self._barrierLevel)),
                
                'memory' :               Object ( objMapping = InstrumentPart(self._memory),
                                                     label = "Memory",
                                                     toolTip = "Once the barrier is breached it will be considered breached for all remaining fixing dates"),

                'levelInterpretation' :  Object ( objMapping = InstrumentPart(self._levelInterpretation),
                                                     choiceListSource = acm.FChoiceList.Select("list = 'sp_BarrierCondition'"),
                                                     toolTip = 'Specify when the barrier should be considered crossed' )
                }

    def OnInit(self, barrierLevel, memory, levelInterpretation):
        self._barrierLevel = barrierLevel
        self._memory = memory
        self._levelInterpretation = levelInterpretation

class TrfFxPivotRateComposite(TrfFxRateComposite):

    def Attributes(self):
        attributes = super(TrfFxPivotRateComposite, self).Attributes()

        attributes['pivotRateStrike'] =     Object ( objMapping = InstrumentPart(self._pivotRateStrike),
                                                     choiceListSource = acm.FChoiceList.Select("list = 'sp_PivotRateStrike'"),
                                                     toolTip = 'Specify which strike to use when fixing equals the pivot rate')

        return attributes

    def OnInit(self, rateDomPerFor, rateForPerDom, pivotRateStrike, foreignCurrency = 'foreignCurrency', domesticCurrency = 'domesticCurrency'):
        super(TrfFxPivotRateComposite, self).OnInit(rateDomPerFor, rateForPerDom, foreignCurrency, domesticCurrency)
        self._pivotRateStrike = pivotRateStrike

class TrfCommodityPivotRateComposite(CompositeAttributeDefinition):

    def Attributes(self):
        return {
                'pivotRate' :       Object ( objMapping = InstrumentPart(self._pivotRate)),
                
                'pivotRateStrike' : Object ( objMapping = InstrumentPart(self._pivotRateStrike),
                                             choiceListSource = acm.FChoiceList.Select("list = 'sp_PivotRateStrike'"),
                                             toolTip = 'Specify which strike to use when fixing equals the pivot rate')
                }

    def OnInit(self, pivotRate, pivotRateStrike):
        self._pivotRate = pivotRate
        self._pivotRateStrike = pivotRateStrike


class TrfFixingEditerComposite(CompositeAttributeDefinition):

    #-----------------------------
    # Interface Overrides
    #-----------------------------
    def Attributes(self):
        attr = {
            # vvv Fields vvv
            'fixingDate' : Date(
                label = 'Fixing Date',
                enabled = self.UniqueCallback('@EnabledFixingDate'),
                validate = self.UniqueCallback('@ValidateFixingDate'),
                transform = self.UniqueCallback('@TransformFixingDate')),
            'payDate' : Date(
                label = 'Pay Date',
                visible = self.UniqueCallback('@VisiblePayDate'),
                validate = self.UniqueCallback('@ValidatePayDate'),
                transform = self.UniqueCallback('@TransformPayDate')),
            'fixingValue' : self.FixingValueAttr(),
            # vvv Buttons vvv
            'fixingAdd' : Action(
                label = 'Add',
                visible = self.UniqueCallback('@VisibleFixingAdd'),
                enabled = self.UniqueCallback('@EnabledFixingAdd'),
                action = self.UniqueCallback('@ActionFixingAdd')),
            'fixingUpdate' : Action(
                label = 'Update',
                enabled = self.UniqueCallback('@EnabledFixingUpdate'),
                action = self.UniqueCallback('@ActionFixingUpdate')),
            'fixingRemove' : Action(
                label = 'Delete',
                visible = self.UniqueCallback('@VisibleFixingRemove'),
                enabled = self.UniqueCallback('@EnabledFixingRemove'),
                action = self.UniqueCallback('@ActionFixingRemove')),
            'fixingFixRate' : Action(
                label = 'Suggest Fixing',
                enabled = self.UniqueCallback('@EnabledFixRate'),
                action = self.UniqueCallback('@ActionFixRate'))
        }
        return attr

    def OnInit(self, instrument):
        self._instrument = instrument
        self._fixingValue = 0.0
        self._fixingEventSelected = None

    def GetLayout(self):
        raise NotImplementedError('GetLayout not implemented')
        
    #-----------------------------
    # Protected Access Methods
    #-----------------------------
    def Instrument(self):
        return self.GetMethod(self._instrument)()

    def GetPairCalendars(self):
        calendars = []
        fcur = self.Instrument().ForeignCurrency()
        dcur = self.Instrument().DomesticCurrency()
        if fcur:
            calendars.append(fcur.Calendar())
        if dcur:
            calendars.append(dcur.Calendar())
        return calendars
        
    def FixingValueAttr(self):
        attr = Object(
            objMapping = self.UniqueCallback('FixingValue'))
        return attr
            
    def GetFixingEventSelected(self, value = 'NoValue'):
        if value == 'NoValue':
            return self._fixingEventSelected
        else:
            self._fixingEventSelected = value
    
    @ReturnDomainDecorator('double')      
    def FixingValue(self, value = 'NoValue'):
        if value == 'NoValue':
            return self._fixingValue
        else:
            self._fixingValue = value
        
    #-----------------------------
    #  Public Access Callbacks
    #-----------------------------
    def OnSelectionChanged(self, rowObj):
        if rowObj:
            self._fixingEventSelected = rowObj
            self._fixingValue = rowObj.EventValue()
            self.fixingDate = rowObj.Date()
            self.payDate = rowObj.EndDate() 
        else:
            self.ResetState()
            
    def ResetState(self):
        self._fixingEventSelected = None
        self._fixingValue = 0.0
        self.fixingDate = None
        self.payDate = None
        
    #-----------------------------
    # Visible Callbacks
    #-----------------------------  
    def VisiblePayDate(self, traitName):
        return True

    def VisibleFixingAdd(self, traitName):
        return True
    
    def VisibleFixingRemove(self, traitName):
        return True
        
    #-----------------------------
    # Enabled Callbacks
    #-----------------------------
    def EnabledFixingDate(self, traitName):
        return True
        
    def EnabledFixingAdd(self, traitName):
        enable = False
        tee = TrfExpiryEvent(self.Instrument(), self.fixingDate)
        teeppd = TrfExpiryEventPerPayDate(self.Instrument(), self.payDate)
        if (self.fixingDate and self.payDate and not (tee or teeppd)):
            enable = True
        return enable
        
    def EnabledFixingUpdate(self, traitName):
        enable = False
        row = self._fixingEventSelected 
        if row:
            edited = (row.Date() != self.fixingDate 
                or row.EndDate() != self.payDate 
                or row.EventValue() != self._fixingValue)
            if edited:
                enable = True
        return enable

    def EnabledFixingRemove(self, traitName):
        enable = (self._fixingEventSelected != None)
        return enable
        
    def EnabledFixRate(self, traitName):
        enable = False
        row = self._fixingEventSelected
        if row:
            rd = row.Date()
            today = acm.Time.DateToday()
            if acm.Time.DateDifference(rd, today) <= 0:
                enable = True
        return enable

    #-----------------------------
    # Validate Callbacks
    #-----------------------------
    def ValidateFixingDate(self, traitName, newDate):
        row = self._fixingEventSelected
        if row and not newDate:
            Md = self.GetMethod('GetAttributeMetaData')
            label = Md(traitName, 'label')()
            str = 'Expected a %s' % label
            raise DealPackageUserException(str)    
        
    def ValidatePayDate(self, traitName, newDate):
        row = self._fixingEventSelected
        if row and not newDate:
            Md = self.GetMethod('GetAttributeMetaData')
            label = Md(traitName, 'label')()
            str = 'Expected a %s' % label
            raise DealPackageUserException(str) 
        
    #-----------------------------
    # Action Callbacks
    #-----------------------------
    def ActionFixingAdd(self, traitName):
        raise NotImplementedError('ActionFixingAdd not implemented')
                
    def ActionFixingUpdate(self, traitName):
        row = self._fixingEventSelected
        if row:
            fvExist = (self._fixingValue and self._fixingValue > 0.0) 
            ev = self._fixingValue if fvExist else -1.0
            row.EventValue(ev)
            row.Date(self.fixingDate)
            row.EndDate(self.payDate)
            
    def ActionFixingRemove(self, traitName):
        row = self._fixingEventSelected
        if row:
            row.Unsimulate()
            
    def ActionFixRate(self, traitName):
        raise NotImplementedError('ActionFixRate not implemented')

    #-----------------------------
    # Transform Callbacks
    #-----------------------------
    def TransformFixingDate(self, attrName, newDate, *rest):
        date = newDate
        oldValue = self.fixingDate
        if date:
            if acm.Time.PeriodSymbolToDate(date):
                dateNow = acm.Time().DateNow()
                nonAdjustedDate = acm.Time.DateAdjustPeriod(dateNow, newDate)
                date = AdjustBankingDaysFromMultiCalendars(
                    nonAdjustedDate, 0, self.GetPairCalendars())
        return date
     
    def TransformPayDate(self, attrName, newDate, *rest):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            if acm.Time.IsValidDateTime(self.fixingDate):
                date = BankingDayPeriodToDateFromStartDate(
                    self.GetPairCalendars(), 
                    self.fixingDate, 
                    newDate, 
                    self.Instrument().SettlementCalendar())
            else:
                raise DealPackageUserException(
                    'Cannot enter pay date as a period '
                    'without a valid fixing date')
        return date

class TrfFxFixingEditerComposite(TrfFixingEditerComposite):

    class FxFixingValue(TrfFxRateComposite):
        @ReturnDomainDecorator('double')
        def ObjectMappingDomesticPerForeign(self, value = 'NoValue'):
            return self.GetMethod(self._rateDomPerFor)(value)

        @ReturnDomainDecorator('double')
        def ObjectMappingForeignPerDomestic(self, value = 'NoValue'):
            return self.GetMethod(self._rateForPerDom)(value)
    
    #-----------------------------
    # Interface Overrides
    #-----------------------------
    def GetLayout(self):
        str = ( 
        '''
            vbox[Fixing;
                hbox(;
                    fixingDate;
                    payDate;
                );
                hbox(;   
                    fixingValue_rateDomesticPerForeign;
                    fixingValue_rateForeignPerDomestic;
                );
                hbox(;
                    fixingAdd;
                    fixingUpdate;
                    fixingRemove;
                    fixingFixRate;
                );
            ];
        ''')
        layout = self.UniqueLayout(str)
        return layout
        
    #-----------------------------
    # Protected Access Methods
    #-----------------------------    
    def FixingValueAttr(self):
        attr = self.FxFixingValue( 
                rateDomPerFor = self.UniqueCallback('FixingValue'),
                rateForPerDom = self.UniqueCallback('FixingValueInvRate'))
        return attr
        
    @ReturnDomainDecorator('double')
    def FixingValueInvRate(self, value = 'NoValue'):
        if value == 'NoValue':
            return GetInverseRate(self.FixingValue())
        else:
            self.FixingValue(GetInverseRate(value))
    
    #-----------------------------
    # Action Callbacks
    #-----------------------------
    def ActionFixingAdd(self, traitName):
        tee = TrfExpiryEvent(self.Instrument(), self.fixingDate)
        teeppd = TrfExpiryEventPerPayDate(self.Instrument(), self.payDate)
        if (self.fixingDate and self.payDate and not (tee or teeppd)):
            AddEe = self.GetMethod('AddExoticEvent')
            AddEe('TRF Expiry', self.fixingDate, 
                self.payDate, self._fixingValue, -1,
                self.Owner().GetExoticEventReference())
        
    def ActionFixRate(self, traitName):
        row = self._fixingEventSelected 
        if row and row.Date() <= acm.Time.DateToday():
            try:
                fxRate = FixFxRateCalculation(self.Instrument(), row)
                self.fixingValue_rateDomesticPerForeign = fxRate
            except RuntimeError as e:
                raise DealPackageUserException(str(e))

class TrfCommodityFixingEditerComposite(TrfFixingEditerComposite):

    #-----------------------------
    # Interface Overrides
    #-----------------------------
    def GetLayout(self):
        str = ( 
        '''
            vbox[Fixing;
                hbox(;
                    fixingDate;
                    payDate;
                );
                hbox(;   
                    fixingValue;
                );
                hbox(;
                    fixingAdd;
                    fixingUpdate;
                    fixingRemove;
                    fixingFixRate;
                );
            ];
        ''')
        layout = self.UniqueLayout(str)
        return layout
            
    #-----------------------------
    # Action Callbacks
    #-----------------------------
    def ActionFixingAdd(self, traitName):
        str = 'Not allowed to add fixing'
        raise DealPackageUserException(str)
    
    def ActionFixingRemove(self, traitName):
        str = 'Not allowed to remove fixing'
        raise DealPackageUserException(str)
        
    def ActionFixRate(self, traitName):
        ape = self.Owner().AveragePriceEvents()
        rs = self.Instrument().RoundingSpecification()
        self.fixingValue = CalculateAverageFixing(ape, rs)
        
    #-----------------------------
    # Enabled Callbacks
    #-----------------------------    
    def EnabledFixingDate(self, traitName):
        return False

    #-----------------------------
    # Visible Callbacks
    #-----------------------------  
    def VisibleFixingAdd(self, traitName):
        return False
        
    def VisibleFixingRemove(self, traitName):
        return False
      
  
class TrfDailyFixingEditerComposite(TrfFixingEditerComposite):

    #-----------------------------
    # Interface Overrides
    #-----------------------------
    def GetLayout(self):
        str = ( 
        '''
            vbox[Fixing;
                hbox(;
                    fixingDate;
                    payDate;
                );
                hbox(;   
                    fixingValue;
                );
                hbox(;
                    fixingAdd;
                    fixingUpdate;
                    fixingRemove;
                    fixingFixRate;
                );
            ];
        ''')
        layout = self.UniqueLayout(str)
        return layout
        
    #-----------------------------
    # Enabled Callbacks
    #-----------------------------
    def EnabledFixingAdd(self, traitName):
        enable = False
        Ymd = acm.Time.DateToYMD
        ape = self.Owner().AveragePriceEvents()
        selected = self.Owner().fixingEditer.GetFixingEventSelected()
        if self.fixingDate:
            c1 = self.fixingDate not in [e.Date() for e in ape]
            c2 = (Ymd(self.fixingDate)[0] == Ymd(selected.Date())[0]
                and Ymd(self.fixingDate)[1] == Ymd(selected.Date())[1])
            c3 = self.fixingValue > 0.0 or self.fixingValue == -1.0
            if c1 and c2 and c3:
                enable = True
        return enable
        
    def EnabledFixingUpdate(self, traitName):
        enable = False
        row = self._fixingEventSelected
        fd = self.fixingDate
        fv = self.fixingValue
        if row and fd and fv:
            Ymd = acm.Time.DateToYMD
            selected = self.Owner().fixingEditer.GetFixingEventSelected()
            ape = self.Owner().AveragePriceEvents()
            changedFd = (fd != row.Date())
            changedFv = (fv != row.EventValue())
            c2 = (Ymd(self.fixingDate)[0] == Ymd(selected.Date())[0]
                and Ymd(self.fixingDate)[1] == Ymd(selected.Date())[1])
            c3 = fd not in [e.Date() for e in ape]
            c4 = (fv > 0.0 or fv == -1.0)
            if changedFd and c2 and c3 and c4:
                enable = True
            if changedFv and not changedFd and c4:
                enable = True
        return enable
    
    #-----------------------------
    # Validate Callbacks
    #-----------------------------
    def ValidateFixingDate(self, traitName, newDate):
        if acm.Time.IsValidDateTime(newDate):   
            Ymd = acm.Time.DateToYMD
            selected = self.Owner().fixingEditer.GetFixingEventSelected()
            ape = self.Owner().AveragePriceEvents()
            c1 = (Ymd(newDate)[0] == Ymd(selected.Date())[0]
                and Ymd(newDate)[1] == Ymd(selected.Date())[1])
            if not c1:
                raise DealPackageUserException(
                    'Observation Date is not within fixing period.')
                    
    def ValidatePayDate(self, traitName, newDate):
        # Do not validate Pay Date, since Pay Date is hidden and 
        # empty (otherwise invalid state in overridden implementation)
        pass
    
    #-----------------------------
    # Action Callbacks
    #-----------------------------
    def ActionFixingAdd(self, traitName):
        valid = False
        if self.fixingDate and self.fixingValue:
            Ymd = acm.Time.DateToYMD
            ape = self.Owner().AveragePriceEvents()
            selected = self.Owner().fixingEditer.GetFixingEventSelected()
            valid = True
            valid = valid and self.fixingDate not in [e.Date() for e in ape]
            valid = valid and Ymd(self.fixingDate)[1] == Ymd(selected.Date())[1]
            valid = valid and (self.fixingValue > 0.0 or self.fixingValue == -1.0)
        if valid:
            AddEe = self.GetMethod('AddExoticEvent')
            AddEe('Average Price', self.fixingDate, None, 
                self.fixingValue, -1, self.Owner().GetExoticEventReference())
        else:
            raise DealPackageUserException('Invalid Fixing')
    
    def ActionFixingUpdate(self, traitName):
        row = self._fixingEventSelected
        if row:
            fvExist = (self.fixingValue and self.fixingValue > 0.0) 
            ev = self.fixingValue if fvExist else -1.0
            row.EventValue(ev)
            row.Date(self.fixingDate)
    
    def ActionFixRate(self, traitName):
        row = self._fixingEventSelected 
        if row and row.Date() <= acm.Time.DateToday():
            price = None
            und = self.Instrument().Underlying()
            fixingSourceMsg = ''
            if row.Instrument().FixingSource():
                fixingSourceMsg = '(fixing source = %s) ' % row.Instrument().FixingSource().Name()
                mtmPrice, handled = MtMPriceFromFixingSource(row)
                if mtmPrice:
                    price = mtmPrice
            else:
                price = und.MtMPrice(row.Date(), und.Currency())
            if price:
                self.FixingValue(price)
            else:
                str = 'No MtM price %savailable for %s' %(fixingSourceMsg, und.Name())
                raise DealPackageUserException(str)

    #-----------------------------
    # Protected Access Methods
    #-----------------------------
    def FixingValueAttr(self):
        attr = Object(
            objMapping = self.UniqueCallback('FixingValue'),
            formatter = 'SP_TrfObservationValue')
        return attr
        
    #-----------------------------
    # Visible Callbacks
    #-----------------------------  
    def VisiblePayDate(self, traitName):
        return False

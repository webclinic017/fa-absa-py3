import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, CalcVal, ParseSuffixedFloat, ReturnDomainDecorator
from CompositeAttributes import SelectInstrumentField, BuySell
from ChoicesExprInstrument import getNominalScalingChoices, getResetTypes, getPassingTypeChoices, getPriceInterpretationTypes, GetReferenceInstrumentTypes, getAverageForwardRefInsChoices, getInterestPaymentTimeTypes
from CompositeResetDefinition import ResetDefinition

EXCLUDED_LEG_TYPES = ['Target Redemption', 'Range Accrual', 'Snowball', 'Fixed Accretive', 'Zero Coupon Fixed']

class LegDefinition(CompositeAttributeDefinition):
    def OnInit(self, leg, trade, showBuySell=True, **kwargs):
        self._leg = leg
        self._trade = trade
        self._showBuySell = showBuySell
        self._refInsChoices = DealPackageChoiceListSource()
        self._floatRateReferenceChoices = DealPackageChoiceListSource()
        
    def Attributes(self):
        return { 'averageOptionPeriod'  : Object( label='Fixing Freq',
                                                  objMapping=self._leg+'.AverageOptionPeriod'),
                 'calcType'             : Object( label='Calc Type',
                                                  objMapping=self._leg+'.CalcType',
                                                  choiceListSource=acm.GetDomain("FChoiceList('CalculationType')").Instances(),
                                                  visible=self.UniqueCallback('@CalcTypeVisible')),
            'calculationPeriodDateRule' : Object( label='Roll Offset',
                                                  objMapping=self._leg+'.CalculationPeriodDateRule',
                                                  visible=self.UniqueCallback('@CalcPeriodDateRuleVisible')),
                 'currency'             : Object( label='Currency',
                                                  objMapping=self._leg+'.Currency',
                                                  visible=self.UniqueCallback('@CurrencyVisible')),
                 'selectCreditRef'      : SelectInstrumentField( label='Credit Ref',
                                                  objMapping=self._leg+'.CreditRef',
                                                  visible=self.UniqueCallback('@CreditRefVisible')),
                 'dayCountMethod'       : Object( label='Day Count',
                                                  objMapping=self._leg+'.DayCountMethod'),
                 'deliverableCurrency'  : Object( label='Settle Curr',
                                                  objMapping=self._leg+'.DeliverableCurrency',
                                                  visible=self.UniqueCallback('@DeliverableCurrencyVisible')),
                 'fixedCoupon'          : Object( label='Fixed Period',
                                                  objMapping=self._leg+'.FixedCoupon',
                                                  visible=self.UniqueCallback('@FixedCouponVisible')),
                 'fixedRate'            : Object( label='Rate',
                                                  objMapping=self._leg+'.FixedRate',
                                                  visible=self.UniqueCallback('@FixedRateVisible'),
                                                  formatter='InstrumentDefinitionFixedRate',
                                                  solverParameter={'minValue':-1.0, 'maxValue':100.0},
                                                  transform=self.UniqueCallback('@TransformSolver'),
                                                  backgroundColor='@SolverColor'),
                 'floatRateFactor'      : Object( label='Float Fctr',
                                                  objMapping=self._leg+'.FloatRateFactor',
                                                  formatter='FullPrecision',
                                                  visible=self.UniqueCallback('@FloatRateFactorVisible')),
                 'floatRateFactor2'     : Object( defaultValue=1, 
                                                  label='Float Fctr 2',
                                                  objMapping=self._leg+'.FloatRateFactor2',
                                                  formatter='FullPrecision',
                                                  visible=self.UniqueCallback('@FloatRateFactor2Visible')),                                                  
                 'floatRateReference'   : Object( label='Float Ref',
                                                  objMapping=self._leg+'.FloatRateReference',
                                                  choiceListSource=self.UniqueCallback('@FloatRateReferenceChoices'),
                                                  visible=self.UniqueCallback('@FloatRateReferenceVisible'),
                                                  width=19),
                 'selectFloatRateRef'   : SelectInstrumentField(label='Float Ref',
                                                  objMapping=self._leg+'.FloatRateReference',
                                                  visible=self.UniqueCallback('@FloatRateReferenceVisible'),
                                                  width=19),
                 'floatRateReference2'  : Object( label='Float Ref 2',
                                                  objMapping=self._leg+'.FloatRateReference2',
                                                  choiceListSource=self.UniqueCallback('@FloatRateReferenceChoices'),
                                                  visible=self.UniqueCallback('@FloatRateReference2Visible'),
                                                  width=19),
                 'floatRefFXFixingDateRule':Object( label='FX Fix Rule',
                                                  objMapping=self._leg+'.FloatRefFXFixingDateRule'),                                                  
                 'includeTaxFactor'     : Object( label='Tax Handling',
                                                  objMapping=self._leg+'.IncludeTaxFactor',
                                                  visible=self.UniqueCallback('@PassingDetailsVisible')),
                 'indexRef'             : Object( label='Index Ref',
                                                  objMapping=self._leg+'.IndexRef',
                                                  visible=self.UniqueCallback('@IndexRefVisible')),
                 'interestPaymentTime'  : Object( label='Payment',
                                                  objMapping=self._leg+'.InterestPaymentTime',
                                                  choiceListSource=self.UniqueCallback('@InterestPaymentTimeChoices'),
                                                  visible=self.UniqueCallback('@InterestPaymentTimeVisible'),
                                                  enabled=self.UniqueCallback('@InterestPaymentTimeEnabled')),                                                  
                 'selectIndexRef'       : SelectInstrumentField(label='Index Ref',
                                                  objMapping=self._leg+'.IndexRef',
                                                  visible=self.UniqueCallback('@IndexRefVisible')),
                 'indexRefFXFixingType' : Object( label='FX Fixing',
                                                  objMapping=self._leg+'.IndexRefFXFixingType',
                                                  choiceListSource=self.UniqueCallback('@IndexRefFXFixingTypeChoices')),
                 'initialIndexValue'    : Object( label='Initial Index',
                                                  objMapping=self._leg+'.InitialIndexValue',
                                                  formatter='FullPrecisionTwoDecimalTick',
                                                  visible=self.UniqueCallback('@IndexRefVisible')),
                 'initialRate'          : Object( label='',
                                                  objMapping=self._leg+'.InitialRate',
                                                  formatter='InitialFixing',
                                                  width=7,
                                                  maxWidth=7,
                                                  visible=self.UniqueCallback('@FloatRateReferenceVisible')),
                 'legNominal'           : BuySell(label='Nominal',
                                                  objMapping=self._leg+'.LegNominal',
                                                  showBuySell=self._showBuySell,
                                                  enabled=self.UniqueCallback('@LegNominalEnabled')),                                         
                 'legType'              : Object( label='Type',
                                                  objMapping=self._leg+'.LegType',
                                                  choiceListSource=self.UniqueCallback('@LegTypeChoices'),
                                                  onChanged=self.UniqueCallback('@OnLegTypeChanged')),
                 'longStub'             : Object( label='Long Stub',
                                                  objMapping=self._leg+'.LongStub',
                                                  visible='@IsShowModeInstrumentDetail'),
                 'nominalAtEnd'         : Object( label='Nom. End',
                                                  objMapping=self._leg+'.NominalAtEnd',
                                                  visible=self.UniqueCallback('@NominalAtEndVisible')),
                 'nominalAtStart'       : Object( label='Nom. Start',
                                                  objMapping=self._leg+'.NominalAtStart',
                                                  visible=self.UniqueCallback('@NominalAtStartVisible')), 
                 'nominalScaling'       : Object( label='Nom Scal',
                                                  objMapping=self._leg+'.NominalScaling',
                                                  choiceListSource=self.UniqueCallback('@NominalScalingChoices')),
                 'nominalScalingPeriod' : Object( label='Nom Period',
                                                  objMapping=self._leg+'.NominalScalingPeriod'),
                 'nonDeliverableCurrency':Object( label='Currency',
                                                  objMapping=self._leg+'.NonDeliverableCurrency',
                                                  visible=self.UniqueCallback('@NonDeliverableCurrencyVisible')),
                 'passingType'          : Object( label='Pass Type',
                                                  objMapping=self._leg+'.PassingType',
                                                  choiceListSource=self.UniqueCallback('@PassingTypeChoices'),
                                                  visible=self.UniqueCallback('@PassingTypeVisible')),
                 'passInReturnCurrency' : Object( label='Pass In Return Curr',
                                                  objMapping=self._leg+'.PassInReturnCurrency',
                                                  visible=self.UniqueCallback('@PassingDetailsVisible')),
                 'payCalendar'          : Object( label='Pay Cal',
                                                  objMapping=self._leg+'.PayCalendar'),
                 'pay2Calendar'         : Object( label='Pay Cal 2',
                                                  objMapping=self._leg+'.Pay2Calendar',
                                                  visible=self.UniqueCallback('@Pay2CalendarVisible')),
                 'pay3Calendar'         : Object( label='Pay Cal 3',
                                                  objMapping=self._leg+'.Pay3Calendar',
                                                  visible=self.UniqueCallback('@Pay3CalendarVisible')),
                 'pay4Calendar'         : Object( label='Pay Cal 4',
                                                  objMapping=self._leg+'.Pay4Calendar',
                                                  visible=self.UniqueCallback('@Pay4CalendarVisible')),
                 'pay5Calendar'         : Object( label='Pay Cal 5',
                                                  objMapping=self._leg+'.Pay5Calendar',
                                                  visible=self.UniqueCallback('@Pay5CalendarVisible')),
                 'payDayMethod'         : Object( label='',
                                                  objMapping=self._leg+'.PayDayMethod',
                                                  visible='@IsShowModeInstrumentDetail'),
                 'payOffset'            : Object( label='Pay Offset',
                                                  objMapping=self._leg+'.PayOffset',
                                                  visible='@IsShowModeInstrumentDetail',
                                                  width=6),
                 'priceInterpretationType': Object(label='Interp Prc',
                                                  objMapping=self._leg+'.PriceInterpretationType',
                                                  choiceListSource=getPriceInterpretationTypes,
                                                  visible='@IsShowModeInstrumentDetail'),
                 'referenceInstrument'  : Object( label='Ref Ins',
                                                  objMapping=self._leg+'.FloatRateReference',
                                                  choiceListSource=self.UniqueCallback('@RefInsChoices')),              
                 'referenceInstrumentType': Object( label='',
                                                   objMapping=self._leg+'.ReferenceInstrumentType',
                                                   choiceListSource=self.UniqueCallback('@ValidRefTypes'),
                                                   onChanged=self.UniqueCallback('@UpdateRefInsChoices'),
                                                   maxWidth=20)  ,
                 'resets'               : ResetDefinition(leg = self._leg),
                 'rollingConv'          : Object( label='Roll Conv',
                                                  objMapping=self._leg+'.RollingConv',
                                                  visible='@IsShowModeInstrumentDetail'),
                 'rollingPeriod'        : Object( label='Rolling',
                                                  objMapping=self._leg+'.RollingPeriod',
                                                  width=6),
                 'rollingPeriodBase'    : Object( label='',
                                                  objMapping=self._leg+'.RollingPeriodBase',
                                                  formatter='RollingBaseDateField',
                                                  transform=self.UniqueCallback('@RollingBaseDateTransform'),
                                                  width=11,
                                                  maxWidth=11),
                 'spread'               : Object( label='Spread',
                                                  objMapping=self._leg+'.Spread',
                                                  visible=self.UniqueCallback('@FloatRateReferenceVisible'),
                                                  formatter='FullPrecisionTwoDecimalTick',
                                                  solverParameter={'minValue':-10.0, 'maxValue':10.0},
                                                  transform=self.UniqueCallback('@TransformSolver'),
                                                  backgroundColor='@SolverColor'),
                 'spread2'              : Object( label='Spread 2',
                                                  objMapping=self._leg+'.Spread2',
                                                  visible=self.UniqueCallback('@Spread2Visible'),
                                                  formatter='FullPrecisionTwoDecimalTick',
                                                  solverParameter={'minValue':-10.0, 'maxValue':10.0},
                                                  transform=self.UniqueCallback('@TransformSolver'),
                                                  backgroundColor='@SolverColor'),
                 'stepUpDay'            : Object( label='Step Up',
                                                  objMapping=self._leg+'.StepUpDay',
                                                  transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                  visible=self.UniqueCallback('@StepUpVisible'),
                                                  width=11),
                 'stepUpValue'          : Object( label='',
                                                  objMapping=self._leg+'.StepUpValue',
                                                  formatter='FullPrecision',
                                                  visible=self.UniqueCallback('@StepUpVisible'),
                                                  enabled=self.UniqueCallback('@StepUpValueEnabled')),
                 'strike'               : Object( label='Cap Strike',
                                                  objMapping=self._leg+'.Strike',
                                                  visible=self.UniqueCallback('@StrikeVisible'),
                                                  formatter='FullPrecisionTwoDecimalTick'),
                 'strike2'              : Object( label='Floor Strike',
                                                  objMapping=self._leg+'.Strike2',
                                                  visible=self.UniqueCallback('@Strike2Visible'),
                                                  formatter='FullPrecisionTwoDecimalTick'),
                 'strikeType'              : Object( label='',
                                                  objMapping=self._leg+'.StrikeType'),
                 'tradePv'              : CalcVal(label='PV',
                                                  calcMapping = self._trade + ':FTradeSheet:Portfolio Present Value',
                                                  solverTopValue = True),
                 'theorPrice'           : CalcVal(label='Theor Price',
                                                  calcMapping = self._trade + ':FTradeSheet:Price Theor',
                                                  solverTopValue = True)
               }
               
    def IsShowModeDetail2(self):
        return True
       
    # Visible callbacks
    def CalculationPeriodVisible(self, attributeName):
        return self.Leg().ResetType() in ['Compound of Weighted', 'Comp of Wght Float Fctr Inc']
    
    def CalcPeriodDateRuleVisible(self, attributeName):
        return self.IsShowModeDetail() or self.calculationPeriodDateRule
    
    def CalcTypeVisible(self, attributeName):
        return self.Leg().CalcType() or self.IsShowModeDetail()
        
    def CreditRefVisible(self, attributeName):
        return self.Leg().CreditRef() or self.IsShowModeDetail()
        
    def CurrencyVisible(self, attributeName):
        return not self.NonDeliverableCurrencyVisible()
        
    def DeliverableCurrencyVisible(self, attributeName):
        return self.Instrument().NonDeliverable()
        
    def FixedCouponVisible(self, attributeName):
        return self.IsShowModeDetail() or (self.Leg().FixedCoupon() and not self.Leg().Instrument().IsSecurity())          
        
    def FixedRateVisible(self, attributeName):
        return self.Leg().IsFixedLeg() or self.Leg().LegType() == 'Reverse Float'
    
    def FloatRateFactorVisible(self, attributeName):
        return self.Leg().IsFloatOrCapFloorLeg() and (self.IsShowModeDetail() or self.Leg().LegType() == 'Reverse Float' or self.floatRateFactor != 1)

    def FloatRateFactor2Visible(self, attributeName):
        return self.floatRateReference2 and (self.IsShowModeDetail() or self.floatRateFactor2 != 1)
    
    def FloatRateReferenceVisible(self, attributeName):
        return self.Leg().IsFloatOrCapFloorLeg() or self.Leg().IsTotalReturnLeg()
    
    def FloatRateReference2Visible(self, attributeName):
        return self.FloatRateReferenceVisible(attributeName) and (self.IsShowModeDetail() or self.floatRateReference2)
    
    def IndexRefVisible(self, attributeName):
        return self.Leg().NominalScaling() != 'None'
        
    def InterestPaymentTimeVisible(self, attributeName):
        return self.Leg().IsVisible('InterestPaymentTime', self.IsShowModeDetail())        
        
    def NominalAtEndVisible(self, attributeName):
        return self.Leg().NominalAtEnd() or self.IsShowModeDetail()
        
    def NominalAtStartVisible(self, attributeName):
        return self.Leg().NominalAtStart() or self.IsShowModeDetail()     

    def NonDeliverableCurrencyVisible(self, *args):
        return self.Instrument().NonDeliverable()
        
    def Pay2CalendarVisible(self, *args):
        return self.IsPayCalendarVisible() and (self.pay2Calendar or (self.IsShowModeDetail() and self.payCalendar))
        
    def Pay3CalendarVisible(self, *args):
        return self.IsPayCalendarVisible() and (self.pay3Calendar or (self.IsShowModeDetail() and self.pay2Calendar))
        
    def Pay4CalendarVisible(self, *args):
        return self.IsPayCalendarVisible() and (self.pay4Calendar or (self.IsShowModeDetail() and self.pay3Calendar))
        
    def Pay5CalendarVisible(self, *args):
        return self.IsPayCalendarVisible() and (self.pay5Calendar or (self.IsShowModeDetail() and self.pay4Calendar))
        
    def PassingDetailsVisible(self, *args):
        return self.PassingTypeVisible() and self.Leg().PassingType() != 'None'
        
    def PassingTypeVisible(self, *args):
        return self.Leg().IsTotalReturnLeg() and self.IsShowModeDetail()
    
    def Spread2Visible(self, *args):
        return self.floatRateReference2 and (self.IsShowModeDetail() or self.spread2 != 0)
            
    def StepUpVisible(self, *args):
        return self.Leg().IsFloatOrCapFloorLeg() and (self.IsShowModeDetail() or self.Leg().StepUpDay())
        
    def StrikeVisible(self, *args):
        return self.Leg().LegType() in ['Cap', 'Digital Cap', 'Reverse Float', 'Capped Float', 'Collared Float']
        
    def Strike2Visible(self, *args):
        return self.Leg().LegType() in ['Floor', 'Digital Floor', 'Floored Float', 'Collared Float']
        
    # Enabled callbacks
    def StepUpValueEnabled(self, attributeName):
        return self.Leg().StepUpDay()
        
    def LegNominalEnabled(self, attributeName):
        return (self.Instrument().FixNominalLeg() == 'None' or (self.Instrument().FixNominalLeg() == 'Pay Leg' and self.Leg().PayLeg()) or (self.Instrument().FixNominalLeg() == 'Receive Leg' and not self.Leg().PayLeg()))
        
    def InterestPaymentTimeEnabled(self, attributeName):
        return self.Leg().IsEnabled('InterestPaymentTime')
        
    # ChoiceListSource callbacks
    def FloatRateReferenceChoices(self, attributeName):
        if self._floatRateReferenceChoices.IsEmpty():
            self.UpdateFloatRateReferenceChoices()
        return self._floatRateReferenceChoices
        
    def LegTypeChoices(self, attributeName):
        validLegTypes = self.Leg().ValidLegTypeChoices()
        source = validLegTypes.GetChoiceListSource()
        sourceCopy = source.Clone()
        source.Clear()
        for type in sourceCopy:
            if type not in EXCLUDED_LEG_TYPES:
                source.Add(type)
        return validLegTypes
        
    def RefInsChoices(self, attributeName):
        if self._refInsChoices.IsEmpty():
            self.UpdateRefInsChoices()
        return self._refInsChoices

    def ValidRefTypes(self, attributeName):
        return GetReferenceInstrumentTypes(self.Instrument())
    
    def GetRefChoices(self, *args):
        if self.Instrument().Originator().StorageId()>0:
            ins=self.Instrument().Originator()
        else:
            ins=None
        references=getAverageForwardRefInsChoices(self.referenceInstrumentType, self.Leg().EndDate(), ins)
        return references
        
    def UpdateRefInsChoices(self, *args):
        self._refInsChoices.Populate(self.GetRefChoices())
        
    def NominalScalingChoices(self, attributeName):
        return getNominalScalingChoices(self.Leg().Instrument())
        
    def PassingTypeChoices(self, attributeName):
        return getPassingTypeChoices(self)
        
    def IndexRefFXFixingTypeChoices(self, attributeName):
        return acm.FIndexedPopulator(['None', 'Explicit', 'Implicit'])
        
    def InterestPaymentTimeChoices(self, attributeName):
        return getInterestPaymentTimeTypes(self.Leg())        
        
    # Transform callbacks
    def RollingBaseDateTransform(self, attributeName, newDate):
        date = self.Leg().RollingBaseDateFromString(newDate)
        return date if date else newDate
        
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    def TransformSolver(self, attrName, value):
        goalValue = None
        topValue = None
        if isinstance(value, str):
            value = value.lower()
        if value in ['p', 'pa', 'par']:
            goalValue = 100.0 if self.Instrument().IsOnBalanceSheet() else 0.0
        if goalValue != None:
            topValue = self.PrefixedName('theorPrice')
        if (goalValue == None or topValue == None):
            f = self.GetAttributeMetaData('tradePv', 'formatter')()
            goalValue = ParseSuffixedFloat(value, suffix=['pv'], formatter=f)
            if goalValue != None:
                topValue = self.PrefixedName('tradePv')
        if goalValue != None and topValue != None:
            return self.GetMethod("Solve")(topValue, attrName, goalValue)
        else:
            return value
    
    # Util
    def Leg(self):
        return self.GetMethod(self._leg)()
        
    def Instrument(self):
        return self.Leg().Instrument()
        
    def OnLegTypeChanged(self, *args):
        self.UpdateFloatRateReferenceChoices()
        self.resets.UpdateResetTypeChoices()
        
    def UpdateFloatRateReferenceChoices(self):
        self._floatRateReferenceChoices.Clear()
        allReferences = self.Leg().AllFloatRefsSorted()
        self._floatRateReferenceChoices.AddAll(allReferences)
        return self._floatRateReferenceChoices
        
    def IsPayCalendarVisible(self):
        return self.GetAttributeMetaData('payCalendar', 'visible')()
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                     legType;
                     hbox(;
                        floatRateReference;
                        initialRate;
                     );
                     floatRateReference2;
                     hbox(;
                        spread;
                        resets;
                     );
                     spread2;
                     floatRateFactor;
                     floatRateFactor2;
                     fixedRate;
                     strike;
                     strike2;
                     hbox(;
                        stepUpDay;
                        stepUpValue;
                     );
                     dayCountMethod;
                     payCalendar;
                     pay2Calendar;
                     pay3Calendar;
                     pay4Calendar;
                     pay5Calendar;
                     hbox(;
                        rollingPeriod;
                        rollingPeriodBase;
                     );
                     rollingConv;
                     hbox(;
                        payOffset;
                        payDayMethod;
                     );
                     selectCreditRef;
                     calcType;
                     hbox(;
                        longStub;
                        fixedCoupon;
                     );
                   """
               )
    

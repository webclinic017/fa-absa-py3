import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, ParseSuffixedFloat
from ChoicesExprInstrument import getResetTypes, getFixingSources


class ResetDefinition(CompositeAttributeDefinition):
    def OnInit(self, leg, **kwargs):
        self._leg = leg
        self._resetTypeChoices = DealPackageChoiceListSource()
        
        
    def Attributes(self):
        return { 'aggregationRollingBaseDateEnabled' : Object( label='Use compounding Rolling Base Day',
                                                               objMapping=self._leg+'.AggregationRollingBaseDateEnabled',
                                                               visible=self.UniqueCallback('@AggregationRollingBaseDateEnabledVisible')),
                 'aggregationRollingBaseDate'        : Object( label='Rolling Base Day',
                                                               objMapping=self._leg+'.AggregationRollingBaseDate',
                                                               visible=self.UniqueCallback('@AggregationRollingBaseDateVisible')),
                 'calculationPeriod'    : Object( label='Comp Period',
                                                  objMapping=self._leg+'.CalculationPeriod',
                                                  visible=self.UniqueCallback('@CalculationPeriodVisible')),
                 'decimals'             : Object( label='Decimals',
                                                  objMapping=self._leg+'.Decimals',
                                                  visible=self.UniqueCallback('@IsNotReturnLeg')),
                 'fixedAggregationDates': Object( label='Fix Compounding Period',
                                                  objMapping=self._leg+'.FixedAggregationDates',
                                                  visible=self.UniqueCallback('@FixedAggregationDatesVisible')),
                 'floatRefFixingSource' : Object( label='Source',
                                                  objMapping=self._leg+'.FloatRefFixingSource',
                                                  visible=self.UniqueCallback('@FloatRefFixingSourceVisible'),
                                                  choiceListSource=getFixingSources(False)),
                 'resetDayOffset'       : Object( label='Fixing Offset',
                                                  objMapping=self._leg+'.ResetDayOffset'),
                 'resetDayMethod'       : Object( label='Day Method',
                                                  objMapping=self._leg+'.ResetDayMethod',
                                                  visible=self.UniqueCallback('@IsNotReturnLeg')),
                 'resetCalendar'        : Object( label='Calendar 1',
                                                  objMapping=self._leg+'.ResetCalendar'),
                 'reset2Calendar'       : Object( label='Calendar 2',
                                                  objMapping=self._leg+'.Reset2Calendar'),
                 'reset3Calendar'       : Object( label='Calendar 3',
                                                  objMapping=self._leg+'.Reset3Calendar',
                                                  visible=self.UniqueCallback('@Reset3CalendarVisible')),
                 'reset4Calendar'       : Object( label='Calendar 4',
                                                  objMapping=self._leg+'.Reset4Calendar',
                                                  visible=self.UniqueCallback('@Reset4CalendarVisible')),
                 'reset5Calendar'       : Object( label='Calendar 5',
                                                  objMapping=self._leg+'.Reset5Calendar',
                                                  visible=self.UniqueCallback('@Reset5CalendarVisible')),
                 'resetInArrear'        : Object( label='Fixing In Arrears',
                                                  objMapping=self._leg+'.ResetInArrear',
                                                  enabled=self.UniqueCallback('@ResetInArrearEnabled')),
                 'resetPeriod'          : Object( label='Period',
                                                  objMapping=self._leg+'.ResetPeriod',
                                                  visible=self.UniqueCallback('@ResetPeriodVisible')),
                 'resets'               : Action( label='Resets...',
                                                  sizeToFit=True,
                                                  dialog=AttributeDialog( label='Resets', 
                                                                          customPanes=self.UniqueCallback('@ResetsDialogCustomPanes')),
                                                  visible=self.UniqueCallback('@ResetsVisible')),
                 'resetType'            : Object( label='Type',
                                                  objMapping=self._leg+'.ResetType',
                                                  enabled=self.UniqueCallback('@IsNotReturnLeg'),
                                                  choiceListSource=self.UniqueCallback('@ResetTypeChoices')),
                 'rounding'             : Object( label='Rounding',
                                                  objMapping=self._leg+'.Rounding',
                                                  visible=self.UniqueCallback('@IsNotReturnLeg'))
               }
               
    # Visible callbacks
    def AggregationRollingBaseDateEnabledVisible(self, *args):
        return self.Leg().IsVisible('AggregationRollingBaseDateEnabled', self.IsShowModeDetail())
        
    def AggregationRollingBaseDateVisible(self, *args):
        return self.Leg().IsVisible('AggregationRollingBaseDate', self.IsShowModeDetail())
        
    def CalculationPeriodVisible(self, attributeName):
        return self.Leg().ResetType() in ['Compound of Weighted', 'Comp of Wght Float Fctr Inc']
    
    def FixedAggregationDatesVisible(self, *args):
        return self.Leg().IsVisible('FixedAggregationDates', self.IsShowModeDetail())
        
    def FloatRefFixingSourceVisible(self, attributeName):
        return self.Leg().LegType() not in ['Zero Coupon Fixed', 'Total Return']
    
    def Reset3CalendarVisible(self, *args):
        return self.reset2Calendar or self.reset3Calendar or self.reset4Calendar or self.reset5Calendar
        
    def Reset4CalendarVisible(self, *args):
        return self.reset3Calendar or self.reset4Calendar or self.reset5Calendar
        
    def Reset5CalendarVisible(self, *args):
        return self.reset4Calendar or self.reset5Calendar
        
    def ResetPeriodVisible(self, *args):
        return self.Leg().ResetType() in  ['Weighted', 'Unweighted', 'Compound', 'Flat Compound', 'Total Weighted', 
                                           'Compound Spread Excluded', 'Accretive', 'Assertive', 'Weighted 1m Compound',
                                           'Aggregate Return', 'Simple Overnight', 'Double', 'Compound Float Fctr Included',
                                           'Comp of Wght Float Fctr Inc', 'Compound of Weighted', 'Return']
                                           
    def ResetsVisible(self, attributeName):
        return self.Leg().IsFloatOrCapFloorLeg() or self.Leg().LegType() == 'Total Return'
        
    # Enabled callbacks
    def ResetInArrearEnabled(self, attributeName):
        return self.Leg().ResetType() == 'Single'
        
    # ChoiceListSource callbacks
    def ResetTypeChoices(self, attributeName):
        if self._resetTypeChoices.IsEmpty():
            self.UpdateResetTypeChoices()
        return self._resetTypeChoices
        
    def IsNotReturnLeg(self, attributeName):
        return self.Leg().ResetType() != 'Return'
    
    # Util
    def Leg(self):
        return self.GetMethod(self._leg)()
        
    def UpdateResetTypeChoices(self):
        resetTypes = getResetTypes(self.Leg())
        self._resetTypeChoices.Populate(resetTypes)
        return self._resetTypeChoices
        
    def ResetsDialogCustomPanes(self, attrName):
        layout = self.UniqueLayout(
                   """
                    hbox(;
                        vbox{;
                            resetDayOffset;
                            rounding;
                            decimals;
                            resetCalendar;
                            reset2Calendar;
                            reset3Calendar;
                            reset4Calendar;
                            reset5Calendar;
                        };
                        vbox{;
                            resetType;
                            resetPeriod;
                            calculationPeriod;
                            resetDayMethod;
                            floatRefFixingSource;
                            resetInArrear;
                            aggregationRollingBaseDateEnabled;
                            aggregationRollingBaseDate;
                            fixedAggregationDates;
                        };
                    );
                   """
               )
        return [{"Resets":layout}]
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                     resets;
                   """
               )
    

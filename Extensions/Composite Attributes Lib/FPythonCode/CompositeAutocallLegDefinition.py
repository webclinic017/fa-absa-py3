import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, List
from DealPackageUtil import UnDecorate
from ChoicesExprInstrument import getTriggerRefChoices, getTriggerRefInsTypeChoices, getAutocallableStrikeTypes, getAutocallableTypes, getFixingSources
from CompositeLegDefinition import LegDefinition

class AutocallLegDefinition(LegDefinition):

    def OnInit(self, leg, trade, **kwargs):
        super(AutocallLegDefinition, self).OnInit(leg, trade, **kwargs)
        self._triggerRefChoices = DealPackageChoiceListSource()
        self._selectedEvent = acm.FObservationEvent()

    def Attributes(self):
        
        attributes = super(AutocallLegDefinition, self).Attributes()
        
        attributes['triggerRef']                 = Object( label='Trigger Ref',
                                                        objMapping=self._leg+'.TriggerReference',
                                                        choiceListSource=self.UniqueCallback('@TriggerRefChoices'))
        attributes['triggerRefType']             = Object( label='',
                                                        objMapping=self._leg+'.TriggerReferenceInstrumentType',
                                                        choiceListSource=self.UniqueCallback('@ValidTriggerRefTypes'),
                                                        onChanged=self.UniqueCallback('@UpdateTriggerRefChoices'),
                                                        maxWidth=20)
        attributes['autocallType']               = Object( label='Type',
                                                        objMapping=self._leg+'.AutocallableType',
                                                        choiceListSource=self.UniqueCallback('@AutocallTypeChoices'))
        attributes['callLevel']                  = Object( label='Call Level',
                                                        objMapping=self._leg+'.EarlyRedemptionBarrier',
                                                        solverParameter=self.UniqueCallback('@SolverParameters'),
                                                        transform=self.UniqueCallback('@TransformSolver'),
                                                        backgroundColor='@SolverColor',)
        attributes['couponBarrier']              = Object( label='Cpn Barrier',
                                                        objMapping=self._leg+'.CouponPaymentBarrier',
                                                        solverParameter=self.UniqueCallback('@SolverParameters'),
                                                        transform=self.UniqueCallback('@TransformSolver'),
                                                        backgroundColor='@SolverColor',
                                                        visible=self.UniqueCallback('@CouponBarrierVisible'))
        attributes['memoryCoupon']               = Object( label='Memory',
                                                        objMapping=self._leg+'.MemoryCoupon',
                                                        visible=self.UniqueCallback('@MemoryCouponVisible'))
        attributes['trigRefFixingSource']        = Object( label='Fixing Src',
                                                        objMapping=self._leg+'.TrigRefFixingSource',
                                                        choiceListSource=getFixingSources(False))                                                
        attributes['trigRefFixingDateRule']      = Object( label='Fixing Lag',
                                                        objMapping=self._leg+'.TrigRefFixingDateRule',)
        attributes['autocallableStrikeType']     = Object( label='Strike Type',
                                                        objMapping=self._leg+'.AutocallableStrikeType',
                                                        choiceListSource=self.UniqueCallback('@AutocallStrikeTypeChoices'))                   
        attributes['maturityPaymentScaling']     = Object( label='Scaling',
                                                        objMapping=self._leg+'.MaturityPaymentScaling',
                                                        solverParameter=self.UniqueCallback('@SolverParameters'),
                                                        transform=self.UniqueCallback('@TransformSolver'),
                                                        backgroundColor='@SolverColor')
        attributes['maturityPaymentTrigger']     = Object( label='Barrier',
                                                        objMapping=self._leg+'.MaturityPaymentTrigger',
                                                        solverParameter=self.UniqueCallback('@SolverParameters'),
                                                        transform=self.UniqueCallback('@TransformSolver'),
                                                        backgroundColor='@SolverColor')

        attributes['observationEvents']          = Object( label='Observation Events',
                                                        objMapping=self._leg+'.ObservationEvents',
                                                        columns=self.UniqueCallback('@ListColumns'),
                                                        addNewItem=['First', 'Sorted'],
                                                        sortIndexCallback=self.UniqueCallback('@SortObservationEvents'),
                                                        onSelectionChanged=self.UniqueCallback('@SetSelectedEvent'),
                                                        dialog=AttributeDialog( label='Edit Observation Event', 
                                                          customPanes=self.UniqueCallback('@EditDialogCustomPanes')))
                                            
        attributes['selectedEvent_Type']        = Object( label='Type',
                                                          objMapping=self.UniqueCallback('SelectedEvent')+'.EventType',
                                                          enabled=False,
                                                          domain='enum(ObservationEventType)')
                                                          
        attributes['selectedEvent_Date']        = Object( label='Date',
                                                          objMapping=self.UniqueCallback('SelectedEvent')+'.Day',
                                                          enabled=False,
                                                          domain='date')
        attributes['selectedEvent_Value']        = Object( label='Value',
                                                          formatter='Detailed',
                                                          objMapping=self.UniqueCallback('SelectedEvent')+'.EventValue',
                                                          enabled=self.UniqueCallback('@IsSavedInstrument'),
                                                          domain='double')
                                                          
        return attributes

    def SortObservationEvents(self, attrName, columnNbr, value, formatter, obj):
        if columnNbr < 0 and obj:
            return [acm.Time.DateTimeToTime(obj.Day()), obj.EventType()]
        elif columnNbr == 1:
            return acm.Time.DateTimeToTime(value)
        else:
            return value
        
    #Attribute Callbacks
    def ListColumns(self, *args):
        return [{'methodChain': 'EventType', 'label': 'Type'},
                {'methodChain': 'Day',     'label': 'Date'},
                {'methodChain': 'EventValue',    'label': 'Value'}]
                
        
    def SelectedEvent(self):
        return self._selectedEvent
            
    def SetSelectedEvent(self, attrName, selectedObj):
        if selectedObj:
            self._selectedEvent=selectedObj 
        
    def EditDialogCustomPanes(self, attrName):
        return [{'General' : self.UniqueLayout(
                    """
                    vbox(;
                        selectedEvent_Type;
                        selectedEvent_Date;
                        selectedEvent_Value;
                    );
                    """
                )}]

    # ChoiceListSource callbacks
    def TriggerRefChoices(self, attributeName):
        if self._triggerRefChoices.IsEmpty():
            self.UpdateTriggerRefChoices()
        return self._triggerRefChoices 
    
    def AutocallStrikeTypeChoices(self, attributeName):
        return getAutocallableStrikeTypes(self.Leg())
        
    def AutocallTypeChoices(self, attributeName):
        return getAutocallableTypes(self.Leg())
        
    def ValidTriggerRefTypes(self, attributeName):
        return getTriggerRefInsTypeChoices(self.Leg())
        
    # OnChanged callbacks
    def UpdateTriggerRefChoices(self, *args):
        self._triggerRefChoices.Populate(getTriggerRefChoices(self.Leg()))
        
    #Visible callbacks
    def MemoryCouponVisible(self, *args):
        return self.Leg().IsVisible('MemoryCoupon', self.IsShowModeDetail())
        
    def CouponBarrierVisible(self, *args):
        return self.Leg().IsVisible('CouponPaymentBarrier', self.IsShowModeDetail())
        
    #Enabled callbacks
    def IsSavedInstrument(self, attributeName):
        return not self.Leg().IsInfant()
        
    #Utils
    def _ObservationEvents(self):
        return self.Leg().ObservationEvents()

                
    def SolverParameters(self, *args):
        return {'minValue':0.0, 'maxValue':200.0, 'precision':1, 'maxIterations':10}
                

